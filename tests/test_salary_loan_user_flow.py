import unittest

import os
import sys

from fastapi.testclient import TestClient


class TestSalaryLoanUserFlow(unittest.TestCase):
    def test_salary_loan_apply_and_upload_proof(self):
        db_path = "./test_salary_loan_user_flow.db"
        try:
            if os.path.exists(db_path):
                os.remove(db_path)
        except Exception:
            pass

        os.environ["DATABASE_URL"] = f"sqlite+pysqlite:///{db_path}"
        os.environ["BOT_TOKENS"] = "test-bot-token"
        os.environ["DEV_TMA_ENABLED"] = "true"
        os.environ["OTP_DEV_MODE"] = "true"
        os.environ["SCHEDULER_ENABLED"] = "false"

        for k in list(sys.modules.keys()):
            if k == "app" or k.startswith("app."):
                del sys.modules[k]

        import app.main

        with TestClient(app.main.app) as client:
            dev = client.get("/auth/dev-tma", params={"tg_id": 90123456})
            self.assertEqual(dev.status_code, 200)
            init_data = dev.json().get("data", {}).get("init_data")
            self.assertTrue(isinstance(init_data, str) and len(init_data) > 10)

            headers = {"Authorization": f"TMA {init_data}"}

            me = client.get("/api/v1/me", headers=headers)
            self.assertEqual(me.status_code, 200)
            user_id = me.json().get("data", {}).get("id")
            self.assertTrue(user_id)

            patch = client.patch(
                "/api/v1/me/profile",
                headers=headers,
                json={"aba_account": "888888", "aba_name": "E2E"},
            )
            self.assertEqual(patch.status_code, 200)

            otp_req = client.post("/auth/otp/request", json={"user_id": user_id, "phone": "088888888"})
            self.assertEqual(otp_req.status_code, 200)
            code = otp_req.json().get("dev_code")
            challenge_id = otp_req.json().get("challenge_id")
            self.assertTrue(code and challenge_id)

            otp_verify = client.post(
                "/auth/otp/verify",
                json={"user_id": user_id, "phone": "088888888", "code": code, "challenge_id": challenge_id},
            )
            self.assertEqual(otp_verify.status_code, 200)

            import app.database
            from app.models.salary_factory import SalaryFactory

            SessionLocal = app.database.get_session_local()
            db = SessionLocal()
            try:
                f = SalaryFactory(name="Factory A", location="PP", risk_level="B", is_active=True)
                db.add(f)
                db.commit()
                factory_id = str(f.id)
            finally:
                db.close()

            factories = client.get("/api/v1/salary-loan/factories", headers=headers)
            self.assertEqual(factories.status_code, 200)

            emp = client.post(
                "/api/v1/salary-loan/employment",
                headers=headers,
                json={"factory_id": factory_id, "employee_no": "E100", "pay_cycle": "monthly", "pay_method": "transfer"},
            )
            self.assertEqual(emp.status_code, 200)
            employment_id = emp.json().get("data", {}).get("id")
            self.assertTrue(employment_id)

            order = client.post(
                "/api/v1/salary-loan/orders",
                headers=headers,
                json={"employment_id": employment_id, "principal": 80, "tenor_days": 14},
            )
            self.assertEqual(order.status_code, 200)
            order_id = order.json().get("data", {}).get("id")
            self.assertTrue(order_id)

            detail = client.get(f"/api/v1/salary-loan/orders/{order_id}", headers=headers)
            self.assertEqual(detail.status_code, 200)

            proof = client.post(
                f"/api/v1/salary-loan/orders/{order_id}/repayment-proof",
                headers=headers,
                params={"amount": 10, "note": "paid"},
                files={"file": ("proof.jpg", b"abc", "image/jpeg")},
            )
            self.assertEqual(proof.status_code, 200)
            url = proof.json().get("data", {}).get("url")
            self.assertTrue(isinstance(url, str) and "/proofs/" in url)

        try:
            if os.path.exists(db_path):
                os.remove(db_path)
        except Exception:
            pass

