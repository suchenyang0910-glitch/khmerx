from __future__ import annotations

import os
import json
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, File, Query, Request, UploadFile
from sqlalchemy.orm import Session

from app.api_v1.auth import ensure_profile_completed, get_current_user_tma
from app.api_v1.errors import ApiError
from app.api_v1.responses import ok
from app.api_v1.schemas import (
    CalculateRequest,
    ConfirmLendRequest,
    ConfirmReceiveRequest,
    ConfirmRepaymentRequest,
    CreateOfferRequest,
    MatchOfferRequest,
    PatchProfileRequest,
    VerifyTelegramContactRequest,
    RepayRequest,
)
from app.config import BOT_TOKENS
from app.database import get_db
from app.models.p2p_offer import P2POffer
from app.models.p2p_trade import P2PTrade
from app.models.repayment_schedule import RepaymentSchedule
from app.models.user import User
from app.risk.models import RiskLog
from app.services.interest_calculator import InterestCalculator
from app.risk.engine import RiskEngine
from app.risk.schemas import CreateOfferRiskInput, MatchOfferRiskInput
from app.risk.service import RiskService
from app.risk.relations import RelationService
from app.ops.service import AgentService
from app.disputes.schemas import CreateDisputeInput, AddEvidenceInput
from app.disputes.service import DisputeService
from app.models.announcement import Announcement
from app.models.notification import Notification
from app.models.notification_settings import NotificationSettings
from app.risk.models import Dispute
from app.services.notifications import get_or_create_notification_settings
from app.services.auth import verify_telegram_contact_response
from app.services.bot_accounts import get_active_bot_tokens


router = APIRouter(prefix="/api/v1", tags=["v1"])


def _credit_level(user: User) -> str:
    level = InterestCalculator.score_to_credit_level(user.credit_score)
    if level == "E":
        return "D"
    return level


def _profile_completed(user: User) -> bool:
    return bool(user.phone_verified_at and user.aba_account and user.aba_name)


def _naive_utc(dt: datetime | None) -> datetime | None:
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt
    return dt.replace(tzinfo=None)


def _utcnow() -> datetime:
    return datetime.utcnow()


@router.get("/me")
def me(
    request: Request,
    user: User = Depends(get_current_user_tma),
    db: Session = Depends(get_db),
):
    credit_level = _credit_level(user)
    max_borrow_amount = RiskService(db).get_or_create_profile(user.id).max_borrow_amount
    return ok(
        {
            "id": str(user.id),
            "global_user_id": str(user.id),
            "tg_id": user.tg_id,
            "name": user.name,
            "role": user.role,
            "sub_role": user.sub_role or "borrower",
            "language": user.preferred_lang,
            "aba_account": user.aba_account or "",
            "aba_name": user.aba_name or "",
            "phone": user.phone or "",
            "phone_verified": bool(user.phone_verified_at),
            "profile_completed": _profile_completed(user),
            "credit_score": user.credit_score,
            "credit_level": credit_level,
            "risk_level": user.risk_level,
            "max_borrow_amount": float(max_borrow_amount),
            "active_trades": user.active_loans,
        }
    )


@router.patch("/me/profile")
def patch_profile(
    payload: PatchProfileRequest,
    user: User = Depends(get_current_user_tma),
    db: Session = Depends(get_db),
):
    if payload.phone is not None:
        new_phone = payload.phone.strip() or None
        if new_phone != (user.phone or None):
            user.phone = new_phone
            user.phone_verified_at = None
            user.verification_level = "unverified"

    if payload.aba_account is not None:
        user.aba_account = payload.aba_account.strip() or None

    if payload.aba_name is not None:
        user.aba_name = payload.aba_name.strip() or None

    if payload.language is not None:
        user.preferred_lang = payload.language

    if user.phone and user.aba_account and user.aba_name:
        if user.verification_level in ("phone", "kyc"):
            user.verification_level = "full"

    db.commit()
    return ok({"profile_completed": _profile_completed(user)})


@router.post("/me/phone/verify-telegram")
def verify_phone_via_telegram_contact(
    payload: VerifyTelegramContactRequest,
    user: User = Depends(get_current_user_tma),
    db: Session = Depends(get_db),
):
    tokens = []
    try:
        tokens = get_active_bot_tokens(db)
    except Exception:
        tokens = []
    if not tokens:
        tokens = BOT_TOKENS

    contact = verify_telegram_contact_response(payload.response, tokens)
    if not contact:
        raise ApiError(code="PHONE_VERIFY_FAILED", message="手机号验证失败", status_code=400)

    tg_user_id = int(contact.get("user_id") or 0)
    if tg_user_id != int(user.tg_id):
        raise ApiError(code="PHONE_VERIFY_FAILED", message="手机号验证失败", status_code=400)

    phone_number = (contact.get("phone_number") or "").strip()
    if not phone_number:
        raise ApiError(code="PHONE_VERIFY_FAILED", message="手机号验证失败", status_code=400)

    user.phone = phone_number
    user.phone_verified_at = datetime.now(timezone.utc)
    if user.verification_level == "unverified":
        user.verification_level = "phone"
    if user.phone and user.aba_account and user.aba_name:
        if user.verification_level in ("phone", "kyc"):
            user.verification_level = "full"

    db.commit()
    return ok({"phone": user.phone, "phone_verified": True, "verification_level": user.verification_level})


