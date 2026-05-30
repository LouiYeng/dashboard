"""Export API endpoints — PDF, Excel, CSV downloads."""

from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import DashboardUser
from app.services.export_service import generate_pdf, generate_excel, generate_csv

router = APIRouter(prefix="/exports", tags=["Exports"])


@router.get("/pdf")
def export_pdf(
    report_type: str = Query("dashboard"),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: DashboardUser = Depends(get_current_user),
):
    """Export dashboard report as PDF."""
    buffer = generate_pdf(db, report_type, date_from, date_to)
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=dashboard_report_{date_from}_{date_to}.pdf"},
    )


@router.get("/excel")
def export_excel(
    report_type: str = Query("dashboard"),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: DashboardUser = Depends(get_current_user),
):
    """Export dashboard report as Excel (.xlsx)."""
    buffer = generate_excel(db, report_type, date_from, date_to)
    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=dashboard_report_{date_from}_{date_to}.xlsx"},
    )


@router.get("/csv")
def export_csv(
    report_type: str = Query("dashboard"),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: DashboardUser = Depends(get_current_user),
):
    """Export dashboard report as CSV."""
    buffer = generate_csv(db, report_type, date_from, date_to)
    return StreamingResponse(
        iter([buffer.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=dashboard_report_{date_from}_{date_to}.csv"},
    )
