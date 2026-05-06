"""
ABA 微借贷路由 — KhmerX P2P Lending
借款人挂单 → 平台自动匹配 → 放款人确认 → ABA 打款 → 凭证上传 → 还款
"""
import uuid
import logging
from datetime import datetime, timezone, timedelta
import json
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.database import get_db
from app.models.user import User
from app.models.p2p_offer import P2POffer
from app.models.p2p_trade import P2PTrade
from app.models.repayment_schedule import RepaymentSchedule
from app.models.interest_rate import InterestRateMatrix
from app.services.interest_calculator import InterestCalculator
from app.config import PLATFORM_FEE_RATE, ADVANCE_PAY_HOURS
from app.i18n import localize_offer, localize_trade, localize_schedule, fmt_amount, status_text, t
from app.risk.engine import RiskEngine
from app.risk.schemas import CreateOfferRiskInput, MatchOfferRiskInput
from app.risk.relations import RelationService
from app.risk.service import RiskService
from app.ops.service import AgentService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/p2p", tags=["p2p"])


# ── Pydantic schemas ─────────────────────────────────────────────

class CreateOfferRequest(BaseModel):
    user_id: str = Field(..., description="借款人 user UUID")
    amount: float = Field(..., gt=0, description="借款金额（美元）")
    term_days: int = Field(..., ge=7, le=30, description="借款天数（7/14/21/30）")
    note: str = Field(default="", description="备注")
    can_bid: bool = Field(default=False, description="是否可竞价")
    lender_selection: str = Field(default="auto", description="匹配方式: auto/specified")


class MatchOfferRequest(BaseModel):
    lender_id: str = Field(..., description="放款人 user UUID")


class ConfirmLendRequest(BaseModel):
    proof_url: str = Field(..., description="ABA 打款凭证 URL")


class ConfirmReceiveRequest(BaseModel):
    proof_url: str = Field(default="", description="收款确认凭证")


class RepayRequest(BaseModel):
    proof_url: str = Field(..., description="还款凭证 URL")


class CalculateLoanRequest(BaseModel):
    amount: float = Field(..., gt=0, description="借款金额（美元）")
    term_days: int = Field(..., description="借款天数（7/14/30）")
    credit_level: str = Field(..., description="信用等级（A/B/C/D）")


# ── Helper ────────────────────────────────────────────────────────

