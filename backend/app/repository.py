import sqlite3
from datetime import date, timedelta

from app.config import REPORT_RETENTION_DAYS
from app.identity import identity_hashes

IDENTITY_FIELDS = ("email_hash", "phone_hash", "license_hash")

BOOKINGS_FOR_HOST = (
    "SELECT b.*, v.name AS vehicle_name FROM bookings b "
    "JOIN vehicles v ON v.id = b.vehicle_id "
    "WHERE b.host_id = ? "
    "ORDER BY CASE b.status WHEN 'pending' THEN 0 WHEN 'info_requested' THEN 1 ELSE 2 END, b.start_date"
)

REPORTS_BY_HOST = (
    "SELECT r.id, r.booking_id, r.incident_type, r.severity, r.incident_date, r.private_note, b.renter_name "
    "FROM network_reports r JOIN bookings b ON b.id = r.booking_id "
    "WHERE r.reporter_host_id = ? "
    "ORDER BY r.incident_date DESC"
)

# Deliberately selects no private notes or booking ids: these rows are shown to other hosts.
NETWORK_MATCHES = (
    "SELECT reporter_host_id, incident_type, severity, incident_date, "
    "license_hash = :license_hash AS license_match, "
    "email_hash = :email_hash AS email_match, "
    "phone_hash = :phone_hash AS phone_match "
    "FROM network_reports "
    "WHERE (license_hash = :license_hash OR email_hash = :email_hash OR phone_hash = :phone_hash) "
    "AND incident_date >= :cutoff "
    "ORDER BY incident_date DESC"
)


def fetch_one(connection: sqlite3.Connection, sql: str, params=()) -> dict | None:
    row = connection.execute(sql, params).fetchone()
    return dict(row) if row else None


def fetch_all(connection: sqlite3.Connection, sql: str, params=()) -> list[dict]:
    return [dict(row) for row in connection.execute(sql, params)]


def insert(connection: sqlite3.Connection, table: str, values: dict) -> int:
    columns = ", ".join(values)
    placeholders = ", ".join(f":{column}" for column in values)
    cursor = connection.execute(f"INSERT INTO {table} ({columns}) VALUES ({placeholders})", values)
    return cursor.lastrowid


def retention_cutoff(today: date) -> date:
    return today - timedelta(days=REPORT_RETENTION_DAYS)


# Hosts and vehicles

def list_hosts(connection):
    return fetch_all(connection, "SELECT * FROM hosts ORDER BY id")


def list_vehicles(connection, host_id: int):
    return fetch_all(connection, "SELECT * FROM vehicles WHERE host_id = ? ORDER BY id", (host_id,))


def get_vehicle(connection, vehicle_id: int):
    return fetch_one(connection, "SELECT * FROM vehicles WHERE id = ?", (vehicle_id,))


def find_host_vehicle(connection, host_id: int, vehicle_id: int):
    return fetch_one(connection, "SELECT * FROM vehicles WHERE id = ? AND host_id = ?", (vehicle_id, host_id))


# Bookings

def get_booking(connection, booking_id: int):
    return fetch_one(connection, "SELECT * FROM bookings WHERE id = ?", (booking_id,))


def list_bookings(connection, host_id: int):
    return fetch_all(connection, BOOKINGS_FOR_HOST, (host_id,))


def create_booking(connection, host_id: int, vehicle_id: int, renter: dict,
                   start_date: str, end_date: str, booked_on: str, status: str = "pending") -> int:
    hashes = identity_hashes(renter["email"], renter["phone"], renter["license_state"], renter["license_number"])
    return insert(connection, "bookings", {
        "host_id": host_id,
        "vehicle_id": vehicle_id,
        "renter_name": renter["name"],
        "renter_email": renter["email"],
        "renter_phone": renter["phone"],
        "license_state": renter["license_state"].upper(),
        "license_number": renter["license_number"],
        "license_expiry": renter["license_expiry"],
        "date_of_birth": renter["date_of_birth"],
        "start_date": start_date,
        "end_date": end_date,
        "booked_on": booked_on,
        "status": status,
        **hashes,
    })


def set_booking_status(connection, booking_id: int, status: str) -> None:
    connection.execute("UPDATE bookings SET status = ? WHERE id = ?", (status, booking_id))


# Network reports

def create_report(connection, booking: dict, reporter_host_id: int, incident_type: str,
                  severity: str, incident_date: str, private_note: str, created_on: str) -> int:
    return insert(connection, "network_reports", {
        "reporter_host_id": reporter_host_id,
        "booking_id": booking["id"],
        **{field: booking[field] for field in IDENTITY_FIELDS},
        "incident_type": incident_type,
        "severity": severity,
        "incident_date": incident_date,
        "private_note": private_note,
        "created_on": created_on,
    })


def get_report(connection, report_id: int):
    return fetch_one(connection, "SELECT * FROM network_reports WHERE id = ?", (report_id,))


def report_exists(connection, booking_id: int, incident_type: str) -> bool:
    return fetch_one(
        connection,
        "SELECT 1 FROM network_reports WHERE booking_id = ? AND incident_type = ?",
        (booking_id, incident_type),
    ) is not None


def delete_report(connection, report_id: int) -> None:
    connection.execute("DELETE FROM network_reports WHERE id = ?", (report_id,))


def list_host_reports(connection, host_id: int):
    return fetch_all(connection, REPORTS_BY_HOST, (host_id,))


def list_booking_reports(connection, booking_id: int, host_id: int):
    return fetch_all(
        connection,
        "SELECT id, incident_type, severity, incident_date, private_note FROM network_reports "
        "WHERE booking_id = ? AND reporter_host_id = ?",
        (booking_id, host_id),
    )


def find_network_matches(connection, hashes: dict, today: date) -> list[dict]:
    rows = fetch_all(connection, NETWORK_MATCHES, {**hashes, "cutoff": retention_cutoff(today).isoformat()})
    return [
        {
            "reporter_host_id": row["reporter_host_id"],
            "incident_type": row["incident_type"],
            "severity": row["severity"],
            "incident_date": row["incident_date"],
            "matched_on": [kind for kind in ("license", "email", "phone") if row[f"{kind}_match"]],
        }
        for row in rows
    ]
