from __future__ import annotations

import os
import uuid
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from fastapi import APIRouter, Depends, File, Query, UploadFile
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api_v1.auth import ensure_profile_completed, get_current_user_tma
from app.api_v1.errors import ApiError
from app.api_v1.responses import ok
from app.api_v1.schemas import (
    CreateSalaryEmploymentRequest,
    CreateSalaryLoanOrderRequest,
    SalaryEmploymentOut,
    SalaryFactoryOut,
    SalaryLoanOrderDetailOut,
    SalaryLoanOrderOut,
    SalaryLoanRepaymentScheduleOut,
    SalaryLoanUploadProofResponse,
)
from app.database import get_db
from app.models.salary_employment import SalaryEmployment
from app.models.salary_factory import SalaryFactory
from app.models.salary_loan_order import SalaryLoanOrder
from app.models.salary_loan_repayment import SalaryLoanCollectionCase, SalaryLoanRepaymentProof, SalaryLoanRepaymentSchedule
from app.models.user import User


router = APIRouter(prefix="/api/v1/salary-loan", tags=["salary-loan"])


def _iso(dt: datetime | None) -> str | None:
    if not dt:
        return None
    try:
        return dt.isoformat()
    except Exception:
        return None


def _parse_ymd(v: str | None) -> date | None:
    if not v:
        return None
    try:
        y, m, d = v.split("-", 2)
        return date(int(y), int(m), int(d))
    except Exception:
        return None


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _days_between(a: date | None, b: date | None) -> int | None:
    if not a or not b:
        return None
    try:
        return (b - a).days
    except Exception:
        return None


def _risk_score(user: User, employment: SalaryEmployment, factory: SalaryFactory | None) -> tuple[int, list[str]]:
    score = 0
    reasons: list[str] = []

    if user.phone_verified_at:
        score += 10
    else:
        reasons.append("phone_unverified")

    if user.aba_account and user.aba_name:
        score += 10
    else:
        reasons.append("aba_missing")

    if factory:
        if factory.risk_level == "A":
            score += 15
        elif factory.risk_level == "B":
            score += 10
        elif factory.risk_level == "C":
            score += 5
        else:
            reasons.append("factory_high_risk")
    else:
        reasons.append("factory_unknown")

    if employment.join_date:
        days = _days_between(employment.join_date, date.today())
        if days is not None and days >= 180:
            score += 15
        elif days is not None and days >= 90:
            score += 10
        elif days is not None and days >= 30:
            score += 5
        else:
            reasons.append("short_tenure")
    else:
        reasons.append("join_date_missing")

    if employment.pay_cycle == "monthly":
        score += 10
    elif employment.pay_cycle == "biweekly":
        score += 5
    else:
        reasons.append("high_risk_pay_cycle")

    if employment.pay_method == "transfer":
        score += 5
    else:
        reasons.append("cash_pay")

    score = max(0, min(100, score))
    return score, reasons


def _suggest_pricing(*, principal: float, tenor_days: int, risk_score: int, factory: SalaryFactory | None) -> dict:
    base_fee_rate_map = {7: 0.10, 14: 0.12, 30: 0.15}
    base_interest_rate_map = {7: 0.0, 14: 0.01, 30: 0.02}

    fee_rate = float(base_fee_rate_map.get(int(tenor_days), 0.12))
    interest_rate = float(base_interest_rate_map.get(int(tenor_days), 0.01))

    if factory and float(factory.default_rate or 0) > 0:
        fee_rate = max(fee_rate, float(factory.default_rate or 0))

    if risk_score >= 55:
        fee_rate = max(0.02, fee_rate - 0.01)
        interest_rate = max(0.0, interest_rate - 0.005)
    elif risk_score < 45:
        fee_rate = min(0.25, fee_rate + 0.015)
        interest_rate = min(0.08, interest_rate + 0.01)

    fee = round(float(principal) * fee_rate, 2)
    interest = round(float(principal) * interest_rate, 2)
    disbursement_amount = round(max(0.0, float(principal) - fee), 2)
    total_due = round(float(principal) + fee + interest, 2)
    return {
        "fee_rate": round(fee_rate, 4),
        "interest_rate": round(interest_rate, 4),
        "fee": fee,
        "interest": interest,
        "disbursement_amount": disbursement_amount,
        "total_due": total_due,
    }


