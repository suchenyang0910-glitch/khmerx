"""orders 表 — 核心订单"""
from datetime import datetime, timezone
from sqlalchemy import String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base, GUID
import uuid


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[uuid.UUID] = mapped_column(GUID, primary_key=True, default=uuid.uuid4)
    product_id: Mapped[uuid.UUID] = mapped_column(GUID, ForeignKey("products.id"), nullable=False)
    buyer_id: Mapped[uuid.UUID] = mapped_column(GUID, ForeignKey("users.id"), nullable=False)
    seller_id: Mapped[uuid.UUID] = mapped_column(GUID, ForeignKey("users.id"), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)

    # KhmerX 订单状态
    status: Mapped[str] = mapped_column(String(32), default="pending_payment")
    # pending_payment → escrowed → shipped → completed → done
    # 异常: pending_payment → cancelled
    #      escrowed → disputed → refunded / released

    # SettleCore 字段
    settlecore_escrow_id: Mapped[str] = mapped_column(String(128), nullable=True, unique=True)
    pay_address: Mapped[str] = mapped_column(String(128), nullable=True)
    pay_amount: Mapped[float] = mapped_column(Float, nullable=True)
    pay_status: Mapped[str] = mapped_column(String(32), default="created")  # created / paid / released / refunded / disputed / expired
    settlement_status: Mapped[str] = mapped_column(String(32), default="")
    settlecore_tx_hash: Mapped[str] = mapped_column(String(128), nullable=True)

    # 发货
    shipped_at = mapped_column(DateTime(timezone=True), nullable=True)
    deliver_deadline = mapped_column(DateTime(timezone=True), nullable=True)

    # 备注
    notes: Mapped[str] = mapped_column(Text, default="")
    created_at = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                                onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Order {self.id} status={self.status}>"
