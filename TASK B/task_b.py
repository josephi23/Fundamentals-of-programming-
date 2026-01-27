import datetime

def print_reservation_number(reservation: list) -> None:
    number = int(reservation[0])
    print(f"Reservation number: {number}", end=" ")

def print_booker(reservation: list) -> None:
    name = reservation[1]
    print(f"Booker: {name}", end=" ")

def print_date(reservation: list) -> None:
    year, month, day = reservation[2].split("-")
    date_obj = datetime.date(int(year), int(month), int(day))
    print(f"Date: {date_obj.strftime('%d.%m.%Y')}", end=" ")

def print_start_time(reservation: list) -> None:
    hour, minute = reservation[3].split(":")
    time_obj = datetime.time(int(hour), int(minute))
    print(f"Start time: {time_obj.strftime('%H.%M')}", end=" ")

def print_hours(reservation: list) -> None:
    hours = int(reservation[4])
    print(f"Number of hours: {hours}", end=" ")

def print_hourly_rate(reservation: list) -> None:
    rate = float(reservation[5])
    formatted = f"{rate:.2f}".replace(".", ",")
    print(f"Hourly price: {formatted} €", end=" ")

def print_total_price(reservation: list) -> None:
    hours = int(reservation[4])
    rate = float(reservation[5])
    total = hours * rate
    formatted = f"{total:.2f}".replace(".", ",")
    print(f"Total price: {formatted} €", end=" ")

def print_paid(reservation: list) -> None:
    paid = reservation[6] == "True"
    print(f"Paid: {'Yes' if paid else 'No'}", end=" ")

def print_venue(reservation: list) -> None:
    print(f"Location: {reservation[7]}", end=" ")

def print_phone(reservation: list) -> None:
    print(f"Phone: {reservation[8]}", end=" ")

def print_email(reservation: list) -> None:
    print(f"Email: {reservation[9]}", end=" ")

def main():
    with open("reservations.txt", "r", encoding="utf-8") as file:
        for line in file:
            reservation = line.strip().split("|")

            print_reservation_number(reservation)
            print_booker(reservation)
            print_date(reservation)
            print_start_time(reservation)
            print_hours(reservation)
            print_hourly_rate(reservation)
            print_total_price(reservation)
            print_paid(reservation)
            print_venue(reservation)
            print_phone(reservation)
            print_email(reservation)

            print()  # newline after each reservation

if __name__ == "__main__":
    main()
