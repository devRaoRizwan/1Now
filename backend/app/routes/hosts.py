from datetime import date

from fastapi import APIRouter, Depends

from app import repository
from app.database import get_connection
from app.services import booking_summary, report_overview

router = APIRouter(prefix="/api/hosts", tags=["hosts"])


@router.get("")
def list_hosts(connection=Depends(get_connection)):
    return repository.list_hosts(connection)


@router.get("/{host_id}/vehicles")
def list_vehicles(host_id: int, connection=Depends(get_connection)):
    return repository.list_vehicles(connection, host_id)


@router.get("/{host_id}/bookings")
def list_bookings(host_id: int, connection=Depends(get_connection)):
    return [booking_summary(connection, booking) for booking in repository.list_bookings(connection, host_id)]


@router.get("/{host_id}/reports")
def list_reports(host_id: int, connection=Depends(get_connection)):
    today = date.today()
    return [report_overview(report, today) for report in repository.list_host_reports(connection, host_id)]
