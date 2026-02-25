# Task G - Class Version
# Refactored from read_reservations.py
# Copyright (c) 2026
# License: MIT

from datetime import datetime, date, time
from typing import List


class Reservation:
    def __init__(
        self,
        reservation_id: int,
        name: str,
        email: str,
        phone: str,
        reservation_date: date,
        reservation_time: time,
        duration_hours: int,
        price: float,
        confirmed: bool,
        reserved_resource: str,
        created_at,
    ):
        self.reservation_id = reservation_id
        self.name = name
        self.email = email
        self.phone = phone
        self.reservation_date = reservation_date
        self.reservation_time = reservation_time
        self.duration_hours = duration_hours
        self.price = price
        self.confirmed = confirmed
        self.reserved_resource = reserved_resource
        self.created_at = created_at

    def is_confirmed(self) -> bool:
        return self.confirmed

    def is_long(self) -> bool:
        return self.duration_hours > 3

    def total_price(self) -> float:
        return self.duration_hours * self.price


def convert_reservation(data: list[str]) -> Reservation:
    """
    Convert a raw list of strings into a Reservation object.
    Mirrors convert_reservation_data in read_reservations.py.
    """
    return Reservation(
        reservation_id=int(data[0]),
        name=data[1],
        email=data[2],
        phone=data[3],
        reservation_date=datetime.strptime(data[4], "%Y-%m-%d").date(),
        reservation_time=datetime.strptime(data[5], "%H:%M").time(),
        duration_hours=int(data[6]),
        price=float(data[7]),
        confirmed=True if data[8].strip() == "True" else False,
        reserved_resource=data[9],
        created_at=datetime.strptime(data[10].strip(), "%Y-%m-%d %H:%M:%S"),
    )


def fetch_reservations(reservation_file: str) -> List[Reservation]:
    """
    Reads reservations from a file and returns a list of Reservation objects.
    Header row is NOT included.
    """
    reservations: List[Reservation] = []
    with open(reservation_file, "r", encoding="utf-8") as f:
        for line in f:
            if len(line) > 1:
                fields = line.split("|")
                reservations.append(convert_reservation(fields))
    return reservations


def confirmed_reservations(reservations: List[Reservation]) -> None:
    """Print confirmed reservations."""
    for r in reservations:
        if r.is_confirmed():
            print(
                f"- {r.name}, {r.reserved_resource}, "
                f"{r.reservation_date.strftime('%d.%m.%Y')} at {r.reservation_time.strftime('%H.%M')}"
            )


def long_reservations(reservations: List[Reservation]) -> None:
    """Print long reservations (duration > 3)."""
    for r in reservations:
        if r.is_long():
            print(
                f"- {r.name}, {r.reservation_date.strftime('%d.%m.%Y')} at "
                f"{r.reservation_time.strftime('%H.%M')}, duration {r.duration_hours} h, "
                f"{r.reserved_resource}"
            )


def confirmation_statuses(reservations: List[Reservation]) -> None:
    """Print confirmation statuses."""
    for r in reservations:
        print(f'{r.name} → {"Confirmed" if r.is_confirmed() else "NOT Confirmed"}')


def confirmation_summary(reservations: List[Reservation]) -> None:
    """Print confirmation summary."""
    confirmed_count = len([r for r in reservations if r.is_confirmed()])
    total = len(reservations)
    not_confirmed = total - confirmed_count
    print(
        f"- Confirmed reservations: {confirmed_count} pcs\n"
        f"- Not confirmed reservations: {not_confirmed} pcs"
    )


def total_revenue(reservations: List[Reservation]) -> None:
    """Print total revenue from confirmed reservations."""
    revenue = sum(r.total_price() for r in reservations if r.is_confirmed())
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
