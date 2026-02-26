from datetime import datetime

def main():
    # Read the reservation line from the file
    with open("reservations.txt", "r", encoding="utf-8") as f:
        line = f.readline().strip()

    # Split into fields
    reservation = line.split("|")

    # Convert data types
    reservation_number = int(reservation[0])
    name = reservation[1]

    # Date conversion
    day = datetime.strptime(reservation[2], "%Y-%m-%d").date()
    finnish_day = day.strftime("%d.%m.%Y")

    # Time conversion
    start_time = datetime.strptime(reservation[3], "%H:%M").time()
    finnish_time = start_time.strftime("%H.%M")

    hours = int(reservation[4])
    hourly_price = float(reservation[5])
    total_price = hours * hourly_price

    paid = True if reservation[6] == "True" else False
    paid_text = "Yes" if paid else "No"

    resource = reservation[7]
    phone = reservation[8]
    email = reservation[9]

    # Print output exactly as required
    print(f"Reservation number: {reservation_number}")
    print(f"Booker: {name}")
    print(f"Date: {finnish_day}")
    print(f"Start time: {finnish_time}")
    print(f"Number of hours: {hours}")
    print(f"Hourly price: {hourly_price:.2f} €".replace(".", ","))
    print(f"Total price: {total_price:.2f} €".replace(".", ","))
    print(f"Paid: {paid_text}")
    print(f"Location: {resource}")
    print(f"Phone: {phone}")
    print(f"Email: {email}")


if __name__ == "__main__":
    main()
