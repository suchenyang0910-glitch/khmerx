from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.p2p_trade import P2PTrade
from app.models.user import User
from app.risk.engine import RiskEngine
from app.risk.models import Dispute, DisputeEvidence
from app.risk.service import RiskService
from app.services.notifications import create_notification, get_or_create_notification_settings


class DisputeService:
    def __init__(self, db: Session):
        self.db = db
        self.risk_service = RiskService(db)
        self.risk_engine = RiskEngine(self.risk_service)

    def create_dispute(self, current_user_id: UUID, payload):
        trade = self.db.query(P2PTrade).filter(P2PTrade.id == payload.trade_id).first()
        if not trade:
            raise HTTPException(status_code=404, detail="trade not found")

        if current_user_id not in [trade.borrower_id, trade.lender_id]:
            raise HTTPException(status_code=403, detail="not trade participant")

        existing = (
            self.db.query(Dispute)
            .filter(Dispute.trade_id == trade.id)
            .filter(Dispute.status.in_(["open", "reviewing"]))
            .first()
        )
        if existing:
            raise HTTPException(status_code=400, detail="active dispute already exists")

        raised_role = "borrower" if current_user_id == trade.borrower_id else "lender"
        priority = "high" if trade.amount >= 300 else "normal"
        old_status = trade.status
        trade.status = "dispute"

        dispute = Dispute(
            trade_id=trade.id,
            offer_id=trade.offer_id,
            borrower_id=trade.borrower_id,
            lender_id=trade.lender_id,
            raised_by_user_id=current_user_id,
            raised_role=raised_role,
            dispute_type=payload.dispute_type,
            reason=payload.reason,
            status="open",
            priority=priority,
        )

        self.db.add(dispute)
        self.db.commit()
        self.db.refresh(dispute)

        self.risk_service.create_risk_event(
            event_type="trade_dispute_opened",
            severity="high",
            user_id=current_user_id,
            trade_id=trade.id,
            offer_id=trade.offer_id,
            payload={
                "old_trade_status": old_status,
                "dispute_type": payload.dispute_type,
                "reason": payload.reason,
            },
        )

        other_user_id = trade.lender_id if current_user_id == trade.borrower_id else trade.borrower_id
        s_other = get_or_create_notification_settings(self.db, other_user_id)
        if s_other.dispute_updates:
            create_notification(
                self.db,
                user_id=other_user_id,
                type="dispute_opened",
                title="交易进入争议",
                body="对方已发起争议，请及时补充证据。",
                target_type="trade",
                target_id=str(trade.id),
            )

        return dispute

    def add_evidence(self, current_user_id: UUID, payload):
        dispute = self.db.query(Dispute).filter(Dispute.id == payload.dispute_id).first()
        if not dispute:
            raise HTTPException(status_code=404, detail="dispute not found")

        if current_user_id not in [dispute.borrower_id, dispute.lender_id]:
            raise HTTPException(status_code=403, detail="not dispute participant")

        uploaded_role = "borrower" if current_user_id == dispute.borrower_id else "lender"
        evidence = DisputeEvidence(
            dispute_id=dispute.id,
            uploaded_by_user_id=current_user_id,
            uploaded_role=uploaded_role,
            evidence_type=payload.evidence_type,
            file_url=payload.file_url,
            text_note=payload.text_note,
            meta=payload.metadata,
        )

        dispute.status = "reviewing"
        dispute.updated_at = datetime.now(timezone.utc)

        self.db.add(evidence)
        self.db.commit()
        self.db.refresh(evidence)

        other_user_id = dispute.lender_id if current_user_id == dispute.borrower_id else dispute.borrower_id
        s_other = get_or_create_notification_settings(self.db, other_user_id)
        if s_other.dispute_updates:
            create_notification(
                self.db,
                user_id=other_user_id,
                type="dispute_evidence",
                title="争议有新证据",
                body="对方已提交新证据，你可以继续补充或等待处理。",
                target_type="dispute",
                target_id=str(dispute.id),
            )
        return evidence

    def resolve_dispute(self, admin_user_id: UUID, payload):
        admin = self.db.query(User).filter(User.id == admin_user_id).first()
        if not admin or admin.role != "admin":
            raise HTTPException(status_code=403, detail="admin access required")

        dispute = self.db.query(Dispute).filter(Dispute.id == payload.dispute_id).first()
        if not dispute:
            raise HTTPException(status_code=404, detail="dispute not found")

        trade = self.db.query(P2PTrade).filter(P2PTrade.id == dispute.trade_id).first()
        if not trade:
            raise HTTPException(status_code=404, detail="trade not found")

        result = payload.resolution_result
        allowed = ["borrower_win", "lender_win", "both_fault", "cancel_trade", "manual_continue", "fraud"]
        if result not in allowed:
            raise HTTPException(status_code=400, detail="invalid resolution_result")

        dispute.status = "resolved"
        dispute.resolution_result = result
        dispute.resolution_note = payload.resolution_note
        dispute.resolved_by = admin_user_id
        dispute.resolved_at = datetime.now(timezone.utc)
        dispute.updated_at = datetime.now(timezone.utc)

        if result == "borrower_win":
            self.risk_service.apply_score_change(
                user_id=dispute.lender_id,
                score_delta=-50,
                reason="dispute lost: borrower win",
                event_type="dispute_lost",
                trade_id=trade.id,
                created_by="admin",
            )
            trade.status = "repaying"

        elif result == "lender_win":
            self.risk_service.apply_score_change(
                user_id=dispute.borrower_id,
                score_delta=-50,
                reason="dispute lost: lender win",
                event_type="dispute_lost",
                trade_id=trade.id,
                created_by="admin",
            )
            trade.status = "repaying"

        elif result == "both_fault":
            self.risk_service.apply_score_change(
                user_id=dispute.borrower_id,
                score_delta=-20,
                reason="dispute both fault",
                event_type="dispute_both_fault",
                trade_id=trade.id,
                created_by="admin",
            )
            self.risk_service.apply_score_change(
                user_id=dispute.lender_id,
                score_delta=-20,
                reason="dispute both fault",
                event_type="dispute_both_fault",
                trade_id=trade.id,
                created_by="admin",
            )
            trade.status = "repaying"

        elif result == "cancel_trade":
            trade.status = "cancelled"

        elif result == "manual_continue":
            trade.status = "repaying"

        elif result == "fraud":
            self.risk_service.block_user(
                user_id=dispute.borrower_id,
                reason="fraud confirmed",
                hours=None,
                created_by="admin",
            )
            trade.status = "cancelled"

        self.risk_service.create_risk_event(
            event_type="trade_dispute_resolved",
            severity="medium",
            user_id=dispute.raised_by_user_id,
            trade_id=trade.id,
            offer_id=trade.offer_id,
            payload={
                "result": result,
                "resolution_note": payload.resolution_note,
            },
        )

        self.db.commit()
        self.db.refresh(dispute)

        for uid in [dispute.borrower_id, dispute.lender_id]:
            s = get_or_create_notification_settings(self.db, uid)
            if not s.dispute_updates:
                continue
            create_notification(
                self.db,
                user_id=uid,
                type="dispute_resolved",
                title="争议已处理",
                body="争议已出结果，可在争议详情查看处理说明。",
                target_type="dispute",
                target_id=str(dispute.id),
            )
        return dispute