@router.get("/me/credit")
def me_credit(
    user: User = Depends(get_current_user_tma),
    db: Session = Depends(get_db),
):
    profile = RiskService(db).get_or_create_profile(user.id)
    reasons: List[str] = []
    if not _profile_completed(user):
        reasons.append("资料未完善，完成手机号与 ABA 绑定可提升通过率")
    if profile.cancel_count and profile.cancel_count > 0:
        reasons.append(f"有{profile.cancel_count}次取消记录，可能影响额度")
    if profile.overdue_count and profile.overdue_count > 0:
        reasons.append(f"有{profile.overdue_count}次逾期记录，额度已收紧")
    if not reasons:
        reasons.append("按时还款可提升额度")

    logs = (
        db.query(RiskLog)
        .filter(RiskLog.user_id == user.id)
        .order_by(RiskLog.created_at.desc())
        .limit(50)
        .all()
    )
    logs_out: List[Dict[str, Any]] = []
    for l in logs:
        logs_out.append(
            {
                "event_type": l.event_type,
                "risk_action": l.risk_action,
                "score_change": l.score_change,
                "old_score": l.old_score,
                "new_score": l.new_score,
                "old_risk_level": l.old_risk_level,
                "new_risk_level": l.new_risk_level,
                "reason": l.reason,
                "created_at": l.created_at.isoformat() if l.created_at else None,
            }
        )

    return ok(
        {
            "credit_score": profile.credit_score,
            "credit_level": profile.credit_level,
            "risk_level": profile.risk_level,
            "max_borrow_amount": float(profile.max_borrow_amount),
            "reasons": reasons,
            "logs": logs_out,
        }
    )


@router.post("/p2p/calculate")
def calculate(payload: CalculateRequest, user: User = Depends(get_current_user_tma), db: Session = Depends(get_db)):
    credit_level = _credit_level(user)
    if payload.term_days not in (7, 14, 30):
        raise ApiError(code="RISK_REJECTED", message="期限不支持", details={"term_days": payload.term_days})
    rate_percent = InterestCalculator.get_cut_interest_rate_percent(db, payload.term_days, credit_level)
    if rate_percent is None:
        raise ApiError(code="RISK_REJECTED", message="未找到利率配置")

    result = InterestCalculator.calc_cut_interest_loan(
        principal=payload.amount,
        term_days=payload.term_days,
        rate_percent=rate_percent,
    )

    return ok(
        {
            "amount": float(result.principal),
            "term_days": result.term_days,
            "rate_percent": float(result.rate_percent),
            "interest": float(result.interest),
            "received_amount": float(result.received_amount),
            "repay_amount": float(result.repay_amount),
            "mode": result.mode,
        }
    )


@router.post("/offers")
def create_offer_v1(
    payload: CreateOfferRequest,
    request: Request,
    user: User = Depends(get_current_user_tma),
    db: Session = Depends(get_db),
):
    ensure_profile_completed(user)

    if payload.term_days not in (7, 14, 30):
        raise ApiError(code="RISK_REJECTED", message="期限不支持", details={"term_days": payload.term_days})

    now = _utcnow()
    offers_24h_count = db.query(P2POffer).filter(
        P2POffer.borrower_id == user.id,
        P2POffer.created_at >= (now - timedelta(hours=24)),
    ).count()

    active_trade_statuses = ["matched", "lend_confirmed", "repayment_confirmed", "repaying", "dispute"]
    active_trades_count = (
        db.query(P2PTrade)
        .filter(P2PTrade.borrower_id == user.id, P2PTrade.status.in_(active_trade_statuses))
        .count()
    )

    decision = RiskEngine(RiskService(db)).check_create_offer(
        CreateOfferRiskInput(
            user_id=user.id,
            amount=payload.amount,
            term_days=payload.term_days,
            user_age_days=(now - _naive_utc(user.created_at)).days if user.created_at else 0,
            active_trades_count=active_trades_count,
            offers_24h_count=offers_24h_count,
        )
    )
    if not decision.allowed:
        raise ApiError(code="RISK_REJECTED", message="风控拒绝", details=json.loads(decision.json()), status_code=403)

    credit_level = _credit_level(user)
    rate_percent = InterestCalculator.get_cut_interest_rate_percent(db, payload.term_days, credit_level)
    if rate_percent is None:
        raise ApiError(code="RISK_REJECTED", message="未找到利率配置")

    calc = InterestCalculator.calc_cut_interest_loan(
        principal=payload.amount,
        term_days=payload.term_days,
        rate_percent=rate_percent,
    )

    offer = P2POffer(
        borrower_id=user.id,
        amount=payload.amount,
        term_days=payload.term_days,
        rate=float(rate_percent),
        fee=0.0,
        total_amount=float(calc.repay_amount),
        status="pending",
        can_bid=True,
        lender_selection="auto",
        note=payload.note or None,
    )
    db.add(offer)
    db.commit()
    db.refresh(offer)

    return ok(
        {
            "offer_id": str(offer.id),
            "status": offer.status,
            "amount": offer.amount,
            "term_days": offer.term_days,
            "rate_percent": float(rate_percent),
            "interest": float(calc.interest),
            "received_amount": float(calc.received_amount),
            "repay_amount": float(calc.repay_amount),
        }
    )


