from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base, GUID


class SalaryFactory(Base):
    __tablename__ = "salary_factories"

    id: Mapped[uuid.UUID] = mapped_column(GUID, primary_key=True, default=uuid.uuid4)

    name: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    industry: Mapped[str] = mapped_column(String(64), nullable=False, default="factory")
    location: Mapped[str] = mapped_column(String(128), nullable=False, default="")
    owner_type: Mapped[str] = mapped_column(String(32), nullable=False, default="unknown")

    salary_cycle: Mapped[str] = mapped_column(String(32), nullable=False, default="monthly")
    worker_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    risk_level: Mapped[str] = mapped_column(String(16), nullable=False, default="C")
    default_rate: Mapped[float] = mapped_column(Numeric(8, 4), nullable=False, default=0)

    hr_contact: Mapped[str] = mapped_column(String(128), nullable=False, default="")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    created_at = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

