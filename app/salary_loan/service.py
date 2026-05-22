from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.salary_loan_order import SalaryLoanOrder
from app.services.salary_loan_payments import apply_repayment


def apply_salary_loan_repayment(db: Session, *, order: SalaryLoanOrder, amount: float, external_ref: str) -> dict:
    return apply_repayment(db, order=order, amount=amount, external_ref=external_ref)

