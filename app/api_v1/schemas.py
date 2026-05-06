from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class PatchProfileRequest(BaseModel):
    aba_account: Optional[str] = None
    aba_name: Optional[str] = None
    phone: Optional[str] = None
    language: Optional[Literal["cn", "km"]] = None


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
