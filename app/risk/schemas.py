from __future__ import annotations

from decimal import Decimal
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class RiskDecision(BaseModel):
    allowed: bool
    action: str = "allow"
    reason: str = ""
    risk_level: str = "normal"
    score_delta: int = 0
    require_manual_review: bool = False
    metadata: Dict[str, Any] = Field(default_factory=dict)


class CreateOfferRiskInput(BaseModel):
    user_id: UUID
    amount: Decimal
    term_days: int
    user_age_days: int
    active_trades_count: int
    offers_24h_count: int


class MatchOfferRiskInput(BaseModel):
    lender_id: UUID
    offer_id: UUID
    active_trades_count: int


class RepaymentRiskInput(BaseModel):
    user_id: UUID
    trade_id: UUID
    overdue_days: int


class AdjustScoreInput(BaseModel):
    user_id: UUID
    score_delta: int
    reason: str

