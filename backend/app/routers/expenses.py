"""Expense Analytics API endpoints — placeholder for future tables."""

from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import DashboardUser

router = APIRouter(prefix="/expenses", tags=["Expense Analytics"])


@router.get("/breakdown")
def expense_breakdown(
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: DashboardUser = Depends(get_current_user),
):
    """Get expense breakdown by category. (Placeholder — needs Expenses table)."""
    return {"message": "Awaiting Expenses table integration", "data": []}


@router.get("/trends")
def expense_trends(
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: DashboardUser = Depends(get_current_user),
):
    """Get monthly expense trends. (Placeholder)."""
    return {"message": "Awaiting Expenses table integration", "data": []}


@router.get("/summary")
def expense_summary(
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: DashboardUser = Depends(get_current_user),
):
    """Get expense summary. (Placeholder)."""
    return {"message": "Awaiting Expenses table integration", "data": {"total": 0, "categories": []}}
