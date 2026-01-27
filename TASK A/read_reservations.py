from datetime import datetime

def parse_reservation_line(line):
    parts = line.strip().split(';')
    return {
        "user_name": parts[0],
        "resource": parts[1],
        "start": datetime.strptime(parts[2], "%Y-%m-%d %H:%M"),
        "end": datetime.strptime(parts[3], "%Y-%m-%d %H:%M"),
        "confirmed": parts[4].lower() == "true",
        "participants": int(parts[5])
    }

def read_reservations(filename):
    reservations = []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                reservation = parse_reservation_line(line)
                reservations.append(reservation)
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    return reservations

def display_reservations(reservations):
    for r in reservations:
        print(f"{r['user_name']} booked {r['resource']} from {r['start'].strftime('%Y-%m-%d %H:%M')} to {r['end'].strftime('%Y-%m-%d %H:%M')}, "
              f"confirmed: {r['confirmed']}, participants: {r['participants']}")

if __name__ == "__main__":
    filename = "reservations.txt"
    reservations = read_reservations(filename)
    display_reservations(reservations)
