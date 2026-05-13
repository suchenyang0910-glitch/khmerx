import unittest

from pathlib import Path
import uuid

from fastapi.testclient import TestClient


class TestIntegrationRequests(unittest.TestCase):
    def _client(self):
        import app.database
        import app.database

        db_file = Path(__file__).parent / f".tmp_integration_{uuid.uuid4().hex}.sqlite"
        new_url = f"sqlite+pysqlite:///{db_file.as_posix()}"

        old_url = app.database.DATABASE_URL
        app.database.DATABASE_URL = new_url
        app.database._engine = None
        app.database._SessionLocal = None
        app.database.init_db()

        client = TestClient(app.main.app)

        def cleanup():
            try:
                client.close()
            finally:
                app.database.DATABASE_URL = old_url
                app.database._engine = None
                app.database._SessionLocal = None

        self.addCleanup(cleanup)
        return client

    def test_create_integration_request_success(self):
        client = self._client()
        res = client.post(
            "/api/integration-requests",
            json={
                "applicantType": "company",
                "orgName": "Example Co.",
                "contactName": "Alice",
                "email": "alice@example.com",
                "telegram": "@alice",
                "useCase": "Need risk score",
                "interestedApis": ["risk_score"],
                "consent": True,
                "source": "/zh/api#auth",
            },
        )
        self.assertEqual(res.status_code, 200)
        body = res.json()
        self.assertTrue(body.get("ok"))
        self.assertTrue(isinstance(body.get("requestId"), str))
        self.assertGreater(len(body.get("requestId")), 10)

    def test_create_integration_request_requires_contact_channel(self):
        client = self._client()
        res = client.post(
            "/api/integration-requests",
            json={
                "applicantType": "company",
                "orgName": "Example Co.",
                "contactName": "Alice",
                "email": "alice@example.com",
                "useCase": "Need risk score",
                "interestedApis": ["risk_score"],
                "consent": True,
            },
        )
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json().get("detail"), "phone_or_telegram_required")

    def test_create_integration_request_invalid_email(self):
        client = self._client()
        res = client.post(
            "/api/integration-requests",
            json={
                "applicantType": "company",
                "orgName": "Example Co.",
                "contactName": "Alice",
                "email": "not-an-email",
                "telegram": "@alice",
                "useCase": "Need risk score",
                "interestedApis": ["risk_score"],
                "consent": True,
            },
        )
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json().get("detail"), "invalid_email")