def _factory_out(f: SalaryFactory) -> SalaryFactoryOut:
    return SalaryFactoryOut(
        id=str(f.id),
        name=f.name,
        industry=f.industry,
        location=f.location,
        owner_type=f.owner_type,
        salary_cycle=f.salary_cycle,
        risk_level=f.risk_level,
        default_rate=float(f.default_rate or 0),
    )


def _employment_out(e: SalaryEmployment) -> SalaryEmploymentOut:
    return SalaryEmploymentOut(
        id=str(e.id),
        user_id=str(e.user_id),
        factory_id=str(e.factory_id),
        employee_no=e.employee_no or "",
        department=e.department or "",
        position=e.position or "",
        join_date=e.join_date.isoformat() if e.join_date else None,
        salary_amount=float(e.salary_amount) if e.salary_amount is not None else None,
        salary_pay_day=int(e.salary_pay_day) if e.salary_pay_day is not None else None,
        pay_cycle=e.pay_cycle,
        pay_method=e.pay_method,
        verify_status=e.verify_status,
        verify_notes=e.verify_notes or "",
        verified_at=_iso(getattr(e, "verified_at", None)),
        created_at=_iso(getattr(e, "created_at", None)),
    )


def _order_out(o: SalaryLoanOrder) -> SalaryLoanOrderOut:
    return SalaryLoanOrderOut(
        id=str(o.id),
        user_id=str(o.user_id),
        employment_id=str(o.employment_id),
        status=o.status,
        currency=o.currency,
        principal=float(o.principal),
        fee=float(o.fee),
        interest=float(o.interest),
        disbursement_amount=float(o.disbursement_amount),
        tenor_days=int(o.tenor_days),
        due_date=o.due_date.isoformat() if o.due_date else None,
        risk_score=o.risk_score,
        decision=o.decision,
        decision_notes=o.decision_notes or "",
        created_at=_iso(getattr(o, "created_at", None)),
        updated_at=_iso(getattr(o, "updated_at", None)),
    )


class CalculateSalaryLoanRequest(BaseModel):
    factory_id: str
    principal: float
    tenor_days: int
    join_date: str | None = None
    salary_amount: float | None = None
    salary_pay_day: int | None = None
    pay_cycle: str = "monthly"
    pay_method: str = "transfer"


@router.get("/factories")
def list_factories(user: User = Depends(get_current_user_tma), db: Session = Depends(get_db)):
    rows = db.query(SalaryFactory).filter(SalaryFactory.is_active == True).order_by(SalaryFactory.name.asc()).limit(500).all()
    return ok([_factory_out(f).dict() for f in rows])


@router.post("/employment")
def create_employment(
    payload: CreateSalaryEmploymentRequest,
    user: User = Depends(get_current_user_tma),
    db: Session = Depends(get_db),
):
    ensure_profile_completed(user)

    try:
        fid = uuid.UUID(payload.factory_id)
    except Exception:
        raise ApiError(code="INVALID_ID", message="参数不合法", status_code=400)

    factory = db.query(SalaryFactory).filter(SalaryFactory.id == fid).first()
    if not factory or not factory.is_active:
        raise ApiError(code="NOT_FOUND", message="未找到工厂", status_code=404)

    join_date = _parse_ymd(payload.join_date)
    e = SalaryEmployment(
        user_id=user.id,
        factory_id=fid,
        employee_no=(payload.employee_no or "").strip(),
        department=(payload.department or "").strip(),
        position=(payload.position or "").strip(),
        join_date=join_date,
        salary_amount=payload.salary_amount,
        salary_pay_day=payload.salary_pay_day,
        pay_cycle=payload.pay_cycle,
        pay_method=payload.pay_method,
        verify_status="pending",
    )
    db.add(e)
    db.commit()
    return ok(_employment_out(e).dict())


