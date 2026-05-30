"""
Dashboard service — business logic for executive KPI calculations.

All sales calculations are derived from the Zeds (Z-reading) table,
which records per-session settlement data for each till.
"""

from datetime import date, datetime, timedelta
from typing import Optional, List
from sqlalchemy import func, cast, Date
from sqlalchemy.orm import Session
from app.models.pos import Zed, Branch
from app.schemas.dashboard import (
    KPISummary, BranchPerformance, PaymentMethodBreakdown,
    DashboardResponse, DailySummary,
)


# Column groups for aggregation
SALES_COLUMNS = [
    "CashSales", "CreditCardSales", "MPESAPayBillSales",
    "AirTelPayBillSales", "mVisaPayBillSales", "EasyPayPayBillSales",
    "UMIPayBillSales", "VOOMAPayBillSales", "GiftVoucherSales",
    "GiftVoucherSalesHQ", "ChqSales", "CAPSales", "LoyaltySales",
    "QSokoSales", "Scheme11DiscountSales", "Scheme11CouponSales",
]

MOBILE_COLUMNS = [
    "MPESAPayBillSales", "AirTelPayBillSales", "mVisaPayBillSales",
    "EasyPayPayBillSales", "UMIPayBillSales", "VOOMAPayBillSales",
]


def _coalesce(col):
    """Wrap column in COALESCE to handle NULLs."""
    return func.coalesce(col, 0)


def _total_sales_expr():
    """SQLAlchemy expression for total sales across all payment methods."""
    return sum(
        _coalesce(getattr(Zed, col)) for col in SALES_COLUMNS
    )


def _mobile_sales_expr():
    """SQLAlchemy expression for total mobile money sales."""
    return sum(
        _coalesce(getattr(Zed, col)) for col in MOBILE_COLUMNS
    )


def _cash_in_hand_expr():
    """SQLAlchemy expression for cash in hand calculation."""
    inflows = (
        _coalesce(Zed.TotalFloat) +
        _coalesce(Zed.CashSales) +
        _coalesce(Zed.StaffDeposits) +
        _coalesce(Zed.EPurseDeposits) +
        _coalesce(Zed.VarianceRecovered)
    )
    outflows = (
        _coalesce(Zed.CashPurchases) +
        _coalesce(Zed.RemitToHq) +
        _coalesce(Zed.StaffPayments) +
        _coalesce(Zed.StaffAdvance) +
        _coalesce(Zed.EPurseWithdrawals) +
        _coalesce(Zed.EBankDeposits) +
        _coalesce(Zed.NewFloatCF)
    )
    return inflows - outflows


def _apply_date_filter(query, date_from: Optional[date] = None, date_to: Optional[date] = None):
    """Apply date range filter to a query."""
    if date_from:
        query = query.filter(cast(Zed.TrnDate, Date) >= date_from)
    if date_to:
        query = query.filter(cast(Zed.TrnDate, Date) <= date_to)
    return query