@router.get("/offers")
def list_offers_v1(
    tab: str = Query("recommended"),
    term_days: Optional[int] = Query(default=None),
    min_amount: Optional[float] = Query(default=None),
    max_amount: Optional[float] = Query(default=None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user_tma),
):
    now = _utcnow()
    q = db.query(P2POffer).filter(P2POffer.status == "pending")
    if term_days:
        q = q.filter(P2POffer.term_days == term_days)
    if min_amount is not None:
        q = q.filter(P2POffer.amount >= min_amount)
    if max_amount is not None:
        q = q.filter(P2POffer.amount <= max_amount)

    offers = q.order_by(P2POffer.created_at.desc()).limit(200).all()

    result: List[Dict[str, Any]] = []
    for o in offers:
        borrower = db.query(User).filter(User.id == o.borrower_id).first()
        if not borrower:
            continue

        completed_trades = db.query(P2PTrade).filter(P2PTrade.borrower_id == borrower.id, P2PTrade.status == "completed").count()
        overdue_count = RiskService(db).get_or_create_profile(borrower.id).overdue_count
        credit_level = _credit_level(borrower)
        rate_percent = float(o.rate)
        calc = InterestCalculator.calc_cut_interest_loan(principal=o.amount, term_days=o.term_days, rate_percent=o.rate)

        risk_level = "low"
        rp = RiskService(db).get_or_create_profile(borrower.id)
        if rp.risk_level in ("flagged", "restricted", "blocked"):
            risk_level = "high"
        elif rp.risk_level == "watch":
            risk_level = "mid"

        borrower_created_at = _naive_utc(borrower.created_at)
        item = {
            "id": str(o.id),
            "borrower_id": str(borrower.id),
            "amount": o.amount,
            "term_days": o.term_days,
            "rate_percent": rate_percent,
            "interest": float(calc.interest),
            "received_amount": float(calc.received_amount),
            "repay_amount": float(calc.repay_amount),
            "status": o.status,
            "borrower_credit_level": credit_level,
            "borrower_completed_trades": completed_trades,
            "borrower_overdue_count": overdue_count,
            "risk_level": risk_level,
            "is_new_user": (now - borrower_created_at).days < 7 if borrower_created_at else True,
            "created_at": o.created_at.isoformat() if o.created_at else None,
        }
        result.append(item)

    return ok(result)


@router.get("/offers/{offer_id}")
def get_offer_v1(offer_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user_tma)):
    try:
        oid = uuid.UUID(offer_id)
    except ValueError:
        raise ApiError(code="OFFER_NOT_FOUND", message="挂单不存在", status_code=404)

    o = db.query(P2POffer).filter(P2POffer.id == oid).first()
    if not o:
        raise ApiError(code="OFFER_NOT_FOUND", message="挂单不存在", status_code=404)

    borrower = db.query(User).filter(User.id == o.borrower_id).first()
    calc = InterestCalculator.calc_cut_interest_loan(principal=o.amount, term_days=o.term_days, rate_percent=o.rate)

    return ok(
        {
            "id": str(o.id),
            "borrower_id": str(o.borrower_id),
            "amount": o.amount,
            "term_days": o.term_days,
            "rate_percent": float(o.rate),
            "interest": float(calc.interest),
            "received_amount": float(calc.received_amount),
            "repay_amount": float(calc.repay_amount),
            "status": o.status,
            "note": o.note or "",
            "borrower_credit_level": _credit_level(borrower) if borrower else "C",
            "created_at": o.created_at.isoformat() if o.created_at else None,
        }
    )


@router.post("/offers/{offer_id}/cancel")
def cancel_offer_v1(offer_id: str, user: User = Depends(get_current_user_tma), db: Session = Depends(get_db)):
    try:
        oid = uuid.UUID(offer_id)
    except ValueError:
        raise ApiError(code="OFFER_NOT_FOUND", message="挂单不存在", status_code=404)

    offer = db.query(P2POffer).filter(P2POffer.id == oid).first()
    if not offer or str(offer.borrower_id) != str(user.id):
        raise ApiError(code="OFFER_NOT_FOUND", message="挂单不存在", status_code=404)
    if offer.status != "pending":
        raise ApiError(code="INVALID_STATUS", message="当前状态不可操作", details={"status": offer.status}, status_code=400)

    offer.status = "cancelled"
    db.commit()
    RiskEngine(RiskService(db)).on_offer_cancelled(user_id=user.id, matched=False)
    return ok({"offer_id": offer_id, "status": "cancelled"})


