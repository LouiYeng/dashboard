"""Dashboard user model — separate from POS users, for dashboard authentication."""

from sqlalchemy import (
    Column, Integer, String, SmallInteger, Boolean, DateTime, ForeignKey
)
from sqlalchemy.sql import func
from app.database import Base


class DashboardUser(Base):
    """
    Users who can log into the BI Dashboard.
    Separate from POS system users — these are management/reporting users.
    """
    __tablename__ = "dashboard_users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False, default="branch_manager")
    branch_code = Column(SmallInteger, ForeignKey("Branches.BranchCode"), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, server_default=func.now())
    last_login = Column(DateTime, nullable=True)


class AuditLog(Base):
    """Audit trail for user actions in the dashboard."""
    __tablename__ = "dashboard_audit_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("dashboard_users.id"), nullable=False)
    action = Column(String(50), nullable=False)
    resource = Column(String(100), nullable=True)
    details = Column(String(500), nullable=True)
    ip_address = Column(String(45), nullable=True)
    timestamp = Column(DateTime, server_default=func.now())
