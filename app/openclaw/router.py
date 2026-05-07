from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.config import OPENCLAW_API_KEY
from app.database import get_db
from app.risk.service import RiskService
from app.services.notifications import create_notification
from app.risk.models import RiskEvent, RiskLog, UserRiskProfile
from app.risk.router import risk_dashboard


router = APIRouter(prefix="/openclaw", tags=["openclaw"])


def require_openclaw_key(x_openclaw_key: str | None = Header(None)):
    if not OPENCLAW_API_KEY:
        raise HTTPException(status_code=500, detail="OPENCLAW_API_KEY not configured")
    if not x_openclaw_key or x_openclaw_key != OPENCLAW_API_KEY:
        raise HTTPException(status_code=401, detail="invalid openclaw key")


@router.get("/risk/events/pending")
def openclaw_pending_events(
    limit: int = 50,
    _: None = Depends(require_openclaw_key),
    db: Session = Depends(get_db),
):
    return (
        db.query(RiskEvent)
        .filter(RiskEvent.status == "pending")
        .order_by(RiskEvent.severity.desc(), RiskEvent.created_at.asc())
        .limit(limit)
        .all()
    )


@router.post("/risk/events/{event_id}/handled")
def openclaw_mark_handled(
    event_id: int,
    handled_by: str = "openclaw",
    _: None = Depends(require_openclaw_key),
    db: Session = Depends(get_db),
):
    event = db.query(RiskEvent).filter(RiskEvent.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="risk event not found")
    from datetime import datetime, timezone

    event.status = "handled"
    event.handled_by = handled_by
    event.handled_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(event)
    return event


@router.get("/risk/dashboard")
def openclaw_dashboard(_: None = Depends(require_openclaw_key), db: Session = Depends(get_db)):
    return risk_dashboard(db)


@router.get("/risk/flagged-users")
def openclaw_flagged_users(_: None = Depends(require_openclaw_key), db: Session = Depends(get_db)):
    return (
        db.query(UserRiskProfile)
        .filter(UserRiskProfile.risk_level.in_(["watch", "flagged", "restricted", "blocked"]))
        .order_by(UserRiskProfile.updated_at.desc())
        .limit(100)
        .all()
    )


@router.get("/risk/logs")
def openclaw_risk_logs(
    user_id: str | None = None,
    trade_id: str | None = None,
    limit: int = 100,
    _: None = Depends(require_openclaw_key),
    db: Session = Depends(get_db),
):
    query = db.query(RiskLog)
    if user_id:
        import uuid

        try:
            query = query.filter(RiskLog.user_id == uuid.UUID(user_id))
        except ValueError:
            raise HTTPException(status_code=400, detail="invalid user_id")
    if trade_id:
        import uuid

        try:
            query = query.filter(RiskLog.trade_id == uuid.UUID(trade_id))
        except ValueError:
            raise HTTPException(status_code=400, detail="invalid trade_id")
    return query.order_by(RiskLog.created_at.desc()).limit(min(limit, 200)).all()


class OpenClawDecision(BaseModel):
    action: str
    reason: str = ""
    severity: str | None = None
    metadata: dict = {}
    block_hours: int | None = None
    score_delta: int | None = None


@router.post("/risk/events/{event_id}/decide")
def openclaw_decide_event(
    event_id: int,
    payload: OpenClawDecision,
    handled_by: str = "openclaw",
    _: None = Depends(require_openclaw_key),
    db: Session = Depends(get_db),
):
    event = db.query(RiskEvent).filter(RiskEvent.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="risk event not found")

    service = RiskService(db)

    if payload.action == "block_user":
        if not event.user_id:
            raise HTTPException(status_code=400, detail="event has no user_id")
        service.block_user(user_id=event.user_id, reason=payload.reason or "openclaw", hours=payload.block_hours, created_by=handled_by)
    elif payload.action == "manual_review":
        service.create_manual_review_case(
            reason=payload.reason or event.event_type,
            user_id=event.user_id,
            trade_id=event.trade_id,
            offer_id=event.offer_id,
            risk_score=int(payload.metadata.get("risk_score", 0)) if isinstance(payload.metadata, dict) else 0,
        )
    elif payload.action == "adjust_score":
        if not event.user_id:
            raise HTTPException(status_code=400, detail="event has no user_id")
        if payload.score_delta is None:
            raise HTTPException(status_code=400, detail="missing score_delta")
        service.apply_score_change(
            user_id=event.user_id,
            score_delta=int(payload.score_delta),
            reason=payload.reason or "openclaw_adjust",
            event_type="openclaw_adjust_score",
            trade_id=event.trade_id,
            offer_id=event.offer_id,
            created_by=handled_by,
            metadata=payload.metadata or {},
        )
    elif payload.action == "notify":
        if not event.user_id:
            raise HTTPException(status_code=400, detail="event has no user_id")
        create_notification(
            db,
            user_id=event.user_id,
            type="risk_notice",
            title="风险提示",
            body=payload.reason or "请查看风险提示并尽快处理。",
            target_type="risk_event",
            target_id=str(event.id),
        )
    elif payload.action == "mark_handled":
        pass
    else:
        raise HTTPException(status_code=400, detail="unsupported action")

    event.status = "handled"
    event.handled_by = handled_by
    event.handled_at = datetime.now(timezone.utc)
    if payload.severity:
        event.severity = payload.severity
    if isinstance(event.payload, dict):
        event.payload["openclaw"] = {
            "action": payload.action,
            "reason": payload.reason,
            "metadata": payload.metadata,
            "handled_at": datetime.now(timezone.utc).isoformat(),
        }
    db.commit()
    db.refresh(event)
    return event
