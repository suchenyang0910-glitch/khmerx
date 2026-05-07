from __future__ import annotations

from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.p2p_offer import P2POffer
from app.models.p2p_trade import P2PTrade
from app.models.repayment_schedule import RepaymentSchedule
from app.models.user import User
from app.models.notification import Notification
from app.ops.service import CollectionService
from app.risk.engine import RiskEngine
from app.risk.models import RiskEvent, RiskEventDelivery
from app.risk.schemas import RepaymentRiskInput
from app.risk.service import RiskService
from app.services.notifications import create_notification, get_or_create_notification_settings


def _utcnow() -> datetime:
    return datetime.utcnow()


def _naive(dt: datetime | None) -> datetime | None:
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt
    return dt.replace(tzinfo=None)


def check_lender_payment_timeout(db: Session):
    service = RiskService(db)
    engine = RiskEngine(service)

    now = _utcnow()
    trades = (
        db.query(P2PTrade)
        .filter(P2PTrade.status == "matched")
        .filter(P2PTrade.advance_pay_deadline != None)
        .filter(P2PTrade.advance_pay_deadline <= now)
        .all()
    )

    for trade in trades:
        trade.status = "cancelled"
        offer = db.query(P2POffer).filter(P2POffer.id == trade.offer_id).first()
        if offer and offer.status == "matched":
            offer.status = "expired"

        engine.on_lender_no_pay_timeout(lender_id=trade.lender_id, trade_id=trade.id)

        s_lender = get_or_create_notification_settings(db, trade.lender_id)
        s_borrower = get_or_create_notification_settings(db, trade.borrower_id)
        if s_lender.repayment_reminders:
            create_notification(
                db,
                user_id=trade.lender_id,
                type="trade_timeout",
                title="交易已取消",
                body="超过打款时限未确认，系统已自动取消该交易。",
                target_type="trade",
                target_id=str(trade.id),
            )
        if s_borrower.repayment_reminders:
            create_notification(
                db,
                user_id=trade.borrower_id,
                type="trade_timeout",
                title="交易已取消",
                body="放款人超过打款时限未确认，系统已自动取消该交易。",
                target_type="trade",
                target_id=str(trade.id),
            )

    db.commit()


def check_repayment_overdue(db: Session):
    service = RiskService(db)
    engine = RiskEngine(service)

    now = _utcnow()
    schedules = (
        db.query(RepaymentSchedule)
        .filter(RepaymentSchedule.status == "pending")
        .filter(RepaymentSchedule.due_at < now)
        .all()
    )

    for schedule in schedules:
        schedule.status = "overdue"

        trade = db.query(P2PTrade).filter(P2PTrade.id == schedule.trade_id).first()
        if not trade:
            continue

        if trade.status == "dispute":
            continue

        due_at = _naive(schedule.due_at) or now
        overdue_days = (now - due_at).days
        decision = engine.on_repayment_overdue(
            RepaymentRiskInput(
                user_id=trade.borrower_id,
                trade_id=trade.id,
                overdue_days=overdue_days,
            )
        )

        if decision.action == "defaulted":
            trade.status = "defaulted"

        settings = get_or_create_notification_settings(db, trade.borrower_id)
        if settings.repayment_reminders:
            create_notification(
                db,
                user_id=trade.borrower_id,
                type="repayment_overdue",
                title="还款已逾期",
                body=f"你的还款已逾期 {overdue_days} 天，请尽快处理。",
                target_type="trade",
                target_id=str(trade.id),
            )

        if overdue_days >= 3:
            borrower = db.query(User).filter(User.id == trade.borrower_id).first()
            agent_id = borrower.agent_id if borrower else None
            CollectionService(db).create_task_if_missing(
                user_id=trade.borrower_id,
                trade_id=trade.id,
                agent_id=agent_id,
                priority="high" if overdue_days >= 7 else "normal",
                note=f"overdue_days={overdue_days}",
            )

    db.commit()


def auto_unblock_users(db: Session):
    service = RiskService(db)
    service.unblock_expired_blocks()


