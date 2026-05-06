from __future__ import annotations

import uuid
from datetime import datetime, timezone
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.ops.models import AgentCommission, AgentStat, CollectionTask

router = APIRouter(prefix="/ops", tags=["ops"])


def _get_user(db: Session, user_id_str: str) -> User:
    try:
        uid = uuid.UUID(user_id_str)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user_id")
    user = db.query(User).filter(User.id == uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/agent/dashboard")
def agent_dashboard(agent_id: str, db: Session = Depends(get_db)):
    agent = _get_user(db, agent_id)
    if agent.role != "agent":
        raise HTTPException(status_code=403, detail="Agent access required")

    stat = db.query(AgentStat).filter(AgentStat.agent_id == agent.id).first()
    if not stat:
        return {
            "agent_id": str(agent.id),
            "total_users": 0,
            "total_loans": 0,
            "total_volume": 0,
            "total_commission": 0,
            "pending_commission": 0,
        }

    return {
        "agent_id": str(agent.id),
        "total_users": stat.total_users,
        "total_loans": stat.total_loans,
        "total_volume": float(stat.total_volume),
        "total_commission": float(stat.total_commission),
        "pending_commission": float(stat.pending_commission),
        "updated_at": stat.updated_at.isoformat() if stat.updated_at else None,
    }


@router.get("/agent/commissions")
def agent_commissions(
    agent_id: str,
    status: str = "pending",
    limit: int = 100,
    db: Session = Depends(get_db),
):
    agent = _get_user(db, agent_id)
    if agent.role != "agent":
        raise HTTPException(status_code=403, detail="Agent access required")

    q = db.query(AgentCommission).filter(AgentCommission.agent_id == agent.id)
    if status:
        q = q.filter(AgentCommission.status == status)
    rows = q.order_by(AgentCommission.created_at.desc()).limit(limit).all()
    return rows


@router.get("/collector/tasks")
def collector_tasks(
    collector_id: str,
    status: str = "pending",
    limit: int = 100,
    db: Session = Depends(get_db),
):
    user = _get_user(db, collector_id)
    if user.role not in ("collector", "admin"):
        raise HTTPException(status_code=403, detail="Collector access required")

    q = db.query(CollectionTask)
    if user.role == "collector":
        q = q.filter(CollectionTask.assigned_to == user.id)
    if status:
        q = q.filter(CollectionTask.status == status)
    return q.order_by(CollectionTask.created_at.desc()).limit(limit).all()


@router.post("/collector/tasks/{task_id}/assign")
def assign_collection_task(
    task_id: int,
    admin_id: str,
    assigned_to: str,
    db: Session = Depends(get_db),
):
    admin = _get_user(db, admin_id)
    if admin.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    collector = _get_user(db, assigned_to)
    if collector.role != "collector":
        raise HTTPException(status_code=400, detail="assigned_to is not a collector")

    task = db.query(CollectionTask).filter(CollectionTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="task not found")

    task.assigned_to = collector.id
    task.status = "assigned"
    task.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(task)
    return task


@router.post("/collector/tasks/{task_id}/close")
def close_collection_task(
    task_id: int,
    collector_id: str,
    note: str = "",
    db: Session = Depends(get_db),
):
    collector = _get_user(db, collector_id)
    if collector.role not in ("collector", "admin"):
        raise HTTPException(status_code=403, detail="Collector access required")

    task = db.query(CollectionTask).filter(CollectionTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="task not found")

    if collector.role == "collector" and task.assigned_to != collector.id:
        raise HTTPException(status_code=403, detail="task not assigned to you")

    task.status = "closed"
    task.note = note or task.note
    task.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(task)
    return task

