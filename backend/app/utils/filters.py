"""
Shared query-builder helpers for applying common filters to SQLAlchemy
queries.

These helpers keep filter logic DRY across services and routers.
"""

from __future__ import annotations

from datetime import date, datetime, time
from typing import Optional

from sqlalchemy.orm import Query

from app.models.pos import Zed


def apply_date_filter(
    query: Query,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> Query:
    """
    Restrict a Zed query to rows whose ``TrnDate`` falls within the given
    date range (inclusive on both ends).

    Parameters
    ----------
    query:
        An existing SQLAlchemy query targeting the Zed model.
    start_date:
        Inclusive lower bound. ``None`` means no lower bound.
    end_date:
        Inclusive upper bound. ``None`` means no upper bound.
    """
    if start_date is not None:
        start_dt = datetime.combine(start_date, time.min)
        query = query.filter(Zed.TrnDate >= start_dt)
    if end_date is not None:
        end_dt = datetime.combine(end_date, time.max)
        query = query.filter(Zed.TrnDate <= end_dt)
    return query


def apply_branch_filter(
    query: Query,
    branch_code: Optional[int] = None,
) -> Query:
    """
    Restrict a Zed query to a specific branch/till.

    .. note::
        The Zeds table itself does not have a ``BranchCode`` column.
        In a multi-branch deployment each branch has its own database
        (or linked-server). This filter is a placeholder that will be
        extended when cross-branch querying is implemented.
    """
    # TODO: Implement branch-level filtering once the multi-branch
    #       architecture is finalised (linked servers, branch DB routing, etc.)
    return query


def apply_till_filter(
    query: Query,
    till: Optional[int] = None,
) -> Query:
    """Filter by a specific till number."""
    if till is not None:
        query = query.filter(Zed.Till == till)
    return query


def apply_user_filter(
    query: Query,
    till_user: Optional[str] = None,
) -> Query:
    """Filter by till operator username."""
    if till_user is not None:
        query = query.filter(Zed.TillUser == till_user)
    return query


def apply_common_filters(
    query: Query,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    branch_code: Optional[int] = None,
    till: Optional[int] = None,
    till_user: Optional[str] = None,
) -> Query:
    """
    Apply all common filters in one call.

    This is the convenience wrapper most callers should use.
    """
    query = apply_date_filter(query, start_date, end_date)
    query = apply_branch_filter(query, branch_code)
    query = apply_till_filter(query, till)
    query = apply_user_filter(query, till_user)
    return query
