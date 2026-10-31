
"""Campus shuttle timetable and fleet tracking system."""

import json
import random
from datetime import datetime

# Global shuttle route data.
routes = {
    "R1": {"name": "Main Gate - Library", "trips": []},
    "R2": {"name": "Hostel - Sports Complex", "trips": []},
    "R3": {"name": "Admin Block - Metro", "trips": []},
}

MIN_CAPACITY = 10


def add_trip_log(route_id, passenger_count, logs=None):
    """Add a passenger count to a route and record the trip."""
    if logs is None:
        logs = []

    if route_id not in routes:
        raise KeyError(f"Route {route_id} does not exist.")

    routes[route_id]["trips"].append(passenger_count)
    logs.append(
        f"{datetime.now()}: {route_id} carried {passenger_count}"
    )
    return logs


def remove_route(route_id):
    """Remove a route from the shuttle system."""
    if route_id not in routes:
        raise KeyError(f"Route {route_id} does not exist.")

    del routes[route_id]


def average_load(route_id):
    """Calculate the average passenger count for a route."""
    if route_id not in routes:
        raise KeyError(f"Route {route_id} does not exist.")

    trips = routes[route_id]["trips"]

    if not trips:
        return 0

    return sum(trips) / len(trips)


def underused_routes():
    """Return routes whose average load is below minimum capacity."""
    flagged = []

    for route_id in routes:
        try:
            if average_load(route_id) < MIN_CAPACITY:
                flagged.append(route_id)
        except (KeyError, TypeError, ZeroDivisionError):
            continue

    return flagged


def assign_driver(route_id):
    """Assign a randomly selected driver to an existing route."""
    if route_id not in routes:
        raise KeyError(f"Route {route_id} does not exist.")

    drivers = ["Prakash", "Leela", "Imran", "Tom"]
    return random.choice(drivers)


def sync_fleet_data(file="fleet.json"):
    """Save fleet data to JSON and read it back safely."""
    with open(file, "w", encoding="utf-8") as fleet_file:
        json.dump(routes, fleet_file, indent=4)

    with open(file, "r", encoding="utf-8") as fleet_file:
        return json.load(fleet_file)


def main():
    """Run the campus shuttle demonstration."""
    add_trip_log("R1", 32)
    add_trip_log("R1", 28)
    add_trip_log("R2", 4)
    add_trip_log("R2", -6)
    add_trip_log("R3", "full")

    print("Driver for R1:", assign_driver("R1"))
    print("Underused:", underused_routes())
    print("R1 average:", average_load("R1"))

    fleet_data = sync_fleet_data()
    routes.update(fleet_data)

    remove_route("R3")

    choice = input("Route to look up (Enter for R2): ") or "R2"

    if choice in routes:
        print("Trips on", choice, ":", routes[choice]["trips"])
    else:
        print(f"Route {choice} was not found.")

    try:
        print("R3 average:", average_load("R3"))
    except KeyError as error:
        print(f"Unable to calculate average: {error}")


if __name__ == "__main__":
    main()