@router.post("/offers/{offer_id}/match")
def match_offer_v1(
    offer_id: str,
    payload: MatchOfferRequest,
    request: Request,
    user: User = Depends(get_current_user_tma),
    db: Session = Depends(get_db),
):
    ensure_profile_completed(user)

    if not payload.confirm_risk:
        raise ApiError(code="PERMISSION_DENIED", message="请先确认风险", status_code=400)

    try:
        oid = uuid.UUID(offer_id)
    except ValueError:
        raise ApiError(code="OFFER_NOT_FOUND", message="挂单不存在", status_code=404)

    offer = db.query(P2POffer).filter(P2POffer.id == oid).first()
    if not offer:
        raise ApiError(code="OFFER_NOT_FOUND", message="挂单不存在", status_code=404)
    if offer.status != "pending":
        raise ApiError(code="INVALID_STATUS", message="当前状态不可操作", details={"status": offer.status}, status_code=400)

    if str(offer.borrower_id) == str(user.id):
        raise ApiError(code="PERMISSION_DENIED", message="无权限", status_code=403)

    borrower = db.query(User).filter(User.id == offer.borrower_id).first()
    if borrower:
        if borrower.agent_id and user.agent_id and borrower.agent_id == user.agent_id:
            raise ApiError(code="RISK_REJECTED", message="关系风险：同业务员用户不可交易", status_code=403)
        if borrower.aba_account and user.aba_account and borrower.aba_account == user.aba_account:
            raise ApiError(code="RISK_REJECTED", message="关系风险：ABA 相同不可交易", status_code=403)
        if borrower.phone and user.phone and borrower.phone == user.phone:
            raise ApiError(code="RISK_REJECTED", message="关系风险：手机号相同不可交易", status_code=403)

        relation_service = RelationService(db)
        relation_service.build_relations_for_user(borrower.id)
        relation_service.build_relations_for_user(user.id)
        relation_score = relation_service.get_relation_score(borrower.id, user.id)
        if relation_score > 80:
            RiskService(db).create_manual_review_case(
                user_id=borrower.id,
                offer_id=offer.id,
                reason=f"high_relation_score:{relation_score}",
                risk_score=relation_score,
            )
            raise ApiError(code="MANUAL_REVIEW_REQUIRED", message="需要人工审核", status_code=403)

    active_trade_statuses = ["matched", "lend_confirmed", "repayment_confirmed", "repaying", "dispute"]
    active_lender_trades_count = (
        db.query(P2PTrade)
        .filter(P2PTrade.lender_id == user.id, P2PTrade.status.in_(active_trade_statuses))
        .count()
    )
    decision = RiskEngine(RiskService(db)).check_match_offer(
        MatchOfferRiskInput(lender_id=user.id, offer_id=offer.id, active_trades_count=active_lender_trades_count)
    )
    if not decision.allowed:
        raise ApiError(code="RISK_REJECTED", message="风控拒绝", details=json.loads(decision.json()), status_code=403)

    total_repayable = InterestCalculator.calculate_total_repayable_cut_interest(offer.amount)
    advance_deadline = InterestCalculator.calculate_advance_pay_deadline(_utcnow())

    trade = P2PTrade(
        offer_id=oid,
        borrower_id=offer.borrower_id,
        lender_id=user.id,
        amount=offer.amount,
        term_days=offer.term_days,
        rate=offer.rate,
        fee=offer.fee,
        total_repayable=total_repayable,
        status="matched",
        advance_pay_deadline=advance_deadline,
    )
    db.add(trade)
    db.flush()

    if borrower:
        RelationService(db).record_trade_relations(borrower.id, user.id, trade.id)

    schedules = InterestCalculator.generate_schedule_cut_interest(trade.id, offer.amount)
    now = _utcnow()
    days_per_period = offer.term_days // len(schedules) if schedules else offer.term_days
    for i, s in enumerate(schedules):
        due_at = now + timedelta(days=(days_per_period * (i + 1)))
        schedule = RepaymentSchedule(
            trade_id=trade.id,
            period=s["period"],
            due_at=due_at,
            principal=s["principal"],
            interest=s["interest"],
            total=s["total"],
            status="pending",
        )
        db.add(schedule)

    if borrower:
        borrower.active_loans += 1
    offer.status = "matched"
    db.commit()
    db.refresh(trade)

    return ok(
        {
            "trade_id": str(trade.id),
            "status": trade.status,
            "lend_deadline": trade.advance_pay_deadline.isoformat() if trade.advance_pay_deadline else None,
            "borrower_aba_account": borrower.aba_account if borrower else "",
            "borrower_aba_name": borrower.aba_name if borrower else "",
        }
    )


