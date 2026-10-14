from fastapi import APIRouter, Depends

from app import repository
from app.access import require_report_owner
from app.database import get_connection

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.delete("/{report_id}")
def withdraw_report(report_id: int, host_id: int, connection=Depends(get_connection)):
    require_report_owner(connection, report_id, host_id)
    repository.delete_report(connection, report_id)
    connection.commit()
    return {"withdrawn": report_id}
