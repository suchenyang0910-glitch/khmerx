import unittest
import os
import sys

from fastapi.testclient import TestClient


class TestAdminReportsExports(unittest.TestCase):
    def test_reports_and_csv_exports(self):
        db_path = "./test_admin_reports.db"
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
            headers = {"Authorization": f"Bearer {token}"}

            o = client.get("/api/admin/reports/overview", headers=headers)
            self.assertEqual(o.status_code, 200)
            self.assertIn("users", o.json())

            t = client.get("/api/admin/reports/trends", headers=headers)
            self.assertEqual(t.status_code, 200)
            self.assertIn("users_new", t.json())

            u = client.get("/api/admin/exports/users.csv", headers=headers)
            self.assertEqual(u.status_code, 200)
            self.assertTrue(u.headers.get("content-type", "").startswith("text/csv"))

            tr = client.get("/api/admin/exports/orders.csv", headers=headers)
            self.assertEqual(tr.status_code, 200)
            self.assertTrue(tr.headers.get("content-type", "").startswith("text/csv"))

            r = client.get("/api/admin/exports/risk-events.csv", headers=headers)
            self.assertEqual(r.status_code, 200)
            self.assertTrue(r.headers.get("content-type", "").startswith("text/csv"))

        try:
            if os.path.exists(db_path):
                os.remove(db_path)
        except Exception:
            pass

