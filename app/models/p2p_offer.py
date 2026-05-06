"""p2p_offers 表 — ABA 微借贷借款人挂单"""
from datetime import datetime, timezone
from sqlalchemy import String, Float, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base, GUID
import uuid


class P2POffer(Base):
    __tablename__ = "p2p_offers"

    id: Mapped[uuid.UUID] = mapped_column(GUID, primary_key=True, default=uuid.uuid4)
    borrower_id: Mapped[uuid.UUID] = mapped_column(GUID, ForeignKey("users.id"), nullable=False, index=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)  # 借款金额（美元）
    term_days: Mapped[int] = mapped_column(Integer, nullable=False)  # 借款天数
    rate: Mapped[float] = mapped_column(Float, nullable=False)  # 月利率%（查利率矩阵得来）
    fee: Mapped[float] = mapped_column(Float, nullable=False)  # 平台服务费（金额）
    total_amount: Mapped[float] = mapped_column(Float, nullable=False)  # amount + fee
    status: Mapped[str] = mapped_column(String(16), default="pending")  # pending / matched / cancelled / completed
    can_bid: Mapped[bool] = mapped_column(Boolean, default=False)  # true=放款人可竞价，false=必须匹配
    lender_selection: Mapped[str] = mapped_column(String(16), default="auto")  # "auto" / "specified"
    note: Mapped[str] = mapped_column(String(512), nullable=True)
    created_at = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                                onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<P2POffer {self.id} ${self.amount} {self.term_days}d {self.status}>"
