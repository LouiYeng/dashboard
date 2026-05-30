"""Inventory Analytics API endpoints — placeholder for future tables."""

from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import DashboardUser

router = APIRouter(prefix="/inventory", tags=["Inventory Analytics"])


@router.get("/overview")
def inventory_overview(
    branch_code: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: DashboardUser = Depends(get_current_user),
):
    """Get inventory overview. (Requires Stock tables — placeholder)."""
    # TODO: Implement when Stock/Inventory tables are added
    return {
        "message": "Awaiting Stock table integration",
        "data": {
            "total_stock_value": 0,
            "total_items": 0,
            "low_stock_count": 0,
            "out_of_stock_count": 0,
        }
    }


@router.get("/low-stock")
def low_stock_alerts(
    threshold: int = Query(10),
    db: Session = Depends(get_db),
    current_user: DashboardUser = Depends(get_current_user),
):
    """Get low stock alerts. (Placeholder)."""
    return {"message": "Awaiting Stock table integration", "data": []}


@router.get("/movement")
def stock_movement(
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: DashboardUser = Depends(get_current_user),
):
    """Get fast/slow moving products. (Placeholder)."""
    return {"message": "Awaiting Stock Movement table integration", "data": {"fast_moving": [], "slow_moving": []}}
