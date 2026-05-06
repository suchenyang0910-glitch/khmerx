"""rates 表 — 每日汇率"""
from datetime import datetime, date, timezone
from sqlalchemy import String, Float, Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
import uuid


class Rate(Base):
    __tablename__ = "rates"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    currency_pair: Mapped[str] = mapped_column(String(16), default="USD/KHR", nullable=False)
    buy_rate: Mapped[float] = mapped_column(Float, nullable=False)
    sell_rate: Mapped[float] = mapped_column(Float, nullable=False)
    source: Mapped[str] = mapped_column(String(64), default="admin")
    rate_date: Mapped[date] = mapped_column(Date, nullable=False, default=lambda: datetime.now(timezone.utc).date())
    created_at = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Rate {self.currency_pair} buy={self.buy_rate} sell={self.sell_rate}>"
