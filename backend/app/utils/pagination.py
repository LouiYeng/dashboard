"""
Pagination utility for list endpoints.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Sequence, TypeVar

from sqlalchemy.orm import Query

T = TypeVar("T")


def paginate_query(
    query: Query,
    page: int = 1,
    page_size: int = 50,
) -> Dict[str, Any]:
    """
    Apply pagination to an SQLAlchemy query and return a dict suitable
    for building a ``PaginatedResponse``.

    Parameters
    ----------
    query:
        The base query (before LIMIT/OFFSET).
    page:
        1-based page number.
    page_size:
        Number of items per page.

    Returns
    -------
    dict
        ``{"items": [...], "total": int, "page": int,
          "page_size": int, "total_pages": int}``
    """
    total: int = query.count()
    offset = (page - 1) * page_size
    items = query.offset(offset).limit(page_size).all()
    total_pages = math.ceil(total / page_size) if page_size > 0 else 0

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    }


def paginate_list(
    items: Sequence[T],
    page: int = 1,
    page_size: int = 50,
) -> Dict[str, Any]:
    """
    Paginate an in-memory list (useful after aggregation in Python).

    Parameters
    ----------
    items:
        Full list of items.
    page:
        1-based page number.
    page_size:
        Number of items per page.

    Returns
    -------
    dict
        Same structure as ``paginate_query``.
    """
    total = len(items)
    offset = (page - 1) * page_size
    page_items = items[offset : offset + page_size]
    total_pages = math.ceil(total / page_size) if page_size > 0 else 0

    return {
        "items": list(page_items),
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    }
