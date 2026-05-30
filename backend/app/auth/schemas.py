"""Pydantic schemas for authentication requests and responses."""

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class LoginRequest(BaseModel):
    """Login request body."""
    username: str
    password: str


class TokenResponse(BaseModel):
    """JWT token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: "UserResponse"


class RefreshRequest(BaseModel):
    """Token refresh request."""
    refresh_token: str


class UserResponse(BaseModel):
    """User data returned in responses."""
    id: int
    username: str
    email: str
    full_name: str
    role: str
    branch_code: Optional[int] = None
    is_active: bool
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class CreateUserRequest(BaseModel):
    """Request to create a new dashboard user."""
    username: str
    email: str
    password: str
    full_name: str
    role: str = "branch_manager"
    branch_code: Optional[int] = None


class UpdateUserRequest(BaseModel):
    """Request to update a user."""
    email: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[str] = None
    branch_code: Optional[int] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None
