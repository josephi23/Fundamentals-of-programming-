# Copyright (c) 2025 Chidiebere
# License: MIT

from __future__ import annotations
import csv
from datetime import datetime, date
from typing import List, Dict, Any


# ------------------------------------------------------------
# DATA READING
# ------------------------------------------------------------

def read_data(filename: str) -> List[Dict[str, Any]]:
    """
    Reads hourly measurement data from 2025.csv.

    CSV format (semicolon-separated):
    timestamp ; consumption ; production ; temperature

    Values use comma decimals, so they must be converted.
    """
    data: List[Dict[str, Any]] = []

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=";")
        header = next(reader, None)

        for row in reader:
            if not row:
                continue

            ts_str = row[0]
            cons = float(row[1].replace(",", "."))   # FIXED
            prod = float(row[2].replace(",", "."))   # FIXED
            temp = float(row[3].replace(",", "."))   # FIXED

            dt = datetime.fromisoformat(ts_str)
            d = dt.date()

            data.append(
                {
                    "datetime": dt,
                    "date": d,
                    "consumption": cons,
                    "production": prod,
                    "temperature": temp,
                }
            )

    return data



# ------------------------------------------------------------
# INPUT HELPERS
# ------------------------------------------------------------

def parse_date_input(prompt: str) -> date:
    """Asks the user for a date in dd.mm.yyyy format and returns a date object."""
    while True:
        value = input(prompt).strip()
        try:
            day, month, year = value.split(".")
            return date(int(year), int(month), int(day))
        except Exception:
            print("Invalid date. Use dd.mm.yyyy (example: 13.10.2025).")


def format_date_fi(d: date) -> str:
    """Formats a date as dd.mm.yyyy."""
    return f"{d.day}.{d.month}.{d.year}"


def format_number_fi(value: float) -> str:
    """Formats a float with two decimals and comma separator."""
    return f"{value:.2f}".replace(".", ",")


# ------------------------------------------------------------
# REPORT GENERATORS
# ------------------------------------------------------------

def create_daily_report(data: List[Dict[str, Any]]) -> List[str]:
    """
    Builds a daily summary report for a selected date range.
    Returns a list of strings representing the report.
    """
    start = parse_date_input("Enter start date (dd.mm.yyyy): ")
    end = parse_date_input("Enter end date (dd.mm.yyyy): ")

    if end < start:
        start, end = end, start

    total_cons = 0.0
    total_prod = 0.0
    temps: List[float] = []

    for row in data:
        d = row["date"]
        if start <= d <= end:
            total_cons += row["consumption"]
            total_prod += row["production"]
            temps.append(row["temperature"])

    avg_temp = sum(temps) / len(temps) if temps else 0.0

    lines = [
        f"Report for the period {format_date_fi(start)}–{format_date_fi(end)}",
        f"- Total consumption: {format_number_fi(total_cons)} kWh",
        f"- Total production: {format_number_fi(total_prod)} kWh",
        f"- Average temperature: {format_number_fi(avg_temp)} °C",
    ]

    return lines


def create_monthly_report(data: List[Dict[str, Any]]) -> List[str]:
    """
    Builds a monthly summary report for a selected month.
    Returns a list of strings representing the report.
    """
    while True:
        month_str = input("Enter month number (1–12): ").strip()
        if month_str.isdigit() and 1 <= int(month_str) <= 12:
            month = int(month_str)
            break
        print("Invalid month. Enter a number between 1 and 12.")

    total_cons = 0.0
    total_prod = 0.0
    temps: List[float] = []

    for row in data:
        d = row["date"]
        if d.year == 2025 and d.month == month:
            total_cons += row["consumption"]
            total_prod += row["production"]
            temps.append(row["temperature"])

    avg_temp = sum(temps) / len(temps) if temps else 0.0

    month_names = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    lines = [
        f"Report for the month: {month_names[month - 1]}",
        f"- Total consumption: {format_number_fi(total_cons)} kWh",
        f"- Total production: {format_number_fi(total_prod)} kWh",
        f"- Average temperature: {format_number_fi(avg_temp)} °C",
    ]

    return lines


def create_yearly_report(data: List[Dict[str, Any]]) -> List[str]:
    """
    Builds a full-year summary report for 2025.
    Returns a list of strings representing the report.
    """
    total_cons = 0.0
    total_prod = 0.0
    temps: List[float] = []

    for row in data:
        d = row["date"]
        if d.year == 2025:
            total_cons += row["consumption"]
            total_prod += row["production"]
            temps.append(row["temperature"])

    avg_temp = sum(temps) / len(temps) if temps else 0.0

    lines = [
        "Report for the year: 2025",
        f"- Total consumption: {format_number_fi(total_cons)} kWh",
        f"- Total production: {format_number_fi(total_prod)} kWh",
        f"- Average temperature: {format_number_fi(avg_temp)} °C",
    ]

    return lines


# ------------------------------------------------------------
# OUTPUT
# ------------------------------------------------------------

def print_report_to_console(lines: List[str]) -> None:
    """Prints report lines to the console."""
    print("-" * 55)
    for line in lines:
        print(line)


def write_report_to_file(lines: List[str]) -> None:
    """Writes report lines to report.txt (overwrites existing file)."""
    with open("report.txt", "w", encoding="utf-8") as file:
        for line in lines:
            file.write(line + "\n")
    print("Report written to report.txt")


# ------------------------------------------------------------
# MENUS
# ------------------------------------------------------------

def show_main_menu() -> str:
    """Shows the main menu and returns the user's choice."""
    print("\nChoose a report type:")
    print("1) Daily summary for a date range")
    print("2) Monthly summary for one month")
    print("3) Full year 2025 summary")
    print("4) Exit")
    return input("Enter your choice (1–4): ").strip()


def show_after_report_menu() -> str:
    """Shows the menu after printing a report."""
    print("\nWhat would you like to do next?")
    print("1) Write the report to report.txt")
    print("2) Create a new report")
    print("3) Exit")
    return input("Enter your choice (1–3): ").strip()


# ------------------------------------------------------------
# MAIN PROGRAM LOOP
# ------------------------------------------------------------

def main() -> None:
    """Main program controller."""
    data = read_data("2025.csv")

    while True:
        choice = show_main_menu()

        if choice == "1":
            report = create_daily_report(data)
        elif choice == "2":
            report = create_monthly_report(data)
        elif choice == "3":
            report = create_yearly_report(data)
        elif choice == "4":
            print("Exiting program.")
            return
        else:
            print("Invalid choice.")
            continue

        print_report_to_console(report)

        while True:
            next_choice = show_after_report_menu()

            if next_choice == "1":
                write_report_to_file(report)
            elif next_choice == "2":
                break
            elif next_choice == "3":
                print("Exiting program.")
                return
            else:
                print("Invalid choice.")


if __name__ == "__main__":
    main()
