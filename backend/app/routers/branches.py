"""Branch Analytics API endpoints."""

from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import DashboardUser
from app.schemas.branches import BranchComparison, BranchRanking, BranchListItem
from app.services.branch_service import (
    get_all_branches, get_branch_comparison, get_branch_rankings,
)

router = APIRouter(prefix="/branches", tags=["Branch Analytics"])


@router.get("/list", response_model=list[BranchListItem])
def list_branches(
    db: Session = Depends(get_db),
    current_user: DashboardUser = Depends(get_current_user),
):
    """Get all branches for selector dropdowns."""
    return get_all_branches(db)


@router.get("/compare", response_model=list[BranchComparison])
def compare_branches(
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: DashboardUser = Depends(get_current_user),
):
    """Compare all branches across key metrics."""
    return get_branch_comparison(db, date_from, date_to)


@router.get("/rankings", response_model=list[BranchRanking])
def branch_rankings(
    metric: str = Query("sales", regex="^(sales|customers|transactions)$"),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: DashboardUser = Depends(get_current_user),
):
    """Get branch rankings by metric."""
    return get_branch_rankings(db, metric, date_from, date_to)
