from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from typing import Any

from sqlalchemy import DateTime, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base, GUID


class AgentCommission(Base):
    __tablename__ = "agent_commissions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    agent_id = mapped_column(GUID, nullable=False, index=True)
    user_id = mapped_column(GUID, nullable=False, index=True)
    trade_id = mapped_column(GUID, nullable=False, index=True)
    amount: Mapped[Any] = mapped_column(Numeric(12, 2), nullable=False)
    commission_type: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="pending")
    created_at = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    settled_at = mapped_column(DateTime(timezone=True), nullable=True)


class AgentStat(Base):
    __tablename__ = "agent_stats"

    agent_id = mapped_column(GUID, primary_key=True)
    total_users: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_loans: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_volume: Mapped[Any] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    total_commission: Mapped[Any] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    pending_commission: Mapped[Any] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    updated_at = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class CollectionTask(Base):
    __tablename__ = "collection_tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(GUID, nullable=False, index=True)
    trade_id = mapped_column(GUID, nullable=False, index=True)
    agent_id = mapped_column(GUID, nullable=True, index=True)
    assigned_to = mapped_column(GUID, nullable=True, index=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="pending")
    priority: Mapped[str] = mapped_column(String(30), nullable=False, default="normal")
    note: Mapped[str] = mapped_column(Text, nullable=True)
    created_at = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