@router.get("/trades")
def list_trades_v1(
    status: str = Query("active"),
    role: str = Query("borrower"),
    user: User = Depends(get_current_user_tma),
    db: Session = Depends(get_db),
):
    q = db.query(P2PTrade)
    if role == "lender":
        q = q.filter(P2PTrade.lender_id == user.id)
    else:
        q = q.filter(P2PTrade.borrower_id == user.id)

    if status == "completed":
        q = q.filter(P2PTrade.status == "completed")
    elif status == "overdue":
        q = q.filter(P2PTrade.status == "overdue")
    elif status == "dispute":
        q = q.filter(P2PTrade.status == "dispute")
    else:
        q = q.filter(P2PTrade.status.in_(["matched", "lend_confirmed", "repayment_confirmed", "repaying"]))

    trades = q.order_by(P2PTrade.created_at.desc()).limit(200).all()
    data: List[Dict[str, Any]] = []
    for t in trades:
        calc = InterestCalculator.calc_cut_interest_loan(t.amount, t.term_days, t.rate)
        data.append(
            {
                "id": str(t.id),
                "offer_id": str(t.offer_id),
                "borrower_id": str(t.borrower_id),
                "lender_id": str(t.lender_id),
                "amount": t.amount,
                "term_days": t.term_days,
                "rate_percent": float(t.rate),
                "interest": float(calc.interest),
                "received_amount": float(calc.received_amount),
                "repay_amount": float(calc.repay_amount),
                "status": t.status,
                "fund_source": t.fund_source,
                "lend_deadline": t.advance_pay_deadline.isoformat() if t.advance_pay_deadline else None,
            }
        )
    return ok(data)


@router.get("/trades/{trade_id}")
def get_trade_v1(trade_id: str, user: User = Depends(get_current_user_tma), db: Session = Depends(get_db)):
    try:
        tid = uuid.UUID(trade_id)
    except ValueError:
        raise ApiError(code="TRADE_NOT_FOUND", message="交易不存在", status_code=404)

    trade = db.query(P2PTrade).filter(P2PTrade.id == tid).first()
    if not trade:
        raise ApiError(code="TRADE_NOT_FOUND", message="交易不存在", status_code=404)
    if str(trade.borrower_id) != str(user.id) and str(trade.lender_id) != str(user.id):
        raise ApiError(code="PERMISSION_DENIED", message="无权限", status_code=403)

    schedules = (
        db.query(RepaymentSchedule)
        .filter(RepaymentSchedule.trade_id == tid)
        .order_by(RepaymentSchedule.period.asc())
        .all()
    )
    schedules_out: List[Dict[str, Any]] = []
    for s in schedules:
        schedules_out.append(
            {
                "id": str(s.id),
                "period": s.period,
                "due_at": s.due_at.isoformat() if s.due_at else None,
                "principal": s.principal,
                "interest": s.interest,
                "total": s.total,
                "status": s.status,
                "paid_at": s.paid_at.isoformat() if getattr(s, "paid_at", None) else None,
                "proof_url": s.proof_url or "",
            }
        )

    calc = InterestCalculator.calc_cut_interest_loan(trade.amount, trade.term_days, trade.rate)

    borrower = db.query(User).filter(User.id == trade.borrower_id).first()

    return ok(
        {
            "id": str(trade.id),
            "offer_id": str(trade.offer_id),
            "borrower_id": str(trade.borrower_id),
            "lender_id": str(trade.lender_id),
            "amount": trade.amount,
            "rate_percent": float(trade.rate),
            "interest": float(calc.interest),
            "received_amount": float(calc.received_amount),
            "repay_amount": float(calc.repay_amount),
            "term_days": trade.term_days,
            "status": trade.status,
            "fund_source": trade.fund_source,
            "lend_deadline": trade.advance_pay_deadline.isoformat() if trade.advance_pay_deadline else None,
            "proof_url_from_lender": trade.proof_url_from_lender or "",
            "proof_url_from_borrower": trade.proof_url_from_borrower or "",
            "borrower_aba_account": borrower.aba_account if borrower else "",
            "borrower_aba_name": borrower.aba_name if borrower else "",
            "next_action": "",
            "repayment_schedules": schedules_out,
        }
    )


