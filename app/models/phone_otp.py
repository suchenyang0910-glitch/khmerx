from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base, GUID


class PhoneOtpChallenge(Base):
    __tablename__ = "phone_otp_challenges"

    id: Mapped[uuid.UUID] = mapped_column(GUID, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(GUID, nullable=False, index=True)
    phone: Mapped[str] = mapped_column(String(32), nullable=False, index=True)

    code_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    salt: Mapped[str] = mapped_column(String(64), nullable=False)

    sent_at = mapped_column(DateTime(timezone=False), nullable=False)
    expires_at = mapped_column(DateTime(timezone=False), nullable=False, index=True)
    verified_at = mapped_column(DateTime(timezone=False), nullable=True)
    attempts: Mapped[int] = mapped_column(Integer, default=0)

    created_at = mapped_column(DateTime(timezone=False), default=datetime.utcnow)

