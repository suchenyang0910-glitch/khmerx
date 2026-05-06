import unittest

import os
import sys

from fastapi.testclient import TestClient


class TestAdminApi(unittest.TestCase):
    def test_admin_login_and_announcements(self):
        db_path = "./test_admin_api.db"
        try:
            if os.path.exists(db_path):
                os.remove(db_path)
        except Exception:
            pass
        os.environ["DATABASE_URL"] = f"sqlite+pysqlite:///{db_path}"
        os.environ["ADMIN_USERNAME"] = "admin"
        os.environ["ADMIN_PASSWORD"] = "pass"
        os.environ["ADMIN_JWT_SECRET"] = "secret"

        for k in list(sys.modules.keys()):
            if k == "app" or k.startswith("app."):
                del sys.modules[k]

        import app.main

        with TestClient(app.main.app) as client:
            login = client.post("/api/admin/login", json={"username": "admin", "password": "pass"})
            self.assertEqual(login.status_code, 200)
            token = login.json().get("token")
            self.assertTrue(isinstance(token, str) and len(token) > 10)

            headers = {"Authorization": f"Bearer {token}"}
            res0 = client.get("/api/admin/announcements", headers=headers)
            self.assertEqual(res0.status_code, 200)
            self.assertEqual(res0.json(), [])

            created = client.post(
                "/api/admin/announcements",
                headers=headers,
                json={"lang": "km", "title": "Hello", "body": "World", "link_url": None, "active": True},
            )
            self.assertEqual(created.status_code, 200)
            created_id = created.json().get("id")
            self.assertTrue(isinstance(created_id, str) and len(created_id) > 10)

            res1 = client.get("/api/admin/announcements", headers=headers, params={"lang": "km"})
            self.assertEqual(res1.status_code, 200)
            self.assertEqual(len(res1.json()), 1)

            risk_events = client.get("/api/admin/risk/events", headers=headers)
            self.assertEqual(risk_events.status_code, 200)

        try:
            if os.path.exists(db_path):
                os.remove(db_path)
        except Exception:
            pass
