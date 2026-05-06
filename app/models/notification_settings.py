from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base, GUID


class NotificationSettings(Base):
    __tablename__ = "notification_settings"

    user_id: Mapped[uuid.UUID] = mapped_column(GUID, primary_key=True)
    repayment_reminders: Mapped[bool] = mapped_column(Boolean, default=True)
    dispute_updates: Mapped[bool] = mapped_column(Boolean, default=True)

    updated_at = mapped_column(DateTime(timezone=False), default=datetime.utcnow)

