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


def test_dispute_add_evidence_body_without_dispute_id():
    db_path = f"./test_api_v1_{uuid.uuid4().hex}.sqlite"
    os.environ["DATABASE_URL"] = f"sqlite+pysqlite:///{db_path}"
    os.environ["SCHEDULER_ENABLED"] = "false"
    os.environ["BOT_TOKENS"] = "test-bot-token"
    os.environ["OTP_DEV_MODE"] = "true"

    for k in list(sys.modules.keys()):
        if k == "app" or k.startswith("app."):
            del sys.modules[k]

    import app.main

    init_a = build_init_data(bot_token="test-bot-token", tg_user={"id": 10001, "first_name": "A"})
    init_b = build_init_data(bot_token="test-bot-token", tg_user={"id": 10002, "first_name": "B"})
    h_a = {"Authorization": f"tma {init_a}", "X-Lang": "cn"}
    h_b = {"Authorization": f"tma {init_b}", "X-Lang": "cn"}

    with TestClient(app.main.app) as client:
        phone_a = "85512345678"
        phone_b = "85512345679"

        client.patch("/api/v1/me/profile", headers=h_a, json={"phone": phone_a, "aba_account": "a", "aba_name": "b", "language": "cn"})
        user_id_a = client.get("/api/v1/me", headers=h_a).json()["data"]["id"]
        code = client.post("/auth/otp/request", json={"user_id": user_id_a, "phone": phone_a}).json().get("dev_code")
        client.post("/auth/otp/verify", json={"user_id": user_id_a, "phone": phone_a, "code": code})

        client.patch("/api/v1/me/profile", headers=h_b, json={"phone": phone_b, "aba_account": "c", "aba_name": "d", "language": "cn"})
        user_id_b = client.get("/api/v1/me", headers=h_b).json()["data"]["id"]
        code2 = client.post("/auth/otp/request", json={"user_id": user_id_b, "phone": phone_b}).json().get("dev_code")
        client.post("/auth/otp/verify", json={"user_id": user_id_b, "phone": phone_b, "code": code2})

        offer = client.post("/api/v1/offers", headers=h_a, json={"amount": 100, "term_days": 7, "note": ""}).json()["data"]
        match = client.post(f"/api/v1/offers/{offer['offer_id']}/match", headers=h_b, json={"confirm_risk": True}).json()["data"]
        trade_id = match["trade_id"]

        d = client.post("/api/v1/disputes", headers=h_a, json={"trade_id": trade_id, "dispute_type": "trade", "reason": "no receive"})
        assert d.status_code == 200
        dispute_id = d.json()["data"]["id"]

        ev = client.post(
            f"/api/v1/disputes/{dispute_id}/evidence",
            headers=h_a,
            json={"evidence_type": "proof", "file_url": "https://example.com/proof.png", "metadata": {}},
        )
        assert ev.status_code == 200
        assert ev.json()["ok"] is True

