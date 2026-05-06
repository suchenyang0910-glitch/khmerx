from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.p2p_trade import P2PTrade
from app.models.user import User
from app.risk.models import DeviceFingerprint, UserRelationEdge


class RelationService:
    def __init__(self, db: Session):
        self.db = db

    @staticmethod
    def _pair(a: UUID, b: UUID) -> tuple[UUID, UUID]:
        return (a, b) if str(a) < str(b) else (b, a)

    def upsert_edge(
        self,
        user_a: UUID,
        user_b: UUID,
        relation_type: str,
        weight: int,
        evidence: dict | None = None,
    ):
        a, b = self._pair(user_a, user_b)
        existing = (
            self.db.query(UserRelationEdge)
            .filter(UserRelationEdge.user_a == a)
            .filter(UserRelationEdge.user_b == b)
            .filter(UserRelationEdge.relation_type == relation_type)
            .first()
        )
        if existing:
            existing.weight = max(existing.weight, weight)
            if evidence:
                merged = dict(existing.evidence or {})
                merged.update(evidence)
                existing.evidence = merged
            self.db.commit()
            return existing

        edge = UserRelationEdge(
            user_a=a,
            user_b=b,
            relation_type=relation_type,
            weight=weight,
            evidence=evidence or {},
        )
        self.db.add(edge)
        self.db.commit()
        self.db.refresh(edge)
        return edge

    def get_relation_score(self, user_a: UUID, user_b: UUID) -> int:
        a, b = self._pair(user_a, user_b)
        edges = (
            self.db.query(UserRelationEdge)
            .filter(UserRelationEdge.user_a == a)
            .filter(UserRelationEdge.user_b == b)
            .all()
        )
        return int(sum(e.weight for e in edges))

    def has_edge_type(self, user_a: UUID, user_b: UUID, relation_type: str) -> bool:
        a, b = self._pair(user_a, user_b)
        return (
            self.db.query(UserRelationEdge)
            .filter(UserRelationEdge.user_a == a)
            .filter(UserRelationEdge.user_b == b)
            .filter(UserRelationEdge.relation_type == relation_type)
            .first()
            is not None
        )

    def can_increase_credit(self, borrower_id: UUID, lender_id: UUID) -> bool:
        score = self.get_relation_score(borrower_id, lender_id)
        if score > 0:
            return False
        if self.has_edge_type(borrower_id, lender_id, "repeated_trade"):
            return False
        if self.has_edge_type(borrower_id, lender_id, "mutual_trade"):
            return False
        return True

    def build_relations_for_user(self, user_id: UUID):
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return

        if user.aba_account:
            others = (
                self.db.query(User)
                .filter(User.aba_account == user.aba_account)
                .filter(User.id != user.id)
                .all()
            )
            for other in others:
                self.upsert_edge(user.id, other.id, "same_aba", 100, {"aba_account": user.aba_account})

        if user.phone:
            others = (
                self.db.query(User)
                .filter(User.phone == user.phone)
                .filter(User.id != user.id)
                .all()
            )
            for other in others:
                self.upsert_edge(user.id, other.id, "same_phone", 90, {"phone": user.phone})

        if user.name:
            others = (
                self.db.query(User)
                .filter(User.name == user.name)
                .filter(User.id != user.id)
                .all()
            )
            for other in others:
                self.upsert_edge(user.id, other.id, "same_name", 30, {"name": user.name})

        fingerprints = self.db.query(DeviceFingerprint).filter(DeviceFingerprint.user_id == user.id).all()
        for fp in fingerprints:
            if fp.fingerprint_hash:
                others = (
                    self.db.query(DeviceFingerprint)
                    .filter(DeviceFingerprint.fingerprint_hash == fp.fingerprint_hash)
                    .filter(DeviceFingerprint.user_id != user.id)
                    .all()
                )
                for other_fp in others:
                    self.upsert_edge(user.id, other_fp.user_id, "same_device", 70, {"fingerprint_hash": fp.fingerprint_hash})

            if fp.ip_hash:
                others = (
                    self.db.query(DeviceFingerprint)
                    .filter(DeviceFingerprint.ip_hash == fp.ip_hash)
                    .filter(DeviceFingerprint.user_id != user.id)
                    .all()
                )
                for other_fp in others:
                    self.upsert_edge(user.id, other_fp.user_id, "same_ip", 40, {"ip_hash": fp.ip_hash})

    def record_trade_relations(self, borrower_id: UUID, lender_id: UUID, trade_id: UUID):
        now = datetime.now(timezone.utc)
        start = now - timedelta(days=7)
        recent = (
            self.db.query(P2PTrade)
            .filter(P2PTrade.created_at >= start)
            .filter(
                ((P2PTrade.borrower_id == borrower_id) & (P2PTrade.lender_id == lender_id))
                | ((P2PTrade.borrower_id == lender_id) & (P2PTrade.lender_id == borrower_id))
            )
            .count()
        )
        if recent >= 2:
            self.upsert_edge(borrower_id, lender_id, "repeated_trade", 30, {"trade_id": str(trade_id)})

        reverse = (
            self.db.query(P2PTrade)
            .filter(P2PTrade.borrower_id == lender_id)
            .filter(P2PTrade.lender_id == borrower_id)
            .count()
        )
        if reverse >= 1:
            self.upsert_edge(borrower_id, lender_id, "mutual_trade", 50, {"trade_id": str(trade_id)})

