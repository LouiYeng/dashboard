"""Purchase Analytics API endpoints — placeholder for future tables."""

from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import DashboardUser

router = APIRouter(prefix="/purchases", tags=["Purchase Analytics"])


@router.get("/trends")
def purchase_trends(
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: DashboardUser = Depends(get_current_user),
):
    """Get purchase trends. (Placeholder — needs Purchase/GRN tables)."""
    return {"message": "Awaiting Purchase/GRN table integration", "data": []}


@router.get("/suppliers")
def supplier_performance(
    db: Session = Depends(get_db),
    current_user: DashboardUser = Depends(get_current_user),
):
    """Get supplier performance. (Placeholder)."""
    return {"message": "Awaiting Supplier table integration", "data": []}


@router.get("/summary")
def purchase_summary(
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: DashboardUser = Depends(get_current_user),
):
    """Get purchase summary. (Placeholder)."""
    return {"message": "Awaiting Purchase table integration", "data": {}}
