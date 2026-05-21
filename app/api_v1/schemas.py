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
    business_type: Literal["loan", "rental", "installment", "pawn"]
    source_type: Literal["p2p_offer", "p2p_trade", "finance_application"]
    source_id: str
    status: str
    principal: float = 0
    interest: float = 0
    total_due: float = 0
    due_at: str | None = None
    created_at: str | None = None