@router.post("/trades/{trade_id}/confirm-lend")
def confirm_lend_v1(
    trade_id: str,
    payload: ConfirmLendRequest,
    user: User = Depends(get_current_user_tma),
    db: Session = Depends(get_db),
):
    ensure_profile_completed(user)
    try:
        tid = uuid.UUID(trade_id)
    except ValueError:
        raise ApiError(code="TRADE_NOT_FOUND", message="交易不存在", status_code=404)
    trade = db.query(P2PTrade).filter(P2PTrade.id == tid).first()
    if not trade:
        raise ApiError(code="TRADE_NOT_FOUND", message="交易不存在", status_code=404)
    if str(trade.lender_id) != str(user.id):
        raise ApiError(code="PERMISSION_DENIED", message="无权限", status_code=403)
    if trade.status != "matched":
        raise ApiError(code="INVALID_STATUS", message="当前状态不可操作", details={"status": trade.status}, status_code=400)
    if trade.status == "dispute":
        raise ApiError(code="DISPUTE_LOCKED", message="交易争议中", status_code=400)

    trade.status = "lend_confirmed"
    trade.proof_url_from_lender = payload.proof_url
    trade.updated_at = _utcnow()
    db.commit()
    return ok({"trade_id": trade_id, "status": "lend_confirmed"})


@router.post("/trades/{trade_id}/confirm-receive")
def confirm_receive_v1(
    trade_id: str,
    payload: ConfirmReceiveRequest,
    user: User = Depends(get_current_user_tma),
    db: Session = Depends(get_db),
):
    ensure_profile_completed(user)
    try:
        tid = uuid.UUID(trade_id)
    except ValueError:
        raise ApiError(code="TRADE_NOT_FOUND", message="交易不存在", status_code=404)
    trade = db.query(P2PTrade).filter(P2PTrade.id == tid).first()
    if not trade:
        raise ApiError(code="TRADE_NOT_FOUND", message="交易不存在", status_code=404)
    if str(trade.borrower_id) != str(user.id):
        raise ApiError(code="PERMISSION_DENIED", message="无权限", status_code=403)
    if trade.status != "lend_confirmed":
        raise ApiError(code="INVALID_STATUS", message="当前状态不可操作", details={"status": trade.status}, status_code=400)
    if trade.status == "dispute":
        raise ApiError(code="DISPUTE_LOCKED", message="交易争议中", status_code=400)

    if not payload.confirmed:
        raise ApiError(code="PERMISSION_DENIED", message="无权限", status_code=400)

    trade.status = "repayment_confirmed"
    trade.updated_at = _utcnow()
    user.total_borrowed = round(user.total_borrowed + trade.amount, 2)
    db.commit()
    AgentService(db).create_borrow_commission_pending(trade)
    return ok({"trade_id": trade_id, "status": "repayment_confirmed"})


@router.post("/trades/{trade_id}/repay")
def repay_v1(
    trade_id: str,
    payload: RepayRequest,
    user: User = Depends(get_current_user_tma),
    db: Session = Depends(get_db),
):
    ensure_profile_completed(user)
    try:
        tid = uuid.UUID(trade_id)
        sid = uuid.UUID(payload.schedule_id)
    except ValueError:
        raise ApiError(code="TRADE_NOT_FOUND", message="交易不存在", status_code=404)

    trade = db.query(P2PTrade).filter(P2PTrade.id == tid).first()
    if not trade:
        raise ApiError(code="TRADE_NOT_FOUND", message="交易不存在", status_code=404)
    if str(trade.borrower_id) != str(user.id):
        raise ApiError(code="PERMISSION_DENIED", message="无权限", status_code=403)
    if trade.status not in ("repayment_confirmed", "repaying"):
        raise ApiError(code="INVALID_STATUS", message="当前状态不可操作", details={"status": trade.status}, status_code=400)
    if trade.status == "dispute":
        raise ApiError(code="DISPUTE_LOCKED", message="交易争议中", status_code=400)

    if trade.status == "repayment_confirmed":
        trade.status = "repaying"

    schedule = db.query(RepaymentSchedule).filter(RepaymentSchedule.id == sid, RepaymentSchedule.trade_id == tid).first()
    if not schedule:
        raise ApiError(code="TRADE_NOT_FOUND", message="还款计划不存在", status_code=404)

    schedule.status = "paid_pending"
    schedule.paid_at = _utcnow()
    schedule.proof_url = payload.proof_url
    trade.updated_at = _utcnow()
    db.commit()
    return ok({"trade_id": trade_id, "schedule_id": payload.schedule_id, "status": "paid_pending"})


