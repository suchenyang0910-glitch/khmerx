from __future__ import annotations

import uuid
from datetime import date, datetime, timezone
from typing import Any

from sqlalchemy import Date, DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base, GUID


class SalaryEmployment(Base):
    __tablename__ = "salary_employments"

    id: Mapped[uuid.UUID] = mapped_column(GUID, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[Any] = mapped_column(GUID, nullable=False, index=True)
    factory_id: Mapped[Any] = mapped_column(GUID, nullable=False, index=True)

    employee_no: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    department: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    position: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    join_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    salary_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=True)
    salary_pay_day: Mapped[int | None] = mapped_column(Integer, nullable=True)
    pay_cycle: Mapped[str] = mapped_column(String(16), nullable=False, default="monthly")
    pay_method: Mapped[str] = mapped_column(String(16), nullable=False, default="transfer")

    verify_status: Mapped[str] = mapped_column(String(16), nullable=False, default="pending", index=True)
    verify_notes: Mapped[str] = mapped_column(String(256), nullable=False, default="")
    verified_at = mapped_column(DateTime(timezone=True), nullable=True)

    created_at = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
