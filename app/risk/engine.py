import json
from decimal import Decimal
from uuid import UUID

from app.risk.schemas import CreateOfferRiskInput, MatchOfferRiskInput, RepaymentRiskInput, RiskDecision
from app.risk.rules import MAX_BORROW_AMOUNT_CAP, NEW_USER_MAX_BORROW_AMOUNT
from app.risk.service import RiskService


class RiskEngine:
    def __init__(self, risk_service: RiskService):
        self.risk_service = risk_service

    def check_create_offer(self, data: CreateOfferRiskInput) -> RiskDecision:
        raw = data.model_dump(mode="json") if hasattr(data, "model_dump") else data.dict()
        payload = json.loads(json.dumps(raw, default=str))
        profile = self.risk_service.get_or_create_profile(data.user_id)

        if profile.is_blocked:
            return RiskDecision(
                allowed=False,
                action="blocked",
                reason=profile.block_reason or "user is blocked",
                risk_level=profile.risk_level,
            )

        if profile.risk_level in ["restricted", "blocked"]:
            return RiskDecision(
                allowed=False,
                action="restricted",
                reason="user is restricted from creating new offers",
                risk_level=profile.risk_level,
            )

        if data.active_trades_count >= profile.max_active_trades:
            return RiskDecision(
                allowed=False,
                action="limit_active_trades",
                reason="active trade limit reached",
                risk_level=profile.risk_level,
            )

        if data.amount > MAX_BORROW_AMOUNT_CAP:
            return RiskDecision(
                allowed=False,
                action="amount_exceeds_app_cap",
                reason=f"amount exceeds app cap {MAX_BORROW_AMOUNT_CAP}",
                risk_level=profile.risk_level,
            )

        if data.user_age_days < 7 and data.amount > NEW_USER_MAX_BORROW_AMOUNT:
            self.risk_service.create_risk_event(
                event_type="new_user_large_amount",
                severity="medium",
                user_id=data.user_id,
                payload=payload,
            )

            self.risk_service.create_manual_review_case(
                user_id=data.user_id,
                reason="new_user_large_amount",
            )

            return RiskDecision(
                allowed=False,
                action="manual_review",
                reason="new user amount requires manual review",
                risk_level="watch",
                require_manual_review=True,
            )

        if data.amount > Decimal(profile.max_borrow_amount):
            return RiskDecision(
                allowed=False,
                action="amount_exceeds_limit",
                reason=f"amount exceeds max borrow amount {profile.max_borrow_amount}",
                risk_level=profile.risk_level,
            )

        if data.offers_24h_count >= 5:
            self.risk_service.apply_score_change(
                user_id=data.user_id,
                score_delta=-10,
                reason="too many offers in 24h",
                event_type="high_frequency_offer",
            )

            self.risk_service.block_user(
                user_id=data.user_id,
                reason="too many offers in 24h",
                hours=24,
            )

            self.risk_service.create_manual_review_case(
                user_id=data.user_id,
                reason="high_frequency_offer",
            )

            return RiskDecision(
                allowed=False,
                action="cooldown_24h",
                reason="too many offers in 24h",
                risk_level="flagged",
            )

        if data.offers_24h_count >= 3:
            self.risk_service.create_risk_event(
                event_type="offer_frequency_watch",
                severity="low",
                user_id=data.user_id,
                payload=payload,
            )

            profile.risk_level = "watch"
            self.risk_service.db.commit()

            return RiskDecision(
                allowed=True,
                action="mark_watch",
                reason="user created multiple offers in 24h",
                risk_level="watch",
            )

        return RiskDecision(
            allowed=True,
            action="allow",
            reason="risk check passed",
            risk_level=profile.risk_level,
        )

    def check_match_offer(self, data: MatchOfferRiskInput) -> RiskDecision:
        profile = self.risk_service.get_or_create_profile(data.lender_id)

        if profile.is_blocked:
            return RiskDecision(
                allowed=False,
                action="blocked",
                reason=profile.block_reason or "lender is blocked",
                risk_level=profile.risk_level,
            )

        if profile.risk_level in ["restricted", "blocked"]:
            return RiskDecision(
                allowed=False,
                action="restricted",
                reason="lender is restricted from matching offers",
                risk_level=profile.risk_level,
            )

        if data.active_trades_count >= profile.max_active_trades:
            return RiskDecision(
                allowed=False,
                action="limit_active_trades",
                reason="active trade limit reached",
                risk_level=profile.risk_level,
            )

        return RiskDecision(
            allowed=True,
            action="allow",
            reason="match offer risk check passed",
            risk_level=profile.risk_level,
        )

    def on_offer_cancelled(self, user_id: UUID, matched: bool = False):
        profile = self.risk_service.get_or_create_profile(user_id)
        profile.cancel_count += 1
        if matched:
            profile.matched_cancel_count += 1
        self.risk_service.db.commit()

        self.risk_service.apply_score_change(
            user_id=user_id,
            score_delta=-10 if matched else -5,
            reason="offer cancelled",
            event_type="offer_cancelled",
        )

        if profile.cancel_count >= 5:
            self.risk_service.block_user(
                user_id=user_id,
                reason="too many cancellations",
                hours=None,
            )
        elif profile.cancel_count >= 3:
            self.risk_service.block_user(
                user_id=user_id,
                reason="cancelled offers 3 times",
                hours=24,
            )

    def on_lender_no_pay_timeout(self, lender_id: UUID, trade_id: UUID):
        self.risk_service.apply_score_change(
            user_id=lender_id,
            score_delta=-20,
            reason="lender did not pay within 24 hours",
            event_type="lender_no_pay_timeout",
            trade_id=trade_id,
        )

        self.risk_service.block_user(
            user_id=lender_id,
            reason="lender no payment timeout",
            hours=24,
        )

        self.risk_service.create_risk_event(
            event_type="lender_no_pay_timeout",
            severity="medium",
            user_id=lender_id,
            trade_id=trade_id,
            payload={"trade_id": str(trade_id)},
        )

    def on_repayment_overdue(self, data: RepaymentRiskInput) -> RiskDecision:
        raw = data.model_dump(mode="json") if hasattr(data, "model_dump") else data.dict()
        payload = json.loads(json.dumps(raw, default=str))
        profile = self.risk_service.get_or_create_profile(data.user_id)

        if data.overdue_days >= 7:
            profile.default_count += 1
            self.risk_service.db.commit()

            self.risk_service.apply_score_change(
                user_id=data.user_id,
                score_delta=-50,
                reason="repayment overdue more than 7 days",
                event_type="repayment_defaulted",
                trade_id=data.trade_id,
            )

            self.risk_service.create_risk_event(
                event_type="repayment_defaulted",
                severity="high",
                user_id=data.user_id,
                trade_id=data.trade_id,
                payload=payload,
            )

            profile.risk_level = "restricted"
            self.risk_service.db.commit()

            return RiskDecision(
                allowed=False,
                action="defaulted",
                reason="repayment overdue more than 7 days",
                risk_level="restricted",
                score_delta=-50,
            )

        profile.overdue_count += 1
        self.risk_service.db.commit()

        self.risk_service.apply_score_change(
            user_id=data.user_id,
            score_delta=-20,
            reason="repayment overdue",
            event_type="repayment_overdue",
            trade_id=data.trade_id,
        )

        self.risk_service.create_risk_event(
            event_type="repayment_overdue",
            severity="medium",
            user_id=data.user_id,
            trade_id=data.trade_id,
            payload=payload,
        )

        profile.risk_level = "watch"
        self.risk_service.db.commit()

        return RiskDecision(
            allowed=True,
            action="mark_overdue",
            reason="repayment overdue",
            risk_level="watch",
            score_delta=-20,
        )

    def on_repayment_paid(self, user_id: UUID, trade_id: UUID, early: bool = False):
        score_delta = 5 if early else 10
        self.risk_service.apply_score_change(
            user_id=user_id,
            score_delta=score_delta,
            reason="early repayment" if early else "on-time repayment",
            event_type="repayment_paid",
            trade_id=trade_id,
        )

