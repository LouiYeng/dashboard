"""Sales Analytics API endpoints."""

from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import DashboardUser
from app.schemas.sales import SalesTrend, PaymentMethodSales
from app.services.sales_service import get_sales_trends, get_payment_method_analysis

router = APIRouter(prefix="/sales", tags=["Sales Analytics"])


@router.get("/trends", response_model=list[SalesTrend])
def sales_trends(
    period: str = Query("daily", regex="^(daily|weekly|monthly)$"),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: DashboardUser = Depends(get_current_user),
):
    """Get sales trends by period (daily, weekly, monthly)."""
    return get_sales_trends(db, period, date_from, date_to)


@router.get("/payment-methods", response_model=list[PaymentMethodSales])
def payment_methods(
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: DashboardUser = Depends(get_current_user),
):
    """Get detailed payment method analysis."""
    return get_payment_method_analysis(db, date_from, date_to)


@router.get("/top-products")
def top_products(
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    limit: int = Query(10),
    db: Session = Depends(get_db),
    current_user: DashboardUser = Depends(get_current_user),
):
    """Get top selling products. (Requires Products table — placeholder)."""
    # TODO: Implement when Products/TransactionDetails tables are added
    return {"message": "Awaiting Products table integration", "data": []}


@router.get("/by-category")
def sales_by_category(
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: DashboardUser = Depends(get_current_user),
):
    """Get sales breakdown by category. (Requires Categories table — placeholder)."""
    # TODO: Implement when Categories table is added
    return {"message": "Awaiting Categories table integration", "data": []}
