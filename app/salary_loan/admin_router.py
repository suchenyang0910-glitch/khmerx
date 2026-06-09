from __future__ import annotations

import uuid
from datetime import date, datetime, timezone

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.admin.auth import AdminPrincipal, get_current_admin
from app.api_v1.errors import ApiError
from app.database import get_db
from app.models.salary_employment import SalaryEmployment
from app.models.salary_factory import SalaryFactory
from app.models.salary_loan_order import SalaryLoanOrder
from app.models.salary_loan_repayment import (
    SalaryLoanCollectionCase,
    SalaryLoanCollectionEvent,
    SalaryLoanLedgerEntry,
    SalaryLoanRepaymentProof,
    SalaryLoanRepaymentSchedule,
)
from app.services.salary_loan_payments import apply_repayment


router = APIRouter(prefix="/api/admin/salary-loan", tags=["admin-salary-loan"])


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _parse_uuid(v: str) -> uuid.UUID:
    try:
        return uuid.UUID(v)
    except Exception:
        raise ApiError(code="INVALID_ID", message="参数不合法", status_code=400)


def _parse_dt(v: str | None) -> datetime | None:
    raw = (v or "").strip()
    if not raw:
        return None
    try:
        dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except Exception:
        raise ApiError(code="INVALID_DATETIME", message="时间格式不合法", status_code=400)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _parse_date(v: str | None) -> date | None:
    raw = (v or "").strip()
    if not raw:
        return None
    try:
        return date.fromisoformat(raw)
    except Exception:
        raise ApiError(code="INVALID_DATE", message="日期格式不合法", status_code=400)


def _post_ledger(db: Session, order_id: uuid.UUID, event_type: str, lines: list[tuple[str, float, float]], external_ref: str = ""):
    for account, dr, cr in lines:
        db.add(
            SalaryLoanLedgerEntry(
                order_id=order_id,
                event_type=event_type,
                account=account,
                dr_amount=float(dr),
                cr_amount=float(cr),
                external_ref=external_ref or "",
            )
        )


class UpsertFactoryInput(BaseModel):
    name: str
    industry: str = "factory"
    location: str = ""
    owner_type: str = "unknown"
    salary_cycle: str = "monthly"
    worker_count: int = 0
    risk_level: str = "C"
    default_rate: float = 0
    hr_contact: str = ""
    is_active: bool = True


class UpdateFactoryInput(BaseModel):
    name: str | None = None
    industry: str | None = None
    location: str | None = None
    owner_type: str | None = None
    salary_cycle: str | None = None
    worker_count: int | None = None
    risk_level: str | None = None
    default_rate: float | None = None
    hr_contact: str | None = None
    is_active: bool | None = None


@router.get("/factories")
def admin_list_factories(_: AdminPrincipal = Depends(get_current_admin), db: Session = Depends(get_db)):
    rows = db.query(SalaryFactory).order_by(SalaryFactory.created_at.desc()).limit(1000).all()
    return [
        {
            "id": str(f.id),
            "name": f.name,
            "industry": f.industry,
            "location": f.location,
            "owner_type": f.owner_type,
            "salary_cycle": f.salary_cycle,
            "worker_count": int(f.worker_count or 0),
            "risk_level": f.risk_level,
            "default_rate": float(f.default_rate or 0),
            "hr_contact": f.hr_contact,
            "is_active": bool(f.is_active),
            "created_at": f.created_at.isoformat() if f.created_at else None,
        }
        for f in rows
    ]