def get_kpi_summary(
    db: Session,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    branch_code: Optional[int] = None,
) -> KPISummary:
    """
    Calculate executive dashboard KPIs from Zeds data.

    Computes: total sales, purchases, cash in hand, customer count,
    transaction count, and percentage changes vs previous period.
    """
    # Default to today if no dates provided
    if not date_from and not date_to:
        date_from = date_to = date.today()

    # Current period query
    query = db.query(
        func.sum(_total_sales_expr()).label("total_sales"),
        func.sum(_coalesce(Zed.CashPurchases)).label("total_purchases"),
        func.sum(_cash_in_hand_expr()).label("cash_in_hand"),
        func.sum(_coalesce(Zed.Customers)).label("customer_count"),
        func.count().label("transaction_count"),
        func.sum(_coalesce(Zed.StaffPayments) + _coalesce(Zed.StampDuty)).label("total_expenses"),
    )
    query = _apply_date_filter(query, date_from, date_to)

    result = query.first()

    total_sales = float(result.total_sales or 0)
    total_purchases = float(result.total_purchases or 0)
    total_expenses = float(result.total_expenses or 0)
    cash_in_hand = float(result.cash_in_hand or 0)
    customer_count = int(result.customer_count or 0)
    transaction_count = int(result.transaction_count or 0)
    gross_profit = total_sales - total_purchases
    net_profit = gross_profit - total_expenses
    avg_transaction = total_sales / transaction_count if transaction_count > 0 else 0

    # Previous period for change calculation
    if date_from and date_to:
        period_length = (date_to - date_from).days + 1
        prev_from = date_from - timedelta(days=period_length)
        prev_to = date_from - timedelta(days=1)

        prev_query = db.query(
            func.sum(_total_sales_expr()).label("total_sales"),
            func.sum(_coalesce(Zed.CashPurchases)).label("total_purchases"),
            func.sum(_coalesce(Zed.Customers)).label("customer_count"),
        )
        prev_query = _apply_date_filter(prev_query, prev_from, prev_to)
        prev = prev_query.first()

        prev_sales = float(prev.total_sales or 0)
        prev_purchases = float(prev.total_purchases or 0)
        prev_customers = int(prev.customer_count or 0)
        prev_profit = prev_sales - prev_purchases

        sales_change = ((total_sales - prev_sales) / prev_sales * 100) if prev_sales else 0
        purchases_change = ((total_purchases - prev_purchases) / prev_purchases * 100) if prev_purchases else 0
        profit_change = ((gross_profit - prev_profit) / prev_profit * 100) if prev_profit else 0
        customer_change = ((customer_count - prev_customers) / prev_customers * 100) if prev_customers else 0
    else:
        sales_change = purchases_change = profit_change = customer_change = 0

    return KPISummary(
        total_sales=round(total_sales, 2),
        total_purchases=round(total_purchases, 2),
        total_expenses=round(total_expenses, 2),
        gross_profit=round(gross_profit, 2),
        net_profit=round(net_profit, 2),
        cash_in_hand=round(cash_in_hand, 2),
        customer_count=customer_count,
        transaction_count=transaction_count,
        avg_transaction_value=round(avg_transaction, 2),
        sales_change=round(sales_change, 1),
        purchases_change=round(purchases_change, 1),
        profit_change=round(profit_change, 1),
        customer_change=round(customer_change, 1),
    )


def get_payment_breakdown(
    db: Session,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
) -> List[PaymentMethodBreakdown]:
    """Get sales breakdown by payment method."""
    if not date_from and not date_to:
        date_from = date_to = date.today()

    # Define payment methods with display names and colors
    payment_methods = [
        ("Cash", "CashSales", "#10b981"),
        ("M-PESA", "MPESAPayBillSales", "#22c55e"),
        ("Credit Card", "CreditCardSales", "#6366f1"),
        ("Airtel Money", "AirTelPayBillSales", "#ef4444"),
        ("mVisa", "mVisaPayBillSales", "#f59e0b"),
        ("VOOMA", "VOOMAPayBillSales", "#06b6d4"),
        ("EasyPay", "EasyPayPayBillSales", "#8b5cf6"),
        ("UMI", "UMIPayBillSales", "#ec4899"),
        ("Cheque", "ChqSales", "#64748b"),
        ("Gift Voucher", "GiftVoucherSales", "#14b8a6"),
        ("CAP (Credit)", "CAPSales", "#f97316"),
        ("Loyalty", "LoyaltySales", "#a855f7"),
        ("QSoko", "QSokoSales", "#0ea5e9"),
    ]

    results = []
    total = 0

    for display_name, col_name, color in payment_methods:
        query = db.query(
            func.sum(_coalesce(getattr(Zed, col_name))).label("amount")
        )
        query = _apply_date_filter(query, date_from, date_to)
        amount = float(query.scalar() or 0)
        if amount > 0:
            results.append(PaymentMethodBreakdown(
                method=display_name,
                amount=round(amount, 2),
                percentage=0,  # calculated below
                color=color,
            ))
            total += amount

    # Calculate percentages
    for item in results:
        item.percentage = round((item.amount / total * 100) if total > 0 else 0, 1)

    return sorted(results, key=lambda x: x.amount, reverse=True)


