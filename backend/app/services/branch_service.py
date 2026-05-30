"""Branch analytics service."""

from datetime import date
from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.pos import Branch
from app.schemas.branches import BranchComparison, BranchRanking, BranchListItem
from app.services.dashboard_service import get_branch_performance


def get_all_branches(db: Session) -> List[BranchListItem]:
    """Get all branches for dropdown selectors."""
    branches = db.query(Branch).order_by(Branch.BranchCode).all()
    return [
        BranchListItem(
            branch_code=b.BranchCode,
            branch_name=b.BranchName or f"Branch {b.BranchCode}",
            branch_name_short=b.BranchNameShort,
        )
        for b in branches
    ]


def get_branch_comparison(
    db: Session,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
) -> List[BranchComparison]:
    """Compare all branches across metrics."""
    performances = get_branch_performance(db, date_from, date_to)
    return [
        BranchComparison(
            branch_code=p.branch_code,
            branch_name=p.branch_name,
            total_sales=p.total_sales,
            total_purchases=0,  # TODO: from purchases table
            total_customers=p.total_customers,
            cash_sales=p.cash_sales,
            mobile_sales=p.mobile_sales,
            card_sales=p.card_sales,
            cash_in_hand=0,
            sessions_count=p.total_sessions,
        )
        for p in performances
    ]


def get_branch_rankings(
    db: Session,
    metric: str = "sales",
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
) -> List[BranchRanking]:
    """Rank branches by a specific metric."""
    performances = get_branch_performance(db, date_from, date_to)

    metric_map = {
        "sales": ("total_sales", "Total Sales"),
        "customers": ("total_customers", "Total Customers"),
        "transactions": ("total_sessions", "Total Sessions"),
    }
    attr, metric_name = metric_map.get(metric, ("total_sales", "Total Sales"))

    sorted_branches = sorted(performances, key=lambda p: getattr(p, attr), reverse=True)

    return [
        BranchRanking(
            rank=i + 1,
            branch_code=b.branch_code,
            branch_name=b.branch_name,
            metric_value=float(getattr(b, attr)),
            metric_name=metric_name,
        )
        for i, b in enumerate(sorted_branches)
    ]