@router.post("/orders")
def create_salary_loan_order(
    payload: CreateSalaryLoanOrderRequest,
    user: User = Depends(get_current_user_tma),
    db: Session = Depends(get_db),
):
    ensure_profile_completed(user)

    if payload.tenor_days not in (7, 14, 30):
        raise ApiError(code="INVALID_TERM", message="期限不支持", status_code=400)

    try:
        eid = uuid.UUID(payload.employment_id)
    except Exception:
        raise ApiError(code="INVALID_ID", message="参数不合法", status_code=400)

    employment = db.query(SalaryEmployment).filter(SalaryEmployment.id == eid).first()
    if not employment or employment.user_id != user.id:
        raise ApiError(code="NOT_FOUND", message="未找到就业信息", status_code=404)

    factory = db.query(SalaryFactory).filter(SalaryFactory.id == employment.factory_id).first()

    risk, reasons = _risk_score(user, employment, factory)
    completed_count = (
        db.query(SalaryLoanOrder)
        .filter(SalaryLoanOrder.user_id == user.id)
        .filter(SalaryLoanOrder.status == "completed")
        .count()
    )
    if completed_count > 0:
        risk = min(100, risk + min(20, 5 * int(completed_count)))

    overdue_bad = (
        db.query(SalaryLoanCollectionCase)
        .join(SalaryLoanOrder, SalaryLoanOrder.id == SalaryLoanCollectionCase.order_id)
        .filter(SalaryLoanOrder.user_id == user.id)
        .filter(SalaryLoanCollectionCase.status == "open")
        .filter(SalaryLoanCollectionCase.dpd >= 7)
        .count()
    )
    if overdue_bad > 0:
        risk = max(0, risk - 20)
        reasons.append("recent_overdue")
    decision = "manual_review"
    status = "submitted"
    if employment.verify_status != "verified":
        status = "factory_pending"

    principal = float(payload.principal)
    if principal < 30 or principal > 5000:
        raise ApiError(code="INVALID_AMOUNT", message="金额不支持", status_code=400)

    due = (date.today() + timedelta(days=int(payload.tenor_days)))
    o = SalaryLoanOrder(
        user_id=user.id,
        employment_id=eid,
        status=status,
        principal=principal,
        fee=0,
        interest=0,
        disbursement_amount=0,
        tenor_days=int(payload.tenor_days),
        due_date=due,
        risk_score=risk,
        decision=decision,
        decision_notes=",".join(reasons)[:256],
    )
    db.add(o)
    db.commit()
    return ok(_order_out(o).dict())


@router.post("/calculate")
def calculate_salary_loan_quote(
    payload: CalculateSalaryLoanRequest,
    user: User = Depends(get_current_user_tma),
    db: Session = Depends(get_db),
):
    ensure_profile_completed(user)

    if payload.tenor_days not in (7, 14, 30):
        raise ApiError(code="INVALID_TERM", message="期限不支持", status_code=400)

    principal = float(payload.principal or 0)
    if principal < 30 or principal > 5000:
        raise ApiError(code="INVALID_AMOUNT", message="金额不支持", status_code=400)

    try:
        fid = uuid.UUID(payload.factory_id)
    except Exception:
        raise ApiError(code="INVALID_ID", message="参数不合法", status_code=400)

    factory = db.query(SalaryFactory).filter(SalaryFactory.id == fid).first()
    if not factory or not factory.is_active:
        raise ApiError(code="NOT_FOUND", message="未找到工厂", status_code=404)

    employment = SalaryEmployment(
        user_id=user.id,
        factory_id=fid,
        join_date=_parse_ymd(payload.join_date),
        salary_amount=payload.salary_amount,
        salary_pay_day=payload.salary_pay_day,
        pay_cycle=(payload.pay_cycle or "monthly").strip(),
        pay_method=(payload.pay_method or "transfer").strip(),
    )
    risk_score, reasons = _risk_score(user, employment, factory)
    pricing = _suggest_pricing(principal=principal, tenor_days=int(payload.tenor_days), risk_score=risk_score, factory=factory)
    return ok(
        {
            "principal": principal,
            "tenor_days": int(payload.tenor_days),
            "risk_score": risk_score,
            "reasons": reasons,
            **pricing,
            "note": "试算结果仅供参考，最终以审核通过后的费用为准",
        }
    )


