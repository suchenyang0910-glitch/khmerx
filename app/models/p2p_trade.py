"""p2p_trades 表 — ABA 微借贷交易记录"""
from datetime import datetime, timezone
from sqlalchemy import String, Float, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base, GUID
import uuid


class P2PTrade(Base):
    __tablename__ = "p2p_trades"

    id: Mapped[uuid.UUID] = mapped_column(GUID, primary_key=True, default=uuid.uuid4)
    offer_id: Mapped[uuid.UUID] = mapped_column(GUID, ForeignKey("p2p_offers.id"), nullable=False, index=True)
    borrower_id: Mapped[uuid.UUID] = mapped_column(GUID, ForeignKey("users.id"), nullable=False, index=True)
    lender_id: Mapped[uuid.UUID] = mapped_column(GUID, ForeignKey("users.id"), nullable=False, index=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)  # 借款金额
    term_days: Mapped[int] = mapped_column(Integer, nullable=False)  # 期限
    rate: Mapped[float] = mapped_column(Float, nullable=False)  # 月利率%
    fee: Mapped[float] = mapped_column(Float, nullable=False)  # 平台费
    fee_status: Mapped[str] = mapped_column(String(16), default="pending")  # pending / paid_to_platform
    total_repayable: Mapped[float] = mapped_column(Float, nullable=False)  # 本息合计
    status: Mapped[str] = mapped_column(String(32), default="matched")
    # matched → 已匹配，等待放款人打款
    # lend_confirmed → 放款人确认已打款
    # repayment_confirmed → 借款人确认已收到（平台确认收款）
    # repaying → 正在还款中
    # completed → 已完成
    # defaulted → 违约（严重逾期）
    # cancelled → 已取消
    proof_url_from_lender: Mapped[str] = mapped_column(Text, default="")  # 打款凭证
    proof_url_from_borrower: Mapped[str] = mapped_column(Text, default="")  # 收到确认
    advance_pay_deadline = mapped_column(DateTime(timezone=True), nullable=True)  # 打款截止时间
    fund_source: Mapped[str] = mapped_column(String(20), default="user")
    created_at = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                                onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<P2PTrade {self.id} ${self.amount} {self.status}>"
