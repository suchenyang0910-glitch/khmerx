import os
import sys
import uuid

from fastapi.testclient import TestClient


def test_telegram_start_webhook_dry_run():
    db_path = f"./test_tg_start_{uuid.uuid4().hex}.sqlite"
    os.environ["DATABASE_URL"] = f"sqlite+pysqlite:///{db_path}"
    os.environ["SCHEDULER_ENABLED"] = "false"
    os.environ["BOT_TOKENS"] = "test-bot-token"
    os.environ["OTP_DEV_MODE"] = "true"
    os.environ["TELEGRAM_SEND_DISABLED"] = "true"

    for k in list(sys.modules.keys()):
        if k == "app" or k.startswith("app."):
            del sys.modules[k]

    import app.main

    with TestClient(app.main.app) as client:
        r = client.post(
            "/telegram/webhook/test-bot-token",
            json={
                "update_id": 1,
                "message": {"message_id": 1, "chat": {"id": 123, "type": "private"}, "text": "/start"},
            },
        )
        assert r.status_code == 200
        body = r.json()
        assert body.get("ok") is True
        assert body.get("dry_run") is True

