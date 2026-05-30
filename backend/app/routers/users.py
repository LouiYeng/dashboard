"""User management API endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.dependencies import get_current_user, require_role
from app.models.user import DashboardUser
from app.auth.schemas import UserResponse, CreateUserRequest, UpdateUserRequest
from app.auth.utils import hash_password

router = APIRouter(prefix="/users", tags=["User Management"])


@router.get("/", response_model=List[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    current_user: DashboardUser = Depends(require_role("super_admin")),
):
    """List all dashboard users. Admin only."""
    users = db.query(DashboardUser).order_by(DashboardUser.id).all()
    return [UserResponse.model_validate(u) for u in users]


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    request: CreateUserRequest,
    db: Session = Depends(get_db),
    current_user: DashboardUser = Depends(require_role("super_admin")),
):
    """Create a new dashboard user. Admin only."""
    # Check for existing username/email
    existing = db.query(DashboardUser).filter(
        (DashboardUser.username == request.username) |
        (DashboardUser.email == request.email)
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already exists",
        )

    user = DashboardUser(
        username=request.username,
        email=request.email,
        hashed_password=hash_password(request.password),
        full_name=request.full_name,
        role=request.role,
        branch_code=request.branch_code,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserResponse.model_validate(user)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    request: UpdateUserRequest,
    db: Session = Depends(get_db),
    current_user: DashboardUser = Depends(require_role("super_admin")),
):
    """Update a dashboard user. Admin only."""
    user = db.query(DashboardUser).filter(DashboardUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if request.email is not None:
        user.email = request.email
    if request.full_name is not None:
        user.full_name = request.full_name
    if request.role is not None:
        user.role = request.role
    if request.branch_code is not None:
        user.branch_code = request.branch_code
    if request.is_active is not None:
        user.is_active = request.is_active
    if request.password is not None:
        user.hashed_password = hash_password(request.password)

    db.commit()
    db.refresh(user)
    return UserResponse.model_validate(user)


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: DashboardUser = Depends(require_role("super_admin")),
):
    """Delete a dashboard user. Admin only."""
    user = db.query(DashboardUser).filter(DashboardUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
