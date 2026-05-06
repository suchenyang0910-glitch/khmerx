import unittest

import os
import importlib

from fastapi.testclient import TestClient


class TestApiV1Auth(unittest.TestCase):
    def test_me_requires_auth(self):
        os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
        import app.config
        import app.database
        import app.main

        importlib.reload(app.config)
        importlib.reload(app.database)
        importlib.reload(app.main)

        app = app.main.app

        client = TestClient(app)
        res = client.get("/api/v1/me")
        self.assertEqual(res.status_code, 401)
        body = res.json()
        self.assertFalse(body.get("ok"))
        self.assertEqual(body.get("error", {}).get("code"), "AUTH_REQUIRED")
