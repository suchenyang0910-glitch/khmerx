from __future__ import annotations

import uuid
from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.admin.auth import AdminPrincipal, get_current_admin, issue_admin_token
from app import config
from app.database import get_db
from app.models.announcement import Announcement
from app.models.app_config import AppConfig
from app.models.interest_rate import InterestRateMatrix
from app.models.notification import Notification
from app.models.p2p_offer import P2POffer
from app.models.p2p_trade import P2PTrade
from app.models.user import User
from app.risk.models import Dispute, DisputeEvidence, ManualReviewCase, RiskEvent, RiskRule, UserRiskProfile
from app.risk.router import risk_dashboard
from app.risk.service import RiskService
from app.services.admin_audit import append_admin_audit_log


router = APIRouter(prefix="/api/admin", tags=["admin"])


def _parse_ymd(v: str | None):
    if not v:
        return None
    try:
        y, m, d = v.split("-", 2)
        return datetime(int(y), int(m), int(d), tzinfo=timezone.utc)
    except Exception:
        return None


def _date_range(from_ymd: str | None, to_ymd: str | None, default_days: int = 14):
    end = _parse_ymd(to_ymd)
    if end is None:
        now = datetime.now(timezone.utc)
        end = datetime(now.year, now.month, now.day, tzinfo=timezone.utc)
    start = _parse_ymd(from_ymd)
    if start is None:
        start = end - timedelta(days=default_days - 1)
    return start, end + timedelta(days=1)


class AdminLoginInput(BaseModel):
    username: str
    password: str


@router.post("/login")
def admin_login(payload: AdminLoginInput):
    if not config.ADMIN_PASSWORD:
        raise HTTPException(status_code=500, detail="ADMIN_PASSWORD not configured")
    if payload.username != config.ADMIN_USERNAME or payload.password != config.ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="invalid credentials")
    token = issue_admin_token(username=payload.username)
    return {"token": token, "expires_in": 86400, "username": payload.username}


@router.get("/dashboard")
def admin_dashboard(_: AdminPrincipal = Depends(get_current_admin), db: Session = Depends(get_db)):
    users = db.query(User).count()
    offers_pending = db.query(P2POffer).filter(P2POffer.status == "pending").count()
    trades_active = db.query(P2PTrade).filter(P2PTrade.status.in_(["matched", "lend_confirmed", "repayment_confirmed", "repaying"]))
    trades_active_count = trades_active.count()
    disputes_open = db.query(Dispute).filter(Dispute.status.in_(["open", "reviewing"])).count()
    risk_pending = db.query(RiskEvent).filter(RiskEvent.status == "pending").count()
    return {
        "users": users,
        "offers": {"pending": offers_pending},
        "trades": {"active": trades_active_count},
        "disputes": {"open": disputes_open},
        "risk": {"pending_events": risk_pending},
    }


