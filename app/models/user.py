"""users 表"""
from datetime import datetime, timezone
from sqlalchemy import String, BigInteger, DateTime, Integer, Float, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base, GUID
import uuid


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(GUID, primary_key=True, default=uuid.uuid4)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    photo_url: Mapped[str] = mapped_column(String(512), default="")
    role: Mapped[str] = mapped_column(String(32), default="user")
    sub_role: Mapped[str] = mapped_column(String(20), nullable=True)
    agent_id: Mapped[uuid.UUID] = mapped_column(GUID, nullable=True, index=True)
    inviter_id: Mapped[uuid.UUID] = mapped_column(GUID, nullable=True, index=True)
    commission_rate: Mapped[float] = mapped_column(Numeric(5, 2), default=0)
    risk_level: Mapped[str] = mapped_column(String(16), default="normal")  # normal / flagged / banned
    consecutive_cancels: Mapped[int] = mapped_column(Integer, default=0)
    cancel_banned_until = mapped_column(DateTime(timezone=True), nullable=True)
    order_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # ── KhmerX ABA 微借贷字段 ────────────────────────────────────
    preferred_lang: Mapped[str] = mapped_column(String(8), default="km")  # km=高棉语, cn=中文
    credit_score: Mapped[int] = mapped_column(Integer, default=650)
    verification_level: Mapped[str] = mapped_column(String(32), default="unverified")  # unverified / phone / kyc / full
    phone: Mapped[str] = mapped_column(String(32), nullable=True)
    phone_verified_at = mapped_column(DateTime(timezone=True), nullable=True)
    aba_account: Mapped[str] = mapped_column(String(64), nullable=True)
    aba_name: Mapped[str] = mapped_column(String(128), nullable=True)
    monthly_referrals: Mapped[int] = mapped_column(Integer, default=0)
    total_borrowed: Mapped[float] = mapped_column(Float, default=0.0)
    total_repaid: Mapped[float] = mapped_column(Float, default=0.0)
    active_loans: Mapped[int] = mapped_column(Integer, default=0)

    def __repr__(self):
        return f"<User tg_id={self.tg_id} name={self.name}>"
