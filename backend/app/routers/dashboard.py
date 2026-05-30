"""Executive Dashboard API endpoints."""

from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import DashboardUser
from app.schemas.dashboard import (
    KPISummary, DashboardResponse, DailySummary, PaymentMethodBreakdown,
    BranchPerformance,
)
from app.services.dashboard_service import (
    get_kpi_summary, get_payment_breakdown, get_daily_trends,
    get_branch_performance,
)

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary", response_model=KPISummary)
def dashboard_summary(
    date_from: Optional[date] = Query(None, description="Start date (YYYY-MM-DD)"),
    date_to: Optional[date] = Query(None, description="End date (YYYY-MM-DD)"),
    branch_code: Optional[int] = Query(None, description="Filter by branch"),
    db: Session = Depends(get_db),
    current_user: DashboardUser = Depends(get_current_user),
):
    """Get executive dashboard KPI summary."""
    return get_kpi_summary(db, date_from, date_to, branch_code)


@router.get("/payment-breakdown", response_model=list[PaymentMethodBreakdown])
def payment_breakdown(
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: DashboardUser = Depends(get_current_user),
):
    """Get sales breakdown by payment method."""
    return get_payment_breakdown(db, date_from, date_to)


@router.get("/trends", response_model=list[DailySummary])
def daily_trends(
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    days: int = Query(30, description="Number of days for trend"),
    db: Session = Depends(get_db),
    current_user: DashboardUser = Depends(get_current_user),
):
    """Get daily sales trend data for charts."""
    return get_daily_trends(db, date_from, date_to, days)


@router.get("/branch-performance", response_model=list[BranchPerformance])
def branch_performance(
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: DashboardUser = Depends(get_current_user),
):
    """Get performance summary for each branch."""
    return get_branch_performance(db, date_from, date_to)
