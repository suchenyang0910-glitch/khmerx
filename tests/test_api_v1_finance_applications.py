import unittest

import os
import importlib
import json
import time
import hmac
import hashlib

from fastapi.testclient import TestClient


def make_init_data(bot_token: str, tg_id: int = 10001) -> str:
    user = {
        "id": tg_id,
        "first_name": "Test",
        "last_name": "User",
        "username": "testuser",
    }
    user_json = json.dumps(user, separators=(",", ":"))
    data_dict = {
        "auth_date": str(int(time.time())),
        "query_id": "AAEAA",
        "user": user_json,
    }

    sorted_keys = sorted(data_dict.keys())
    data_check_string = "\n".join([f"{k}={data_dict[k]}" for k in sorted_keys])
    secret_key = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
    expected_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    parts = [
        f"auth_date={data_dict['auth_date']}",
        f"query_id={data_dict['query_id']}",
        f"user={user_json}",
        f"hash={expected_hash}",
    ]
    return "&".join(parts)


class TestApiV1FinanceApplications(unittest.TestCase):
    def _boot(self):
        os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
        os.environ["BOT_TOKENS"] = "test-bot-token"

        import app.config
        import app.database
        import app.api_v1.auth
        import app.api_v1.router
        import app.main

        importlib.reload(app.config)
        importlib.reload(app.database)
        importlib.reload(app.api_v1.auth)
        importlib.reload(app.api_v1.router)
        importlib.reload(app.main)

        app.database.init_db()
        return app.main.app

    def test_create_requires_profile_completed(self):
        app = self._boot()
        client = TestClient(app)

        init_data = make_init_data("test-bot-token")
        headers = {"Authorization": f"TMA {init_data}"}

        res = client.post(
            "/api/v1/applications",
            headers=headers,
            json={"biz_type": "lease", "payload": {"amount": "100"}},
        )
        self.assertEqual(res.status_code, 403)
        body = res.json()
        self.assertFalse(body.get("ok"))
        self.assertEqual(body.get("error", {}).get("code"), "PROFILE_INCOMPLETE")

    def test_create_and_list_and_get(self):
        app = self._boot()
        client = TestClient(app)

        init_data = make_init_data("test-bot-token")
        headers = {"Authorization": f"TMA {init_data}"}

        me = client.get("/api/v1/me", headers=headers)
        self.assertEqual(me.status_code, 200)
        user_id = me.json().get("data", {}).get("id")
        self.assertTrue(user_id)

        import app.database
        from app.models.user import User

        SessionLocal = app.database.get_session_local()
        db = SessionLocal()
        try:
            u = db.query(User).filter(User.id == user_id).first()
            u.phone = "012345678"
            u.phone_verified_at = app.database.datetime.now(app.database.timezone.utc)
            u.aba_account = "000000"
            u.aba_name = "TEST"
            db.commit()
        finally:
            db.close()

        created = client.post(
            "/api/v1/applications",
            headers=headers,
            json={"biz_type": "pledge", "payload": {"imei": "111", "amount": "80"}},
        )
        self.assertEqual(created.status_code, 200)
        created_id = created.json().get("data", {}).get("id")
        self.assertTrue(created_id)

        lst = client.get("/api/v1/applications", headers=headers)
        self.assertEqual(lst.status_code, 200)
        data = lst.json().get("data")
        self.assertIsInstance(data, list)
        self.assertTrue(any(x.get("id") == created_id for x in data))

        detail = client.get(f"/api/v1/applications/{created_id}", headers=headers)
        self.assertEqual(detail.status_code, 200)
        self.assertEqual(detail.json().get("data", {}).get("id"), created_id)