def generate_daily_risk_summary(db: Session):
    service = RiskService(db)

    now = _utcnow()
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)

    overdue_count = (
        db.query(RepaymentSchedule)
        .filter(RepaymentSchedule.status == "overdue")
        .filter(RepaymentSchedule.updated_at >= start)
        .count()
    )

    defaulted_count = (
        db.query(P2PTrade)
        .filter(P2PTrade.status == "defaulted")
        .filter(P2PTrade.updated_at >= start)
        .count()
    )

    pending_risk_events = db.query(RiskEvent).filter(RiskEvent.status == "pending").count()

    service.create_risk_event(
        event_type="daily_risk_summary",
        severity="medium" if overdue_count > 0 or defaulted_count > 0 else "low",
        payload={
            "overdue_count_today": overdue_count,
            "defaulted_count_today": defaulted_count,
            "pending_risk_events": pending_risk_events,
            "generated_at": now.isoformat(),
        },
    )


def generate_repayment_due_reminders(db: Session):
    now = _utcnow()
    in_24h = now + timedelta(hours=24)

    schedules = (
        db.query(RepaymentSchedule)
        .filter(RepaymentSchedule.status == "pending")
        .filter(RepaymentSchedule.due_at != None)
        .filter(RepaymentSchedule.due_at <= in_24h)
        .filter(RepaymentSchedule.due_at > now)
        .all()
    )

    for s in schedules:
        trade = db.query(P2PTrade).filter(P2PTrade.id == s.trade_id).first()
        if not trade:
            continue
        settings = get_or_create_notification_settings(db, trade.borrower_id)
        if not settings.repayment_reminders:
            continue

        exists = (
            db.query(Notification)
            .filter(Notification.user_id == trade.borrower_id)
            .filter(Notification.type == "repayment_due_24h")
            .filter(Notification.target_type == "schedule")
            .filter(Notification.target_id == str(s.id))
            .count()
        )
        if exists:
            continue

        create_notification(
            db,
            user_id=trade.borrower_id,
            type="repayment_due_24h",
            title="还款提醒",
            body="你的还款将在 24 小时内到期，请提前准备。",
            target_type="schedule",
            target_id=str(s.id),
        )


def push_pending_risk_events_to_openclaw(db: Session):
    from app.services.openclaw_webhook import push_risk_event
    from app import config

    if not config.OPENCLAW_WEBHOOK_ENABLED:
        return
    if not config.OPENCLAW_WEBHOOK_URL:
        return

    events = (
        db.query(RiskEvent)
        .filter(RiskEvent.status == "pending")
        .order_by(RiskEvent.severity.desc(), RiskEvent.created_at.asc())
        .limit(50)
        .all()
    )

    for ev in events:
        delivery = db.query(RiskEventDelivery).filter(RiskEventDelivery.event_id == ev.id).first()
        if delivery and delivery.status == "delivered":
            continue
        if not delivery:
            delivery = RiskEventDelivery(event_id=ev.id)
            db.add(delivery)
            db.commit()
            db.refresh(delivery)

        if delivery.attempt_count >= 10:
            continue

        try:
            payload = {
                "event_id": ev.id,
                "event_key": str(ev.event_key),
                "event_type": ev.event_type,
                "severity": ev.severity,
                "status": ev.status,
                "user_id": str(ev.user_id) if ev.user_id else None,
                "trade_id": str(ev.trade_id) if ev.trade_id else None,
                "offer_id": str(ev.offer_id) if ev.offer_id else None,
                "payload": ev.payload,
                "created_at": ev.created_at.isoformat() if ev.created_at else None,
            }
            push_risk_event(payload)
            delivery.status = "delivered"
            delivery.delivered_at = datetime.now(timezone.utc)
            delivery.last_error = None
        except Exception as e:
            delivery.status = "failed"
            delivery.last_error = str(e)
        finally:
            delivery.attempt_count = int(delivery.attempt_count or 0) + 1
            delivery.last_attempt_at = datetime.now(timezone.utc)
            db.commit()

