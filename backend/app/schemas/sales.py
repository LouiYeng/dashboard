"""Sales analytics response schemas."""

from pydantic import BaseModel
from typing import List, Optional


class SalesTrend(BaseModel):
    """Sales trend data point."""
    period: str  # date string, week label, or month label
    total_sales: float = 0
    cash_sales: float = 0
    card_sales: float = 0
    mobile_sales: float = 0
    other_sales: float = 0
    customers: int = 0


class PaymentMethodSales(BaseModel):
    """Sales for a specific payment method."""
    method: str
    amount: float
    percentage: float
    transaction_count: int = 0


class HourlySales(BaseModel):
    """Sales broken down by hour of day."""
    hour: int
    total_sales: float = 0
    customers: int = 0


class SalesSummaryResponse(BaseModel):
    """Full sales analytics response."""
    trends: List[SalesTrend]
    payment_methods: List[PaymentMethodSales]
    total_sales: float = 0
    total_customers: int = 0
    avg_daily_sales: float = 0