@router.post("/trades/{trade_id}/confirm-repayment")
def confirm_repayment_v1(
    trade_id: str,
    payload: ConfirmRepaymentRequest,
    user: User = Depends(get_current_user_tma),
    db: Session = Depends(get_db),
):
    ensure_profile_completed(user)
    try:
        tid = uuid.UUID(trade_id)
        sid = uuid.UUID(payload.schedule_id)
    except ValueError:
        raise ApiError(code="TRADE_NOT_FOUND", message="交易不存在", status_code=404)

    trade = db.query(P2PTrade).filter(P2PTrade.id == tid).first()
    if not trade:
        raise ApiError(code="TRADE_NOT_FOUND", message="交易不存在", status_code=404)
    if str(trade.lender_id) != str(user.id):
        raise ApiError(code="PERMISSION_DENIED", message="无权限", status_code=403)
    if trade.status == "dispute":
        raise ApiError(code="DISPUTE_LOCKED", message="交易争议中", status_code=400)

    schedule = db.query(RepaymentSchedule).filter(RepaymentSchedule.id == sid, RepaymentSchedule.trade_id == tid).first()
    if not schedule:
        raise ApiError(code="TRADE_NOT_FOUND", message="还款计划不存在", status_code=404)
    if schedule.status != "paid_pending":
        raise ApiError(code="INVALID_STATUS", message="当前状态不可操作", details={"status": schedule.status}, status_code=400)

    if not payload.confirmed:
        raise ApiError(code="PERMISSION_DENIED", message="无权限", status_code=400)

    schedule.status = "paid"
    schedule.updated_at = _utcnow()

    borrower = db.query(User).filter(User.id == trade.borrower_id).first()
    if borrower:
        borrower.total_repaid = round(borrower.total_repaid + schedule.total, 2)

    all_schedules = db.query(RepaymentSchedule).filter(RepaymentSchedule.trade_id == tid).all()
    if all_schedules and all(s.status == "paid" for s in all_schedules):
        trade.status = "completed"
        trade.fee_status = "paid_to_platform"
        if borrower:
            borrower.active_loans = max(0, borrower.active_loans - 1)

        relation_service = RelationService(db)
        relation_service.build_relations_for_user(trade.borrower_id)
        relation_service.build_relations_for_user(trade.lender_id)
        if relation_service.can_increase_credit(trade.borrower_id, trade.lender_id):
            early = bool(schedule.due_at and schedule.paid_at and schedule.paid_at <= schedule.due_at)
            RiskEngine(RiskService(db)).on_repayment_paid(user_id=trade.borrower_id, trade_id=trade.id, early=early)

        AgentService(db).settle_commissions_for_trade(trade.id)

    db.commit()
    return ok({"trade_id": trade_id, "schedule_id": payload.schedule_id, "status": schedule.status})


@router.post("/uploads/proof")
async def upload_proof(
    purpose: str = Query(...),
    trade_id: str = Query(...),
    file: UploadFile = File(...),
    user: User = Depends(get_current_user_tma),
):
    if purpose not in ("lend", "repay", "dispute"):
        raise ApiError(code="UPLOAD_FAILED", message="上传失败", details={"purpose": purpose}, status_code=400)

    upload_dir = Path(os.getenv("UPLOAD_DIR", "./uploads/proofs"))
    upload_dir.mkdir(parents=True, exist_ok=True)
    suffix = Path(file.filename or "file").suffix
    name = f"{uuid.uuid4().hex}{suffix}"
    out_path = upload_dir / name
    content = await file.read()
    if not content:
        raise ApiError(code="UPLOAD_FAILED", message="上传失败", status_code=400)
    out_path.write_bytes(content)

    base_url = os.getenv("UPLOAD_BASE_URL", "")
    url = f"{base_url.rstrip('/')}/proofs/{name}" if base_url else f"/proofs/{name}"
    return ok({"url": url})


@router.post("/disputes")
def create_dispute_v1(
    payload: CreateDisputeInput,
    user: User = Depends(get_current_user_tma),
    db: Session = Depends(get_db),
):
    service = DisputeService(db)
    try:
        d = service.create_dispute(user.id, payload)
        return ok(
            {
                "id": d.id,
                "trade_id": str(d.trade_id),
                "status": d.status,
                "reason": d.reason,
                "dispute_type": d.dispute_type,
                "created_at": d.created_at.isoformat() if d.created_at else None,
                "updated_at": d.updated_at.isoformat() if d.updated_at else None,
            }
        )
    except Exception as e:
        raise ApiError(code="DISPUTE_LOCKED", message="交易争议中", details={"reason": str(e)}, status_code=400)


@router.get("/disputes")
def list_disputes_v1(
    trade_id: Optional[str] = Query(default=None),
    user: User = Depends(get_current_user_tma),
    db: Session = Depends(get_db),
):
    q = db.query(Dispute).filter((Dispute.borrower_id == user.id) | (Dispute.lender_id == user.id))
    if trade_id:
        try:
            tid = uuid.UUID(trade_id)
        except ValueError:
            raise ApiError(code="TRADE_NOT_FOUND", message="交易不存在", status_code=404)
        q = q.filter(Dispute.trade_id == tid)

    rows = q.order_by(Dispute.created_at.desc()).limit(50).all()
    return ok(
        [
            {
                "id": d.id,
                "trade_id": str(d.trade_id),
                "status": d.status,
                "reason": d.reason,
                "dispute_type": d.dispute_type,
                "created_at": d.created_at.isoformat() if d.created_at else None,
                "updated_at": d.updated_at.isoformat() if d.updated_at else None,
            }
            for d in rows
        ]
    )


