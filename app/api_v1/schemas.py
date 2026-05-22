from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class PatchProfileRequest(BaseModel):
    aba_account: Optional[str] = None
    aba_name: Optional[str] = None
    phone: Optional[str] = None
    language: Optional[Literal["cn", "km", "en"]] = None


class VerifyTelegramContactRequest(BaseModel):
    response: str


class CalculateRequest(BaseModel):
    amount: float = Field(..., gt=0)
    term_days: int


class CreateOfferRequest(BaseModel):
    amount: float = Field(..., gt=0)
    term_days: int
    note: str = ""


class MatchOfferRequest(BaseModel):
    confirm_risk: bool = False


class ConfirmLendRequest(BaseModel):
    proof_url: str
    amount: float = Field(..., gt=0)
    note: str = ""


class ConfirmReceiveRequest(BaseModel):
    confirmed: bool = True


class RepayRequest(BaseModel):
    schedule_id: str
    proof_url: str
    amount: float = Field(..., gt=0)
    note: str = ""


class ConfirmRepaymentRequest(BaseModel):
    schedule_id: str
    confirmed: bool = True


class UploadProofResponse(BaseModel):
    url: str


class CreditDetail(BaseModel):
    credit_score: int
    credit_level: str
    risk_level: str
    max_borrow_amount: float
    reasons: List[str] = []
    logs: List[Dict[str, Any]] = []


class CreateFinanceApplicationRequest(BaseModel):
    biz_type: Literal["lease", "installment", "pledge"]
    payload: Dict[str, Any] = Field(default_factory=dict)


class FinanceApplicationOut(BaseModel):
    id: str
    user_id: str
    biz_type: str
    status: str
    payload: Dict[str, Any]
    created_at: str | None = None
    updated_at: str | None = None


class UnifiedOrderOut(BaseModel):
    id: str
    business_type: Literal["loan", "salary", "rental", "installment", "pawn"]
    source_type: Literal["p2p_offer", "p2p_trade", "finance_application", "salary_loan"]
    source_id: str
    status: str
    principal: float = 0
    interest: float = 0
    total_due: float = 0
    due_at: str | None = None
    created_at: str | None = None


class SalaryFactoryOut(BaseModel):
    id: str
    name: str
    industry: str
    location: str
    owner_type: str
    salary_cycle: str
    risk_level: str
    default_rate: float


class CreateSalaryEmploymentRequest(BaseModel):
    factory_id: str
    employee_no: str = ""
    department: str = ""
    position: str = ""
    join_date: str | None = None
    salary_amount: float | None = None
    salary_pay_day: int | None = None
    pay_cycle: Literal["monthly", "biweekly", "daily"] = "monthly"
    pay_method: Literal["transfer", "cash"] = "transfer"


class SalaryEmploymentOut(BaseModel):
    id: str
    user_id: str
    factory_id: str
    employee_no: str
    department: str
    position: str
    join_date: str | None
    salary_amount: float | None
    salary_pay_day: int | None
    pay_cycle: str
    pay_method: str
    verify_status: str
    verify_notes: str
    verified_at: str | None
    created_at: str | None


class CreateSalaryLoanOrderRequest(BaseModel):
    employment_id: str
    principal: float = Field(..., gt=0)
    tenor_days: int = 14
    note: str = ""


class SalaryLoanOrderOut(BaseModel):
    id: str
    user_id: str
    employment_id: str
    status: str
    currency: str
    principal: float
    fee: float
    interest: float
    disbursement_amount: float
    tenor_days: int
    due_date: str | None
    risk_score: int | None
    decision: str
    decision_notes: str
    created_at: str | None
    updated_at: str | None


class SalaryLoanRepaymentScheduleOut(BaseModel):
    id: str
    order_id: str
    installment_no: int
    due_date: str
    due_amount: float
    paid_amount: float
    status: str
    paid_at: str | None


class SalaryLoanOrderDetailOut(BaseModel):
    order: SalaryLoanOrderOut
    employment: SalaryEmploymentOut
    factory: SalaryFactoryOut | None = None
    schedules: List[SalaryLoanRepaymentScheduleOut] = []


class SalaryLoanUploadProofResponse(BaseModel):
    proof_id: str
    url: str
