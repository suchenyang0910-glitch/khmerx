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


def build_contact_response(*, bot_token: str, contact: dict) -> str:
    contact_json = json.dumps(contact, separators=(",", ":"), ensure_ascii=False)
    data = {
        "auth_date": str(int(time.time())),
        "contact": contact_json,
    }
    dcs = "\n".join(f"{k}={data[k]}" for k in sorted(data.keys()))
    secret_key = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
    data["hash"] = hmac.new(secret_key, dcs.encode(), hashlib.sha256).hexdigest()
    return urllib.parse.urlencode(data)


def test_phone_verify_via_telegram_contact():
    db_path = f"./test_api_v1_{uuid.uuid4().hex}.sqlite"
    os.environ["DATABASE_URL"] = f"sqlite+pysqlite:///{db_path}"
    os.environ["SCHEDULER_ENABLED"] = "false"
    os.environ["BOT_TOKENS"] = "test-bot-token"

    for k in list(sys.modules.keys()):
        if k == "app" or k.startswith("app."):
            del sys.modules[k]

    import app.main

    init_data = build_init_data(bot_token="test-bot-token", tg_user={"id": 12345, "first_name": "A"})
    headers = {"Authorization": f"tma {init_data}", "X-Lang": "cn"}

    response = build_contact_response(
        bot_token="test-bot-token",
        contact={"user_id": 12345, "phone_number": "85512345678", "first_name": "A"},
    )

    with TestClient(app.main.app) as client:
        r = client.post("/api/v1/me/phone/verify-telegram", headers=headers, json={"response": response})
        assert r.status_code == 200
        payload = r.json()
        assert payload["ok"] is True
        assert payload["data"]["phone_verified"] is True

        me = client.get("/api/v1/me", headers=headers)
        assert me.status_code == 200
        assert me.json()["data"]["phone_verified"] is True

