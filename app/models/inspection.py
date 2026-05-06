"""inspections 验机表"""
from datetime import datetime, timezone
from sqlalchemy import String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base, GUID
import uuid


class Inspection(Base):
    __tablename__ = "inspections"

    id: Mapped[uuid.UUID] = mapped_column(GUID, primary_key=True, default=uuid.uuid4)
    product_id: Mapped[uuid.UUID] = mapped_column(GUID, ForeignKey("products.id"), nullable=False, index=True)
    inspector_id: Mapped[uuid.UUID] = mapped_column(GUID, ForeignKey("users.id"), nullable=True)

    # 验机结果
    condition: Mapped[str] = mapped_column(String(64), default="")  # 外观等级: excellent / good / fair / poor
    battery_health: Mapped[int] = mapped_column(Integer, default=0)  # 电池健康百分比
    result: Mapped[str] = mapped_column(String(16), default="pass")  # pass / fail
    notes: Mapped[str] = mapped_column(Text, default="")
    video_url: Mapped[str] = mapped_column(String(512), default="")

    created_at = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Inspection product={self.product_id} result={self.result}>"
