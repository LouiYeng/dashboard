"""Sales analytics service — trends, breakdowns, and detailed analysis."""

from datetime import date, timedelta
from typing import Optional, List
from sqlalchemy import func, cast, Date, extract
from sqlalchemy.orm import Session
from app.models.pos import Zed
from app.schemas.sales import SalesTrend, PaymentMethodSales
from app.services.dashboard_service import (
    _total_sales_expr, _mobile_sales_expr, _coalesce, _apply_date_filter
)


def get_sales_trends(
    db: Session,
    period: str = "daily",
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
) -> List[SalesTrend]:
    """
    Get sales trends grouped by period (daily, weekly, monthly).
    """
    if not date_to:
        date_to = date.today()
    if not date_from:
        if period == "daily":
            date_from = date_to - timedelta(days=30)
        elif period == "weekly":
            date_from = date_to - timedelta(weeks=12)
        else:
            date_from = date_to - timedelta(days=365)

    if period == "daily":
        group_expr = cast(Zed.TrnDate, Date)
        label_func = lambda r: str(r.period)
    elif period == "weekly":
        group_expr = func.datepart("iso_week", Zed.TrnDate)
        label_func = lambda r: f"Week {r.period}"
    else:  # monthly
        group_expr = func.format(Zed.TrnDate, "yyyy-MM")
        label_func = lambda r: str(r.period)

    query = db.query(
        group_expr.label("period"),
        func.sum(_total_sales_expr()).label("total_sales"),
        func.sum(_coalesce(Zed.CashSales)).label("cash_sales"),
        func.sum(_coalesce(Zed.CreditCardSales)).label("card_sales"),
        func.sum(_mobile_sales_expr()).label("mobile_sales"),
        func.sum(_coalesce(Zed.Customers)).label("customers"),
    ).filter(
        cast(Zed.TrnDate, Date) >= date_from,
        cast(Zed.TrnDate, Date) <= date_to,
    ).group_by(group_expr).order_by(group_expr)

    results = []
    for row in query.all():
        total = float(row.total_sales or 0)
        cash = float(row.cash_sales or 0)
        card = float(row.card_sales or 0)
        mobile = float(row.mobile_sales or 0)
        other = total - cash - card - mobile

        results.append(SalesTrend(
            period=label_func(row),
            total_sales=round(total, 2),
            cash_sales=round(cash, 2),
            card_sales=round(card, 2),
            mobile_sales=round(mobile, 2),
            other_sales=round(max(other, 0), 2),
            customers=int(row.customers or 0),
        ))

    return results


def get_payment_method_analysis(
    db: Session,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
) -> List[PaymentMethodSales]:
    """Detailed payment method breakdown with transaction counts."""
    if not date_from and not date_to:
        date_from = date_to = date.today()

    methods = [
        ("Cash", "CashSales"),
        ("M-PESA", "MPESAPayBillSales"),
        ("Credit Card", "CreditCardSales"),
        ("Airtel Money", "AirTelPayBillSales"),
        ("mVisa", "mVisaPayBillSales"),
        ("VOOMA", "VOOMAPayBillSales"),
        ("EasyPay", "EasyPayPayBillSales"),
        ("UMI", "UMIPayBillSales"),
        ("Cheque", "ChqSales"),
        ("Gift Voucher", "GiftVoucherSales"),
        ("CAP (Credit)", "CAPSales"),
        ("Loyalty", "LoyaltySales"),
        ("QSoko", "QSokoSales"),
    ]

    results = []
    total = 0

    for name, col in methods:
        col_attr = getattr(Zed, col)
        query = db.query(
            func.sum(_coalesce(col_attr)).label("amount"),
            func.count(func.nullif(col_attr, 0)).label("txn_count"),
        )
        query = _apply_date_filter(query, date_from, date_to)
        row = query.first()
        amount = float(row.amount or 0)
        if amount > 0:
            results.append(PaymentMethodSales(
                method=name,
                amount=round(amount, 2),
                percentage=0,
                transaction_count=int(row.txn_count or 0),
            ))
            total += amount

    for item in results:
        item.percentage = round((item.amount / total * 100) if total else 0, 1)

    return sorted(results, key=lambda x: x.amount, reverse=True)
