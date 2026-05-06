import hashlib
import hmac
import json
import os
import sys
import time
import urllib.parse
import uuid

from fastapi.testclient import TestClient


def build_init_data(*, bot_token: str, tg_user: dict) -> str:
    user_json = json.dumps(tg_user, separators=(",", ":"), ensure_ascii=False)
    data = {
        "auth_date": str(int(time.time())),
        "query_id": uuid.uuid4().hex,
        "user": user_json,
    }
    dcs = "\n".join(f"{k}={data[k]}" for k in sorted(data.keys()))
    secret_key = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
    data["hash"] = hmac.new(secret_key, dcs.encode(), hashlib.sha256).hexdigest()
    return urllib.parse.urlencode(data)


def test_v1_offer_create_and_list():
    db_path = f"./test_api_v1_{uuid.uuid4().hex}.sqlite"
    os.environ["DATABASE_URL"] = f"sqlite+pysqlite:///{db_path}"
    os.environ["SCHEDULER_ENABLED"] = "false"
    os.environ["BOT_TOKENS"] = "test-bot-token"
    os.environ["OTP_DEV_MODE"] = "true"

    for k in list(sys.modules.keys()):
        if k == "app" or k.startswith("app."):
            del sys.modules[k]

    import app.main

    init_data_a = build_init_data(bot_token="test-bot-token", tg_user={"id": 10001, "first_name": "A"})
    init_data_b = build_init_data(bot_token="test-bot-token", tg_user={"id": 10002, "first_name": "B"})
    headers_a = {"Authorization": f"tma {init_data_a}", "X-Lang": "cn"}
    headers_b = {"Authorization": f"tma {init_data_b}", "X-Lang": "cn"}

    with TestClient(app.main.app) as client:
        phone_a = "85512345678"
        phone_b = "85512345679"

        r = client.patch(
            "/api/v1/me/profile",
            headers=headers_a,
            json={"phone": phone_a, "aba_account": "a", "aba_name": "b", "language": "cn"},
        )
        assert r.status_code == 200
        assert r.json()["ok"] is True

        user_id_a = client.get("/api/v1/me", headers=headers_a).json()["data"]["id"]
        otp_req = client.post("/auth/otp/request", json={"user_id": user_id_a, "phone": phone_a})
        assert otp_req.status_code == 200
        code = otp_req.json().get("dev_code")
        assert code
        otp_ok = client.post("/auth/otp/verify", json={"user_id": user_id_a, "phone": phone_a, "code": code})
        assert otp_ok.status_code == 200

        r = client.patch(
            "/api/v1/me/profile",
            headers=headers_b,
            json={"phone": phone_b, "aba_account": "c", "aba_name": "d", "language": "cn"},
        )
        assert r.status_code == 200
        assert r.json()["ok"] is True

        r = client.post("/api/v1/offers", headers=headers_a, json={"amount": 100, "term_days": 7, "note": "e2e"})
        assert r.status_code == 200
        payload = r.json()
        assert payload["ok"] is True
        offer_id = payload["data"]["offer_id"]

        r = client.get("/api/v1/offers", headers=headers_b, params={"term_days": 7})
        assert r.status_code == 200
        payload = r.json()
        assert payload["ok"] is True
        assert any(o["id"] == offer_id for o in payload["data"])
