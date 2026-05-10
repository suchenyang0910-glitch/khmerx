from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Any, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.user import User
from app.risk.models import ManualReviewCase, RiskEvent, RiskLog, RiskScoreLog, UserRiskProfile
from app.risk.rules import MAX_BORROW_AMOUNT_CAP, credit_level_from_score, max_borrow_amount_by_level, normalize_risk_level


class RiskService:
    def __init__(self, db: Session):
        self.db = db

    def get_or_create_profile(self, user_id: UUID) -> UserRiskProfile:
        profile = (
            self.db.query(UserRiskProfile)
            .filter(UserRiskProfile.user_id == user_id)
            .first()
        )
        if profile:
            if profile.max_borrow_amount is not None and profile.max_borrow_amount > MAX_BORROW_AMOUNT_CAP:
                profile.max_borrow_amount = MAX_BORROW_AMOUNT_CAP
                self.db.commit()
            return profile

        user = self.db.query(User).filter(User.id == user_id).first()
        credit_score = user.credit_score if user else 650
        credit_level = credit_level_from_score(credit_score)

        profile = UserRiskProfile(
            user_id=user_id,
            credit_score=credit_score,
            credit_level=credit_level if credit_level in ("A", "B", "C", "D") else "C",
            risk_level="normal",
            max_borrow_amount=max_borrow_amount_by_level(credit_level),
        )
        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)
        return profile

    def apply_score_change(
        self,
        user_id: UUID,
        score_delta: int,
        reason: str,
        event_type: str,
        trade_id: UUID | None = None,
        offer_id: UUID | None = None,
        created_by: str = "system",
        metadata: dict | None = None,
    ) -> UserRiskProfile:
        profile = self.get_or_create_profile(user_id)

        old_score = profile.credit_score
        old_risk_level = profile.risk_level

        new_score = max(0, min(1000, old_score + score_delta))
        new_credit_level = credit_level_from_score(new_score)
        new_risk_level = normalize_risk_level(new_score, old_risk_level)

        profile.credit_score = new_score
        profile.credit_level = new_credit_level
        profile.risk_level = new_risk_level
        profile.max_borrow_amount = max_borrow_amount_by_level(new_credit_level)
        profile.updated_at = datetime.now(timezone.utc)

        log = RiskLog(
            user_id=user_id,
            trade_id=trade_id,
            offer_id=offer_id,
            event_type=event_type,
            risk_action="score_change",
            score_change=score_delta,
            old_score=old_score,
            new_score=new_score,
            old_risk_level=old_risk_level,
            new_risk_level=new_risk_level,
            reason=reason,
            created_by=created_by,
            meta=metadata or {},
        )

        self.db.add(log)
        self.db.commit()
        self.db.refresh(profile)

        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            user.credit_score = profile.credit_score
            user.risk_level = profile.risk_level
            self.db.commit()
        return profile

    def apply_risk_score_change(
        self,
        user_id: UUID,
        score_delta: int,
        reason: str,
        created_by: str = "system",
    ) -> UserRiskProfile:
        profile = self.get_or_create_profile(user_id)
        old_score = int(profile.risk_score or 0)
        new_score = max(0, old_score + int(score_delta))
        profile.risk_score = new_score
        profile.updated_at = datetime.now(timezone.utc)

        self.db.add(
            RiskScoreLog(
                user_id=user_id,
                score_change=int(score_delta),
                old_score=old_score,
                new_score=new_score,
                reason=reason,
                created_by=created_by,
            )
        )
        self.db.commit()
        self.db.refresh(profile)
        return profile

    def create_manual_review_case(
        self,
        reason: str,
        user_id: UUID | None = None,
        trade_id: UUID | None = None,
        offer_id: UUID | None = None,
        risk_score: int = 0,
    ):
        case = ManualReviewCase(
            user_id=user_id,
            trade_id=trade_id,
            offer_id=offer_id,
            reason=reason,
            risk_score=risk_score,
            status="pending",
        )
        self.db.add(case)
        self.db.commit()
        self.db.refresh(case)
        return case

    def block_user(
        self,
        user_id: UUID,
        reason: str,
        hours: int | None = None,
        created_by: str = "system",
    ) -> UserRiskProfile:
        profile = self.get_or_create_profile(user_id)

        old_risk_level = profile.risk_level

        profile.is_blocked = True
        profile.risk_level = "blocked"
        profile.block_reason = reason
        profile.updated_at = datetime.now(timezone.utc)

        if hours:
            profile.blocked_until = datetime.now(timezone.utc) + timedelta(hours=hours)

        log = RiskLog(
            user_id=user_id,
            event_type="block_user",
            risk_action="blocked",
            old_score=profile.credit_score,
            new_score=profile.credit_score,
            old_risk_level=old_risk_level,
            new_risk_level="blocked",
            reason=reason,
            created_by=created_by,
            meta={},
        )

        self.db.add(log)
        self.db.commit()
        self.db.refresh(profile)
        return profile

    def unblock_user(self, user_id: UUID, created_by: str = "system", reason: str = "manual_unblock") -> UserRiskProfile:
        profile = self.get_or_create_profile(user_id)
        old_risk_level = profile.risk_level

        profile.is_blocked = False
        profile.blocked_until = None
        profile.block_reason = None
        profile.risk_level = "normal" if profile.credit_score >= 650 else "watch"
        profile.updated_at = datetime.now(timezone.utc)

        self.db.add(
            RiskLog(
                user_id=user_id,
                event_type="unblock_user",
                risk_action="unblocked",
                old_score=profile.credit_score,
                new_score=profile.credit_score,
                old_risk_level=old_risk_level,
                new_risk_level=profile.risk_level,
                reason=reason,
                created_by=created_by,
                meta={},
            )
        )

        self.db.commit()
        self.db.refresh(profile)
        return profile

    def unblock_expired_blocks(self):
        now = datetime.now(timezone.utc)

        profiles = (
            self.db.query(UserRiskProfile)
            .filter(UserRiskProfile.is_blocked == True)
            .filter(UserRiskProfile.blocked_until != None)
            .filter(UserRiskProfile.blocked_until <= now)
            .all()
        )

        for profile in profiles:
            old_risk_level = profile.risk_level
            profile.is_blocked = False
            profile.blocked_until = None
            profile.risk_level = "normal" if profile.credit_score >= 650 else "watch"
            profile.updated_at = now

            self.db.add(
                RiskLog(
                    user_id=profile.user_id,
                    event_type="auto_unblock",
                    risk_action="unblocked",
                    old_score=profile.credit_score,
                    new_score=profile.credit_score,
                    old_risk_level=old_risk_level,
                    new_risk_level=profile.risk_level,
                    reason="temporary block expired",
                    created_by="system",
                    meta={},
                )
            )

        self.db.commit()

    def create_risk_event(
        self,
        event_type: str,
        severity: str,
        payload: dict,
        user_id: UUID | None = None,
        trade_id: UUID | None = None,
        offer_id: UUID | None = None,
    ):
        event = RiskEvent(
            event_key=uuid.uuid4(),
            event_type=event_type,
            severity=severity,
            user_id=user_id,
            trade_id=trade_id,
            offer_id=offer_id,
            payload=payload,
            status="pending",
        )
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event

