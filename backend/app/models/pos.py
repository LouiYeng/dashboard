"""SQLAlchemy models mapped to the existing POS database tables."""

from sqlalchemy import (
    Column, SmallInteger, Integer, String, Float, DateTime, LargeBinary, Text
)
from app.database import Base


class CompanyInfo(Base):
    """Company information table — stores business identity details."""
    __tablename__ = "CompanyInfo"

    CompanyName = Column(String(40), primary_key=True)
    VATReg = Column(String(20), nullable=True)
    PinNo = Column(String(20), nullable=True)
    Address1 = Column(String(40), nullable=True)
    Address2 = Column(String(40), nullable=True)
    Address3 = Column(String(40), nullable=True)
    Logo = Column(LargeBinary, nullable=True)
    RegKey = Column(Text, nullable=True)


class Branch(Base):
    """Branches table — store/branch definitions."""
    __tablename__ = "Branches"

    BranchCode = Column(SmallInteger, primary_key=True)
    BranchName = Column(String(50), nullable=True)
    BranchNameShort = Column(String(50), nullable=True)
    BranchTypeCode = Column(SmallInteger, nullable=True)
    ServerName = Column(String(255), nullable=True)
    BranchCatalogue = Column(String(255), nullable=True)
    POSPath = Column(String(255), nullable=True)


class Zed(Base):
    """
    Zeds table — Z-reading / till session settlement data.

    Each row represents one till session closure. Contains all sales
    broken down by payment method, plus cash management fields.
    This is the primary data source for sales analytics.
    """
    __tablename__ = "Zeds"

    Till = Column("Till", SmallInteger, primary_key=True)
    Session = Column("Session", Integer, primary_key=True)
    TrnDate = Column(DateTime, nullable=False)
    TrnTime = Column(String(8), nullable=False)

    # Float
    TotalFloat = Column(Float, nullable=False, default=0)
    NewFloatCF = Column(Float, nullable=False, default=0)

    # Sales by payment method
    CashSales = Column(Float, nullable=False, default=0)
    EChange = Column(Float, nullable=True, default=0)
    CreditCardSales = Column(Float, nullable=False, default=0)
    GiftVoucherSales = Column(Float, nullable=False, default=0)
    GiftVoucherSalesHQ = Column(Float, nullable=True, default=0)
    ChqSales = Column(Float, nullable=False, default=0)

    # Mobile payment methods (Kenyan market)
    AirTelPayBillSales = Column(Float, nullable=True, default=0)
    MPESAPayBillSales = Column(Float, nullable=True, default=0)
    mVisaPayBillSales = Column(Float, nullable=True, default=0)
    EasyPayPayBillSales = Column(Float, nullable=True, default=0)
    UMIPayBillSales = Column(Float, nullable=True, default=0)
    VOOMAPayBillSales = Column(Float, nullable=True, default=0)
    QSokoSales = Column(Float, nullable=True, default=0)

    # Loyalty & schemes
    LoyaltySales = Column(Float, nullable=True, default=0)
    Scheme11DiscountSales = Column(Float, nullable=True, default=0)
    Scheme11CouponSales = Column(Float, nullable=True, default=0)

    # Credit / Account sales
    CAPSales = Column(Float, nullable=False, default=0)
    CAPCrNotes = Column(Float, nullable=True, default=0)

    # Cash management
    CashPurchases = Column(Float, nullable=False, default=0)
    RemitToHq = Column(Float, nullable=False, default=0)
    StaffPayments = Column(Float, nullable=True, default=0)
    StaffDeposits = Column(Float, nullable=True, default=0)
    StaffAdvance = Column(Float, nullable=True, default=0)
    EPurseDeposits = Column(Float, nullable=True, default=0)
    EPurseWithdrawals = Column(Float, nullable=True, default=0)
    ChangeIntoEPurse = Column(Float, nullable=True, default=0)
    EBankDeposits = Column(Float, nullable=True, default=0)

    # Tax & compliance
    StampDuty = Column(Float, nullable=False, default=0)
    VatCertiSales = Column(Float, nullable=False, default=0)
    ActualVatCertis = Column(Float, nullable=False, default=0)

    # Counters
    Customers = Column(Integer, nullable=False, default=0)
    CrNotesUsed = Column(Float, nullable=False, default=0)
    TillUser = Column(String(30), nullable=False)
    VarianceRecovered = Column(Float, nullable=False, default=0)

    @property
    def total_sales(self) -> float:
        """Calculate total sales across all payment methods."""
        return sum(filter(None, [
            self.CashSales, self.CreditCardSales, self.MPESAPayBillSales,
            self.AirTelPayBillSales, self.mVisaPayBillSales,
            self.EasyPayPayBillSales, self.UMIPayBillSales,
            self.VOOMAPayBillSales, self.GiftVoucherSales,
            self.GiftVoucherSalesHQ, self.ChqSales, self.CAPSales,
            self.LoyaltySales, self.QSokoSales,
            self.Scheme11DiscountSales, self.Scheme11CouponSales,
        ]))

    @property
    def total_mobile_sales(self) -> float:
        """Total mobile money sales (MPESA, Airtel, mVisa, etc.)."""
        return sum(filter(None, [
            self.MPESAPayBillSales, self.AirTelPayBillSales,
            self.mVisaPayBillSales, self.EasyPayPayBillSales,
            self.UMIPayBillSales, self.VOOMAPayBillSales,
        ]))

    @property
    def cash_in_hand(self) -> float:
        """Calculate cash in hand for this session."""
        inflows = sum(filter(None, [
            self.TotalFloat, self.CashSales, self.StaffDeposits,
            self.EPurseDeposits, self.VarianceRecovered,
        ]))
        outflows = sum(filter(None, [
            self.CashPurchases, self.RemitToHq, self.StaffPayments,
            self.StaffAdvance, self.EPurseWithdrawals,
            self.EBankDeposits, self.NewFloatCF,
        ]))
        return inflows - outflows
