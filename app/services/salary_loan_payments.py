from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.salary_loan_order import SalaryLoanOrder
from app.models.salary_loan_repayment import SalaryLoanCollectionCase, SalaryLoanLedgerEntry, SalaryLoanRepaymentSchedule


def _balance(db: Session, order_id: uuid.UUID, account: str) -> float:
    dr = (
        db.query(func.coalesce(func.sum(SalaryLoanLedgerEntry.dr_amount), 0))
        .filter(SalaryLoanLedgerEntry.order_id == order_id)
        .filter(SalaryLoanLedgerEntry.account == account)
        .scalar()
    )
    cr = (
        db.query(func.coalesce(func.sum(SalaryLoanLedgerEntry.cr_amount), 0))
        .filter(SalaryLoanLedgerEntry.order_id == order_id)
        .filter(SalaryLoanLedgerEntry.account == account)
        .scalar()
    )
    try:
        return float(dr) - float(cr)
    except Exception:
        return 0.0


def _post_ledger(
    db: Session,
    *,
    order_id: uuid.UUID,
    event_type: str,
    external_ref: str,
    lines: list[tuple[str, float, float]],
):
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


def apply_repayment(
    db: Session,
    *,
    order: SalaryLoanOrder,
    amount: float,
    external_ref: str,
) -> dict:
    if amount <= 0:
        return {"ok": False, "code": "INVALID_AMOUNT", "message": "amount must be > 0"}

    external_ref = (external_ref or "").strip()[:128]
    if not external_ref:
        return {"ok": False, "code": "MISSING_REF", "message": "external_ref is required"}

    exists = (
        db.query(SalaryLoanLedgerEntry)
        .filter(SalaryLoanLedgerEntry.order_id == order.id)
        .filter(SalaryLoanLedgerEntry.event_type == "REPAY")
        .filter(SalaryLoanLedgerEntry.external_ref == external_ref)
        .count()
    )
    if exists:
        return {"ok": True, "status": "skipped", "message": "already processed"}

    outstanding_fee = max(0.0, _balance(db, order.id, "fee_receivable"))
    outstanding_interest = max(0.0, _balance(db, order.id, "interest_receivable"))
    outstanding_principal = max(0.0, _balance(db, order.id, "loan_receivable"))

    remaining = float(amount)
    pay_fee = min(remaining, outstanding_fee)
    remaining -= pay_fee
    pay_interest = min(remaining, outstanding_interest)
    remaining -= pay_interest
    pay_principal = min(remaining, outstanding_principal)
    remaining -= pay_principal

    total_applied = pay_fee + pay_interest + pay_principal
    if total_applied <= 0:
        return {"ok": False, "code": "NOTHING_DUE", "message": "no outstanding balance"}

    lines: list[tuple[str, float, float]] = [("cash", total_applied, 0.0)]
    if pay_fee > 0:
        lines.append(("fee_receivable", 0.0, pay_fee))
    if pay_interest > 0:
        lines.append(("interest_receivable", 0.0, pay_interest))
    if pay_principal > 0:
        lines.append(("loan_receivable", 0.0, pay_principal))

    _post_ledger(db, order_id=order.id, event_type="REPAY", external_ref=external_ref, lines=lines)

    schedule = (
        db.query(SalaryLoanRepaymentSchedule)
        .filter(SalaryLoanRepaymentSchedule.order_id == order.id)
        .order_by(SalaryLoanRepaymentSchedule.installment_no.asc())
        .first()
    )
    if not schedule:
        due_date = order.due_date
        if not due_date:
            return {"ok": False, "code": "MISSING_DUE_DATE", "message": "order missing due_date"}
        schedule = SalaryLoanRepaymentSchedule(
            order_id=order.id,
            installment_no=1,
            due_date=due_date,
            due_amount=float(order.principal) + float(order.fee) + float(order.interest),
            paid_amount=0,
            status="due",
        )
        db.add(schedule)
        db.flush()

    schedule.paid_amount = float(schedule.paid_amount) + float(total_applied)

    if float(schedule.paid_amount) >= float(schedule.due_amount):
        schedule.status = "paid"
        schedule.paid_at = datetime.now(timezone.utc)
        order.status = "completed"

        case = db.query(SalaryLoanCollectionCase).filter(SalaryLoanCollectionCase.order_id == order.id).first()
        if case:
            case.status = "closed"
    else:
        if order.status not in ("completed", "rejected"):
            order.status = "repaying"

    return {
        "ok": True,
        "status": "processed",
        "applied": {
            "fee": pay_fee,
            "interest": pay_interest,
            "principal": pay_principal,
            "total": total_applied,
        },
    }
