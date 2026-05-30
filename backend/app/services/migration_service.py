"""
Data migration service — import/export data and seed utilities.

Provides tools for:
- Seeding sample data for testing
- Importing data from CSV/Excel
- Exporting raw table data
- Creating dashboard-specific tables
"""

from datetime import datetime, date, timedelta
import random
from sqlalchemy.orm import Session
from app.models.pos import Zed, Branch, CompanyInfo
from app.models.user import DashboardUser, AuditLog
from app.auth.utils import hash_password
from app.database import Base, engine


def create_dashboard_tables():
    """
    Create dashboard-specific tables (dashboard_users, dashboard_audit_log).
    Does NOT touch existing POS tables.
    """
    from app.models.user import DashboardUser, AuditLog
    DashboardUser.__table__.create(bind=engine, checkfirst=True)
    AuditLog.__table__.create(bind=engine, checkfirst=True)


def seed_admin_user(db: Session) -> dict:
    """Create the default super admin user if it doesn't exist."""
    existing = db.query(DashboardUser).filter(
        DashboardUser.username == "admin"
    ).first()

    if existing:
        return {"message": "Admin user already exists", "created": False}

    admin = DashboardUser(
        username="admin",
        email="admin@dashboard.local",
        hashed_password=hash_password("admin123"),
        full_name="System Administrator",
        role="super_admin",
        is_active=True,
    )
    db.add(admin)
    db.commit()
    return {"message": "Admin user created (username: admin, password: admin123)", "created": True}


def seed_sample_zeds(db: Session, days: int = 30) -> dict:
    """
    Seed sample Z-reading data for testing.
    Creates realistic Kenyan retail transaction data.
    """
    existing_count = db.query(Zed).count()
    if existing_count > 0:
        return {"message": f"Zeds table already has {existing_count} records. Skipping seed.", "created": 0}

    records_created = 0
    session_counter = 1
    tills = [1, 2, 3, 4]
    users = ["JOY", "MERCY", "BRIAN", "ALICE"]

    for day_offset in range(days, 0, -1):
        trn_date = datetime.now() - timedelta(days=day_offset)

        for till in tills:
            # 2-3 sessions per till per day
            sessions_today = random.randint(2, 3)
            for _ in range(sessions_today):
                cash = round(random.uniform(15000, 80000), 2)
                mpesa = round(random.uniform(5000, 40000), 2)
                card = round(random.uniform(2000, 20000), 2)
                airtel = round(random.uniform(0, 5000), 2)
                vooma = round(random.uniform(0, 3000), 2)
                customers = random.randint(20, 120)

                zed = Zed(
                    TrnDate=trn_date,
                    TrnTime=f"{random.randint(8,20):02d}:{random.randint(0,59):02d}:00",
                    Till=till,
                    Session=session_counter,
                    TotalFloat=round(random.uniform(5000, 15000), 2),
                    CashSales=cash,
                    EChange=round(random.uniform(0, 500), 2),
                    CreditCardSales=card,
                    GiftVoucherSales=round(random.uniform(0, 2000), 2),
                    GiftVoucherSalesHQ=0,
                    AirTelPayBillSales=airtel,
                    MPESAPayBillSales=mpesa,
                    mVisaPayBillSales=round(random.uniform(0, 1000), 2),
                    EasyPayPayBillSales=0,
                    UMIPayBillSales=0,
                    VOOMAPayBillSales=vooma,
                    QSokoSales=0,
                    LoyaltySales=round(random.uniform(0, 1500), 2),
                    Scheme11DiscountSales=0,
                    Scheme11CouponSales=0,
                    CAPSales=round(random.uniform(0, 5000), 2),
                    CAPCrNotes=0,
                    ChqSales=0,
                    NewFloatCF=round(random.uniform(5000, 10000), 2),
                    CashPurchases=round(random.uniform(1000, 8000), 2),
                    RemitToHq=round(random.uniform(10000, 50000), 2),
                    StaffPayments=round(random.uniform(0, 3000), 2),
                    StaffDeposits=round(random.uniform(0, 1000), 2),
                    StaffAdvance=0,
                    EPurseDeposits=0,
                    EPurseWithdrawals=0,
                    ChangeIntoEPurse=0,
                    EBankDeposits=round(random.uniform(0, 5000), 2),
                    StampDuty=round(random.uniform(0, 200), 2),
                    VatCertiSales=round(cash + mpesa + card, 2),
                    ActualVatCertis=round((cash + mpesa + card) * 0.16, 2),
                    Customers=customers,
                    CrNotesUsed=0,
                    TillUser=random.choice(users),
                    VarianceRecovered=0,
                )
                db.add(zed)
                session_counter += 1
                records_created += 1

    db.commit()
    return {"message": f"Created {records_created} sample Zeds records", "created": records_created}


def seed_branches(db: Session) -> dict:
    """Seed sample branches if none exist."""
    existing = db.query(Branch).count()
    if existing > 0:
        return {"message": f"Branches table already has {existing} records", "created": 0}

    branches = [
        Branch(BranchCode=1, BranchName="Main Branch - Nairobi CBD", BranchNameShort="NRB-CBD", BranchTypeCode=1),
        Branch(BranchCode=2, BranchName="Westlands Branch", BranchNameShort="NRB-WTL", BranchTypeCode=1),
    ]
    db.add_all(branches)
    db.commit()
    return {"message": "Created 2 sample branches", "created": 2}


def seed_all(db: Session) -> dict:
    """Run all seed operations."""
    create_dashboard_tables()
    results = {
        "branches": seed_branches(db),
        "admin_user": seed_admin_user(db),
        "zeds": seed_sample_zeds(db),
    }
    return results