def _get_user(db: Session, user_id_str: str) -> User:
    """解析 user_id 并查询用户"""
    try:
        uid = uuid.UUID(user_id_str)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user_id")
    user = db.query(User).filter(User.id == uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def _ensure_profile_completed(user: User):
    if not user.phone_verified_at:
        raise HTTPException(status_code=403, detail="Please verify your phone number")
    if not (user.aba_account and user.aba_name):
        raise HTTPException(status_code=403, detail="Please bind your ABA account")


def _get_lang(req: Request, currency: str = "") -> tuple:
    """从 request 解析 lang 和 currency"""
    lang = getattr(req.state, "lang", "cn")
    if lang not in ("km", "cn"):
        lang = "cn"
    # 如果用户指定了币种
    currency = currency or ("khr" if lang == "km" else "usd")
    return lang, currency


@router.post("/calculate")
async def calculate_loan(
    req: CalculateLoanRequest,
    db: Session = Depends(get_db),
):
    credit_level = (req.credit_level or "").strip().upper()
    if credit_level not in ("A", "B", "C", "D"):
        raise HTTPException(status_code=400, detail="credit_level must be one of: A, B, C, D")

    if req.term_days not in (7, 14, 30):
        raise HTTPException(status_code=400, detail="term_days must be one of: 7, 14, 30")

    rate_percent = InterestCalculator.get_cut_interest_rate_percent(db, req.term_days, credit_level)
    if rate_percent is None:
        raise HTTPException(status_code=400, detail="No matching interest rate found")

    try:
        result = InterestCalculator.calc_cut_interest_loan(
            principal=req.amount,
            term_days=req.term_days,
            rate_percent=rate_percent,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "principal": float(result.principal),
        "term_days": result.term_days,
        "rate_percent": float(result.rate_percent),
        "interest": float(result.interest),
        "received_amount": float(result.received_amount),
        "repay_amount": float(result.repay_amount),
        "real_rate_percent": float(result.real_rate_percent),
        "apr_percent": float(result.apr_percent),
        "mode": result.mode,
    }


# ── 挂单管理 ─────────────────────────────────────────────────────

@router.post("/offers")
async def create_offer(
    req: CreateOfferRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    借款人创建挂单
    1. 查利率矩阵获取利率
    2. 计算平台费
    3. 创建挂单
    """
    borrower = _get_user(db, req.user_id)
    _ensure_profile_completed(borrower)

    now = datetime.now(timezone.utc)
    offers_24h_count = db.query(P2POffer).filter(
        P2POffer.borrower_id == borrower.id,
        P2POffer.created_at >= (now - timedelta(hours=24)),
    ).count()

    active_trade_statuses = ["matched", "lend_confirmed", "repayment_confirmed", "repaying", "dispute"]
    active_trades_count = db.query(P2PTrade).filter(
        P2PTrade.borrower_id == borrower.id,
        P2PTrade.status.in_(active_trade_statuses),
    ).count()

    user_age_days = (now - borrower.created_at).days if borrower.created_at else 0
    risk_engine = RiskEngine(RiskService(db))
    decision = risk_engine.check_create_offer(
        CreateOfferRiskInput(
            user_id=borrower.id,
            amount=req.amount,
            term_days=req.term_days,
            user_age_days=user_age_days,
            active_trades_count=active_trades_count,
            offers_24h_count=offers_24h_count,
        )
    )

    if not decision.allowed:
        raise HTTPException(status_code=403, detail=json.loads(decision.json()))

    # 验证 term_days
    if req.term_days not in (7, 14, 30):
        raise HTTPException(
            status_code=400,
            detail="term_days must be one of: 7, 14, 30"
        )

    # 验证 lender_selection
    if req.lender_selection not in ("auto", "specified"):
        raise HTTPException(status_code=400, detail="lender_selection must be 'auto' or 'specified'")

    credit_level = InterestCalculator.score_to_credit_level(borrower.credit_score)
    if credit_level == "E":
        raise HTTPException(status_code=403, detail="Credit level E is not allowed to borrow")

    rate_percent = InterestCalculator.get_cut_interest_rate_percent(db, req.term_days, credit_level)
    if rate_percent is None:
        raise HTTPException(status_code=400, detail="No matching interest rate found")

    # 计算平台费
    fee = InterestCalculator.calculate_fee(req.amount)

    # 总金额 = 本金 + 平台费
    total_amount = round(req.amount + fee, 2)

    # 创建挂单
    offer = P2POffer(
        borrower_id=borrower.id,
        amount=req.amount,
        term_days=req.term_days,
        rate=float(rate_percent),
        fee=fee,
        total_amount=total_amount,
        status="pending",
        can_bid=req.can_bid,
        lender_selection=req.lender_selection,
        note=req.note or None,
    )
    db.add(offer)
    db.commit()
    db.refresh(offer)

    logger.info(
        f"P2P offer created: {offer.id} - ${req.amount} "
        f"{req.term_days}d @ {offer.rate}% fee=${fee}"
    )

    lang, currency = _get_lang(request)

    return localize_offer({
        "id": str(offer.id),
        "borrower_id": str(offer.borrower_id),
        "amount": offer.amount,
        "term_days": offer.term_days,
        "rate": offer.rate,
        "fee": offer.fee,
        "total_amount": offer.total_amount,
        "status": offer.status,
        "can_bid": offer.can_bid,
        "lender_selection": offer.lender_selection,
        "note": offer.note or "",
        "created_at": offer.created_at.isoformat(),
    }, lang, currency)


@router.get("/offers")
async def list_offers(
    request: Request,
    status: str = Query("pending", description="筛选状态"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """
    查看所有可匹配的挂单（支持分页、筛选）
    """
    allowed = [s.strip() for s in status.split(",") if s.strip()]
    query = db.query(P2POffer).filter(P2POffer.status.in_(allowed))
    query = query.order_by(P2POffer.created_at.desc())
    query = query.offset(skip).limit(limit)
    offers = query.all()

    total = db.query(P2POffer).filter(P2POffer.status.in_(allowed)).count()

    lang, currency = _get_lang(request)

    result = []
    for o in offers:
        borrower = db.query(User).filter(User.id == o.borrower_id).first()
        result.append(localize_offer({
            "id": str(o.id),
            "borrower_id": str(o.borrower_id),
            "borrower_name": borrower.name if borrower else "",
            "amount": o.amount,
            "term_days": o.term_days,
            "rate": o.rate,
            "fee": o.fee,
            "total_amount": o.total_amount,
            "status": o.status,
            "can_bid": o.can_bid,
            "lender_selection": o.lender_selection,
            "note": o.note or "",
            "created_at": o.created_at.isoformat(),
        }, lang, currency))

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "offers": result,
        "lang": lang,
    }


@router.get("/offers/my")
async def list_my_offers(
    request: Request,
    user_id: str = Query(..., description="用户 UUID"),
    db: Session = Depends(get_db),
):
    """我的挂单"""
    user = _get_user(db, user_id)
    offers = db.query(P2POffer).filter(
        P2POffer.borrower_id == user.id
    ).order_by(P2POffer.created_at.desc()).all()

    lang, currency = _get_lang(request)

    result = []
    for o in offers:
        result.append(localize_offer({
            "id": str(o.id),
            "amount": o.amount,
            "term_days": o.term_days,
            "rate": o.rate,
            "fee": o.fee,
            "total_amount": o.total_amount,
            "status": o.status,
            "can_bid": o.can_bid,
            "note": o.note or "",
            "created_at": o.created_at.isoformat(),
        }, lang, currency))
    return result


@router.post("/offers/{offer_id}/cancel")
async def cancel_offer(
    offer_id: str,
    user_id: str = Query(..., description="借款人 UUID"),
    db: Session = Depends(get_db),
):
    """取消挂单（仅限 pending 状态）"""
    try:
        oid = uuid.UUID(offer_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid offer_id")

    user = _get_user(db, user_id)
    offer = db.query(P2POffer).filter(P2POffer.id == oid).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    if str(offer.borrower_id) != str(user.id):
        raise HTTPException(status_code=403, detail="Only the borrower can cancel this offer")
    if offer.status != "pending":
        raise HTTPException(status_code=400, detail=f"Cannot cancel offer with status {offer.status}")

    offer.status = "cancelled"
    db.commit()

    risk_engine = RiskEngine(RiskService(db))
    risk_engine.on_offer_cancelled(user_id=user.id, matched=False)
    return {"status": "ok", "offer_id": offer_id, "new_status": "cancelled"}


# ── 匹配与交易 ─────────────────────────────────────────────────

@router.post("/offers/{offer_id}/match")
async def match_offer(
    offer_id: str,
    req: MatchOfferRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    放款人接单匹配
    1. 校验挂单状态
    2. 校验放款人不是借款人本人
    3. 计算总应还金额和还款计划
    4. 创建交易记录
    5. 更新挂单状态
    """
    try:
        oid = uuid.UUID(offer_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid offer_id")

    lender = _get_user(db, req.lender_id)
    _ensure_profile_completed(lender)

    offer = db.query(P2POffer).filter(P2POffer.id == oid).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    if offer.status != "pending":
        raise HTTPException(status_code=400, detail=f"Offer status is {offer.status}, cannot match")

    # 放款人不能是自己的挂单
    if str(offer.borrower_id) == str(lender.id):
        raise HTTPException(status_code=400, detail="Cannot match your own offer")

    borrower = db.query(User).filter(User.id == offer.borrower_id).first()
    if borrower:
        if borrower.agent_id and lender.agent_id and borrower.agent_id == lender.agent_id:
            raise HTTPException(status_code=403, detail="Same agent users cannot trade")
        if borrower.aba_account and lender.aba_account and borrower.aba_account == lender.aba_account:
            raise HTTPException(status_code=403, detail="Borrower and lender ABA account cannot be the same")
        if borrower.phone and lender.phone and borrower.phone == lender.phone:
            raise HTTPException(status_code=403, detail="Borrower and lender phone cannot be the same")

        relation_service = RelationService(db)
        relation_service.build_relations_for_user(borrower.id)
        relation_service.build_relations_for_user(lender.id)
        relation_score = relation_service.get_relation_score(borrower.id, lender.id)
        if relation_score > 80:
            RiskService(db).create_manual_review_case(
                user_id=borrower.id,
                offer_id=offer.id,
                reason=f"high_relation_score:{relation_score}",
                risk_score=relation_score,
            )
            raise HTTPException(status_code=403, detail="High risk relation between borrower and lender")

    active_trade_statuses = ["matched", "lend_confirmed", "repayment_confirmed", "repaying", "dispute"]
    active_lender_trades_count = db.query(P2PTrade).filter(
        P2PTrade.lender_id == lender.id,
        P2PTrade.status.in_(active_trade_statuses),
    ).count()

    risk_engine = RiskEngine(RiskService(db))
    decision = risk_engine.check_match_offer(
        MatchOfferRiskInput(
            lender_id=lender.id,
            offer_id=offer.id,
            active_trades_count=active_lender_trades_count,
        )
    )
    if not decision.allowed:
        raise HTTPException(status_code=403, detail=json.loads(decision.json()))

    total_repayable = InterestCalculator.calculate_total_repayable_cut_interest(offer.amount)

    advance_deadline = InterestCalculator.calculate_advance_pay_deadline(
        datetime.now(timezone.utc)
    )

    # 创建交易
    trade = P2PTrade(
        offer_id=oid,
        borrower_id=offer.borrower_id,
        lender_id=lender.id,
        amount=offer.amount,
        term_days=offer.term_days,
        rate=offer.rate,
        fee=offer.fee,
        total_repayable=total_repayable,
        status="matched",
        advance_pay_deadline=advance_deadline,
    )
    db.add(trade)
    db.flush()  # 获取 trade.id

    if borrower:
        relation_service.record_trade_relations(borrower.id, lender.id, trade.id)

    # 生成还款计划
    schedules = InterestCalculator.generate_schedule_cut_interest(trade.id, offer.amount)

    now = datetime.now(timezone.utc)
    days_per_period = offer.term_days // len(schedules) if schedules else offer.term_days

    for i, s in enumerate(schedules):
        # 计算每期到期时间
        period_days = days_per_period
        due_at = now + timedelta(days=period_days * (i + 1))

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

    # 更新借款人活跃借款数
    borrower = db.query(User).filter(User.id == offer.borrower_id).first()
    if borrower:
        borrower.active_loans += 1

    # 更新挂单状态
    offer.status = "matched"

    db.commit()
    db.refresh(trade)

    logger.info(
        f"P2P trade matched: {trade.id} - ${offer.amount} "
        f"borrower={trade.borrower_id} lender={trade.lender_id}"
    )

    lang, currency = _get_lang(request)

    return localize_trade({
        "id": str(trade.id),
        "offer_id": str(trade.offer_id),
        "borrower_id": str(trade.borrower_id),
        "lender_id": str(trade.lender_id),
        "amount": trade.amount,
        "term_days": trade.term_days,
        "rate": trade.rate,
        "fee": trade.fee,
        "total_repayable": trade.total_repayable,
        "status": trade.status,
        "advance_pay_deadline": trade.advance_pay_deadline.isoformat() if trade.advance_pay_deadline else None,
        "created_at": trade.created_at.isoformat(),
    }, lang, currency)


@router.post("/trades/{trade_id}/confirm-lend")
async def confirm_lend(
    trade_id: str,
    req: ConfirmLendRequest,
    request: Request,
    user_id: str = Query(..., description="放款人 UUID"),
    db: Session = Depends(get_db),
):
    """
    放款人确认已 ABA 打款（上传凭证）
    status → lend_confirmed
    """
    try:
        tid = uuid.UUID(trade_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid trade_id")

    lender = _get_user(db, user_id)

    trade = db.query(P2PTrade).filter(P2PTrade.id == tid).first()
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    if str(trade.lender_id) != str(lender.id):
        raise HTTPException(status_code=403, detail="Only the lender can confirm lending")
    if trade.status != "matched":
        raise HTTPException(status_code=400, detail=f"Trade status is {trade.status}, expected 'matched'")

    trade.status = "lend_confirmed"
    trade.proof_url_from_lender = req.proof_url
    trade.updated_at = datetime.now(timezone.utc)
    db.commit()

    logger.info(f"Trade {trade_id}: lender confirmed payment, proof={req.proof_url}")
    lang, currency = _get_lang(request)
    return {
        "status": "ok",
        "trade_id": trade_id,
        "new_status": "lend_confirmed",
        "proof_url": req.proof_url,
        "_label": {
            "status": status_text("pending", lang),
            "proof_upload": t("proof_upload", lang),
        },
        "lang": lang,
    }


@router.post("/trades/{trade_id}/confirm-receive")
async def confirm_receive(
    trade_id: str,
    req: ConfirmReceiveRequest,
    request: Request,
    user_id: str = Query(..., description="借款人 UUID"),
    db: Session = Depends(get_db),
):
    """
    借款人确认收到款（或平台确认）
    status → repayment_confirmed
    """
    try:
        tid = uuid.UUID(trade_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid trade_id")

    borrower = _get_user(db, user_id)

    trade = db.query(P2PTrade).filter(P2PTrade.id == tid).first()
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    if str(trade.borrower_id) != str(borrower.id):
        raise HTTPException(status_code=403, detail="Only the borrower can confirm receipt")
    if trade.status != "lend_confirmed":
        raise HTTPException(status_code=400, detail=f"Trade status is {trade.status}, expected 'lend_confirmed'")

    if trade.status == "dispute":
        raise HTTPException(status_code=400, detail="Trade is in dispute")

    trade.status = "repayment_confirmed"
    trade.proof_url_from_borrower = req.proof_url
    trade.updated_at = datetime.now(timezone.utc)

    # 更新借款人的 total_borrowed
    borrower.total_borrowed = round(borrower.total_borrowed + trade.amount, 2)

    db.commit()

    AgentService(db).create_borrow_commission_pending(trade)

    logger.info(f"Trade {trade_id}: borrower confirmed receipt")
    return {
        "status": "ok",
        "trade_id": trade_id,
        "new_status": "repayment_confirmed",
        "proof_url": req.proof_url,
    }


@router.post("/trades/{trade_id}/repay")
async def repay_trade(
    trade_id: str,
    req: RepayRequest,
    request: Request,
    user_id: str = Query(..., description="借款人 UUID"),
    period: int = Query(..., ge=1, description="第几期还款"),
    db: Session = Depends(get_db),
):
    """
    借款人发起指定期数的还款（上传还款凭证）
    标记载为 paid
    """
    try:
        tid = uuid.UUID(trade_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid trade_id")

    borrower = _get_user(db, user_id)

    trade = db.query(P2PTrade).filter(P2PTrade.id == tid).first()
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    if str(trade.borrower_id) != str(borrower.id):
        raise HTTPException(status_code=403, detail="Only the borrower can repay")

    if trade.status not in ("repayment_confirmed", "repaying"):
        raise HTTPException(
            status_code=400,
            detail=f"Trade status is {trade.status}, expected 'repayment_confirmed' or 'repaying'"
        )

    if trade.status == "dispute":
        raise HTTPException(status_code=400, detail="Trade is in dispute")

    # 如果第一笔还款，改为 repaying 状态
    if trade.status == "repayment_confirmed":
        trade.status = "repaying"

    # 查还款计划
    schedule = db.query(RepaymentSchedule).filter(
        RepaymentSchedule.trade_id == tid,
        RepaymentSchedule.period == period,
    ).first()

    if not schedule:
        raise HTTPException(status_code=404, detail=f"Schedule period {period} not found")
    if schedule.status in ("paid", "paid_pending"):
        raise HTTPException(status_code=400, detail=f"Schedule period {period} is already paid")
    if schedule.status == "overdue":
        # 允许逾期还款
        pass

    schedule.status = "paid_pending"
    schedule.paid_at = datetime.now(timezone.utc)
    schedule.proof_url = req.proof_url

    trade.updated_at = datetime.now(timezone.utc)
    db.commit()

    logger.info(
        f"Trade {trade_id}: period {period} repaid ${schedule.total}, "
        f"trade status={trade.status}"
    )

    return {
        "status": "ok",
        "trade_id": trade_id,
        "period": period,
        "amount_paid": schedule.total,
        "proof_url": req.proof_url,
        "schedule_status": "paid_pending",
        "trade_status": trade.status,
        "paid_at": schedule.paid_at.isoformat() if schedule.paid_at else None,
    }


@router.post("/trades/{trade_id}/confirm-repay")
async def confirm_repay(
    trade_id: str,
    request: Request,
    user_id: str = Query(..., description="放款人 UUID"),
    period: int = Query(..., ge=1, description="第几期还款"),
    db: Session = Depends(get_db),
):
    """
    放款人确认收到还款
    """
    try:
        tid = uuid.UUID(trade_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid trade_id")

    lender = _get_user(db, user_id)

    trade = db.query(P2PTrade).filter(P2PTrade.id == tid).first()
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    if str(trade.lender_id) != str(lender.id):
        raise HTTPException(status_code=403, detail="Only the lender can confirm repayment")

    if trade.status == "dispute":
        raise HTTPException(status_code=400, detail="Trade is in dispute")

    schedule = db.query(RepaymentSchedule).filter(
        RepaymentSchedule.trade_id == tid,
        RepaymentSchedule.period == period,
    ).first()

    if not schedule:
        raise HTTPException(status_code=404, detail=f"Schedule period {period} not found")
    if schedule.status != "paid_pending":
        raise HTTPException(status_code=400, detail=f"Schedule period {period} is not pending confirmation")

    schedule.status = "paid"
    schedule.updated_at = datetime.now(timezone.utc)

    borrower = db.query(User).filter(User.id == trade.borrower_id).first()
    if borrower:
        borrower.total_repaid = round(borrower.total_repaid + schedule.total, 2)

    all_schedules = db.query(RepaymentSchedule).filter(RepaymentSchedule.trade_id == tid).all()
    all_paid = all(s.status == "paid" for s in all_schedules)
    if all_paid:
        trade.status = "completed"
        trade.fee_status = "paid_to_platform"
        if borrower:
            borrower.active_loans = max(0, borrower.active_loans - 1)

    relation_service = RelationService(db)
    relation_service.build_relations_for_user(trade.borrower_id)
    relation_service.build_relations_for_user(trade.lender_id)
    if relation_service.can_increase_credit(trade.borrower_id, trade.lender_id):
        early = schedule.due_at and schedule.paid_at and schedule.paid_at <= schedule.due_at
        RiskEngine(RiskService(db)).on_repayment_paid(
            user_id=trade.borrower_id,
            trade_id=trade.id,
            early=bool(early),
        )

    if trade.status == "completed":
        AgentService(db).settle_commissions_for_trade(trade.id)

    db.commit()

    # 放款人确认 — 已通过 schedule.status=paid 表示
    # 这里的确认是放款人确认收到款
    logger.info(f"Trade {trade_id}: lender confirmed receipt of period {period} repayment")

    return {
        "status": "ok",
        "trade_id": trade_id,
        "period": period,
        "amount": schedule.total,
        "confirmed": True,
    }


# ── 查询 ──────────────────────────────────────────────────────────

@router.get("/trades")
async def list_trades(
    request: Request,
    user_id: str = Query(..., description="用户 UUID"),
    role: str = Query("borrower", description="角色: borrower / lender"),
    status: str = Query("", description="筛选状态"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """查看我的交易（支持 filter by role）"""
    user = _get_user(db, user_id)

    query = db.query(P2PTrade)
    if role == "borrower":
        query = query.filter(P2PTrade.borrower_id == user.id)
    else:
        query = query.filter(P2PTrade.lender_id == user.id)

    if status:
        query = query.filter(P2PTrade.status == status)

    total = query.count()
    query = query.order_by(P2PTrade.created_at.desc()).offset(skip).limit(limit)
    trades = query.all()

    lang, currency = _get_lang(request)

    result = []
    for t in trades:
        offer = db.query(P2POffer).filter(P2POffer.id == t.offer_id).first()
        result.append(localize_trade({
            "id": str(t.id),
            "offer_id": str(t.offer_id),
            "borrower_id": str(t.borrower_id),
            "lender_id": str(t.lender_id),
            "amount": t.amount,
            "term_days": t.term_days,
            "rate": t.rate,
            "fee": t.fee,
            "fee_status": t.fee_status,
            "total_repayable": t.total_repayable,
            "status": t.status,
            "advance_pay_deadline": t.advance_pay_deadline.isoformat() if t.advance_pay_deadline else None,
            "note": offer.note if offer else "",
            "created_at": t.created_at.isoformat(),
            "updated_at": t.updated_at.isoformat(),
        }, lang, currency))
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "trades": result,
        "lang": lang,
    }


@router.get("/trades/my")
async def list_my_trades(
    request: Request,
    user_id: str = Query(..., description="用户 UUID"),
    db: Session = Depends(get_db),
):
    """我的所有交易（同时作为 borrower 和 lender）"""
    user = _get_user(db, user_id)

    as_borrower = db.query(P2PTrade).filter(
        P2PTrade.borrower_id == user.id
    ).order_by(P2PTrade.created_at.desc()).all()

    as_lender = db.query(P2PTrade).filter(
        P2PTrade.lender_id == user.id
    ).order_by(P2PTrade.created_at.desc()).all()

    lang, currency = _get_lang(request)

    def _format_trade(t):
        offer = db.query(P2POffer).filter(P2POffer.id == t.offer_id).first()
        return localize_trade({
            "id": str(t.id),
            "offer_id": str(t.offer_id),
            "borrower_id": str(t.borrower_id),
            "lender_id": str(t.lender_id),
            "amount": t.amount,
            "term_days": t.term_days,
            "rate": t.rate,
            "fee": t.fee,
            "fee_status": t.fee_status,
            "total_repayable": t.total_repayable,
            "status": t.status,
            "advance_pay_deadline": t.advance_pay_deadline.isoformat() if t.advance_pay_deadline else None,
            "note": offer.note if offer else "",
            "created_at": t.created_at.isoformat(),
            "updated_at": t.updated_at.isoformat(),
        }, lang, currency)

    return {
        "as_borrower": [_format_trade(t) for t in as_borrower],
        "as_lender": [_format_trade(t) for t in as_lender],
        "lang": lang,
    }


@router.get("/trades/{trade_id}/repayments")
async def get_trade_repayments(
    trade_id: str,
    request: Request,
    db: Session = Depends(get_db),
):
    """查看某笔交易的还款计划表"""
    try:
        tid = uuid.UUID(trade_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid trade_id")

    trade = db.query(P2PTrade).filter(P2PTrade.id == tid).first()
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")

    schedules = db.query(RepaymentSchedule).filter(
        RepaymentSchedule.trade_id == tid
    ).order_by(RepaymentSchedule.period).all()

    lang, currency = _get_lang(request)

    result = []
    for s in schedules:
        result.append({
            "id": str(s.id),
            "period": s.period,
            "due_at": s.due_at.isoformat() if s.due_at else None,
            "principal": s.principal,
            "interest": s.interest,
            "total": s.total,
            "status": s.status,
            "paid_at": s.paid_at.isoformat() if s.paid_at else None,
            "proof_url": s.proof_url or "",
        })

    return {
        "trade_id": trade_id,
        "amount": trade.amount,
        "rate": trade.rate,
        "term_days": trade.term_days,
        "total_repayable": trade.total_repayable,
        "schedules": localize_schedule(result, lang, currency),
        "_labels": localize_trade({}, lang, currency).get("_label", {}),
        "lang": lang,
    }


@router.get("/trades/{trade_id}")
async def get_trade(
    trade_id: str,
    request: Request,
    db: Session = Depends(get_db),
):
    """交易详情"""
    try:
        tid = uuid.UUID(trade_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid trade_id")

    trade = db.query(P2PTrade).filter(P2PTrade.id == tid).first()
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")

    offer = db.query(P2POffer).filter(P2POffer.id == trade.offer_id).first()

    lang, currency = _get_lang(request)

    return localize_trade({
        "id": str(trade.id),
        "offer_id": str(trade.offer_id),
        "borrower_id": str(trade.borrower_id),
        "lender_id": str(trade.lender_id),
        "amount": trade.amount,
        "term_days": trade.term_days,
        "rate": trade.rate,
        "fee": trade.fee,
        "fee_status": trade.fee_status,
        "total_repayable": trade.total_repayable,
        "status": trade.status,
        "proof_url_from_lender": trade.proof_url_from_lender or "",
        "proof_url_from_borrower": trade.proof_url_from_borrower or "",
        "advance_pay_deadline": trade.advance_pay_deadline.isoformat() if trade.advance_pay_deadline else None,
        "note": offer.note if offer else "",
        "created_at": trade.created_at.isoformat(),
        "updated_at": trade.updated_at.isoformat(),
    }, lang, currency)


print("=== Task 3.1 done ===")
