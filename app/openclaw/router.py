from __future__ import annotations

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.config import OPENCLAW_API_KEY
from app.database import get_db
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

