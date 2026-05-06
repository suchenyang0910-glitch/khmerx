from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Session

from app import config
from app.models.notification import Notification
from app.models.notification_settings import NotificationSettings


def _utcnow() -> datetime:
    return datetime.utcnow()


def get_or_create_notification_settings(db: Session, user_id) -> NotificationSettings:
    row = db.query(NotificationSettings).filter(NotificationSettings.user_id == user_id).first()
    if row:
        return row
    row = NotificationSettings(user_id=user_id, repayment_reminders=True, dispute_updates=True)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def can_send_type_today(db: Session, *, user_id, type: str, max_per_day: int) -> bool:
    now = _utcnow()
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    cnt = (
        db.query(Notification)
        .filter(Notification.user_id == user_id)
        .filter(Notification.type == type)
        .filter(Notification.created_at >= start)
        .count()
    )
    return cnt < max_per_day


def create_notification(
    db: Session,
    *,
    user_id,
    type: str,
    title: str,
    body: str,
    target_type: str | None = None,
    target_id: str | None = None,
    max_per_day: int | None = None,
):
    limit = config.NOTIFY_MAX_PER_TYPE_PER_DAY if max_per_day is None else max_per_day
    if limit > 0 and not can_send_type_today(db, user_id=user_id, type=type, max_per_day=limit):
        return None

    row = Notification(
        user_id=user_id,
        type=type,
        title=title,
        body=body,
        target_type=target_type,
        target_id=target_id,
        read=False,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row

