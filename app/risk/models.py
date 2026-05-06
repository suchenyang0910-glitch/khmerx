from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from sqlalchemy import Boolean, DateTime, Integer, Numeric, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.database import Base, GUID


class UserRiskProfile(Base):
    __tablename__ = "user_risk_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[Any] = mapped_column(GUID, unique=True, nullable=False, index=True)

    risk_level: Mapped[str] = mapped_column(String(30), nullable=False, default="normal")
    credit_score: Mapped[int] = mapped_column(Integer, nullable=False, default=650)
    credit_level: Mapped[str] = mapped_column(String(10), nullable=False, default="C")

    max_borrow_amount: Mapped[Any] = mapped_column(Numeric(12, 2), nullable=False, default=300)
    max_active_trades: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    risk_score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    cancel_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    matched_cancel_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    overdue_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    default_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    dispute_lost_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    is_blocked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    blocked_until = mapped_column(DateTime(timezone=True), nullable=True)
    block_reason: Mapped[str] = mapped_column(Text, nullable=True)

    created_at = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )


class RiskLog(Base):
    __tablename__ = "risk_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    user_id = mapped_column(GUID, nullable=True, index=True)
    trade_id = mapped_column(GUID, nullable=True, index=True)
    offer_id = mapped_column(GUID, nullable=True, index=True)

    event_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    risk_action: Mapped[str] = mapped_column(String(100), nullable=True)

    score_change: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    old_score: Mapped[int] = mapped_column(Integer, nullable=True)
    new_score: Mapped[int] = mapped_column(Integer, nullable=True)

    old_risk_level: Mapped[str] = mapped_column(String(30), nullable=True)
    new_risk_level: Mapped[str] = mapped_column(String(30), nullable=True)

    reason: Mapped[str] = mapped_column(Text, nullable=True)
    meta: Mapped[dict] = mapped_column(
        "metadata",
        JSON().with_variant(JSONB, "postgresql"),
        nullable=False,
        default=dict,
    )

    created_by: Mapped[str] = mapped_column(String(50), nullable=False, default="system")
    created_at = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class RiskRule(Base):
    __tablename__ = "risk_rules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    rule_type: Mapped[str] = mapped_column(String(50), nullable=False)

    threshold_value: Mapped[Any] = mapped_column(Numeric(12, 2), nullable=True)
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    score_delta: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    created_at = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )


class RiskEvent(Base):
    __tablename__ = "risk_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    event_key = mapped_column(GUID, nullable=False)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)

    user_id = mapped_column(GUID, nullable=True)
    trade_id = mapped_column(GUID, nullable=True)
    offer_id = mapped_column(GUID, nullable=True)

    severity: Mapped[str] = mapped_column(String(30), nullable=False, default="low")
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="pending")

    payload: Mapped[dict] = mapped_column(JSON().with_variant(JSONB, "postgresql"), nullable=False, default=dict)

    handled_by: Mapped[str] = mapped_column(String(50), nullable=True)
    handled_at = mapped_column(DateTime(timezone=True), nullable=True)
    created_at = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class Dispute(Base):
    __tablename__ = "disputes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    trade_id = mapped_column(GUID, nullable=False, index=True)
    offer_id = mapped_column(GUID, nullable=True, index=True)
    borrower_id = mapped_column(GUID, nullable=True, index=True)
    lender_id = mapped_column(GUID, nullable=True, index=True)

    raised_by_user_id = mapped_column(GUID, nullable=False, index=True)
    raised_role: Mapped[str] = mapped_column(String(30), nullable=False)

    dispute_type: Mapped[str] = mapped_column(String(50), nullable=True)
    reason: Mapped[str] = mapped_column(Text, nullable=False)

    status: Mapped[str] = mapped_column(String(30), nullable=False, default="open")
    priority: Mapped[str] = mapped_column(String(30), nullable=False, default="normal")

    resolution_result: Mapped[str] = mapped_column(String(50), nullable=True)
    resolution_note: Mapped[str] = mapped_column(Text, nullable=True)
    resolved_by = mapped_column(GUID, nullable=True)
    resolved_at = mapped_column(DateTime(timezone=True), nullable=True)

    created_at = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )


class DisputeEvidence(Base):
    __tablename__ = "dispute_evidences"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    dispute_id: Mapped[int] = mapped_column(Integer, ForeignKey("disputes.id", ondelete="CASCADE"), nullable=False, index=True)
    uploaded_by_user_id = mapped_column(GUID, nullable=False, index=True)
    uploaded_role: Mapped[str] = mapped_column(String(30), nullable=False)
    evidence_type: Mapped[str] = mapped_column(String(50), nullable=False)
    file_url: Mapped[str] = mapped_column(Text, nullable=True)
    text_note: Mapped[str] = mapped_column(Text, nullable=True)
    meta: Mapped[dict] = mapped_column(
        "metadata",
        JSON().with_variant(JSONB, "postgresql"),
        nullable=False,
        default=dict,
    )
    created_at = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class DeviceFingerprint(Base):
    __tablename__ = "device_fingerprints"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(GUID, nullable=False, index=True)
    tg_id: Mapped[int] = mapped_column(Integer, nullable=True, index=True)
    device_id: Mapped[str] = mapped_column(String(255), nullable=True)
    ip_hash: Mapped[str] = mapped_column(String(255), nullable=True, index=True)
    user_agent_hash: Mapped[str] = mapped_column(String(255), nullable=True)
    fingerprint_hash: Mapped[str] = mapped_column(String(255), nullable=True, index=True)
    created_at = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class UserRelationEdge(Base):
    __tablename__ = "user_relation_edges"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_a = mapped_column(GUID, nullable=False, index=True)
    user_b = mapped_column(GUID, nullable=False, index=True)
    relation_type: Mapped[str] = mapped_column(String(50), nullable=False)
    weight: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    evidence: Mapped[dict] = mapped_column(JSON().with_variant(JSONB, "postgresql"), nullable=False, default=dict)
    created_at = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class RiskScoreLog(Base):
    __tablename__ = "risk_score_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(GUID, nullable=False, index=True)
    score_change: Mapped[int] = mapped_column(Integer, nullable=False)
    old_score: Mapped[int] = mapped_column(Integer, nullable=True)
    new_score: Mapped[int] = mapped_column(Integer, nullable=True)
    reason: Mapped[str] = mapped_column(Text, nullable=True)
    created_by: Mapped[str] = mapped_column(String(50), nullable=False, default="system")
    created_at = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class ManualReviewCase(Base):
    __tablename__ = "manual_review_cases"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(GUID, nullable=True, index=True)
    trade_id = mapped_column(GUID, nullable=True, index=True)
    offer_id = mapped_column(GUID, nullable=True, index=True)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    risk_score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="pending")
    decision: Mapped[str] = mapped_column(String(30), nullable=True)
    reviewed_by = mapped_column(GUID, nullable=True)
    review_note: Mapped[str] = mapped_column(Text, nullable=True)
    created_at = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    reviewed_at = mapped_column(DateTime(timezone=True), nullable=True)

