from __future__ import annotations

import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.disputes.schemas import AddEvidenceInput, CreateDisputeInput, ResolveDisputeInput
from app.disputes.service import DisputeService
from app.models.user import User
from app.risk.models import Dispute

router = APIRouter(prefix="/disputes", tags=["disputes"])


def _get_user(db: Session, user_id_str: str) -> User:
    try:
        uid = uuid.UUID(user_id_str)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user_id")
    user = db.query(User).filter(User.id == uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("")
def create_dispute(
    payload: CreateDisputeInput,
    user_id: str = Query(..., description="用户 UUID"),
    db: Session = Depends(get_db),
):
    current_user = _get_user(db, user_id)
    service = DisputeService(db)
    return service.create_dispute(current_user.id, payload)


@router.post("/evidence")
def add_evidence(
    payload: AddEvidenceInput,
    user_id: str = Query(..., description="用户 UUID"),
    db: Session = Depends(get_db),
):
    current_user = _get_user(db, user_id)
    service = DisputeService(db)
    return service.add_evidence(current_user.id, payload)


@router.post("/resolve")
def resolve_dispute(
    payload: ResolveDisputeInput,
    admin_id: str = Query(..., description="管理员 UUID"),
    db: Session = Depends(get_db),
):
    admin = _get_user(db, admin_id)
    if admin.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    service = DisputeService(db)
    return service.resolve_dispute(admin.id, payload)


@router.get("/my")
def list_my_disputes(
    user_id: str = Query(..., description="用户 UUID"),
    limit: int = 50,
    db: Session = Depends(get_db),
):
    user = _get_user(db, user_id)
    disputes = (
        db.query(Dispute)
        .filter((Dispute.borrower_id == user.id) | (Dispute.lender_id == user.id))
        .order_by(Dispute.created_at.desc())
        .limit(limit)
        .all()
    )
    return disputes

