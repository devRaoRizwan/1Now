from datetime import date

from fastapi import APIRouter, Depends, HTTPException

from app import repository
from app.access import require_booking_owner
from app.database import get_connection
from app.models import BookingCreate, DecisionUpdate, ReportCreate
from app.services import booking_detail

router = APIRouter(prefix="/api/bookings", tags=["bookings"])

OPEN_STATUSES = {"pending", "info_requested"}


@router.get("/{booking_id}")
def read_booking(booking_id: int, host_id: int, connection=Depends(get_connection)):
    return booking_detail(connection, require_booking_owner(connection, booking_id, host_id))


@router.post("", status_code=201)
def create_booking(body: BookingCreate, connection=Depends(get_connection)):
    if repository.find_host_vehicle(connection, body.host_id, body.vehicle_id) is None:
        raise HTTPException(400, "This car does not belong to the company")

    booking_id = repository.create_booking(
        connection, body.host_id, body.vehicle_id, body.renter(),
        body.start_date.isoformat(), body.end_date.isoformat(), date.today().isoformat(),
    )
    connection.commit()
    return booking_detail(connection, repository.get_booking(connection, booking_id))


@router.post("/{booking_id}/decision")
def decide(booking_id: int, body: DecisionUpdate, connection=Depends(get_connection)):
    booking = require_booking_owner(connection, booking_id, body.host_id)
    if booking["status"] not in OPEN_STATUSES:
        raise HTTPException(409, f"Booking is already {booking['status']}")

    repository.set_booking_status(connection, booking_id, body.decision)
    connection.commit()
    return booking_detail(connection, repository.get_booking(connection, booking_id))


@router.post("/{booking_id}/report", status_code=201)
def report_customer(booking_id: int, body: ReportCreate, connection=Depends(get_connection)):
    booking = require_booking_owner(connection, booking_id, body.host_id)
    today = date.today()
    if body.incident_date > today:
        raise HTTPException(400, "Incident date can't be in the future")
    if repository.report_exists(connection, booking_id, body.incident_type):
        raise HTTPException(409, "You already reported this incident type for this booking")

    repository.create_report(
        connection, booking, body.host_id, body.incident_type, body.severity,
        body.incident_date.isoformat(), body.private_note.strip(), today.isoformat(),
    )
    connection.commit()
    return booking_detail(connection, booking)