def get_daily_trends(
    db: Session,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    days: int = 30,
) -> List[DailySummary]:
    """Get daily sales trends for the specified period."""
    if not date_from:
        date_from = date.today() - timedelta(days=days)
    if not date_to:
        date_to = date.today()

    query = db.query(
        cast(Zed.TrnDate, Date).label("sale_date"),
        func.sum(_total_sales_expr()).label("total_sales"),
        func.sum(_coalesce(Zed.CashSales)).label("cash_sales"),
        func.sum(_coalesce(Zed.CreditCardSales)).label("card_sales"),
        func.sum(_mobile_sales_expr()).label("mobile_sales"),
        func.sum(_coalesce(Zed.Customers)).label("customers"),
        func.count().label("transactions"),
    ).filter(
        cast(Zed.TrnDate, Date) >= date_from,
        cast(Zed.TrnDate, Date) <= date_to,
    ).group_by(
        cast(Zed.TrnDate, Date)
    ).order_by(
        cast(Zed.TrnDate, Date)
    )

    return [
        DailySummary(
            date=str(row.sale_date),
            total_sales=round(float(row.total_sales or 0), 2),
            cash_sales=round(float(row.cash_sales or 0), 2),
            card_sales=round(float(row.card_sales or 0), 2),
            mobile_sales=round(float(row.mobile_sales or 0), 2),
            customers=int(row.customers or 0),
            transactions=int(row.transactions or 0),
        )
        for row in query.all()
    ]


def get_branch_performance(
    db: Session,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
) -> List[BranchPerformance]:
    """
    Get performance summary per branch.

    NOTE: Since the Zeds table doesn't have a direct branch_code column,
    this currently returns aggregate data. When branch-till mapping is
    available, this will be updated to group by branch.
    """
    if not date_from and not date_to:
        date_from = date_to = date.today()

    # Get all branches
    branches = db.query(Branch).all()

    # For now, return aggregate data attributed to each branch
    # TODO: Update when branch-till mapping is available
    query = db.query(
        func.sum(_total_sales_expr()).label("total_sales"),
        func.sum(_coalesce(Zed.CashSales)).label("cash_sales"),
        func.sum(_mobile_sales_expr()).label("mobile_sales"),
        func.sum(_coalesce(Zed.CreditCardSales)).label("card_sales"),
        func.sum(_coalesce(Zed.Customers)).label("total_customers"),
        func.count().label("total_sessions"),
    )
    query = _apply_date_filter(query, date_from, date_to)
    agg = query.first()

    results = []
    for branch in branches:
        total_sales = float(agg.total_sales or 0) / max(len(branches), 1)
        total_customers = int(agg.total_customers or 0) // max(len(branches), 1)
        total_sessions = int(agg.total_sessions or 0) // max(len(branches), 1)

        results.append(BranchPerformance(
            branch_code=branch.BranchCode,
            branch_name=branch.BranchName or f"Branch {branch.BranchCode}",
            total_sales=round(total_sales, 2),
            total_customers=total_customers,
            total_sessions=total_sessions,
            cash_sales=round(float(agg.cash_sales or 0) / max(len(branches), 1), 2),
            mobile_sales=round(float(agg.mobile_sales or 0) / max(len(branches), 1), 2),
            card_sales=round(float(agg.card_sales or 0) / max(len(branches), 1), 2),
            avg_transaction=round(total_sales / total_sessions, 2) if total_sessions else 0,
        ))

    return results
