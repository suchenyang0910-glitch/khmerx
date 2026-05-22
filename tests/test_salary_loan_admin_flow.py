import unittest

import os
import sys

from fastapi.testclient import TestClient


class TestSalaryLoanAdminFlow(unittest.TestCase):
    def test_admin_review_and_disburse_and_repay(self):
        db_path = "./test_salary_loan_admin_flow.db"
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
        os.environ["ADMIN_USERNAME"] = "admin"
        os.environ["ADMIN_PASSWORD"] = "pass"
        os.environ["ADMIN_JWT_SECRET"] = "secret"

        for k in list(sys.modules.keys()):
            if k == "app" or k.startswith("app."):
                del sys.modules[k]

        import app.main

        with TestClient(app.main.app) as client:
            admin_login = client.post("/api/admin/login", json={"username": "admin", "password": "pass"})
            self.assertEqual(admin_login.status_code, 200)
            token = admin_login.json().get("token")
            self.assertTrue(token)
            admin_headers = {"Authorization": f"Bearer {token}"}

            created_factory = client.post(
                "/api/admin/salary-loan/factories",
                headers=admin_headers,
                json={"name": "Factory B", "location": "PP", "risk_level": "B", "is_active": True},
            )
            self.assertEqual(created_factory.status_code, 200)
            factory_id = created_factory.json().get("id")
            self.assertTrue(factory_id)

            dev = client.get("/auth/dev-tma", params={"tg_id": 90234567})
            self.assertEqual(dev.status_code, 200)
            init_data = dev.json().get("data", {}).get("init_data")
            headers = {"Authorization": f"TMA {init_data}"}

            me = client.get("/api/v1/me", headers=headers)
            user_id = me.json().get("data", {}).get("id")

            client.patch(
                "/api/v1/me/profile",
                headers=headers,
                json={"aba_account": "777777", "aba_name": "E2E"},
            )
            otp_req = client.post("/auth/otp/request", json={"user_id": user_id, "phone": "087777777"})
            code = otp_req.json().get("dev_code")
            challenge_id = otp_req.json().get("challenge_id")
            client.post(
                "/auth/otp/verify",
                json={"user_id": user_id, "phone": "087777777", "code": code, "challenge_id": challenge_id},
            )

            emp = client.post(
                "/api/v1/salary-loan/employment",
                headers=headers,
                json={"factory_id": factory_id, "employee_no": "E200", "pay_cycle": "monthly", "pay_method": "transfer"},
            )
            self.assertEqual(emp.status_code, 200)
            employment_id = emp.json().get("data", {}).get("id")

            order = client.post(
                "/api/v1/salary-loan/orders",
                headers=headers,
                json={"employment_id": employment_id, "principal": 100, "tenor_days": 14},
            )
            self.assertEqual(order.status_code, 200)
            order_id = order.json().get("data", {}).get("id")

            ver = client.post(
                f"/api/admin/salary-loan/employments/{employment_id}/verify",
                headers=admin_headers,
                json={"verify_status": "verified", "verify_notes": "ok"},
            )
            self.assertEqual(ver.status_code, 200)

            dec = client.post(
                f"/api/admin/salary-loan/orders/{order_id}/decision",
                headers=admin_headers,
                json={"decision": "approve", "approved_principal": 100, "fee": 5, "interest": 3, "decision_notes": ""},
            )
            self.assertEqual(dec.status_code, 200)

            dis = client.post(
                f"/api/admin/salary-loan/orders/{order_id}/disburse",
                headers=admin_headers,
                json={"disbursement_ref": "TX123"},
            )
            self.assertEqual(dis.status_code, 200)

            proof = client.post(
                f"/api/v1/salary-loan/orders/{order_id}/repayment-proof",
                headers=headers,
                params={"amount": 108, "note": "paid"},
                files={"file": ("proof.jpg", b"abc", "image/jpeg")},
            )
            self.assertEqual(proof.status_code, 200)
            proof_id = proof.json().get("data", {}).get("proof_id")
            self.assertTrue(proof_id)

            rev = client.post(
                f"/api/admin/salary-loan/proofs/{proof_id}/review",
                headers=admin_headers,
                json={"status": "accepted", "note": ""},
            )
            self.assertEqual(rev.status_code, 200)

            o = client.get(f"/api/admin/salary-loan/orders/{order_id}", headers=admin_headers)
            self.assertEqual(o.status_code, 200)
            status = o.json().get("order", {}).get("status")
            self.assertIn(status, ("repaying", "completed"))

        try:
            if os.path.exists(db_path):
                os.remove(db_path)
        except Exception:
            pass

