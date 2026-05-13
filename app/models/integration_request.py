from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base, GUID


class IntegrationRequest(Base):
    __tablename__ = "integration_requests"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    applicant_type: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    org_name: Mapped[str] = mapped_column(String(200), nullable=False)
    contact_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    telegram: Mapped[str | None] = mapped_column(String(100), nullable=True)
    country_or_region: Mapped[str | None] = mapped_column(String(100), nullable=True)
    use_case: Mapped[str] = mapped_column(Text, nullable=False)
    interested_apis: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    expected_volume_range: Mapped[str | None] = mapped_column(String(50), nullable=True)
    expected_launch_time: Mapped[str | None] = mapped_column(String(50), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    source: Mapped[str | None] = mapped_column(String(500), nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="new", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), default=datetime.utcnow, index=True)

