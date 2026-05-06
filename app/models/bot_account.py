from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class BotAccount(Base):
    __tablename__ = "bot_accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    bot_username: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    bot_token: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="active")
    is_primary: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

