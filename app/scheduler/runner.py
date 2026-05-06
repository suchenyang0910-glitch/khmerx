from __future__ import annotations

import os
import logging

from app.database import get_session_local
from app.scheduler.jobs import (
    auto_unblock_users,
    check_lender_payment_timeout,
    check_repayment_overdue,
    generate_daily_risk_summary,
    generate_repayment_due_reminders,
)


logger = logging.getLogger(__name__)


def run_job(job_func):
    SessionLocal = get_session_local()
    db = SessionLocal()
    try:
        job_func(db)
    finally:
        db.close()


def start_scheduler():
    enabled = os.getenv("SCHEDULER_ENABLED", "true").lower() == "true"
    if not enabled:
        return None

    try:
        from apscheduler.schedulers.background import BackgroundScheduler
    except Exception as e:
        logger.warning("scheduler disabled: %s", e)
        return None

    scheduler = BackgroundScheduler(timezone="UTC")

    scheduler.add_job(
        lambda: run_job(check_lender_payment_timeout),
        "interval",
        minutes=5,
        id="check_lender_payment_timeout",
        replace_existing=True,
    )

    scheduler.add_job(
        lambda: run_job(check_repayment_overdue),
        "interval",
        minutes=30,
        id="check_repayment_overdue",
        replace_existing=True,
    )

    scheduler.add_job(
        lambda: run_job(generate_repayment_due_reminders),
        "interval",
        minutes=30,
        id="generate_repayment_due_reminders",
        replace_existing=True,
    )

    scheduler.add_job(
        lambda: run_job(auto_unblock_users),
        "interval",
        minutes=10,
        id="auto_unblock_users",
        replace_existing=True,
    )

    scheduler.add_job(
        lambda: run_job(generate_daily_risk_summary),
        "cron",
        hour=23,
        minute=55,
        id="generate_daily_risk_summary",
        replace_existing=True,
    )

    scheduler.start()
    return scheduler

