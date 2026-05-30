"""Dashboard response schemas for executive KPIs and summaries."""

from pydantic import BaseModel
from typing import List, Optional


class KPISummary(BaseModel):
    """Executive dashboard KPI summary."""
    total_sales: float = 0
    total_purchases: float = 0
    total_expenses: float = 0
    gross_profit: float = 0
    net_profit: float = 0
    cash_in_hand: float = 0
    customer_count: int = 0
    transaction_count: int = 0
    avg_transaction_value: float = 0
    # Change percentages compared to previous period
    sales_change: float = 0
    purchases_change: float = 0
    profit_change: float = 0
    customer_change: float = 0


class BranchPerformance(BaseModel):
    """Performance data for a single branch."""
    branch_code: int
    branch_name: str
    total_sales: float = 0
    total_customers: int = 0
    total_sessions: int = 0
    cash_sales: float = 0
    mobile_sales: float = 0
    card_sales: float = 0
    avg_transaction: float = 0


class PaymentMethodBreakdown(BaseModel):
    """Sales breakdown by payment method."""
    method: str
    amount: float
    percentage: float
    color: str = ""


class DashboardResponse(BaseModel):
    """Complete executive dashboard response."""
    kpi: KPISummary
    branch_performance: List[BranchPerformance]
    payment_breakdown: List[PaymentMethodBreakdown]


class DailySummary(BaseModel):
    """Single day summary for trend charts."""
    date: str
    total_sales: float = 0
    cash_sales: float = 0
    card_sales: float = 0
    mobile_sales: float = 0
    customers: int = 0
    transactions: int = 0
