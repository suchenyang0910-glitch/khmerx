from __future__ import annotations

import uuid
from datetime import date, datetime, timezone
from typing import Any

from sqlalchemy import Date, DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base, GUID


class SalaryLoanOrder(Base):
    __tablename__ = "salary_loan_orders"

    id: Mapped[uuid.UUID] = mapped_column(GUID, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[Any] = mapped_column(GUID, nullable=False, index=True)
    employment_id: Mapped[Any] = mapped_column(GUID, nullable=False, index=True)

    status: Mapped[str] = mapped_column(String(32), nullable=False, default="submitted", index=True)

    currency: Mapped[str] = mapped_column(String(8), nullable=False, default="USD")
    principal: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    fee: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    interest: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    disbursement_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)

    tenor_days: Mapped[int] = mapped_column(Integer, nullable=False, default=14)
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    risk_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    decision: Mapped[str] = mapped_column(String(16), nullable=False, default="pending")
    decision_notes: Mapped[str] = mapped_column(String(256), nullable=False, default="")

    approved_by: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    disbursed_by: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    disbursed_at = mapped_column(DateTime(timezone=True), nullable=True)
    disbursement_ref: Mapped[str] = mapped_column(String(128), nullable=False, default="")

    created_at = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

