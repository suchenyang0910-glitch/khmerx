from __future__ import annotations

from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class CreateDisputeInput(BaseModel):
    trade_id: UUID
    dispute_type: str = Field(..., min_length=1)
    reason: str = Field(..., min_length=1)


class AddEvidenceInput(BaseModel):
    dispute_id: Optional[int] = None
    evidence_type: str = Field(..., min_length=1)
    file_url: Optional[str] = None
    text_note: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ResolveDisputeInput(BaseModel):
    dispute_id: int
    resolution_result: str
    resolution_note: str = ""

