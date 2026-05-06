from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class AdminAuditLog(Base):
    __tablename__ = "admin_audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    admin_username: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    action: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    resource_type: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    resource_id: Mapped[str] = mapped_column(String(128), nullable=True)

    before = mapped_column(JSON, nullable=True)
    after = mapped_column(JSON, nullable=True)
    ip: Mapped[str] = mapped_column(String(64), nullable=True)

    created_at = mapped_column(DateTime(timezone=False), default=datetime.utcnow, index=True)
