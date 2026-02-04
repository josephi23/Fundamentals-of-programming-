import datetime

def parse_reservation(line: str) -> list:
    return line.strip().split("|")

def format_date(date_str: str) -> str:
    year, month, day = date_str.split("-")
    d = datetime.date(int(year), int(month), int(day))
    return d.strftime("%d.%m.%Y")

def format_time(time_str: str) -> str:
    hour, minute = time_str.split(":")
    t = datetime.time(int(hour), int(minute))
    return t.strftime("%H.%M")

def format_price(price_str: str) -> str:
    price = float(price_str)
    return f"{price:.2f}".replace(".", ",") + " €"

def format_total(hours: str, price: str) -> str:
    total = int(hours) * float(price)
    return f"{total:.2f}".replace(".", ",") + " €"

def format_paid(paid_str: str) -> str:
    return "Yes" if paid_str == "True" else "No"

def main():
    with open("reservations.txt", "r", encoding="utf-8") as file:
        for line in file:
            r = parse_reservation(line)

            output = (
                f"Reservation number: {r[0]} "
                f"Booker: {r[1]} "
                f"Date: {format_date(r[2])} "
                f"Start time: {format_time(r[3])} "
                f"Number of hours: {r[4]} "
                f"Hourly price: {format_price(r[5])} "
                f"Total price: {format_total(r[4], r[5])} "
                f"Paid: {format_paid(r[6])} "
                f"Location: {r[7]} "
                f"Phone: {r[8]} "
                f"Email: {r[9]}"
            )

            print(output)

if __name__ == "__main__":
    main()

