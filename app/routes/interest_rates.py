"""
利率矩阵路由 — KhmerX ABA 微借贷
提供利率查询和管理端点
"""
import logging
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.database import get_db
from app.models.interest_rate import InterestRateMatrix
from app.models.user import User
from app.i18n import localize_trade, t

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/rates", tags=["rates"])


# ── Pydantic schemas ─────────────────────────────────────────────

class RateCreateRequest(BaseModel):
    term_days: int = Field(..., description="期限天数（7/14/30）")
    credit_level: str = Field(..., description="信用等级（A/B/C/D）")
    rate_percent: float = Field(..., gt=0, le=100, description="利率百分比")
    mode: str = Field(default="cut_interest")
    enabled: bool = Field(default=True)


class RateUpdateRequest(BaseModel):
    term_days: Optional[int] = None
    credit_level: Optional[str] = None
    rate_percent: Optional[float] = None
    mode: Optional[str] = None
    enabled: Optional[bool] = None


# ── Helper ────────────────────────────────────────────────────────

def _require_admin(user_id: str, db: Session):
    """校验管理员权限"""
    try:
        import uuid

        uid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user_id")
    user = db.query(User).filter(User.id == uid).first()
    if not user or user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


# ── 公开接口 ──────────────────────────────────────────────────────

@router.get("")
async def list_rates(
    request: Request,
    term_days: Optional[int] = Query(None, description="按期限筛选"),
    enabled_only: bool = Query(True, description="只显示启用的"),
    db: Session = Depends(get_db),
):
    """
    查询利率矩阵（公开）
    借款人/放款人均可查看
    """
    query = db.query(InterestRateMatrix)
    if enabled_only:
        query = query.filter(InterestRateMatrix.enabled == True)
    if term_days:
        query = query.filter(InterestRateMatrix.term_days == term_days)

    query = query.order_by(
        InterestRateMatrix.term_days,
        InterestRateMatrix.credit_level
    )
    rates = query.all()

    result = []
    for r in rates:
        result.append({
            "id": r.id,
            "term_days": r.term_days,
            "credit_level": r.credit_level,
            "rate_percent": float(r.rate_percent),
            "mode": r.mode,
            "enabled": r.enabled,
        })

    lang = getattr(request.state, "lang", "cn")
    return {
        "total": len(result),
        "rates": result,
        "_label": {
            "term": t("loan_term", lang),
            "rate": t("interest_rate", lang),
            "credit_score": t("credit_score", lang),
            "days": t("days", lang),
        },
        "lang": lang,
    }


@router.get("/calculate")
async def calculate_rate(
    request: Request,
    term_days: int = Query(..., description="期限天数（7/14/30）"),
    amount: float = Query(..., gt=0, description="借款金额"),
    credit_level: Optional[str] = Query(None, description="信用等级（A/B/C/D）"),
    credit_score: Optional[int] = Query(None, ge=0, le=999, description="信用分（可选，用于推导等级）"),
    db: Session = Depends(get_db),
):
    """
    根据信用分和期限计算利率和还款预估（公开）
    借款人可在创建挂单前预览
    """
    from app.services.interest_calculator import InterestCalculator

    if term_days not in (7, 14, 30):
        raise HTTPException(status_code=400, detail="term_days must be one of: 7, 14, 30")

    if credit_level is None:
        if credit_score is None:
            raise HTTPException(status_code=400, detail="credit_level or credit_score is required")
        credit_level = InterestCalculator.score_to_credit_level(credit_score)

    credit_level = credit_level.strip().upper()
    if credit_level not in ("A", "B", "C", "D"):
        raise HTTPException(status_code=400, detail="credit_level must be one of: A, B, C, D")

    rate_percent = InterestCalculator.get_cut_interest_rate_percent(db, term_days, credit_level)
    if rate_percent is None:
        raise HTTPException(status_code=400, detail="No matching rate for the given credit level and term")

    lang = getattr(request.state, "lang", "cn")

    result = InterestCalculator.calc_cut_interest_loan(amount, term_days, rate_percent)

    from app.i18n import fmt_amount, fmt_period, status_text

    return {
        "credit_level": credit_level,
        "term_days": term_days,
        "amount": amount,
        "rate_percent": float(result.rate_percent),
        "interest": float(result.interest),
        "received_amount": float(result.received_amount),
        "repay_amount": float(result.repay_amount),
        "real_rate_percent": float(result.real_rate_percent),
        "apr_percent": float(result.apr_percent),
        "mode": result.mode,
        "_labels": {
            "amount": t("loan_amount", lang),
            "rate": t("interest_rate", lang),
            "term": t("loan_term", lang),
            "period": t("period", lang),
            "principal": t("principal", lang),
            "interest": t("interest", lang),
            "credit_score": t("credit_score", lang),
        },
        "lang": lang,
    }


