from __future__ import annotations

from datetime import datetime, date
from typing import Dict, List


def read_data(filename: str) -> List[List[str]]:
    """
    Read the CSV file and return the data rows as a list of lists.

    The first row (header) is skipped. Each row contains:
    [timestamp, cons_v1, cons_v2, cons_v3, prod_v1, prod_v2, prod_v3]
    as strings.
    """
    rows: List[List[str]] = []

    with open(filename, "r", encoding="utf-8") as f:
        # Read all lines, strip newline characters
        lines = [line.strip() for line in f]

    # Skip header line (index 0)
    for line in lines[1:]:
        if not line:
            continue
        # The file uses semicolon as separator
        parts = line.split(";")
        if len(parts) < 7:
            # Skip invalid lines
            continue
        rows.append(parts)

    return rows


def calculate_daily_totals(rows: List[List[str]]) -> Dict[date, Dict[str, List[float]]]:
    """
    Calculate daily totals for consumption and production (in Wh) per phase.

    Returns a dictionary:
        {
            date_obj: {
                "cons": [v1_wh, v2_wh, v3_wh],
                "prod": [v1_wh, v2_wh, v3_wh],
            },
            ...
        }
    """
    daily: Dict[date, Dict[str, List[float]]] = {}

    for parts in rows:
        timestamp_str = parts[0]

        # Example format: "2025-10-13T00:00:00"
        dt = datetime.fromisoformat(timestamp_str)
        d = dt.date()

        # Convert string values to float (Wh)
        cons_v1 = float(parts[1])
        cons_v2 = float(parts[2])
        cons_v3 = float(parts[3])
        prod_v1 = float(parts[4])
        prod_v2 = float(parts[5])
        prod_v3 = float(parts[6])

        if d not in daily:
            daily[d] = {
                "cons": [0.0, 0.0, 0.0],
                "prod": [0.0, 0.0, 0.0],
            }

        daily[d]["cons"][0] += cons_v1
        daily[d]["cons"][1] += cons_v2
        daily[d]["cons"][2] += cons_v3
        daily[d]["prod"][0] += prod_v1
        daily[d]["prod"][1] += prod_v2
        daily[d]["prod"][2] += prod_v3

        # End for loop

    return daily


def format_kwh(value_wh: float) -> str:
    """
    Convert Wh to kWh and format with two decimals and a comma as decimal separator.

    Example: 12345 Wh -> "12,35"
    """
    value_kwh = value_wh / 1000.0
    value_str = f"{value_kwh:.2f}"
    value_str = value_str.replace(".", ",")
    return value_str


def weekday_name_finnish(d: date) -> str:
    """
    Return the weekday name in Finnish-style lowercase (monday, tuesday, ...).

    The task example uses English names, but mentions Finnish formatting.
    """
    names = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    ]
    return names[d.weekday()]


def print_report(daily_totals: Dict[date, Dict[str, List[float]]]) -> None:
    """
    Print a user-friendly table of weekly electricity consumption and production.

    Values are printed in kWh with two decimals and a comma as decimal separator.
    """
    print("Week 42 electricity consumption and production (kWh, by phase)")
    print(
        "Day       Date         "
        "Consumption [kWh]           Production [kWh]"
    )
    print(
        "          (dd.mm.yyyy)  "
        "v1      v2      v3      v1      v2      v3"
    )
    print("-" * 75)

    # Sort days by date
    for d in sorted(daily_totals.keys()):
        data = daily_totals[d]
        cons = data["cons"]
        prod = data["prod"]

        day_name = weekday_name_finnish(d).capitalize()
        date_str = d.strftime("%d.%m.%Y")

        cons_v1 = format_kwh(cons[0])
        cons_v2 = format_kwh(cons[1])
        cons_v3 = format_kwh(cons[2])
        prod_v1 = format_kwh(prod[0])
        prod_v2 = format_kwh(prod[1])
        prod_v3 = format_kwh(prod[2])

        # Simple spacing; you can tweak widths if you like
        print(
            f"{day_name:<9} {date_str:<11} "
            f"{cons_v1:>6}  {cons_v2:>6}  {cons_v3:>6}  "
            f"{prod_v1:>6}  {prod_v2:>6}  {prod_v3:>6}"
        )


def main() -> None:
    """
    Main function: read data, compute daily totals, and print the report.
    """
    filename = "week42.csv"
    rows = read_data(filename)
    daily_totals = calculate_daily_totals(rows)
    print_report(daily_totals)


if __name__ == "__main__":
    main()
