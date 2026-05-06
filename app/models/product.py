"""products 表"""
from datetime import datetime, timezone
from sqlalchemy import String, Float, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base, GUID
import uuid


class Product(Base):
    __tablename__ = "products"

    id: Mapped[uuid.UUID] = mapped_column(GUID, primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    price: Mapped[float] = mapped_column(Float, nullable=False)  # USDT
    status: Mapped[str] = mapped_column(String(32), default="on_sale")  # on_sale / locked / sold
    owner_id: Mapped[uuid.UUID] = mapped_column(GUID, ForeignKey("users.id"), nullable=False)
    source: Mapped[str] = mapped_column(String(32), default="user")  # user / stock
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    images: Mapped[str] = mapped_column(Text, default="")  # JSON array of image URLs
    video_url: Mapped[str] = mapped_column(String(512), default="")
    contact_info: Mapped[str] = mapped_column(String(255), default="")
    category: Mapped[str] = mapped_column(String(64), default="phone")  # phone / tablet / laptop / other
    created_at = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Product {self.title} ${self.price}>"