@router.get("/orders/{order_id}")
def get_salary_loan_order(order_id: str, user: User = Depends(get_current_user_tma), db: Session = Depends(get_db)):
    try:
        oid = uuid.UUID(order_id)
    except Exception:
        raise ApiError(code="INVALID_ID", message="参数不合法", status_code=400)

    o = db.query(SalaryLoanOrder).filter(SalaryLoanOrder.id == oid).first()
    if not o or o.user_id != user.id:
        raise ApiError(code="NOT_FOUND", message="未找到订单", status_code=404)

    employment = db.query(SalaryEmployment).filter(SalaryEmployment.id == o.employment_id).first()
    if not employment:
        raise ApiError(code="NOT_FOUND", message="未找到就业信息", status_code=404)

    factory = db.query(SalaryFactory).filter(SalaryFactory.id == employment.factory_id).first()

    schedules = (
        db.query(SalaryLoanRepaymentSchedule)
        .filter(SalaryLoanRepaymentSchedule.order_id == o.id)
        .order_by(SalaryLoanRepaymentSchedule.installment_no.asc())
        .all()
    )
    out_schedules = [
        SalaryLoanRepaymentScheduleOut(
            id=str(s.id),
            order_id=str(s.order_id),
            installment_no=int(s.installment_no),
            due_date=s.due_date.isoformat(),
            due_amount=float(s.due_amount),
            paid_amount=float(s.paid_amount),
            status=s.status,
            paid_at=_iso(getattr(s, "paid_at", None)),
        )
        for s in schedules
    ]

    detail = SalaryLoanOrderDetailOut(
        order=_order_out(o),
        employment=_employment_out(employment),
        factory=_factory_out(factory).dict() if factory else None,
        schedules=out_schedules,
    )
    return ok(detail.dict())


@router.post("/orders/{order_id}/repayment-proof")
async def upload_repayment_proof(
    order_id: str,
    amount: float = Query(..., gt=0),
    note: str = Query(default=""),
    file: UploadFile = File(...),
    user: User = Depends(get_current_user_tma),
    db: Session = Depends(get_db),
):
    ensure_profile_completed(user)
    try:
        oid = uuid.UUID(order_id)
    except Exception:
        raise ApiError(code="INVALID_ID", message="参数不合法", status_code=400)

    o = db.query(SalaryLoanOrder).filter(SalaryLoanOrder.id == oid).first()
    if not o or o.user_id != user.id:
        raise ApiError(code="NOT_FOUND", message="未找到订单", status_code=404)

    upload_dir = Path(os.getenv("UPLOAD_DIR", "./uploads/proofs")) / "salary_loan"
    upload_dir.mkdir(parents=True, exist_ok=True)
    suffix = Path(file.filename or "file").suffix
    name = f"{uuid.uuid4().hex}{suffix}"
    out_path = upload_dir / name
    content = await file.read()
    if not content:
        raise ApiError(code="UPLOAD_FAILED", message="上传失败", status_code=400)
    out_path.write_bytes(content)

    base_url = os.getenv("UPLOAD_BASE_URL", "")
    url = f"{base_url.rstrip('/')}/proofs/salary_loan/{name}" if base_url else f"/proofs/salary_loan/{name}"

    proof = SalaryLoanRepaymentProof(
        order_id=o.id,
        user_id=user.id,
        file_path=url,
        note=(note or "")[:256],
        amount=float(amount),
        status="pending",
    )
    db.add(proof)
    db.commit()

    return ok(SalaryLoanUploadProofResponse(proof_id=str(proof.id), url=url).dict())
