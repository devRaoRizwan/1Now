from datetime import date

from app import repository
from app.repository import IDENTITY_FIELDS
from app.risk import INCIDENT_LABELS, assess


def assess_booking(connection, booking: dict) -> tuple[dict, list[dict], dict]:
    # Computed on every read, so a new or withdrawn report changes every host's view at once.
    vehicle = repository.get_vehicle(connection, booking["vehicle_id"])
    hashes = {field: booking[field] for field in IDENTITY_FIELDS}
    matches = repository.find_network_matches(connection, hashes, date.today())
    return assess(booking, vehicle, matches, booking["host_id"]), matches, vehicle


def with_incident_label(report: dict) -> dict:
    return {**report, "incident": INCIDENT_LABELS[report["incident_type"]]}


def public_match(match: dict, viewer_host_id: int) -> dict:
    # Other hosts may see what happened and when, never who reported it.
    return {
        "incident": INCIDENT_LABELS[match["incident_type"]],
        "severity": match["severity"],
        "incident_date": match["incident_date"],
        "matched_on": match["matched_on"],
        "reported_by_you": match["reporter_host_id"] == viewer_host_id,
    }


def booking_summary(connection, booking: dict) -> dict:
    risk, _, _ = assess_booking(connection, booking)
    return {
        "id": booking["id"],
        "renter_name": booking["renter_name"],
        "vehicle_name": booking["vehicle_name"],
        "start_date": booking["start_date"],
        "end_date": booking["end_date"],
        "status": booking["status"],
        "risk_score": risk["score"],
        "risk_level": risk["level"],
    }


def booking_detail(connection, booking: dict) -> dict:
    risk, matches, vehicle = assess_booking(connection, booking)
    own_reports = repository.list_booking_reports(connection, booking["id"], booking["host_id"])
    private_details = {key: value for key, value in booking.items() if key not in IDENTITY_FIELDS}
    return {
        **private_details,
        "vehicle": vehicle,
        "risk": risk,
        "network_matches": [public_match(match, booking["host_id"]) for match in matches],
        "my_reports": [with_incident_label(report) for report in own_reports],
    }


def report_overview(report: dict, today: date) -> dict:
    expired = date.fromisoformat(report["incident_date"]) < repository.retention_cutoff(today)
    return {**with_incident_label(report), "expired": expired}
