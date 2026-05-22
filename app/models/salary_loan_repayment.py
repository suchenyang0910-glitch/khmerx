from __future__ import annotations

import uuid
from datetime import date, datetime, timezone
from typing import Any

from sqlalchemy import Date, DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base, GUID


class SalaryLoanRepaymentSchedule(Base):
    __tablename__ = "salary_loan_repayment_schedules"

    id: Mapped[uuid.UUID] = mapped_column(GUID, primary_key=True, default=uuid.uuid4)
    order_id: Mapped[Any] = mapped_column(GUID, nullable=False, index=True)
    installment_no: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    due_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    paid_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)

    status: Mapped[str] = mapped_column(String(16), nullable=False, default="due", index=True)
    paid_at = mapped_column(DateTime(timezone=True), nullable=True)

    created_at = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class SalaryLoanLedgerEntry(Base):
    __tablename__ = "salary_loan_ledger_entries"

    id: Mapped[uuid.UUID] = mapped_column(GUID, primary_key=True, default=uuid.uuid4)
    order_id: Mapped[Any] = mapped_column(GUID, nullable=False, index=True)
    event_type: Mapped[str] = mapped_column(String(16), nullable=False, index=True)
    account: Mapped[str] = mapped_column(String(64), nullable=False)

    dr_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    cr_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)

    external_ref: Mapped[str] = mapped_column(String(128), nullable=False, default="")
    created_at = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class SalaryLoanRepaymentProof(Base):
    __tablename__ = "salary_loan_repayment_proofs"

    id: Mapped[uuid.UUID] = mapped_column(GUID, primary_key=True, default=uuid.uuid4)
    order_id: Mapped[Any] = mapped_column(GUID, nullable=False, index=True)
    user_id: Mapped[Any] = mapped_column(GUID, nullable=False, index=True)

    file_path: Mapped[str] = mapped_column(String(256), nullable=False, default="")
    note: Mapped[str] = mapped_column(String(256), nullable=False, default="")
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)

    status: Mapped[str] = mapped_column(String(16), nullable=False, default="pending", index=True)
    reviewed_by: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    reviewed_at = mapped_column(DateTime(timezone=True), nullable=True)

    created_at = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class SalaryLoanCollectionCase(Base):
    __tablename__ = "salary_loan_collection_cases"

    id: Mapped[uuid.UUID] = mapped_column(GUID, primary_key=True, default=uuid.uuid4)
    order_id: Mapped[Any] = mapped_column(GUID, nullable=False, index=True)

    dpd: Mapped[int] = mapped_column(Integer, nullable=False, default=0, index=True)
    stage: Mapped[str] = mapped_column(String(16), nullable=False, default="pre", index=True)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="open", index=True)
    assignee: Mapped[str] = mapped_column(String(64), nullable=False, default="")

    last_contact_at = mapped_column(DateTime(timezone=True), nullable=True)
    next_follow_up_at = mapped_column(DateTime(timezone=True), nullable=True)

    created_at = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )


class SalaryLoanCollectionEvent(Base):
    __tablename__ = "salary_loan_collection_events"

    id: Mapped[uuid.UUID] = mapped_column(GUID, primary_key=True, default=uuid.uuid4)
    case_id: Mapped[Any] = mapped_column(GUID, nullable=False, index=True)

    channel: Mapped[str] = mapped_column(String(16), nullable=False, default="call")
    result: Mapped[str] = mapped_column(String(32), nullable=False, default="")
    reason_code: Mapped[str] = mapped_column(String(32), nullable=False, default="")
    note: Mapped[str] = mapped_column(String(512), nullable=False, default="")

    ptp_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    ptp_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)

    actor: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    created_at = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

