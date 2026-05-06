"""
还款提醒服务 — KhmerX ABA 微借贷

功能：
- 每天检查快到期的还款
- 检查逾期的还款
- 发送通知（先打 log，后续接 TG Bot）
"""
import logging
from datetime import datetime, timezone, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.repayment_schedule import RepaymentSchedule
from app.models.p2p_trade import P2PTrade
from app.models.user import User
from app.config import OVERDUE_DAYS_LIMIT

logger = logging.getLogger(__name__)


class ReminderService:
    """还款提醒服务"""

    @staticmethod
    def check_upcoming_repayments(db: Session, hours_before: int = 24) -> list:
        """
        检查未来 hours_before 小时内到期的还款
        返回需要提醒的还款记录列表
        """
        now = datetime.now(timezone.utc)
        deadline = now + timedelta(hours=hours_before)

        schedules = db.query(RepaymentSchedule).filter(
            and_(
                RepaymentSchedule.status == "pending",
                RepaymentSchedule.due_at <= deadline,
                RepaymentSchedule.due_at > now,
            )
        ).all()

        reminders = []
        for s in schedules:
            trade = db.query(P2PTrade).filter(P2PTrade.id == s.trade_id).first()
            borrower = db.query(User).filter(User.id == trade.borrower_id).first() if trade else None

            reminder = {
                "schedule_id": str(s.id),
                "trade_id": str(s.trade_id),
                "borrower_id": str(trade.borrower_id) if trade else "",
                "borrower_name": borrower.name if borrower else "",
                "period": s.period,
                "total_due": s.total,
                "due_at": s.due_at.isoformat(),
                "hours_remaining": round((s.due_at - now).total_seconds() / 3600, 1),
            }
            reminders.append(reminder)

            ReminderService.send_notification(
                trade.borrower_id if trade else None,
                f"⏰ 还款提醒：您有一笔借款第{s.period}期即将到期，"
                f"应还 ${s.total:.2f}，到期时间 {s.due_at.strftime('%Y-%m-%d %H:%M')}"
            )

        return reminders

    @staticmethod
    def check_overdue_repayments(db: Session) -> list:
        """
        检查已逾期的还款
        返回逾期记录列表
        """
        now = datetime.now(timezone.utc)

        schedules = db.query(RepaymentSchedule).filter(
            and_(
                RepaymentSchedule.status == "pending",
                RepaymentSchedule.due_at <= now,
            )
        ).all()

        overdue_records = []
        for s in schedules:
            # 标记为逾期
            s.status = "overdue"

            trade = db.query(P2PTrade).filter(P2PTrade.id == s.trade_id).first()

            # 检查是否超过违约天数
            days_overdue = (now - s.due_at).days if s.due_at else 0

            record = {
                "schedule_id": str(s.id),
                "trade_id": str(s.trade_id),
                "borrower_id": str(trade.borrower_id) if trade else "",
                "period": s.period,
                "total_due": s.total,
                "days_overdue": days_overdue,
                "due_at": s.due_at.isoformat() if s.due_at else "",
            }
            overdue_records.append(record)

            # 严重逾期 → 标记为违约
            if days_overdue >= OVERDUE_DAYS_LIMIT and trade:
                trade.status = "defaulted"
                logger.warning(
                    f"Trade {trade.id} marked as defaulted: "
                    f"{days_overdue} days overdue"
                )

            ReminderService.send_notification(
                trade.borrower_id if trade else None,
                f"⚠️ 逾期提醒：您有一笔还款已逾期 {days_overdue} 天！"
                f"第{s.period}期应还 ${s.total:.2f}，请尽快处理"
            )

        db.commit()
        return overdue_records

    @staticmethod
    def check_pending_repayments(db: Session) -> dict:
        """
        综合检查：即将到期 + 已逾期
        返回汇总结果
        """
        upcoming = ReminderService.check_upcoming_repayments(db)
        overdue = ReminderService.check_overdue_repayments(db)

        logger.info(
            f"Repayment check complete: {len(upcoming)} upcoming, "
            f"{len(overdue)} overdue"
        )

        return {
            "upcoming_reminders": upcoming,
            "overdue_records": overdue,
            "total_upcoming": len(upcoming),
            "total_overdue": len(overdue),
        }

    @staticmethod
    def send_notification(user_id, message: str):
        """
        发送通知（先打 log，后续接 TG Bot）
        """
        logger.info(f"[NOTIFICATION] User {user_id}: {message}")
        # TODO: 集成 TG Bot 推送


print("=== Task 2.2 done ===")
