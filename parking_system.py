"""
Campus Parking Permit Manager
This module manages parking permits and handles zone validations.
"""

import json
import secrets
from datetime import datetime, timedelta

# Global state
PERMITS = {}
ZONES = ["A", "B", "C"]


def register_permit(vehicle_plate, zone_id, zone_records=None):
    """Register a new permit for a vehicle in a specific zone."""
    if zone_records is None:
        zone_records = []

    if not vehicle_plate or not zone_id:
        return None

    try:
        permit_no = "P" + str(secrets.randbelow(90000) + 10000)
        expiry = datetime.now() + timedelta(days=180)
        PERMITS[vehicle_plate] = {
            "zone": zone_id,
            "permit": permit_no,
            "expiry": expiry.strftime("%Y-%m-%d")
        }
        zone_records.append((vehicle_plate, zone_id))
        return permit_no
    except (TypeError, ValueError):
        return None


def revoke_permit(vehicle_plate):
    """Revoke an existing permit by vehicle plate."""
    try:
        if vehicle_plate in PERMITS:
            del PERMITS[vehicle_plate]
    except KeyError:
        pass


def is_expired(vehicle_plate):
    """Check if a vehicle's permit has expired based on the current date."""
    try:
        expiry_str = PERMITS[vehicle_plate]["expiry"]
        expiry = datetime.strptime(expiry_str, "%Y-%m-%d")
        return expiry < datetime.now()
    except (KeyError, ValueError, TypeError):
        return False


def scan_zone(zone_id, plates_seen):
    """Scan a zone and flag vehicles without valid, unexpired permits."""
    flagged = []
    for plate in plates_seen:
        if (plate not in PERMITS or
                PERMITS[plate]["zone"] != zone_id or
                is_expired(plate)):
            flagged.append(plate)
    return flagged


def load_permit_database(file="permits.json"):
    """Load the permit database from a JSON file into global memory."""
    try:
        with open(file, 'r', encoding="utf-8") as file_handle:
            data = json.load(file_handle)
            PERMITS.clear()
            PERMITS.update(data)
    except (FileNotFoundError, json.JSONDecodeError):
        PERMITS.clear()


def save_permit_database(file="permits.json"):
    """Save the current permit database state to a JSON file."""
    with open(file, "w", encoding="utf-8") as file_handle:
        json.dump(PERMITS, file_handle)


def set_expiry(vehicle_plate, date_text):
    """Set a specific expiry date for testing purposes."""
    if vehicle_plate in PERMITS:
        PERMITS[vehicle_plate]["expiry"] = date_text


def main():
    """Main execution flow for the parking permit system."""
    load_permit_database()
    register_permit("KA01AB1234", "A")
    register_permit("KA05XY9999", "Z")
    register_permit("", "B")
    register_permit(None, "C")

    # Fixed date format to match expected %Y-%m-%d in strptime
    set_expiry("KA01AB1234", "2020-01-01")
    revoke_permit("MH12ZZ0000")

    flagged_vehicles = scan_zone("A", ["KA01AB1234", "KA05XY9999", "TN09QQ1111"])
    print("Flagged in zone A:", flagged_vehicles)

    plate = input("Plate to revoke (Enter to skip): ")
    if plate:
        revoke_permit(plate)

    save_permit_database()
    print("Permits on file:", len(PERMITS))


if __name__ == "__main__":
    main()