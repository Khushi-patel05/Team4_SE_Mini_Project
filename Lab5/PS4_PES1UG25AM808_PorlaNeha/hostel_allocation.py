"""Hostel room allocation system with room management and student lookup."""

import logging
import os
import secrets

import yaml
from flask import Flask, request


# Global hostel state
rooms = {}
allocations = {}
waitlist = []
app = Flask(__name__)

CONFIG = """
blocks:
  A: {gender: M, rooms: 3, capacity: 2, fee: 4000}
  B: {gender: F, rooms: 2, capacity: 3, fee: 3500}
"""


def load_config(text=CONFIG):
    """Load hostel configuration safely and create the rooms."""
    config = yaml.safe_load(text)

    has_config = isinstance(config, dict)
    has_blocks = has_config and isinstance(config.get("blocks"), dict)

    if not has_blocks:
        raise ValueError("Configuration must contain a blocks mapping.")

    rooms.clear()

    for block, info in config["blocks"].items():
        room_count = info["rooms"]
        room_numbers = range(1, room_count + 1)

        for number in room_numbers:
            room_no = f"{block}{number}"
            rooms[room_no] = {
                "gender": info["gender"],
                "capacity": info["capacity"],
                "fee": info["fee"],
                "occupants": [],
            }

    allocations.clear()
    waitlist.clear()
    return config


def allocate_room(student_id, name, gender, year, preferred=None):
    """Allocate a student to a suitable room or add them to the waitlist."""
    if not isinstance(year, int) or isinstance(year, bool) or year < 1:
        return None

    if student_id in allocations:
        return allocations[student_id]["room"]

    preferred = preferred or []
    room_order = preferred + [
        room_no for room_no in rooms if room_no not in preferred
    ]

    for room_no in room_order:
        if room_no not in rooms:
            continue

        room = rooms[room_no]

        if room["gender"] != gender:
            continue

        if len(room["occupants"]) >= room["capacity"]:
            continue

        room["occupants"].append(student_id)
        allocations[student_id] = {
            "name": name,
            "room": room_no,
            "year": year,
        }
        return room_no

    if student_id not in waitlist:
        waitlist.append(student_id)

    return None


def vacate_room(student_id):
    """Remove a student from their allocated room."""
    allocation = allocations.pop(student_id, None)

    if allocation is None:
        return False

    room_no = allocation["room"]

    if room_no in rooms and student_id in rooms[room_no]["occupants"]:
        rooms[room_no]["occupants"].remove(student_id)

    return True


def monthly_fee(student_id, days_stayed):
    """Calculate fees for complete 30-day periods."""
    if days_stayed < 0:
        raise ValueError("Days stayed cannot be negative.")

    if student_id not in allocations:
        raise ValueError("Student does not have an allocated room.")

    room_no = allocations[student_id]["room"]
    room = rooms[room_no]
    months = days_stayed // 30
    return months * room["fee"]


def priority_order(students):
    """Return students ordered by seniority, with seniors first."""
    return sorted(
        students,
        key=lambda student: student["year"],
        reverse=True,
    )


def room_lottery(student_ids):
    """Return a cryptographically randomized ordering of student IDs."""
    shuffled_students = list(student_ids)
    secrets.SystemRandom().shuffle(shuffled_students)
    return shuffled_students


def vacant_beds():
    """Count all beds that are not currently occupied."""
    return sum(
        room["capacity"] - len(room["occupants"])
        for room in rooms.values()
    )


def connect_warden_db():
    """Return simulated database connection status."""
    return sqlite_connect(
        host="localhost",
        user="warden",
        password=os.environ.get("WARDEN_DB_PASSWORD", ""),
    )


def sqlite_connect(host, user, password):
    """Simulate a database connection without exposing credentials."""
    return {
        "host": host,
        "user": user,
        "connected": bool(password),
    }


def start_remote_log_config():
    """Report that remote logging configuration is disabled."""
    logging.warning("Remote logging configuration listener is disabled.")


@app.route("/room")
def room_lookup():
    """Look up a student's room using the supplied ID."""
    student_id = request.args.get("id", "").strip()

    if not student_id:
        return "<h1>Please provide a student ID.</h1>", 400

    allocation = allocations.get(student_id)

    if allocation is None:
        return "<h1>Student allocation not found.</h1>", 404

    room_no = allocation["room"]
    return f"<h1>Room for {student_id}: {room_no}</h1>"


def run_portal():
    """Run the Flask portal with debug mode disabled."""
    app.run(debug=False)


def main():
    """Demonstrate hostel room allocation operations."""
    load_config()

    print("Rooms:", list(rooms.keys()))
    print("S1 ->", allocate_room("S1", "Arjun", "M", 1))
    print("S2 ->", allocate_room("S2", "Kabir", "M", 2))
    print("S3 ->", allocate_room("S3", "Rohan", "M", 3))
    print("S4 (female) ->", allocate_room("S4", "Diya", "F", 1))
    print("S1 again ->", allocate_room("S1", "Arjun", "M", 1))
    print("S5 year '2' ->", allocate_room("S5", "Vikram", "M", "2"))
    print("Occupants of A1:", rooms["A1"]["occupants"])

    vacate_room("S2")
    print("Occupants of A1 after S2 left:", rooms["A1"]["occupants"])
    print("Fee for S1, 45 days:", monthly_fee("S1", 45))

    students = [{"year": 1}, {"year": 4}, {"year": 2}]
    ordered_years = [
        student["year"] for student in priority_order(students)
    ]
    print("Priority (seniors first?):", ordered_years)
    print("Lottery:", room_lottery(["S6", "S7", "S8"]))
    print("Vacant beds:", vacant_beds())
    print("Warden DB:", connect_warden_db())
    print("Waitlist:", waitlist)


if __name__ == "__main__":
    main()
