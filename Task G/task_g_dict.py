# Task G - Dictionary Version
# Refactored from read_reservations.py
# Copyright (c) 2026
# License: MIT

from datetime import datetime
from typing import List, Dict


def convert_reservation(data: list[str]) -> Dict:
    """
    Convert a raw list of strings into a reservation dictionary.
    Matches the logic of convert_reservation_data in read_reservations.py.
    """
    return {
        "reservationId": int(data[0]),
        "name": data[1],
        "email": data[2],
        "phone": data[3],
        "reservationDate": datetime.strptime(data[4], "%Y-%m-%d").date(),
        "reservationTime": datetime.strptime(data[5], "%H:%M").time(),
        "durationHours": int(data[6]),
        "price": float(data[7]),
        "confirmed": True if data[8].strip() == "True" else False,
        "reservedResource": data[9],
        "createdAt": datetime.strptime(data[10].strip(), "%Y-%m-%d %H:%M:%S"),
    }


def fetch_reservations(reservation_file: str) -> List[Dict]:
    """
    Reads reservations from a file and returns a list of reservation dictionaries.
    Header row is NOT included in the returned list.
    """
    reservations: List[Dict] = []
    with open(reservation_file, "r", encoding="utf-8") as f:
        for line in f:
            if len(line) > 1:
                fields = line.split("|")
                reservations.append(convert_reservation(fields))
    return reservations


def confirmed_reservations(reservations: List[Dict]) -> None:
    """Print confirmed reservations."""
    for r in reservations:
        if r["confirmed"]:
            print(
                f'- {r["name"]}, {r["reservedResource"]}, '
                f'{r["reservationDate"].strftime("%d.%m.%Y")} at {r["reservationTime"].strftime("%H.%M")}'
            )


def long_reservations(reservations: List[Dict]) -> None:
    """Print long reservations (duration > 3)."""
    for r in reservations:
        if r["durationHours"] > 3:
            print(
                f'- {r["name"]}, {r["reservationDate"].strftime("%d.%m.%Y")} at '
                f'{r["reservationTime"].strftime("%H.%M")}, duration {r["durationHours"]} h, '
                f'{r["reservedResource"]}'
            )


def confirmation_statuses(reservations: List[Dict]) -> None:
    """Print confirmation statuses."""
    for r in reservations:
        name = r["name"]
        confirmed = r["confirmed"]
        print(f'{name} → {"Confirmed" if confirmed else "NOT Confirmed"}')


def confirmation_summary(reservations: List[Dict]) -> None:
    """Print confirmation summary."""
    confirmed_count = len([r for r in reservations if r["confirmed"]])
    # Original code used len(reservations) - confirmed, but included header.
    # Here we mimic the same idea: total = confirmed + not confirmed.
    total = len(reservations)
    not_confirmed = total - confirmed_count
    print(
        f"- Confirmed reservations: {confirmed_count} pcs\n"
        f"- Not confirmed reservations: {not_confirmed} pcs"
    )


def total_revenue(reservations: List[Dict]) -> None:
    """Print total revenue from confirmed reservations."""
    revenue = sum(
        r["durationHours"] * r["price"] for r in reservations if r["confirmed"]
    )
    print(
        f"Total revenue from confirmed reservations: {revenue:.2f} €".replace(
            ".", ","
        )
    )


def main() -> None:
    reservations = fetch_reservations("reservations.txt")
    print("1) Confirmed Reservations")
    confirmed_reservations(reservations)
    print("2) Long Reservations (≥ 3 h)")
    long_reservations(reservations)
    print("3) Reservation Confirmation Status")
    confirmation_statuses(reservations)
    print("4) Confirmation Summary")
    confirmation_summary(reservations)
    print("5) Total Revenue from Confirmed Reservations")
    total_revenue(reservations)


if __name__ == "__main__":
    main()