@router.post("/disputes/{dispute_id}/evidence")
def add_dispute_evidence_v1(
    dispute_id: int,
    payload: AddEvidenceInput,
    user: User = Depends(get_current_user_tma),
    db: Session = Depends(get_db),
):
    service = DisputeService(db)
    payload.dispute_id = dispute_id
    ev = service.add_evidence(user.id, payload)
    return ok(
        {
            "id": ev.id,
            "dispute_id": ev.dispute_id,
            "evidence_type": ev.evidence_type,
            "file_url": ev.file_url or "",
            "text_note": ev.text_note or "",
            "created_at": ev.created_at.isoformat() if ev.created_at else None,
        }
    )


@router.get("/disputes/{dispute_id}")
def get_dispute_v1(dispute_id: int, user: User = Depends(get_current_user_tma), db: Session = Depends(get_db)):
    d = db.query(Dispute).filter(Dispute.id == dispute_id).first()
    if not d:
        raise ApiError(code="TRADE_NOT_FOUND", message="争议不存在", status_code=404)
    if str(d.borrower_id) != str(user.id) and str(d.lender_id) != str(user.id) and user.role != "admin":
        raise ApiError(code="PERMISSION_DENIED", message="无权限", status_code=403)
    return ok(
        {
            "id": d.id,
            "trade_id": str(d.trade_id),
            "status": d.status,
            "reason": d.reason,
            "dispute_type": d.dispute_type,
            "created_at": d.created_at.isoformat() if d.created_at else None,
            "updated_at": d.updated_at.isoformat() if d.updated_at else None,
        }
    )


@router.get("/notifications")
def list_notifications_v1(user: User = Depends(get_current_user_tma), db: Session = Depends(get_db)):
    rows = (
        db.query(Notification)
        .filter(Notification.user_id == user.id)
        .order_by(Notification.created_at.desc())
        .limit(50)
        .all()
    )
    return ok(
        [
            {
                "id": str(n.id),
                "type": n.type,
                "title": n.title,
                "body": n.body,
                "target_type": n.target_type,
                "target_id": n.target_id,
                "read": bool(n.read),
                "created_at": n.created_at.isoformat() if n.created_at else None,
            }
            for n in rows
        ]
    )


@router.get("/notifications/settings")
def get_notification_settings_v1(user: User = Depends(get_current_user_tma), db: Session = Depends(get_db)):
    row = get_or_create_notification_settings(db, user.id)
    return ok({"repayment_reminders": bool(row.repayment_reminders), "dispute_updates": bool(row.dispute_updates)})


@router.put("/notifications/settings")
def update_notification_settings_v1(
    payload: Dict[str, Any],
    user: User = Depends(get_current_user_tma),
    db: Session = Depends(get_db),
):
    row = get_or_create_notification_settings(db, user.id)
    if "repayment_reminders" in payload:
        row.repayment_reminders = bool(payload["repayment_reminders"])
    if "dispute_updates" in payload:
        row.dispute_updates = bool(payload["dispute_updates"])
    row.updated_at = _utcnow()
    db.commit()
    return ok({"repayment_reminders": bool(row.repayment_reminders), "dispute_updates": bool(row.dispute_updates)})


@router.post("/notifications/{notification_id}/read")
def mark_notification_read_v1(
    notification_id: str,
    user: User = Depends(get_current_user_tma),
    db: Session = Depends(get_db),
):
    try:
        nid = uuid.UUID(notification_id)
    except ValueError:
        raise ApiError(code="TRADE_NOT_FOUND", message="通知不存在", status_code=404)

    n = db.query(Notification).filter(Notification.id == nid).first()
    if not n or str(n.user_id) != str(user.id):
        raise ApiError(code="TRADE_NOT_FOUND", message="通知不存在", status_code=404)
    n.read = True
    db.commit()
    db.refresh(n)
    return ok({"id": str(n.id), "read": True})


@router.get("/announcements")
def list_announcements_v1(
    request: Request,
    user: User = Depends(get_current_user_tma),
    db: Session = Depends(get_db),
):
    lang = getattr(request.state, "lang", "cn")
    if lang not in ("km", "cn"):
        lang = "cn"
    website_lang = "km" if lang == "km" else "zh"
    now = datetime.now(timezone.utc)
    rows = (
        db.query(Announcement)
        .filter(Announcement.active.is_(True))
        .filter(Announcement.lang == website_lang)
        .filter((Announcement.starts_at.is_(None)) | (Announcement.starts_at <= now))
        .filter((Announcement.ends_at.is_(None)) | (Announcement.ends_at >= now))
        .order_by(Announcement.created_at.desc())
        .limit(10)
        .all()
    )
    return ok(
        [
            {
                "id": str(a.id),
                "lang": a.lang,
                "title": a.title,
                "body": a.body,
                "link_url": a.link_url,
                "created_at": a.created_at.isoformat() if a.created_at else None,
            }
            for a in rows
        ]
    )
