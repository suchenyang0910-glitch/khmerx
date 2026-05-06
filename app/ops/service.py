from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.p2p_trade import P2PTrade
from app.models.user import User
from app.ops.models import AgentCommission, AgentStat, CollectionTask
from app.risk.relations import RelationService


def _money(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class AgentService:
    def __init__(self, db: Session):
        self.db = db

    def _get_or_create_stat(self, agent_id: UUID) -> AgentStat:
        stat = self.db.query(AgentStat).filter(AgentStat.agent_id == agent_id).first()
        if stat:
            return stat
        stat = AgentStat(agent_id=agent_id)
        self.db.add(stat)
        self.db.commit()
        self.db.refresh(stat)
        return stat

    def can_generate_commission(self, borrower: User, lender: User) -> bool:
        if borrower.agent_id and lender.agent_id and borrower.agent_id == lender.agent_id:
            return False
        rel = RelationService(self.db)
        rel.build_relations_for_user(borrower.id)
        rel.build_relations_for_user(lender.id)
        if rel.get_relation_score(borrower.id, lender.id) > 0:
            return False
        return True

    def create_borrow_commission_pending(self, trade: P2PTrade):
        borrower = self.db.query(User).filter(User.id == trade.borrower_id).first()
        lender = self.db.query(User).filter(User.id == trade.lender_id).first()
        if not borrower or not lender:
            return None
        if not borrower.agent_id:
            return None
        if borrower.agent_id == borrower.id:
            return None
        if not self.can_generate_commission(borrower, lender):
            return None

        agent = self.db.query(User).filter(User.id == borrower.agent_id).first()
        if not agent or agent.role != "agent":
            return None

        exists = (
            self.db.query(AgentCommission)
            .filter(AgentCommission.trade_id == trade.id)
            .filter(AgentCommission.agent_id == borrower.agent_id)
            .filter(AgentCommission.commission_type == "borrow")
            .first()
        )
        if exists:
            return exists

        rate = Decimal(str(agent.commission_rate or 0))
        if rate <= 0:
            rate = Decimal("2.00")
        amount = _money(Decimal(str(trade.amount)) * rate / Decimal("100"))

        commission = AgentCommission(
            agent_id=borrower.agent_id,
            user_id=borrower.id,
            trade_id=trade.id,
            amount=amount,
            commission_type="borrow",
            status="pending",
        )
        self.db.add(commission)

        stat = self._get_or_create_stat(borrower.agent_id)
        stat.pending_commission = _money(Decimal(str(stat.pending_commission)) + amount)
        stat.updated_at = datetime.now(timezone.utc)

        self.db.commit()
        self.db.refresh(commission)
        return commission

    def settle_commissions_for_trade(self, trade_id: UUID):
        now = datetime.now(timezone.utc)
        commissions = (
            self.db.query(AgentCommission)
            .filter(AgentCommission.trade_id == trade_id)
            .filter(AgentCommission.status == "pending")
            .all()
        )
        for c in commissions:
            c.status = "settled"
            c.settled_at = now
            stat = self._get_or_create_stat(c.agent_id)
            stat.pending_commission = _money(Decimal(str(stat.pending_commission)) - Decimal(str(c.amount)))
            stat.total_commission = _money(Decimal(str(stat.total_commission)) + Decimal(str(c.amount)))
            stat.updated_at = now
        self.db.commit()


class CollectionService:
    def __init__(self, db: Session):
        self.db = db

    def create_task_if_missing(self, user_id: UUID, trade_id: UUID, agent_id: UUID | None, priority: str, note: str):
        existing = (
            self.db.query(CollectionTask)
            .filter(CollectionTask.trade_id == trade_id)
            .filter(CollectionTask.status.in_(["pending", "assigned", "in_progress"]))
            .first()
        )
        if existing:
            return existing
        task = CollectionTask(
            user_id=user_id,
            trade_id=trade_id,
            agent_id=agent_id,
            status="pending",
            priority=priority,
            note=note,
        )
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

