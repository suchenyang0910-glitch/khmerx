import hashlib
import hmac
import json
import os
import sys
import time
import urllib.parse
import uuid

import httpx


def build_init_data(*, bot_token: str, tg_user: dict, auth_date: int | None = None) -> str:
    if auth_date is None:
        auth_date = int(time.time())

    user_json = json.dumps(tg_user, separators=(",", ":"), ensure_ascii=False)
    data = {
        "auth_date": str(auth_date),
        "query_id": uuid.uuid4().hex,
        "user": user_json,
    }

    data_check_string = "\n".join(f"{k}={data[k]}" for k in sorted(data.keys()))
    secret_key = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
    received_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    data["hash"] = received_hash
    return urllib.parse.urlencode(data)


def tma_headers(init_data: str) -> dict:
    return {"Authorization": f"tma {init_data}", "X-Lang": "cn"}


def assert_ok(res: httpx.Response) -> dict:
    try:
        payload = res.json()
    except Exception:
        raise RuntimeError(f"http={res.status_code} content_type={res.headers.get('content-type')} body={res.text[:800]}")
    if not payload.get("ok"):
        raise RuntimeError(f"http={res.status_code} body={payload}")
    return payload


def main() -> int:
    root_url = os.getenv("KHX_ROOT", "http://127.0.0.1:3030").rstrip("/")
    base_url = os.getenv("KHX_V1_BASE", f"{root_url}/api/v1").rstrip("/")
    auth_url = os.getenv("KHX_AUTH_BASE", f"{root_url}/auth").rstrip("/")
    bot_token = os.getenv("KHX_TEST_BOT_TOKEN", "test-bot-token")

    now_tag = int(time.time())
    borrower_tg_id = 80000000 + (now_tag % 10000000)
    lender_tg_id = borrower_tg_id + 1

    borrower_init = build_init_data(
        bot_token=bot_token,
        tg_user={"id": borrower_tg_id, "first_name": "Borrower", "username": f"borrower{borrower_tg_id}"},
    )
    lender_init = build_init_data(
        bot_token=bot_token,
        tg_user={"id": lender_tg_id, "first_name": "Lender", "username": f"lender{lender_tg_id}"},
    )

    with httpx.Client(timeout=30) as client:
        me_a = assert_ok(client.get(f"{base_url}/me", headers=tma_headers(borrower_init)))["data"]
        me_b = assert_ok(client.get(f"{base_url}/me", headers=tma_headers(lender_init)))["data"]

        otp_a = client.post(f"{auth_url}/otp/request", json={"user_id": me_a["id"], "phone": "012345678"})
        otp_a_payload = otp_a.json()
        otp_a_code = otp_a_payload.get("dev_code")
        if not otp_a_code:
            raise RuntimeError("OTP dev_code missing; set OTP_DEV_MODE=true for local test")
        client.post(f"{auth_url}/otp/verify", json={"user_id": me_a["id"], "phone": "012345678", "code": otp_a_code})

        otp_b = client.post(f"{auth_url}/otp/request", json={"user_id": me_b["id"], "phone": "098765432"})
        otp_b_payload = otp_b.json()
        otp_b_code = otp_b_payload.get("dev_code")
        if not otp_b_code:
            raise RuntimeError("OTP dev_code missing; set OTP_DEV_MODE=true for local test")
        client.post(f"{auth_url}/otp/verify", json={"user_id": me_b["id"], "phone": "098765432", "code": otp_b_code})

        assert_ok(
            client.patch(
                f"{base_url}/me/profile",
                headers=tma_headers(borrower_init),
                json={
                    "aba_account": "001234567",
                    "aba_name": "BORROWER",
                    "language": "cn",
                },
            )
        )
        assert_ok(
            client.patch(
                f"{base_url}/me/profile",
                headers=tma_headers(lender_init),
                json={
                    "aba_account": "009876543",
                    "aba_name": "LENDER",
                    "language": "cn",
                },
            )
        )

        calc = assert_ok(
            client.post(
                f"{base_url}/p2p/calculate",
                headers=tma_headers(borrower_init),
                json={"amount": 100, "term_days": 7},
            )
        )["data"]
        if "received_amount" not in calc or "repay_amount" not in calc:
            raise RuntimeError(f"calculate invalid: {calc}")

        offer = assert_ok(
            client.post(
                f"{base_url}/offers",
                headers=tma_headers(borrower_init),
                json={"amount": 100, "term_days": 7, "note": "e2e"},
            )
        )["data"]
        offer_id = offer["offer_id"]

        offers = assert_ok(
            client.get(
                f"{base_url}/offers",
                headers=tma_headers(lender_init),
                params={"tab": "recommended", "term_days": 7},
            )
        )["data"]
        if not any(o["id"] == offer_id for o in offers):
            raise RuntimeError("offer not visible in market")

        match = assert_ok(
            client.post(
                f"{base_url}/offers/{offer_id}/match",
                headers=tma_headers(lender_init),
                json={"confirm_risk": True},
            )
        )["data"]
        trade_id = match["trade_id"]

        lend_file = ("lend.png", b"lend-proof", "image/png")
        proof_url = assert_ok(
            client.post(
                f"{base_url}/uploads/proof",
                headers=tma_headers(lender_init),
                params={"purpose": "lend", "trade_id": trade_id},
                files={"file": lend_file},
            )
        )["data"]["url"]

        assert_ok(
            client.post(
                f"{base_url}/trades/{trade_id}/confirm-lend",
                headers=tma_headers(lender_init),
                json={"proof_url": proof_url, "amount": 100, "note": "paid"},
            )
        )

        assert_ok(
            client.post(
                f"{base_url}/trades/{trade_id}/confirm-receive",
                headers=tma_headers(borrower_init),
                json={"confirmed": True},
            )
        )

        trade = assert_ok(client.get(f"{base_url}/trades/{trade_id}", headers=tma_headers(borrower_init)))[
            "data"
        ]
        schedules = trade.get("repayment_schedules") or []
        if not schedules:
            raise RuntimeError(f"repayment_schedules missing: {trade}")
        schedule_id = schedules[0]["id"]

        repay_file = ("repay.png", b"repay-proof", "image/png")
        repay_proof_url = assert_ok(
            client.post(
                f"{base_url}/uploads/proof",
                headers=tma_headers(borrower_init),
                params={"purpose": "repay", "trade_id": trade_id},
                files={"file": repay_file},
            )
        )["data"]["url"]

        assert_ok(
            client.post(
                f"{base_url}/trades/{trade_id}/repay",
                headers=tma_headers(borrower_init),
                json={
                    "schedule_id": schedule_id,
                    "proof_url": repay_proof_url,
                    "amount": schedules[0]["total"],
                    "note": "repay",
                },
            )
        )

        assert_ok(
            client.post(
                f"{base_url}/trades/{trade_id}/confirm-repayment",
                headers=tma_headers(lender_init),
                json={"schedule_id": schedule_id, "confirmed": True},
            )
        )

        trade2 = assert_ok(client.get(f"{base_url}/trades/{trade_id}", headers=tma_headers(borrower_init)))[
            "data"
        ]
        if trade2.get("status") not in ("completed", "repaying", "repayment_confirmed"):
            raise RuntimeError(f"unexpected trade status: {trade2.get('status')} trade={trade2}")

    sys.stdout.write(
        json.dumps(
            {
                "borrower_id": me_a.get("id"),
                "lender_id": me_b.get("id"),
                "offer_id": offer_id,
                "trade_id": trade_id,
                "final_status": trade2.get("status"),
            },
            ensure_ascii=False,
        )
        + "\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
