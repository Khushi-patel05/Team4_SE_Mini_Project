"""Conference room and equipment scheduling system."""

import json
from datetime import datetime
from itertools import count

# Global state
reservations = {}
equipment_pool = {"projector": 2, "microphone": 4, "webcam": 1}
conflicts = []
reservation_ids = count(1)


def schedule_room(room_id, time_slot, equipment_list=None):
    """Schedule a room and allocate the requested equipment."""
    if equipment_list is None:
        equipment_list = []

    if not isinstance(time_slot, str):
        raise TypeError("Time slot must be a string.")

    slot_hours(time_slot)

    for reservation_id, reservation in reservations.items():
        if (reservation["room"] == room_id
                and reservation["slot"] == time_slot):
            conflicts.append(
                f"{room_id} double-booked at {time_slot}"
            )

    for equipment in equipment_list:
        if equipment not in equipment_pool:
            raise ValueError(f"Unknown equipment: {equipment}")
        if equipment_pool[equipment] <= 0:
            raise ValueError(f"{equipment} is unavailable.")

    for equipment in equipment_list:
        equipment_pool[equipment] -= 1

    reservation_id = next(reservation_ids)
    reservations[reservation_id] = {
        "room": room_id,
        "slot": time_slot,
        "equipment": equipment_list
    }
    return reservation_id


def cancel_reservation(reservation_id):
    """Cancel a reservation and return its allocated equipment."""
    reservation = reservations.get(reservation_id)

    if reservation is None:
        return False

    for equipment in reservation["equipment"]:
        equipment_pool[equipment] += 1

    del reservations[reservation_id]
    return True


def slot_hours(time_slot):
    """Calculate the duration of a valid time slot."""
    try:
        start, end = time_slot.split("-")
        start_hour = int(start)
        end_hour = int(end)
    except (AttributeError, ValueError) as error:
        raise ValueError(
            "Time slot must use the format HH-HH."
        ) from error

    if not 0 <= start_hour < end_hour <= 24:
        raise ValueError(
            "End time must be later than start time."
        )

    return end_hour - start_hour


def export_schedule(file="schedule.json"):
    """Export all reservations to a JSON file."""
    with open(file, "w", encoding="utf-8") as output_file:
        json.dump(reservations, output_file, indent=4)


def log_conflicts(file="conflicts.log"):
    """Append scheduling conflicts to a log file."""
    with open(file, "a", encoding="utf-8") as output_file:
        for conflict in conflicts:
            output_file.write(
                f"{datetime.now()} {conflict}\n"
            )

    with open(file, "r", encoding="utf-8") as log_file:
        print(log_file.read())


def main():
    """Run the room scheduling demonstration."""
    schedule_room("Board-1", "09-11")
    schedule_room("Board-1", "09-11")
    reservation_id = schedule_room("Huddle-3", "12-14")

    schedule_room("Huddle-3", "15-16")

    print(
        "Slot length for reservation:",
        slot_hours(reservations[reservation_id]["slot"])
    )

    cancel_reservation(77)

    slot = input(
        "Slot for Board-2, like 10-12 (Enter for 10-12): "
    ) or "10-12"

    schedule_room("Board-2", slot, ["projector", "webcam"])

    export_schedule()
    log_conflicts()

    print("Equipment left:", equipment_pool)
    print("Reservations:", reservations)


if __name__ == "__main__":
    main()
