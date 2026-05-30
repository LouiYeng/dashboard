"""Branch analytics response schemas."""

from pydantic import BaseModel
from typing import List, Optional


class BranchComparison(BaseModel):
    """Branch comparison data."""
    branch_code: int
    branch_name: str
    total_sales: float = 0
    total_purchases: float = 0
    total_customers: int = 0
    cash_sales: float = 0
    mobile_sales: float = 0
    card_sales: float = 0
    cash_in_hand: float = 0
    sessions_count: int = 0


class BranchRanking(BaseModel):
    """Branch ranking entry."""
    rank: int
    branch_code: int
    branch_name: str
    metric_value: float
    metric_name: str


class BranchListItem(BaseModel):
    """Branch list item for dropdowns."""
    branch_code: int
    branch_name: str
    branch_name_short: Optional[str] = None

    class Config:
        from_attributes = True
