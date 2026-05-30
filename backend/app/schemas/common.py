"""Common schemas used across multiple endpoints."""

from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class DateRange(BaseModel):
    """Date range filter."""
    date_from: Optional[date] = None
    date_to: Optional[date] = None


class FilterParams(BaseModel):
    """Shared filter parameters for analytics queries."""
    date_from: Optional[date] = None
    date_to: Optional[date] = None
    branch_code: Optional[int] = None
    till: Optional[int] = None
    user: Optional[str] = None


class PaginationParams(BaseModel):
    """Pagination parameters."""
    page: int = 1
    page_size: int = 20


class PaginatedResponse(BaseModel):
    """Generic paginated response wrapper."""
    total: int
    page: int
    page_size: int
    total_pages: int
    data: list


class MessageResponse(BaseModel):
    """Simple message response."""
    message: str
    success: bool = True
