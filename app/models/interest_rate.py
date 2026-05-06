"""interest_rate_matrix 表 — P2P 砍头息利率矩阵"""
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import BigInteger, Boolean, DateTime, Integer, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class InterestRateMatrix(Base):
    __tablename__ = "interest_rate_matrix"
    __table_args__ = (
        UniqueConstraint("term_days", "credit_level", name="uq_interest_rate_matrix_term_credit"),
    )

    id: Mapped[int] = mapped_column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        autoincrement=True,
    )
    term_days: Mapped[int] = mapped_column(Integer, nullable=False)
    credit_level: Mapped[str] = mapped_column(String(10), nullable=False)
    rate_percent: Mapped[Decimal] = mapped_column(Numeric(6, 2), nullable=False)
    mode: Mapped[str] = mapped_column(String(20), nullable=False, default="cut_interest")
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return f"<InterestRateMatrix {self.term_days}d level={self.credit_level} {self.rate_percent}% mode={self.mode}>"