@router.get("/reports/overview")
def admin_reports_overview(
    from_ymd: str | None = None,
    to_ymd: str | None = None,
    _: AdminPrincipal = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    start, end = _date_range(from_ymd, to_ymd, default_days=14)

    users_total = db.query(User).count()
    users_new = db.query(User).filter(User.created_at >= start).filter(User.created_at < end).count()

    offers_total = db.query(P2POffer).count()
    offers_new = db.query(P2POffer).filter(P2POffer.created_at >= start).filter(P2POffer.created_at < end).count()
    offers_pending = db.query(P2POffer).filter(P2POffer.status == "pending").count()

    trades_total = db.query(P2PTrade).count()
    trades_new = db.query(P2PTrade).filter(P2PTrade.created_at >= start).filter(P2PTrade.created_at < end).count()
    trades_active = db.query(P2PTrade).filter(P2PTrade.status.in_(["matched", "lend_confirmed", "repayment_confirmed", "repaying"]))
    trades_active_count = trades_active.count()
    trades_completed = db.query(P2PTrade).filter(P2PTrade.status == "completed").filter(P2PTrade.updated_at >= start).filter(P2PTrade.updated_at < end).count()
    trades_failed = db.query(P2PTrade).filter(P2PTrade.status.in_(["cancelled", "defaulted"]))
    trades_failed = trades_failed.filter(P2PTrade.updated_at >= start).filter(P2PTrade.updated_at < end).count()

    disputes_open = db.query(Dispute).filter(Dispute.status.in_(["open", "reviewing"])).count()
    disputes_new = db.query(Dispute).filter(Dispute.created_at >= start).filter(Dispute.created_at < end).count()

    risk_pending = db.query(RiskEvent).filter(RiskEvent.status == "pending").count()
    risk_new = db.query(RiskEvent).filter(RiskEvent.created_at >= start).filter(RiskEvent.created_at < end).count()

    return {
        "range": {"from": start.date().isoformat(), "to": (end - timedelta(days=1)).date().isoformat()},
        "users": {"total": users_total, "new": users_new},
        "offers": {"total": offers_total, "new": offers_new, "pending": offers_pending},
        "trades": {
            "total": trades_total,
            "new": trades_new,
            "active": trades_active_count,
            "completed": trades_completed,
            "failed": trades_failed,
        },
        "disputes": {"open": disputes_open, "new": disputes_new},
        "risk": {"pending_events": risk_pending, "new_events": risk_new},
    }


def _series_by_day(rows, start: datetime, end: datetime):
    days = int((end - start).days)
    points = { (start + timedelta(days=i)).date().isoformat(): 0 for i in range(days) }
    for dt in rows:
        if not dt:
            continue
        if getattr(dt, "tzinfo", None) is None:
            dt = dt.replace(tzinfo=timezone.utc)
        k = dt.astimezone(timezone.utc).date().isoformat()
        if k in points:
            points[k] += 1
    labels = list(points.keys())
    values = [points[k] for k in labels]
    return {"labels": labels, "values": values}


@router.get("/reports/trends")
def admin_reports_trends(
    from_ymd: str | None = None,
    to_ymd: str | None = None,
    _: AdminPrincipal = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    start, end = _date_range(from_ymd, to_ymd, default_days=14)

    users_rows = [r[0] for r in db.query(User.created_at).filter(User.created_at >= start).filter(User.created_at < end).all()]
    offers_rows = [r[0] for r in db.query(P2POffer.created_at).filter(P2POffer.created_at >= start).filter(P2POffer.created_at < end).all()]
    trades_rows = [r[0] for r in db.query(P2PTrade.created_at).filter(P2PTrade.created_at >= start).filter(P2PTrade.created_at < end).all()]
    risk_rows = [r[0] for r in db.query(RiskEvent.created_at).filter(RiskEvent.created_at >= start).filter(RiskEvent.created_at < end).all()]
    dispute_rows = [r[0] for r in db.query(Dispute.created_at).filter(Dispute.created_at >= start).filter(Dispute.created_at < end).all()]

    return {
        "range": {"from": start.date().isoformat(), "to": (end - timedelta(days=1)).date().isoformat()},
        "users_new": _series_by_day(users_rows, start, end),
        "offers_new": _series_by_day(offers_rows, start, end),
        "trades_new": _series_by_day(trades_rows, start, end),
        "risk_events_new": _series_by_day(risk_rows, start, end),
        "disputes_new": _series_by_day(dispute_rows, start, end),
    }


def _csv_escape(v):
    if v is None:
        return ""
    s = str(v)
    if any(ch in s for ch in [",", "\n", "\r", '"']):
        s = s.replace('"', '""')
        return f'"{s}"'
    return s


def _csv_stream(headers: list[str], rows: list[list]):
    yield "\ufeff" + ",".join(headers) + "\n"
    for row in rows:
        yield ",".join(_csv_escape(v) for v in row) + "\n"


@router.get("/exports/users.csv")
def admin_export_users_csv(
    from_ymd: str | None = None,
    to_ymd: str | None = None,
    _: AdminPrincipal = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    from fastapi.responses import StreamingResponse

    start, end = _date_range(from_ymd, to_ymd, default_days=30)
    users = (
        db.query(User)
        .filter(User.created_at >= start)
        .filter(User.created_at < end)
        .order_by(User.created_at.desc())
        .limit(20000)
        .all()
    )
    headers = ["id", "tg_id", "name", "role", "risk_level", "credit_score", "phone", "aba_account", "aba_name", "created_at"]
    rows = [
        [
            str(u.id),
            u.tg_id,
            u.name,
            u.role,
            u.risk_level,
            u.credit_score,
            u.phone or "",
            u.aba_account or "",
            u.aba_name or "",
            u.created_at.isoformat() if u.created_at else "",
        ]
        for u in users
    ]
    filename = f"users_{start.date().isoformat()}_{(end - timedelta(days=1)).date().isoformat()}.csv"
    resp = StreamingResponse(_csv_stream(headers, rows), media_type="text/csv; charset=utf-8")
    resp.headers["Content-Disposition"] = f"attachment; filename={filename}"
    return resp


@router.get("/exports/orders.csv")
def admin_export_orders_csv(
    from_ymd: str | None = None,
    to_ymd: str | None = None,
    _: AdminPrincipal = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    from fastapi.responses import StreamingResponse

    start, end = _date_range(from_ymd, to_ymd, default_days=30)
    trades = (
        db.query(P2PTrade)
        .filter(P2PTrade.created_at >= start)
        .filter(P2PTrade.created_at < end)
        .order_by(P2PTrade.created_at.desc())
        .limit(20000)
        .all()
    )
    headers = [
        "id",
        "offer_id",
        "borrower_id",
        "lender_id",
        "amount",
        "term_days",
        "rate",
        "fee",
        "status",
        "created_at",
        "updated_at",
    ]
    rows = [
        [
            str(t.id),
            str(t.offer_id),
            str(t.borrower_id),
            str(t.lender_id),
            float(t.amount),
            t.term_days,
            float(t.rate),
            float(t.fee),
            t.status,
            t.created_at.isoformat() if t.created_at else "",
            t.updated_at.isoformat() if t.updated_at else "",
        ]
        for t in trades
    ]
    filename = f"orders_{start.date().isoformat()}_{(end - timedelta(days=1)).date().isoformat()}.csv"
    resp = StreamingResponse(_csv_stream(headers, rows), media_type="text/csv; charset=utf-8")
    resp.headers["Content-Disposition"] = f"attachment; filename={filename}"
    return resp


@router.get("/exports/risk-events.csv")
def admin_export_risk_events_csv(
    from_ymd: str | None = None,
    to_ymd: str | None = None,
    status: str | None = None,
    _: AdminPrincipal = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    from fastapi.responses import StreamingResponse

    start, end = _date_range(from_ymd, to_ymd, default_days=30)
    query = db.query(RiskEvent).filter(RiskEvent.created_at >= start).filter(RiskEvent.created_at < end)
    if status:
        query = query.filter(RiskEvent.status == status)
    events = query.order_by(RiskEvent.created_at.desc()).limit(20000).all()
    headers = ["id", "event_type", "severity", "status", "user_id", "trade_id", "offer_id", "handled_by", "created_at", "handled_at"]
    rows = [
        [
            e.id,
            e.event_type,
            e.severity,
            e.status,
            str(e.user_id) if e.user_id else "",
            str(e.trade_id) if e.trade_id else "",
            str(e.offer_id) if e.offer_id else "",
            e.handled_by or "",
            e.created_at.isoformat() if e.created_at else "",
            e.handled_at.isoformat() if e.handled_at else "",
        ]
        for e in events
    ]
    filename = f"risk_events_{start.date().isoformat()}_{(end - timedelta(days=1)).date().isoformat()}.csv"
    resp = StreamingResponse(_csv_stream(headers, rows), media_type="text/csv; charset=utf-8")
    resp.headers["Content-Disposition"] = f"attachment; filename={filename}"
    return resp


@router.get("/config")
def admin_get_config(_: AdminPrincipal = Depends(get_current_admin), db: Session = Depends(get_db)):
    rows = db.query(AppConfig).order_by(AppConfig.key.asc()).all()
    return [{"key": r.key, "value": r.value, "updated_at": r.updated_at.isoformat() if r.updated_at else None} for r in rows]


class AdminConfigUpsert(BaseModel):
    key: str
    value: dict


@router.post("/config")
def admin_upsert_config(
    payload: AdminConfigUpsert,
    request: Request,
    admin: AdminPrincipal = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    k = payload.key.strip()
    if not k:
        raise HTTPException(status_code=400, detail="key required")
    row = db.query(AppConfig).filter(AppConfig.key == k).first()
    before = {"key": k, "value": row.value} if row else None
    if not row:
        row = AppConfig(key=k, value=payload.value)
        db.add(row)
    else:
        row.value = payload.value
        row.updated_at = datetime.now(timezone.utc)
    append_admin_audit_log(
        db,
        admin_username=admin.username,
        action="upsert",
        resource_type="app_config",
        resource_id=k,
        before=before,
        after={"key": k, "value": payload.value},
        ip=(request.client.host if request.client else None),
    )
    db.commit()
    db.refresh(row)
    return {"key": row.key, "value": row.value, "updated_at": row.updated_at.isoformat() if row.updated_at else None}


@router.get("/risk/dashboard")
def admin_risk_dashboard(_: AdminPrincipal = Depends(get_current_admin), db: Session = Depends(get_db)):
    return risk_dashboard(db)


@router.get("/risk/events")
def admin_list_risk_events(
    status: str | None = None,
    limit: int = 50,
    _: AdminPrincipal = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    query = db.query(RiskEvent)
    if status:
        query = query.filter(RiskEvent.status == status)
    rows = query.order_by(RiskEvent.created_at.desc()).limit(min(limit, 200)).all()
    return [
        {
            "id": e.id,
            "event_type": e.event_type,
            "severity": e.severity,
            "status": e.status,
            "user_id": str(e.user_id) if e.user_id else None,
            "trade_id": str(e.trade_id) if e.trade_id else None,
            "offer_id": str(e.offer_id) if e.offer_id else None,
            "payload": e.payload,
            "handled_by": e.handled_by,
            "handled_at": e.handled_at.isoformat() if e.handled_at else None,
            "created_at": e.created_at.isoformat() if e.created_at else None,
        }
        for e in rows
    ]


class AdminRiskEventHandle(BaseModel):
    handled_by: str = "admin"


@router.post("/risk/events/{event_id}/handled")
def admin_mark_risk_event_handled(
    event_id: int,
    payload: AdminRiskEventHandle,
    request: Request,
    admin: AdminPrincipal = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    event = db.query(RiskEvent).filter(RiskEvent.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="risk event not found")
    before = {"id": event.id, "status": event.status, "handled_by": event.handled_by}
    event.status = "handled"
    event.handled_by = payload.handled_by
    event.handled_at = datetime.now(timezone.utc)
    append_admin_audit_log(
        db,
        admin_username=admin.username,
        action="mark_handled",
        resource_type="risk_event",
        resource_id=str(event.id),
        before=before,
        after={"id": event.id, "status": event.status, "handled_by": event.handled_by},
        ip=(request.client.host if request.client else None),
    )
    db.commit()
    db.refresh(event)
    return {
        "id": event.id,
        "status": event.status,
        "handled_by": event.handled_by,
        "handled_at": event.handled_at.isoformat() if event.handled_at else None,
    }


@router.get("/risk/flagged-users")
def admin_flagged_users(_: AdminPrincipal = Depends(get_current_admin), db: Session = Depends(get_db)):
    rows = (
        db.query(UserRiskProfile)
        .filter(UserRiskProfile.risk_level.in_(["watch", "flagged", "restricted", "blocked"]))
        .order_by(UserRiskProfile.updated_at.desc())
        .limit(200)
        .all()
    )
    return [
        {
            "user_id": str(r.user_id),
            "risk_level": r.risk_level,
            "credit_score": r.credit_score,
            "credit_level": r.credit_level,
            "max_borrow_amount": float(r.max_borrow_amount),
            "max_active_trades": r.max_active_trades,
            "is_blocked": bool(r.is_blocked),
            "blocked_until": r.blocked_until.isoformat() if r.blocked_until else None,
            "block_reason": r.block_reason,
            "updated_at": r.updated_at.isoformat() if r.updated_at else None,
        }
        for r in rows
    ]


@router.get("/risk/rules")
def admin_list_risk_rules(_: AdminPrincipal = Depends(get_current_admin), db: Session = Depends(get_db)):
    rows = db.query(RiskRule).order_by(RiskRule.id.asc()).all()
    return [
        {
            "id": r.id,
            "code": r.code,
            "name": r.name,
            "rule_type": r.rule_type,
            "threshold_value": float(r.threshold_value) if r.threshold_value is not None else None,
            "action": r.action,
            "score_delta": r.score_delta,
            "enabled": bool(r.enabled),
        }
        for r in rows
    ]


class AdminRiskRuleUpsert(BaseModel):
    code: str
    name: str
    rule_type: str
    threshold_value: float | None = None
    action: str
    score_delta: int = 0
    enabled: bool = True


@router.post("/risk/rules")
def admin_upsert_risk_rule(
    payload: AdminRiskRuleUpsert,
    _: AdminPrincipal = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    code = payload.code.strip()
    if not code:
        raise HTTPException(status_code=400, detail="code required")
    row = db.query(RiskRule).filter(RiskRule.code == code).first()
    if not row:
        row = RiskRule(
            code=code,
            name=payload.name,
            rule_type=payload.rule_type,
            threshold_value=payload.threshold_value,
            action=payload.action,
            score_delta=payload.score_delta,
            enabled=payload.enabled,
        )
        db.add(row)
    else:
        row.name = payload.name
        row.rule_type = payload.rule_type
        row.threshold_value = payload.threshold_value
        row.action = payload.action
        row.score_delta = payload.score_delta
        row.enabled = payload.enabled
        row.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(row)
    return {
        "id": row.id,
        "code": row.code,
        "name": row.name,
        "rule_type": row.rule_type,
        "threshold_value": float(row.threshold_value) if row.threshold_value is not None else None,
        "action": row.action,
        "score_delta": row.score_delta,
        "enabled": bool(row.enabled),
    }


class AdminUserBlockInput(BaseModel):
    reason: str = ""
    hours: int | None = None


@router.post("/risk/users/{user_id}/block")
def admin_block_user(
    user_id: str,
    payload: AdminUserBlockInput,
    _: AdminPrincipal = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    try:
        uid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="invalid user_id")
    RiskService(db).block_user(user_id=uid, reason=payload.reason, hours=payload.hours, created_by="admin")
    return {"ok": True}


@router.post("/risk/users/{user_id}/unblock")
def admin_unblock_user(
    user_id: str,
    _: AdminPrincipal = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    try:
        uid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="invalid user_id")
    RiskService(db).unblock_user(user_id=uid, created_by="admin")
    return {"ok": True}


class AdminScoreAdjustInput(BaseModel):
    score_delta: int
    reason: str = "manual adjust"


@router.post("/risk/users/{user_id}/score")
def admin_adjust_score(
    user_id: str,
    payload: AdminScoreAdjustInput,
    _: AdminPrincipal = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    try:
        uid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="invalid user_id")
    RiskService(db).apply_score_change(
        user_id=uid,
        score_delta=payload.score_delta,
        reason=payload.reason,
        event_type="manual_adjust",
        created_by="admin",
    )
    return {"ok": True}


@router.get("/disputes")
def admin_list_disputes(
    status: str | None = None,
    limit: int = 50,
    _: AdminPrincipal = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    query = db.query(Dispute)
    if status:
        query = query.filter(Dispute.status == status)
    rows = query.order_by(Dispute.created_at.desc()).limit(min(limit, 200)).all()
    return [
        {
            "id": d.id,
            "trade_id": str(d.trade_id),
            "borrower_id": str(d.borrower_id) if d.borrower_id else None,
            "lender_id": str(d.lender_id) if d.lender_id else None,
            "status": d.status,
            "priority": d.priority,
            "dispute_type": d.dispute_type,
            "reason": d.reason,
            "resolution_result": d.resolution_result,
            "created_at": d.created_at.isoformat() if d.created_at else None,
        }
        for d in rows
    ]


@router.get("/disputes/{dispute_id}")
def admin_get_dispute(
    dispute_id: int,
    _: AdminPrincipal = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    d = db.query(Dispute).filter(Dispute.id == dispute_id).first()
    if not d:
        raise HTTPException(status_code=404, detail="dispute not found")
    evidences = db.query(DisputeEvidence).filter(DisputeEvidence.dispute_id == d.id).order_by(DisputeEvidence.created_at.asc()).all()
    return {
        "id": d.id,
        "trade_id": str(d.trade_id),
        "offer_id": str(d.offer_id) if d.offer_id else None,
        "borrower_id": str(d.borrower_id) if d.borrower_id else None,
        "lender_id": str(d.lender_id) if d.lender_id else None,
        "raised_role": d.raised_role,
        "dispute_type": d.dispute_type,
        "reason": d.reason,
        "status": d.status,
        "priority": d.priority,
        "resolution_result": d.resolution_result,
        "resolution_note": d.resolution_note,
        "created_at": d.created_at.isoformat() if d.created_at else None,
        "updated_at": d.updated_at.isoformat() if d.updated_at else None,
        "evidence": [
            {
                "id": e.id,
                "uploaded_by_user_id": str(e.uploaded_by_user_id),
                "uploaded_role": e.uploaded_role,
                "evidence_type": e.evidence_type,
                "file_url": e.file_url,
                "text_note": e.text_note,
                "created_at": e.created_at.isoformat() if e.created_at else None,
            }
            for e in evidences
        ],
    }


class AdminDisputeResolveInput(BaseModel):
    resolution_result: str
    resolution_note: str = ""


@router.post("/disputes/{dispute_id}/resolve")
def admin_resolve_dispute(
    dispute_id: int,
    payload: AdminDisputeResolveInput,
    request: Request,
    admin: AdminPrincipal = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    dispute = db.query(Dispute).filter(Dispute.id == dispute_id).first()
    if not dispute:
        raise HTTPException(status_code=404, detail="dispute not found")

    before = {"id": dispute.id, "status": dispute.status, "resolution_result": dispute.resolution_result}

    trade = db.query(P2PTrade).filter(P2PTrade.id == dispute.trade_id).first()
    if not trade:
        raise HTTPException(status_code=404, detail="trade not found")

    result = payload.resolution_result
    allowed = ["borrower_win", "lender_win", "both_fault", "cancel_trade", "manual_continue", "fraud"]
    if result not in allowed:
        raise HTTPException(status_code=400, detail="invalid resolution_result")

    service = RiskService(db)
    dispute.status = "resolved"
    dispute.resolution_result = result
    dispute.resolution_note = payload.resolution_note
    dispute.resolved_by = None
    dispute.resolved_at = datetime.now(timezone.utc)
    dispute.updated_at = datetime.now(timezone.utc)

    if result == "borrower_win":
        if dispute.lender_id:
            service.apply_score_change(
                user_id=dispute.lender_id,
                score_delta=-50,
                reason="dispute lost: borrower win",
                event_type="dispute_lost",
                trade_id=trade.id,
                created_by="admin",
            )
        trade.status = "repaying"
    elif result == "lender_win":
        if dispute.borrower_id:
            service.apply_score_change(
                user_id=dispute.borrower_id,
                score_delta=-50,
                reason="dispute lost: lender win",
                event_type="dispute_lost",
                trade_id=trade.id,
                created_by="admin",
            )
        trade.status = "repaying"
    elif result == "both_fault":
        if dispute.borrower_id:
            service.apply_score_change(
                user_id=dispute.borrower_id,
                score_delta=-20,
                reason="dispute both fault",
                event_type="dispute_both_fault",
                trade_id=trade.id,
                created_by="admin",
            )
        if dispute.lender_id:
            service.apply_score_change(
                user_id=dispute.lender_id,
                score_delta=-20,
                reason="dispute both fault",
                event_type="dispute_both_fault",
                trade_id=trade.id,
                created_by="admin",
            )
        trade.status = "repaying"
    elif result == "cancel_trade":
        trade.status = "cancelled"
    elif result == "manual_continue":
        trade.status = "repaying"
    elif result == "fraud":
        if dispute.borrower_id:
            service.block_user(user_id=dispute.borrower_id, reason="fraud confirmed", hours=None, created_by="admin")
        trade.status = "cancelled"

    service.create_risk_event(
        event_type="trade_dispute_resolved",
        severity="medium",
        user_id=dispute.raised_by_user_id,
        trade_id=trade.id,
        offer_id=trade.offer_id,
        payload={"result": result, "resolution_note": payload.resolution_note},
    )

    append_admin_audit_log(
        db,
        admin_username=admin.username,
        action="resolve",
        resource_type="dispute",
        resource_id=str(dispute.id),
        before=before,
        after={"id": dispute.id, "status": dispute.status, "resolution_result": dispute.resolution_result},
        ip=(request.client.host if request.client else None),
    )
    db.commit()
    db.refresh(dispute)
    return {
        "id": dispute.id,
        "status": dispute.status,
        "resolution_result": dispute.resolution_result,
        "resolution_note": dispute.resolution_note,
    }


@router.get("/manual-reviews")
def admin_list_manual_reviews(
    status: str | None = None,
    limit: int = 50,
    _: AdminPrincipal = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    query = db.query(ManualReviewCase)
    if status:
        query = query.filter(ManualReviewCase.status == status)
    rows = query.order_by(ManualReviewCase.created_at.desc()).limit(min(limit, 200)).all()
    return [
        {
            "id": r.id,
            "user_id": str(r.user_id) if r.user_id else None,
            "trade_id": str(r.trade_id) if r.trade_id else None,
            "offer_id": str(r.offer_id) if r.offer_id else None,
            "reason": r.reason,
            "risk_score": r.risk_score,
            "status": r.status,
            "decision": r.decision,
            "review_note": r.review_note,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in rows
    ]


class AdminManualReviewDecideInput(BaseModel):
    decision: str
    review_note: str = ""


@router.post("/manual-reviews/{case_id}/decide")
def admin_decide_manual_review(
    case_id: int,
    payload: AdminManualReviewDecideInput,
    _: AdminPrincipal = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    row = db.query(ManualReviewCase).filter(ManualReviewCase.id == case_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="review case not found")
    row.status = "reviewed"
    row.decision = payload.decision
    row.review_note = payload.review_note
    row.reviewed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(row)
    return {"id": row.id, "status": row.status, "decision": row.decision}


@router.get("/announcements")
def admin_list_announcements(
    lang: str | None = None,
    limit: int = 50,
    _: AdminPrincipal = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    query = db.query(Announcement)
    if lang:
        query = query.filter(Announcement.lang == lang)
    rows = query.order_by(Announcement.created_at.desc()).limit(min(limit, 200)).all()
    return [
        {
            "id": str(a.id),
            "lang": a.lang,
            "title": a.title,
            "body": a.body,
            "link_url": a.link_url,
            "active": bool(a.active),
            "starts_at": a.starts_at.isoformat() if a.starts_at else None,
            "ends_at": a.ends_at.isoformat() if a.ends_at else None,
            "created_at": a.created_at.isoformat() if a.created_at else None,
        }
        for a in rows
    ]


class AdminAnnouncementUpsert(BaseModel):
    id: str | None = None
    lang: str = "km"
    title: str
    body: str
    link_url: str | None = None
    active: bool = True


@router.post("/announcements")
def admin_upsert_announcement(
    payload: AdminAnnouncementUpsert,
    _: AdminPrincipal = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    if payload.lang not in ("km", "en", "zh"):
        raise HTTPException(status_code=400, detail="invalid lang")
    row = None
    if payload.id:
        try:
            aid = uuid.UUID(payload.id)
        except ValueError:
            raise HTTPException(status_code=400, detail="invalid id")
        row = db.query(Announcement).filter(Announcement.id == aid).first()
    if not row:
        row = Announcement(
            lang=payload.lang,
            title=payload.title,
            body=payload.body,
            link_url=payload.link_url,
            active=payload.active,
        )
        db.add(row)
    else:
        row.lang = payload.lang
        row.title = payload.title
        row.body = payload.body
        row.link_url = payload.link_url
        row.active = payload.active
    db.commit()
    db.refresh(row)
    return {
        "id": str(row.id),
        "lang": row.lang,
        "title": row.title,
        "body": row.body,
        "link_url": row.link_url,
        "active": bool(row.active),
    }


@router.get("/users")
def admin_list_users(
    q: str = "",
    limit: int = 50,
    _: AdminPrincipal = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    query = db.query(User)
    if q:
        like = f"%{q}%"
        try:
            tg = int(q)
        except Exception:
            tg = None
        if tg is not None:
            query = query.filter(User.tg_id == tg)
        else:
            query = query.filter(User.name.ilike(like))
    rows = query.order_by(User.created_at.desc()).limit(min(limit, 200)).all()
    return [
        {
            "id": str(u.id),
            "tg_id": u.tg_id,
            "name": u.name,
            "role": u.role,
            "risk_level": u.risk_level,
            "credit_score": u.credit_score,
            "phone": u.phone,
            "aba_account": u.aba_account,
            "aba_name": u.aba_name,
            "created_at": u.created_at.isoformat() if u.created_at else None,
        }
        for u in rows
    ]


@router.get("/offers")
def admin_list_offers(
    status: str | None = None,
    limit: int = 50,
    _: AdminPrincipal = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    query = db.query(P2POffer)
    if status:
        query = query.filter(P2POffer.status == status)
    rows = query.order_by(P2POffer.created_at.desc()).limit(min(limit, 200)).all()
    return [
        {
            "id": str(o.id),
            "borrower_id": str(o.borrower_id),
            "amount": o.amount,
            "term_days": o.term_days,
            "rate": o.rate,
            "fee": o.fee,
            "total_amount": o.total_amount,
            "status": o.status,
            "note": o.note or "",
            "created_at": o.created_at.isoformat() if o.created_at else None,
        }
        for o in rows
    ]


@router.get("/trades")
def admin_list_trades(
    status: str | None = None,
    limit: int = 50,
    _: AdminPrincipal = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    query = db.query(P2PTrade)
    if status:
        query = query.filter(P2PTrade.status == status)
    rows = query.order_by(P2PTrade.created_at.desc()).limit(min(limit, 200)).all()
    return [
        {
            "id": str(t.id),
            "offer_id": str(t.offer_id),
            "borrower_id": str(t.borrower_id),
            "lender_id": str(t.lender_id),
            "amount": t.amount,
            "term_days": t.term_days,
            "rate": t.rate,
            "fee": t.fee,
            "total_repayable": t.total_repayable,
            "status": t.status,
            "fund_source": t.fund_source,
            "created_at": t.created_at.isoformat() if t.created_at else None,
        }
        for t in rows
    ]


class AdminNotificationCreate(BaseModel):
    user_id: str
    type: str = "system"
    title: str
    body: str
    target_type: str | None = None
    target_id: str | None = None


@router.post("/notifications")
def admin_create_notification(
    payload: AdminNotificationCreate,
    _: AdminPrincipal = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    try:
        uid = uuid.UUID(payload.user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="invalid user_id")

    u = db.query(User).filter(User.id == uid).first()
    if not u:
        raise HTTPException(status_code=404, detail="user not found")

    n = Notification(
        user_id=uid,
        type=payload.type,
        title=payload.title,
        body=payload.body,
        target_type=payload.target_type,
        target_id=payload.target_id,
        read=False,
    )
    db.add(n)
    db.commit()
    db.refresh(n)
    return {
        "id": str(n.id),
        "user_id": str(n.user_id),
        "type": n.type,
        "title": n.title,
        "body": n.body,
        "read": n.read,
        "created_at": n.created_at.isoformat() if n.created_at else None,
    }


@router.get("/notifications")
def admin_list_notifications(
    user_id: str | None = None,
    limit: int = 50,
    _: AdminPrincipal = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    query = db.query(Notification)
    if user_id:
        try:
            uid = uuid.UUID(user_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="invalid user_id")
        query = query.filter(Notification.user_id == uid)
    rows = query.order_by(Notification.created_at.desc()).limit(min(limit, 200)).all()
    return [
        {
            "id": str(n.id),
            "user_id": str(n.user_id),
            "type": n.type,
            "title": n.title,
            "body": n.body,
            "read": n.read,
            "created_at": n.created_at.isoformat() if n.created_at else None,
        }
        for n in rows
    ]


@router.get("/interest-rates")
def admin_list_interest_rates(_: AdminPrincipal = Depends(get_current_admin), db: Session = Depends(get_db)):
    rows = db.query(InterestRateMatrix).order_by(InterestRateMatrix.term_days.asc(), InterestRateMatrix.credit_level.asc()).all()
    return [
        {
            "id": r.id,
            "term_days": r.term_days,
            "credit_level": r.credit_level,
            "rate_percent": float(r.rate_percent),
            "mode": r.mode,
            "enabled": bool(r.enabled),
            "updated_at": r.updated_at.isoformat() if r.updated_at else None,
        }
        for r in rows
    ]


class AdminInterestRateUpsert(BaseModel):
    term_days: int
    credit_level: str
    rate_percent: float
    mode: str = "cut_interest"
    enabled: bool = True


@router.post("/interest-rates")
def admin_upsert_interest_rate(
    payload: AdminInterestRateUpsert,
    request: Request,
    admin: AdminPrincipal = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    level = payload.credit_level.strip().upper()
    if level not in ("A", "B", "C", "D"):
        raise HTTPException(status_code=400, detail="invalid credit_level")
    if payload.term_days not in (7, 14, 30):
        raise HTTPException(status_code=400, detail="invalid term_days")
    row = (
        db.query(InterestRateMatrix)
        .filter(InterestRateMatrix.term_days == payload.term_days)
        .filter(InterestRateMatrix.credit_level == level)
        .first()
    )
    before = (
        {
            "term_days": row.term_days,
            "credit_level": row.credit_level,
            "rate_percent": float(row.rate_percent),
            "mode": row.mode,
            "enabled": bool(row.enabled),
        }
        if row
        else None
    )
    if not row:
        row = InterestRateMatrix(
            term_days=payload.term_days,
            credit_level=level,
            rate_percent=payload.rate_percent,
            mode=payload.mode,
            enabled=payload.enabled,
        )
        db.add(row)
    else:
        row.rate_percent = payload.rate_percent
        row.mode = payload.mode
        row.enabled = payload.enabled
        row.updated_at = datetime.now(timezone.utc)

    append_admin_audit_log(
        db,
        admin_username=admin.username,
        action="upsert",
        resource_type="interest_rate",
        resource_id=f"{payload.term_days}:{level}",
        before=before,
        after={
            "term_days": payload.term_days,
            "credit_level": level,
            "rate_percent": payload.rate_percent,
            "mode": payload.mode,
            "enabled": payload.enabled,
        },
        ip=(request.client.host if request.client else None),
    )
    db.commit()
    db.refresh(row)
    return {
        "id": row.id,
        "term_days": row.term_days,
        "credit_level": row.credit_level,
        "rate_percent": float(row.rate_percent),
        "mode": row.mode,
        "enabled": bool(row.enabled),
    }


@router.get("/audit-logs")
def admin_list_audit_logs(
    limit: int = 50,
    action: str | None = None,
    resource_type: str | None = None,
    _: AdminPrincipal = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    from app.models.admin_audit_log import AdminAuditLog

    q = db.query(AdminAuditLog)
    if action:
        q = q.filter(AdminAuditLog.action == action)
    if resource_type:
        q = q.filter(AdminAuditLog.resource_type == resource_type)
    rows = q.order_by(AdminAuditLog.id.desc()).limit(min(limit, 200)).all()
    return [
        {
            "id": r.id,
            "admin_username": r.admin_username,
            "action": r.action,
            "resource_type": r.resource_type,
            "resource_id": r.resource_id,
            "before": r.before,
            "after": r.after,
            "ip": r.ip,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in rows
    ]
