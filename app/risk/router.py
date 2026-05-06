from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.risk.engine import RiskEngine
from app.risk.models import RiskEvent, RiskLog, UserRiskProfile
from app.risk.schemas import AdjustScoreInput, CreateOfferRiskInput, MatchOfferRiskInput, RepaymentRiskInput
from app.risk.service import RiskService

router = APIRouter(prefix="/risk", tags=["risk"])


def _require_admin(admin_id: str, db: Session) -> User:
    import uuid

    try:
        uid = uuid.UUID(admin_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid admin_id")

    user = db.query(User).filter(User.id == uid).first()
    if not user or user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


def get_risk_engine(db: Session) -> RiskEngine:
    service = RiskService(db)
    return RiskEngine(service)


@router.post("/check/create-offer")
def check_create_offer(payload: CreateOfferRiskInput, db: Session = Depends(get_db)):
    engine = get_risk_engine(db)
    return engine.check_create_offer(payload)


@router.post("/check/match-offer")
def check_match_offer(payload: MatchOfferRiskInput, db: Session = Depends(get_db)):
    engine = get_risk_engine(db)
    return engine.check_match_offer(payload)


@router.post("/events/repayment-overdue")
def repayment_overdue(payload: RepaymentRiskInput, db: Session = Depends(get_db)):
    engine = get_risk_engine(db)
    return engine.on_repayment_overdue(payload)


@router.post("/events/repayment-paid")
def repayment_paid(
    user_id: UUID,
    trade_id: UUID,
    early: bool = False,
    db: Session = Depends(get_db),
):
    engine = get_risk_engine(db)
    engine.on_repayment_paid(user_id=user_id, trade_id=trade_id, early=early)
    return {"ok": True}


@router.get("/events/pending")
def get_pending_risk_events(limit: int = 50, db: Session = Depends(get_db)):
    events = (
        db.query(RiskEvent)
        .filter(RiskEvent.status == "pending")
        .order_by(RiskEvent.severity.desc(), RiskEvent.created_at.asc())
        .limit(limit)
        .all()
    )
    return events


@router.post("/events/{event_id}/handled")
def mark_risk_event_handled(
    event_id: int,
    handled_by: str = "openclaw",
    db: Session = Depends(get_db),
):
    event = db.query(RiskEvent).filter(RiskEvent.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="risk event not found")

    event.status = "handled"
    event.handled_by = handled_by
    event.handled_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(event)
    return event


@router.get("/dashboard")
def risk_dashboard(db: Session = Depends(get_db)):
    normal_users = db.query(UserRiskProfile).filter(UserRiskProfile.risk_level == "normal").count()
    watch_users = db.query(UserRiskProfile).filter(UserRiskProfile.risk_level == "watch").count()
    flagged_users = db.query(UserRiskProfile).filter(UserRiskProfile.risk_level == "flagged").count()
    restricted_users = db.query(UserRiskProfile).filter(UserRiskProfile.risk_level == "restricted").count()
    blocked_users = db.query(UserRiskProfile).filter(UserRiskProfile.risk_level == "blocked").count()

    pending_events = db.query(RiskEvent).filter(RiskEvent.status == "pending").count()
    high_events = (
        db.query(RiskEvent)
        .filter(RiskEvent.status == "pending")
        .filter(RiskEvent.severity == "high")
        .count()
    )

    return {
        "users": {
            "normal": normal_users,
            "watch": watch_users,
            "flagged": flagged_users,
            "restricted": restricted_users,
            "blocked": blocked_users,
        },
        "events": {
            "pending": pending_events,
            "high": high_events,
        },
    }


@router.get("/flagged-users")
def get_flagged_users(db: Session = Depends(get_db)):
    users = (
        db.query(UserRiskProfile)
        .filter(UserRiskProfile.risk_level.in_(["watch", "flagged", "restricted", "blocked"]))
        .order_by(UserRiskProfile.updated_at.desc())
        .limit(100)
        .all()
    )
    return users


@router.get("/logs")
def get_risk_logs(
    user_id: UUID | None = None,
    trade_id: UUID | None = None,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    query = db.query(RiskLog)
    if user_id:
        query = query.filter(RiskLog.user_id == user_id)
    if trade_id:
        query = query.filter(RiskLog.trade_id == trade_id)
    return query.order_by(RiskLog.created_at.desc()).limit(limit).all()


@router.get("/users/{user_id}")
def get_user_risk_profile(user_id: UUID, db: Session = Depends(get_db)):
    service = RiskService(db)
    return service.get_or_create_profile(user_id)


@router.post("/users/{user_id}/block")
def block_user(
    user_id: UUID,
    reason: str,
    hours: int | None = None,
    admin_id: str | None = Query(None, description="管理员 user UUID"),
    db: Session = Depends(get_db),
):
    if admin_id:
        _require_admin(admin_id, db)
        created_by = "admin"
    else:
        created_by = "system"

    service = RiskService(db)
    profile = service.block_user(user_id=user_id, reason=reason, hours=hours, created_by=created_by)
    return profile


@router.post("/users/{user_id}/unblock")
def unblock_user(
    user_id: UUID,
    admin_id: str = Query(..., description="管理员 user UUID"),
    db: Session = Depends(get_db),
):
    _require_admin(admin_id, db)
    service = RiskService(db)
    return service.unblock_user(user_id=user_id, created_by="admin")


@router.post("/users/adjust-score")
def adjust_score(payload: AdjustScoreInput, admin_id: str = Query(...), db: Session = Depends(get_db)):
    _require_admin(admin_id, db)
    service = RiskService(db)
    profile = service.apply_score_change(
        user_id=payload.user_id,
        score_delta=payload.score_delta,
        reason=payload.reason,
        event_type="admin_adjust_score",
        created_by="admin",
    )
    return profile

