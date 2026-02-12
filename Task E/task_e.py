# Copyright (c) 2026 Chidiebere
# License: MIT

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, date
from pathlib import Path
from typing import Dict, List, Iterable
import csv


@dataclass
class Measurement:
    """Represents one hourly measurement of consumption and production in Wh."""
    timestamp: datetime
    cons_v1: float
    cons_v2: float
    cons_v3: float
    prod_v1: float
    prod_v2: float
    prod_v3: float


DailySummary = Dict[str, float]
WeekDailySummaries = Dict[date, DailySummary]


def read_data(filename: str) -> List[Measurement]:
    """
    Reads a CSV file and returns a list of Measurement objects.

    Expected CSV format (semicolon-separated):
    timestamp;cons_v1;cons_v2;cons_v3;prod_v1;prod_v2;prod_v3
    """
    measurements: List[Measurement] = []

    with open(filename, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader, None)  # skip header

        for row in reader:
            if len(row) < 7:
                continue

            ts = datetime.fromisoformat(row[0].strip())

            measurements.append(
                Measurement(
                    timestamp=ts,
                    cons_v1=float(row[1]),
                    cons_v2=float(row[2]),
                    cons_v3=float(row[3]),
                    prod_v1=float(row[4]),
                    prod_v2=float(row[5]),
                    prod_v3=float(row[6]),
                )
            )

    return measurements


def wh_to_kwh(value_wh: float) -> float:
    """Convert Wh to kWh."""
    return value_wh / 1000.0


def format_kwh_finnish(value_kwh: float) -> str:
    """Format a kWh value with two decimals and a comma as decimal separator."""
    return f"{value_kwh:.2f}".replace(".", ",")


def format_date_finnish(day: date) -> str:
    """Format a date as dd.mm.yyyy."""
    return f"{day.day:02d}.{day.month:02d}.{day.year}"


def weekday_name(day: date) -> str:
    """
    Return weekday name (Mon–Sun).

    The assignment text is a bit confusing about “Finnish”, but the example
    uses English names like Monday, Tuesday, etc., so we follow that.
    """
    names = [
        "Monday", "Tuesday", "Wednesday",
        "Thursday", "Friday", "Saturday", "Sunday"
    ]
    return names[day.weekday()]


def calculate_daily_summaries(measurements: Iterable[Measurement]) -> WeekDailySummaries:
    """
    Calculate daily totals (in Wh) from hourly measurements.

    Returns a mapping: date -> DailySummary.
    """
    daily: WeekDailySummaries = {}

    for m in measurements:
        d = m.timestamp.date()

        if d not in daily:
            daily[d] = {
                "cons_v1": 0.0, "cons_v2": 0.0, "cons_v3": 0.0,
                "prod_v1": 0.0, "prod_v2": 0.0, "prod_v3": 0.0,
            }

        daily[d]["cons_v1"] += m.cons_v1
        daily[d]["cons_v2"] += m.cons_v2
        daily[d]["cons_v3"] += m.cons_v3
        daily[d]["prod_v1"] += m.prod_v1
        daily[d]["prod_v2"] += m.prod_v2
        daily[d]["prod_v3"] += m.prod_v3

    return daily


def format_week_section(week_number: int, daily_summaries: WeekDailySummaries) -> List[str]:
    """
    Format one week's daily summaries into a list of text lines for the report.
    Values are converted to kWh and formatted using Finnish conventions.
    """
    lines: List[str] = []

    lines.append(f"Week {week_number} electricity consumption and production (kWh, by phase)")
    lines.append("Day       Date         Consumption [kWh]           Production [kWh]")
    lines.append("                      v1      v2      v3           v1      v2      v3")
    lines.append("-" * 75)

    for day in sorted(daily_summaries.keys()):
        s = daily_summaries[day]

        cons = [format_kwh_finnish(wh_to_kwh(s[f"cons_v{i}"])) for i in (1, 2, 3)]
        prod = [format_kwh_finnish(wh_to_kwh(s[f"prod_v{i}"])) for i in (1, 2, 3)]

        line = (
            f"{weekday_name(day):<9} {format_date_finnish(day):<11} "
            f"{cons[0]:>7} {cons[1]:>7} {cons[2]:>7}   "
            f"{prod[0]:>7} {prod[1]:>7} {prod[2]:>7}"
        )
        lines.append(line)

    lines.append("")
    return lines


def sum_week_totals(daily_summaries: WeekDailySummaries) -> DailySummary:
    """Sum all days of a week into one summary (still in Wh)."""
    totals: DailySummary = {
        "cons_v1": 0.0, "cons_v2": 0.0, "cons_v3": 0.0,
        "prod_v1": 0.0, "prod_v2": 0.0, "prod_v3": 0.0,
    }

    for day_summary in daily_summaries.values():
        for key in totals:
            totals[key] += day_summary[key]

    return totals


def write_report(filename: str, week_sections: List[List[str]], weekly_totals: Dict[int, DailySummary]) -> None:
    """
    Write the final report to summary.txt.

    Includes all three weeks and a combined summary at the end.
    """
    with open(filename, "w", encoding="utf-8") as f:
        for section in week_sections:
            for line in section:
                f.write(line + "\n")

        f.write("Combined summary of all weeks (kWh, by phase)\n")
        f.write("Week   cons_v1  cons_v2  cons_v3   prod_v1  prod_v2  prod_v3\n")
        f.write("-" * 70 + "\n")

        for week in sorted(weekly_totals.keys()):
            t = weekly_totals[week]

            cons = [format_kwh_finnish(wh_to_kwh(t[f"cons_v{i}"])) for i in (1, 2, 3)]
            prod = [format_kwh_finnish(wh_to_kwh(t[f"prod_v{i}"])) for i in (1, 2, 3)]

            line = (
                f"{week:<5}  {cons[0]:>7}  {cons[1]:>7}  {cons[2]:>7}   "
                f"{prod[0]:>7}  {prod[1]:>7}  {prod[2]:>7}"
            )
            f.write(line + "\n")


def main() -> None:
    """
    Main function: reads weekly CSV files, computes daily summaries,
    and writes a clear report to summary.txt.
    """
    week_files: Dict[int, str] = {
        41: "week41.csv",
        42: "week42.csv",
        43: "week43.csv",
    }

    week_sections: List[List[str]] = []
    weekly_totals: Dict[int, DailySummary] = {}

    for week, filename in week_files.items():
        measurements = read_data(filename)
        daily = calculate_daily_summaries(measurements)
        week_sections.append(format_week_section(week, daily))
        weekly_totals[week] = sum_week_totals(daily)

    write_report("summary.txt", week_sections, weekly_totals)


if __name__ == "__main__":
    main()
