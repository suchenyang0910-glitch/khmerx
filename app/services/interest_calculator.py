"""利率与还款计算引擎 — KhmerX P2P ABA 微借贷"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.config import PLATFORM_FEE_RATE
from app.models.interest_rate import InterestRateMatrix


@dataclass(frozen=True)
class CutInterestLoanResult:
    principal: Decimal
    term_days: int
    rate_percent: Decimal
    interest: Decimal
    received_amount: Decimal
    repay_amount: Decimal
    real_rate_percent: Decimal
    apr_percent: Decimal
    mode: str


def _money(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class InterestCalculator:
    @staticmethod
    def score_to_credit_level(credit_score: int) -> str:
        if credit_score >= 800:
            return "A"
        if credit_score >= 700:
            return "B"
        if credit_score >= 600:
            return "C"
        if credit_score >= 500:
            return "D"
        return "E"

    @staticmethod
    def get_cut_interest_rate_percent(db: Session, term_days: int, credit_level: str) -> Optional[Decimal]:
        row = db.query(InterestRateMatrix).filter(
            and_(
                InterestRateMatrix.term_days == term_days,
                InterestRateMatrix.credit_level == credit_level,
                InterestRateMatrix.mode == "cut_interest",
                InterestRateMatrix.enabled == True,
            )
        ).first()
        if not row:
            return None
        return Decimal(row.rate_percent)

    @staticmethod
    def calculate_fee(amount: float) -> float:
        return round(amount * PLATFORM_FEE_RATE, 2)

    @staticmethod
    def calc_cut_interest_loan(
        principal: float | Decimal,
        term_days: int,
        rate_percent: float | Decimal,
    ) -> CutInterestLoanResult:
        principal_d = _money(Decimal(str(principal)))
        rate_d = Decimal(str(rate_percent))

        if principal_d <= 0:
            raise ValueError("principal must be greater than 0")
        if term_days not in (7, 14, 30):
            raise ValueError("term_days must be 7, 14, or 30")

        interest = _money(principal_d * rate_d / Decimal("100"))
        received_amount = _money(principal_d - interest)
        repay_amount = principal_d

        if received_amount <= 0:
            raise ValueError("received_amount must be greater than 0")

        real_rate_percent = _money((interest / received_amount) * Decimal("100"))
        apr_percent = _money(
            (interest / received_amount) * Decimal(365) / Decimal(term_days) * Decimal("100")
        )

        return CutInterestLoanResult(
            principal=principal_d,
            term_days=term_days,
            rate_percent=rate_d,
            interest=interest,
            received_amount=received_amount,
            repay_amount=repay_amount,
            real_rate_percent=real_rate_percent,
            apr_percent=apr_percent,
            mode="cut_interest",
        )

    @staticmethod
    def calculate_total_repayable_cut_interest(principal: float) -> float:
        return round(principal, 2)

    @staticmethod
    def generate_schedule_cut_interest(trade_id, principal: float) -> list[dict]:
        principal_d = _money(Decimal(str(principal)))
        return [
            {
                "trade_id": trade_id,
                "period": 1,
                "principal": float(principal_d),
                "interest": 0.0,
                "total": float(principal_d),
                "status": "pending",
            }
        ]

    @staticmethod
    def calculate_advance_pay_deadline(created_at: datetime) -> datetime:
        from app.config import ADVANCE_PAY_HOURS

        return created_at + timedelta(hours=ADVANCE_PAY_HOURS)
