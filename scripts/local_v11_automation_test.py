import hashlib
import hmac
import json
import os
import sys
import time
import urllib.parse
import uuid
from datetime import datetime, timedelta, timezone

from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import httpx


def build_init_data(*, bot_token: str, tg_user: dict, auth_date: int | None = None) -> str:
    if auth_date is None:
        auth_date = int(time.time())
    user_json = json.dumps(tg_user, separators=(",", ":"), ensure_ascii=False)
    data = {"auth_date": str(auth_date), "query_id": uuid.uuid4().hex, "user": user_json}
    dcs = "\n".join(f"{k}={data[k]}" for k in sorted(data.keys()))
    secret_key = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
    data["hash"] = hmac.new(secret_key, dcs.encode(), hashlib.sha256).hexdigest()
    return urllib.parse.urlencode(data)


def tma_headers(init_data: str) -> dict:
    return {"Authorization": f"tma {init_data}", "X-Lang": "cn"}


def assert_ok(res: httpx.Response) -> dict:
    try:
        payload = res.json()
    except Exception:
        raise RuntimeError(
            f"http={res.status_code} content_type={res.headers.get('content-type')} body={res.text[:800]}"
        )
    if not payload.get("ok"):
        raise RuntimeError(f"http={res.status_code} body={payload}")
    return payload


def main() -> int:
    root_url = os.getenv("KHX_ROOT", "http://127.0.0.1:3030").rstrip("/")
    v1 = f"{root_url}/api/v1"
    auth = f"{root_url}/auth"
    bot_token = os.getenv("KHX_TEST_BOT_TOKEN", "test-bot-token")

    os.environ.setdefault("DATABASE_URL", os.getenv("KHX_DB_URL", "sqlite:///./khmerx_local.db"))

    now_tag = int(time.time())
    borrower_tg_id = 90000000 + (now_tag % 10000000)
    lender_tg_id = borrower_tg_id + 1
    borrower_init = build_init_data(bot_token=bot_token, tg_user={"id": borrower_tg_id, "first_name": "BorrowerV11"})
    lender_init = build_init_data(bot_token=bot_token, tg_user={"id": lender_tg_id, "first_name": "LenderV11"})

    with httpx.Client(timeout=30) as client:
        me_a = assert_ok(client.get(f"{v1}/me", headers=tma_headers(borrower_init)))["data"]
        me_b = assert_ok(client.get(f"{v1}/me", headers=tma_headers(lender_init)))["data"]

        otp_a = client.post(f"{auth}/otp/request", json={"user_id": me_a["id"], "phone": "011000001"}).json()
        otp_b = client.post(f"{auth}/otp/request", json={"user_id": me_b["id"], "phone": "011000002"}).json()
        if not otp_a.get("dev_code") or not otp_b.get("dev_code"):
            raise RuntimeError("OTP dev_code missing; set OTP_DEV_MODE=true")
        client.post(
            f"{auth}/otp/verify",
            json={"user_id": me_a["id"], "phone": "011000001", "code": otp_a["dev_code"]},
        )
        client.post(
            f"{auth}/otp/verify",
            json={"user_id": me_b["id"], "phone": "011000002", "code": otp_b["dev_code"]},
        )

        assert_ok(
            client.patch(
                f"{v1}/me/profile",
                headers=tma_headers(borrower_init),
                json={"aba_account": "011000001", "aba_name": "BORROWER", "language": "cn"},
            )
        )
        assert_ok(
            client.patch(
                f"{v1}/me/profile",
                headers=tma_headers(lender_init),
                json={"aba_account": "011000002", "aba_name": "LENDER", "language": "cn"},
            )
        )

        offer = assert_ok(
            client.post(
                f"{v1}/offers",
                headers=tma_headers(borrower_init),
                json={"amount": 50, "term_days": 7, "note": "v11-timeout"},
            )
        )["data"]
        offer_id = offer["offer_id"]
        match = assert_ok(
            client.post(
                f"{v1}/offers/{offer_id}/match",
                headers=tma_headers(lender_init),
                json={"confirm_risk": True},
            )
        )["data"]
        trade_id = match["trade_id"]

    from app.database import get_session_local
    from app.models.notification import Notification
    from app.models.p2p_trade import P2PTrade
    from app.models.repayment_schedule import RepaymentSchedule
    from app.scheduler.jobs import check_lender_payment_timeout, check_repayment_overdue

    SessionLocal = get_session_local()
    db = SessionLocal()
    try:
        def utcnow_naive() -> datetime:
            return datetime.now(timezone.utc).replace(tzinfo=None)

        tid = uuid.UUID(trade_id)
        trade = db.query(P2PTrade).filter(P2PTrade.id == tid).first()
        if not trade:
            raise RuntimeError("trade not found")
        trade.advance_pay_deadline = utcnow_naive() - timedelta(minutes=1)
        db.commit()

        before_n = db.query(Notification).filter(Notification.target_type == "trade").filter(Notification.target_id == trade_id).count()
        check_lender_payment_timeout(db)
        db.refresh(trade)
        after_n = db.query(Notification).filter(Notification.target_type == "trade").filter(Notification.target_id == trade_id).count()
        if trade.status != "cancelled":
            raise RuntimeError(f"timeout not applied: {trade.status}")
        if after_n <= before_n:
            raise RuntimeError("timeout notification missing")

        schedules = db.query(RepaymentSchedule).filter(RepaymentSchedule.trade_id == tid).all()
        if not schedules:
            raise RuntimeError("repayment schedule missing")
        s = schedules[0]
        s.status = "pending"
        s.due_at = utcnow_naive() - timedelta(days=2)
        trade.status = "repayment_confirmed"
        db.commit()

        before_o = (
            db.query(Notification)
            .filter(Notification.user_id == trade.borrower_id)
            .filter(Notification.type == "repayment_overdue")
            .count()
        )
        check_repayment_overdue(db)
        db.refresh(s)
        after_o = (
            db.query(Notification)
            .filter(Notification.user_id == trade.borrower_id)
            .filter(Notification.type == "repayment_overdue")
            .count()
        )
        if s.status != "overdue":
            raise RuntimeError(f"overdue not applied: {s.status}")
        if after_o <= before_o:
            raise RuntimeError("overdue notification missing")

    finally:
        db.close()

    sys.stdout.write(json.dumps({"ok": True, "trade_id": trade_id}, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
