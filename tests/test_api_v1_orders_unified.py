import unittest

import os
import importlib
import json
import time
import hmac
import hashlib

from fastapi.testclient import TestClient


def make_init_data(bot_token: str, tg_id: int = 20001) -> str:
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


class TestApiV1UnifiedOrders(unittest.TestCase):
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

    def _complete_profile(self, user_id: str):
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

    def test_list_orders_contains_offer_and_application(self):
        app = self._boot()
        client = TestClient(app)

        init_data = make_init_data("test-bot-token")
        headers = {"Authorization": f"TMA {init_data}"}

        me = client.get("/api/v1/me", headers=headers)
        self.assertEqual(me.status_code, 200)
        user_id = me.json().get("data", {}).get("id")
        self.assertTrue(user_id)

        self._complete_profile(user_id)

        created_offer = client.post(
            "/api/v1/offers",
            headers=headers,
            json={"amount": 50, "term_days": 7, "note": ""},
        )
        self.assertEqual(created_offer.status_code, 200)

        created_app = client.post(
            "/api/v1/applications",
            headers=headers,
            json={"biz_type": "pledge", "payload": {"imei": "111", "amount": "80"}},
        )
        self.assertEqual(created_app.status_code, 200)

        res = client.get("/api/v1/orders", headers=headers)
        self.assertEqual(res.status_code, 200)
        data = res.json().get("data")
        self.assertIsInstance(data, list)
        source_types = {x.get("source_type") for x in data}
        self.assertIn("p2p_offer", source_types)
        self.assertIn("finance_application", source_types)

