from fastapi import HTTPException

from app import repository

# There is no login in this MVP: callers say which host they are with host_id.
# In production host_id would come from the authenticated session instead.


def require_booking_owner(connection, booking_id: int, host_id: int) -> dict:
    booking = repository.get_booking(connection, booking_id)
    if booking is None:
        raise HTTPException(404, "Booking not found")
    if booking["host_id"] != host_id:
        raise HTTPException(403, "This booking belongs to another company")
    return booking


def require_report_owner(connection, report_id: int, host_id: int) -> dict:
    report = repository.get_report(connection, report_id)
    if report is None:
        raise HTTPException(404, "Report not found")
    if report["reporter_host_id"] != host_id:
        raise HTTPException(403, "Only the company that made a report can withdraw it")
    return report