# ── 管理接口 ──────────────────────────────────────────────────────

@router.post("/admin")
async def create_rate(
    req: RateCreateRequest,
    user_id: str = Query(..., description="管理员 user UUID"),
    db: Session = Depends(get_db),
):
    """管理员创建利率记录"""
    _require_admin(user_id, db)

    if req.term_days not in (7, 14, 30):
        raise HTTPException(status_code=400, detail="term_days must be one of: 7, 14, 30")

    credit_level = (req.credit_level or "").strip().upper()
    if credit_level not in ("A", "B", "C", "D"):
        raise HTTPException(status_code=400, detail="credit_level must be one of: A, B, C, D")

    rate = InterestRateMatrix(
        term_days=req.term_days,
        credit_level=credit_level,
        rate_percent=req.rate_percent,
        mode=req.mode,
        enabled=req.enabled,
    )
    db.add(rate)
    db.commit()
    db.refresh(rate)

    logger.info(f"Rate created: {req.term_days}d level={rate.credit_level} rate={rate.rate_percent}% mode={rate.mode}")
    return {
        "id": rate.id,
        "term_days": rate.term_days,
        "credit_level": rate.credit_level,
        "rate_percent": float(rate.rate_percent),
        "mode": rate.mode,
        "enabled": rate.enabled,
    }


@router.put("/admin/{rate_id}")
async def update_rate(
    rate_id: str,
    req: RateUpdateRequest,
    user_id: str = Query(..., description="管理员 user UUID"),
    db: Session = Depends(get_db),
):
    """管理员更新利率记录"""
    _require_admin(user_id, db)

    try:
        rid = int(rate_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid rate_id")

    rate = db.query(InterestRateMatrix).filter(InterestRateMatrix.id == rid).first()
    if not rate:
        raise HTTPException(status_code=404, detail="Rate not found")

    if req.term_days is not None:
        rate.term_days = req.term_days
    if req.credit_level is not None:
        rate.credit_level = req.credit_level.strip().upper()
    if req.rate_percent is not None:
        rate.rate_percent = req.rate_percent
    if req.mode is not None:
        rate.mode = req.mode
    if req.enabled is not None:
        rate.enabled = req.enabled

    rate.updated_at = datetime.now()
    db.commit()
    db.refresh(rate)

    return {
        "id": rate.id,
        "term_days": rate.term_days,
        "credit_level": rate.credit_level,
        "rate_percent": float(rate.rate_percent),
        "mode": rate.mode,
        "enabled": rate.enabled,
    }


@router.delete("/admin/{rate_id}")
async def delete_rate(
    rate_id: str,
    user_id: str = Query(..., description="管理员 user UUID"),
    db: Session = Depends(get_db),
):
    """管理员删除利率记录（软删除：置为 disabled）"""
    _require_admin(user_id, db)

    try:
        rid = int(rate_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid rate_id")

    rate = db.query(InterestRateMatrix).filter(InterestRateMatrix.id == rid).first()
    if not rate:
        raise HTTPException(status_code=404, detail="Rate not found")

    rate.enabled = False
    rate.updated_at = datetime.now()
    db.commit()

    return {"status": "ok", "rate_id": rate_id, "enabled": False}
