"""repayment_schedules 表 — 还款计划表"""
from datetime import datetime, timezone
from sqlalchemy import String, Float, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base, GUID
import uuid


class RepaymentSchedule(Base):
    __tablename__ = "repayment_schedules"

    id: Mapped[uuid.UUID] = mapped_column(GUID, primary_key=True, default=uuid.uuid4)
    trade_id: Mapped[uuid.UUID] = mapped_column(GUID, ForeignKey("p2p_trades.id"), nullable=False, index=True)
    period: Mapped[int] = mapped_column(Integer, nullable=False)  # 第几期（从1开始）
    due_at = mapped_column(DateTime(timezone=True), nullable=False)  # 到期时间
    principal: Mapped[float] = mapped_column(Float, nullable=False)  # 本金部分
    interest: Mapped[float] = mapped_column(Float, nullable=False)  # 利息部分
    total: Mapped[float] = mapped_column(Float, nullable=False)  # 应还总额（principal + interest）
    status: Mapped[str] = mapped_column(String(16), default="pending")  # pending / paid / overdue
    paid_at = mapped_column(DateTime(timezone=True), nullable=True)  # 还款时间
    proof_url: Mapped[str] = mapped_column(String(512), nullable=True)  # 还款凭证
    created_at = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                                onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<RepaymentSchedule trade={self.trade_id} period={self.period} total={self.total} status={self.status}>"