@router.post("/factories")
def admin_create_factory(
    payload: UpsertFactoryInput,
    _: AdminPrincipal = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    f = SalaryFactory(
        name=payload.name.strip(),
        industry=payload.industry,
        location=payload.location,
        owner_type=payload.owner_type,
        salary_cycle=payload.salary_cycle,
        worker_count=payload.worker_count,
        risk_level=payload.risk_level,
        default_rate=payload.default_rate,
        hr_contact=payload.hr_contact,
        is_active=payload.is_active,
    )
    db.add(f)
    db.commit()
    return {"id": str(f.id)}


@router.patch("/factories/{factory_id}")
def admin_update_factory(
    factory_id: str,
    payload: UpdateFactoryInput,
    _: AdminPrincipal = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    fid = _parse_uuid(factory_id)
    f = db.query(SalaryFactory).filter(SalaryFactory.id == fid).first()
    if not f:
        raise ApiError(code="NOT_FOUND", message="未找到工厂", status_code=404)

    data = payload.model_dump(exclude_unset=True)
    if "name" in data and data["name"] is not None:
        f.name = str(data["name"]).strip()
    if "industry" in data and data["industry"] is not None:
        f.industry = str(data["industry"])[:64]
    if "location" in data and data["location"] is not None:
        f.location = str(data["location"])[:128]
    if "owner_type" in data and data["owner_type"] is not None:
        f.owner_type = str(data["owner_type"])[:32]
    if "salary_cycle" in data and data["salary_cycle"] is not None:
        f.salary_cycle = str(data["salary_cycle"])[:32]
    if "worker_count" in data and data["worker_count"] is not None:
        f.worker_count = int(data["worker_count"])
    if "risk_level" in data and data["risk_level"] is not None:
        f.risk_level = str(data["risk_level"])[:16]
    if "default_rate" in data and data["default_rate"] is not None:
        f.default_rate = float(data["default_rate"])
    if "hr_contact" in data and data["hr_contact"] is not None:
        f.hr_contact = str(data["hr_contact"])[:128]
    if "is_active" in data and data["is_active"] is not None:
        f.is_active = bool(data["is_active"])

    db.commit()
    return {"id": str(f.id)}


class VerifyEmploymentInput(BaseModel):
    verify_status: str = Field(..., pattern="^(verified|rejected|pending)$")
    verify_notes: str = ""


@router.post("/employments/{employment_id}/verify")
def admin_verify_employment(
    employment_id: str,
    payload: VerifyEmploymentInput,
    admin: AdminPrincipal = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    eid = _parse_uuid(employment_id)
    e = db.query(SalaryEmployment).filter(SalaryEmployment.id == eid).first()
    if not e:
        raise ApiError(code="NOT_FOUND", message="未找到就业信息", status_code=404)
    e.verify_status = payload.verify_status
    e.verify_notes = (payload.verify_notes or "")[:256]
    e.verified_at = _utcnow() if payload.verify_status == "verified" else None
    db.commit()
    return {"id": str(e.id), "verify_status": e.verify_status}


@router.get("/orders")
def admin_list_orders(
    status: str | None = None,
    limit: int = 50,
    offset: int = 0,
    _: AdminPrincipal = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    q = db.query(SalaryLoanOrder)
    if status:
        q = q.filter(SalaryLoanOrder.status == status)
    rows = (
        q.order_by(SalaryLoanOrder.created_at.desc())
        .offset(max(0, offset))
        .limit(min(200, max(1, limit)))
        .all()
    )
    return [
        {
            "id": str(o.id),
            "user_id": str(o.user_id),
            "employment_id": str(o.employment_id),
            "status": o.status,
            "principal": float(o.principal),
            "fee": float(o.fee),
            "interest": float(o.interest),
            "total_due": float(o.principal) + float(o.fee) + float(o.interest),
            "tenor_days": int(o.tenor_days),
            "due_date": o.due_date.isoformat() if o.due_date else None,
            "risk_score": o.risk_score,
            "decision": o.decision,
            "created_at": o.created_at.isoformat() if o.created_at else None,
        }
        for o in rows
    ]


@router.get("/orders/{order_id}")
def admin_get_order(order_id: str, _: AdminPrincipal = Depends(get_current_admin), db: Session = Depends(get_db)):
    oid = _parse_uuid(order_id)
    o = db.query(SalaryLoanOrder).filter(SalaryLoanOrder.id == oid).first()
    if not o:
        raise ApiError(code="NOT_FOUND", message="未找到订单", status_code=404)
    e = db.query(SalaryEmployment).filter(SalaryEmployment.id == o.employment_id).first()
    f = db.query(SalaryFactory).filter(SalaryFactory.id == e.factory_id).first() if e else None
    proofs = db.query(SalaryLoanRepaymentProof).filter(SalaryLoanRepaymentProof.order_id == o.id).order_by(SalaryLoanRepaymentProof.created_at.desc()).limit(50).all()
    schedules = db.query(SalaryLoanRepaymentSchedule).filter(SalaryLoanRepaymentSchedule.order_id == o.id).order_by(SalaryLoanRepaymentSchedule.installment_no.asc()).all()
    ledger = db.query(SalaryLoanLedgerEntry).filter(SalaryLoanLedgerEntry.order_id == o.id).order_by(SalaryLoanLedgerEntry.created_at.asc()).all()
    case = db.query(SalaryLoanCollectionCase).filter(SalaryLoanCollectionCase.order_id == o.id).first()
    return {
        "order": {
            "id": str(o.id),
            "user_id": str(o.user_id),
            "employment_id": str(o.employment_id),
            "status": o.status,
            "currency": o.currency,
            "principal": float(o.principal),
            "fee": float(o.fee),
            "interest": float(o.interest),
            "disbursement_amount": float(o.disbursement_amount),
            "tenor_days": int(o.tenor_days),
            "due_date": o.due_date.isoformat() if o.due_date else None,
            "risk_score": o.risk_score,
            "decision": o.decision,
            "decision_notes": o.decision_notes,
            "approved_by": o.approved_by,
            "disbursed_by": o.disbursed_by,
            "disbursed_at": o.disbursed_at.isoformat() if o.disbursed_at else None,
            "disbursement_ref": o.disbursement_ref,
            "created_at": o.created_at.isoformat() if o.created_at else None,
            "updated_at": o.updated_at.isoformat() if o.updated_at else None,
        },
        "employment": (
            {
                "id": str(e.id),
                "user_id": str(e.user_id),
                "factory_id": str(e.factory_id),
                "employee_no": e.employee_no,
                "department": e.department,
                "position": e.position,
                "join_date": e.join_date.isoformat() if e.join_date else None,
                "salary_amount": float(e.salary_amount) if e.salary_amount is not None else None,
                "salary_pay_day": int(e.salary_pay_day) if e.salary_pay_day is not None else None,
                "pay_cycle": e.pay_cycle,
                "pay_method": e.pay_method,
                "verify_status": e.verify_status,
                "verify_notes": e.verify_notes,
                "verified_at": e.verified_at.isoformat() if e.verified_at else None,
                "created_at": e.created_at.isoformat() if e.created_at else None,
            }
            if e
            else None
        ),
        "factory": (
            {
                "id": str(f.id),
                "name": f.name,
                "industry": f.industry,
                "location": f.location,
                "owner_type": f.owner_type,
                "salary_cycle": f.salary_cycle,
                "risk_level": f.risk_level,
                "default_rate": float(f.default_rate or 0),
                "hr_contact": f.hr_contact,
                "is_active": bool(f.is_active),
            }
            if f
            else None
        ),
        "proofs": [
            {
                "id": str(p.id),
                "amount": float(p.amount),
                "file_path": p.file_path,
                "note": p.note,
                "status": p.status,
                "reviewed_by": p.reviewed_by,
                "reviewed_at": p.reviewed_at.isoformat() if p.reviewed_at else None,
                "created_at": p.created_at.isoformat() if p.created_at else None,
            }
            for p in proofs
        ],
        "schedules": [
            {
                "id": str(s.id),
                "installment_no": int(s.installment_no),
                "due_date": s.due_date.isoformat(),
                "due_amount": float(s.due_amount),
                "paid_amount": float(s.paid_amount),
                "status": s.status,
                "paid_at": s.paid_at.isoformat() if s.paid_at else None,
            }
            for s in schedules
        ],
        "ledger": [
            {
                "id": str(le.id),
                "event_type": le.event_type,
                "account": le.account,
                "dr_amount": float(le.dr_amount),
                "cr_amount": float(le.cr_amount),
                "external_ref": le.external_ref,
                "created_at": le.created_at.isoformat() if le.created_at else None,
            }
            for le in ledger
        ],
        "collection": (
            {
                "id": str(case.id),
                "dpd": int(case.dpd),
                "stage": case.stage,
                "status": case.status,
                "assignee": case.assignee,
                "last_contact_at": case.last_contact_at.isoformat() if case.last_contact_at else None,
                "next_follow_up_at": case.next_follow_up_at.isoformat() if case.next_follow_up_at else None,
                "updated_at": case.updated_at.isoformat() if case.updated_at else None,
            }
            if case
            else None
        ),
    }


class DecisionInput(BaseModel):
    decision: str = Field(..., pattern="^(approve|reject)$")
    approved_principal: float | None = Field(default=None, gt=0)
    fee: float = 0
    interest: float = 0
    decision_notes: str = ""


@router.post("/orders/{order_id}/decision")
def admin_decide_order(
    order_id: str,
    payload: DecisionInput,
    admin: AdminPrincipal = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    oid = _parse_uuid(order_id)
    o = db.query(SalaryLoanOrder).filter(SalaryLoanOrder.id == oid).first()
    if not o:
        raise ApiError(code="NOT_FOUND", message="未找到订单", status_code=404)
    if o.status not in ("submitted", "factory_pending", "manual_review"):
        raise ApiError(code="INVALID_STATE", message="状态不允许", status_code=400)

    if payload.decision == "reject":
        o.decision = "rejected"
        o.decision_notes = (payload.decision_notes or "")[:256]
        o.status = "rejected"
        o.approved_by = admin.username
        db.commit()
        return {"id": str(o.id), "status": o.status}

    principal = float(payload.approved_principal or o.principal)
    fee = max(0.0, float(payload.fee or 0))
    interest = max(0.0, float(payload.interest or 0))

    o.principal = principal
    o.fee = fee
    o.interest = interest
    o.disbursement_amount = max(0.0, principal - fee)
    o.decision = "approved"
    o.decision_notes = (payload.decision_notes or "")[:256]
    o.status = "approved"
    o.approved_by = admin.username

    due = o.due_date or date.today()
    existing = db.query(SalaryLoanRepaymentSchedule).filter(SalaryLoanRepaymentSchedule.order_id == o.id).first()
    if not existing:
        db.add(
            SalaryLoanRepaymentSchedule(
                order_id=o.id,
                installment_no=1,
                due_date=due,
                due_amount=principal + fee + interest,
                paid_amount=0,
                status="due",
            )
        )
    db.commit()
    return {"id": str(o.id), "status": o.status}


class DisburseInput(BaseModel):
    disbursement_ref: str = ""


@router.post("/orders/{order_id}/disburse")
def admin_disburse_order(
    order_id: str,
    payload: DisburseInput,
    admin: AdminPrincipal = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    oid = _parse_uuid(order_id)
    o = db.query(SalaryLoanOrder).filter(SalaryLoanOrder.id == oid).first()
    if not o:
        raise ApiError(code="NOT_FOUND", message="未找到订单", status_code=404)
    if o.status != "approved":
        raise ApiError(code="INVALID_STATE", message="状态不允许", status_code=400)

    o.status = "disbursed"
    o.disbursed_by = admin.username
    o.disbursed_at = _utcnow()
    o.disbursement_ref = (payload.disbursement_ref or "")[:128]

    principal = float(o.principal)
    fee = float(o.fee)
    interest = float(o.interest)

    _post_ledger(
        db,
        order_id=o.id,
        event_type="DISBURSE",
        lines=[
            ("loan_receivable", principal, 0),
            ("cash", 0, principal),
        ],
        external_ref=o.disbursement_ref,
    )

    if fee > 0:
        _post_ledger(
            db,
            order_id=o.id,
            event_type="ACCRUE",
            lines=[
                ("fee_receivable", fee, 0),
                ("fee_income", 0, fee),
            ],
        )
    if interest > 0:
        _post_ledger(
            db,
            order_id=o.id,
            event_type="ACCRUE",
            lines=[
                ("interest_receivable", interest, 0),
                ("interest_income", 0, interest),
            ],
        )

    db.commit()
    return {"id": str(o.id), "status": o.status}


class ReviewProofInput(BaseModel):
    status: str = Field(..., pattern="^(accepted|rejected)$")
    note: str = ""


class CollectionEventInput(BaseModel):
    channel: str = "call"
    result: str = ""
    reason_code: str = ""
    note: str = ""
    ptp_date: str | None = None
    ptp_amount: float = 0
    next_follow_up_at: str | None = None
    assignee: str = ""


@router.post("/proofs/{proof_id}/review")
def admin_review_proof(
    proof_id: str,
    payload: ReviewProofInput,
    admin: AdminPrincipal = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    pid = _parse_uuid(proof_id)
    p = db.query(SalaryLoanRepaymentProof).filter(SalaryLoanRepaymentProof.id == pid).first()
    if not p:
        raise ApiError(code="NOT_FOUND", message="未找到凭证", status_code=404)
    if p.status != "pending":
        raise ApiError(code="INVALID_STATE", message="状态不允许", status_code=400)

    o = db.query(SalaryLoanOrder).filter(SalaryLoanOrder.id == p.order_id).first()
    if not o:
        raise ApiError(code="NOT_FOUND", message="未找到订单", status_code=404)

    p.status = payload.status
    p.reviewed_by = admin.username
    p.reviewed_at = _utcnow()
    p.note = ((p.note or "") + ("\n" + payload.note if payload.note else ""))[:256]

    if payload.status == "accepted":
        apply_repayment(db, order=o, amount=float(p.amount), external_ref=str(p.id))

    db.commit()
    return {"id": str(p.id), "status": p.status}


@router.get("/collections")
def admin_list_collection_cases(
    status: str | None = None,
    stage: str | None = None,
    limit: int = 50,
    offset: int = 0,
    _: AdminPrincipal = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    q = db.query(SalaryLoanCollectionCase)
    if status:
        q = q.filter(SalaryLoanCollectionCase.status == status)
    if stage:
        q = q.filter(SalaryLoanCollectionCase.stage == stage)
    rows = (
        q.order_by(SalaryLoanCollectionCase.dpd.desc(), SalaryLoanCollectionCase.updated_at.desc())
        .offset(max(0, offset))
        .limit(min(200, max(1, limit)))
        .all()
    )
    items = []
    for case in rows:
        order = db.query(SalaryLoanOrder).filter(SalaryLoanOrder.id == case.order_id).first()
        employment = db.query(SalaryEmployment).filter(SalaryEmployment.id == order.employment_id).first() if order else None
        factory = db.query(SalaryFactory).filter(SalaryFactory.id == employment.factory_id).first() if employment else None
        items.append(
            {
                "id": str(case.id),
                "order_id": str(case.order_id),
                "dpd": int(case.dpd),
                "stage": case.stage,
                "status": case.status,
                "assignee": case.assignee,
                "last_contact_at": case.last_contact_at.isoformat() if case.last_contact_at else None,
                "next_follow_up_at": case.next_follow_up_at.isoformat() if case.next_follow_up_at else None,
                "updated_at": case.updated_at.isoformat() if case.updated_at else None,
                "principal": float(order.principal) if order else 0.0,
                "total_due": (float(order.principal) + float(order.fee) + float(order.interest)) if order else 0.0,
                "due_date": order.due_date.isoformat() if order and order.due_date else None,
                "order_status": order.status if order else "",
                "risk_score": order.risk_score if order else None,
                "factory_name": factory.name if factory else "",
                "factory_risk_level": factory.risk_level if factory else "",
                "employee_no": employment.employee_no if employment else "",
            }
        )
    return items


@router.get("/collections/{case_id}")
def admin_get_collection_case(case_id: str, _: AdminPrincipal = Depends(get_current_admin), db: Session = Depends(get_db)):
    cid = _parse_uuid(case_id)
    case = db.query(SalaryLoanCollectionCase).filter(SalaryLoanCollectionCase.id == cid).first()
    if not case:
        raise ApiError(code="NOT_FOUND", message="未找到催收案件", status_code=404)

    order = db.query(SalaryLoanOrder).filter(SalaryLoanOrder.id == case.order_id).first()
    employment = db.query(SalaryEmployment).filter(SalaryEmployment.id == order.employment_id).first() if order else None
    factory = db.query(SalaryFactory).filter(SalaryFactory.id == employment.factory_id).first() if employment else None
    events = (
        db.query(SalaryLoanCollectionEvent)
        .filter(SalaryLoanCollectionEvent.case_id == case.id)
        .order_by(SalaryLoanCollectionEvent.created_at.desc())
        .all()
    )
    return {
        "case": {
            "id": str(case.id),
            "order_id": str(case.order_id),
            "dpd": int(case.dpd),
            "stage": case.stage,
            "status": case.status,
            "assignee": case.assignee,
            "last_contact_at": case.last_contact_at.isoformat() if case.last_contact_at else None,
            "next_follow_up_at": case.next_follow_up_at.isoformat() if case.next_follow_up_at else None,
            "updated_at": case.updated_at.isoformat() if case.updated_at else None,
        },
        "order": (
            {
                "id": str(order.id),
                "status": order.status,
                "principal": float(order.principal),
                "fee": float(order.fee),
                "interest": float(order.interest),
                "total_due": float(order.principal) + float(order.fee) + float(order.interest),
                "disbursement_amount": float(order.disbursement_amount),
                "due_date": order.due_date.isoformat() if order.due_date else None,
                "risk_score": order.risk_score,
            }
            if order
            else None
        ),
        "employment": (
            {
                "id": str(employment.id),
                "employee_no": employment.employee_no,
                "department": employment.department,
                "position": employment.position,
                "verify_status": employment.verify_status,
                "salary_amount": float(employment.salary_amount) if employment.salary_amount is not None else None,
            }
            if employment
            else None
        ),
        "factory": (
            {
                "id": str(factory.id),
                "name": factory.name,
                "location": factory.location,
                "risk_level": factory.risk_level,
                "hr_contact": factory.hr_contact,
            }
            if factory
            else None
        ),
        "events": [
            {
                "id": str(event.id),
                "channel": event.channel,
                "result": event.result,
                "reason_code": event.reason_code,
                "note": event.note,
                "ptp_date": event.ptp_date.isoformat() if event.ptp_date else None,
                "ptp_amount": float(event.ptp_amount or 0),
                "actor": event.actor,
                "created_at": event.created_at.isoformat() if event.created_at else None,
            }
            for event in events
        ],
    }


@router.post("/collections/{case_id}/events")
def admin_create_collection_event(
    case_id: str,
    payload: CollectionEventInput,
    admin: AdminPrincipal = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    cid = _parse_uuid(case_id)
    case = db.query(SalaryLoanCollectionCase).filter(SalaryLoanCollectionCase.id == cid).first()
    if not case:
        raise ApiError(code="NOT_FOUND", message="未找到催收案件", status_code=404)

    event = SalaryLoanCollectionEvent(
        case_id=case.id,
        channel=(payload.channel or "call")[:16],
        result=(payload.result or "")[:32],
        reason_code=(payload.reason_code or "")[:32],
        note=(payload.note or "")[:512],
        ptp_date=_parse_date(payload.ptp_date),
        ptp_amount=max(0.0, float(payload.ptp_amount or 0)),
        actor=admin.username,
    )
    db.add(event)
    case.last_contact_at = _utcnow()
    case.next_follow_up_at = _parse_dt(payload.next_follow_up_at)
    if (payload.assignee or "").strip():
        case.assignee = (payload.assignee or "").strip()[:64]
    elif not case.assignee:
        case.assignee = admin.username
    db.commit()
    return {
        "id": str(event.id),
        "case_id": str(case.id),
        "status": case.status,
        "assignee": case.assignee,
    }
