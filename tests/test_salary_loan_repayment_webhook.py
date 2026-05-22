import unittest

import os
import sys
import time
import hmac
import hashlib

from fastapi.testclient import TestClient


def _sign(secret: str, ts: str, body: bytes) -> str:
    msg = ts.encode("utf-8") + b"." + body
    return hmac.new(secret.encode("utf-8"), msg, hashlib.sha256).hexdigest()


class TestSalaryLoanRepaymentWebhook(unittest.TestCase):
    def test_webhook_repay_idempotent_and_allocated(self):
        db_path = "./test_salary_loan_repayment_webhook.db"
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
        os.environ["SALARY_LOAN_WEBHOOK_SECRET"] = "whsec_test"

        for k in list(sys.modules.keys()):
            if k == "app" or k.startswith("app."):
                del sys.modules[k]

        import app.main

        with TestClient(app.main.app) as client:
            admin_login = client.post("/api/admin/login", json={"username": "admin", "password": "pass"})
            token = admin_login.json().get("token")
            admin_headers = {"Authorization": f"Bearer {token}"}

            created_factory = client.post(
                "/api/admin/salary-loan/factories",
                headers=admin_headers,
                json={"name": "Factory A", "location": "PP", "risk_level": "A", "is_active": True},
            )
            factory_id = created_factory.json().get("id")

            dev = client.get("/auth/dev-tma", params={"tg_id": 90345678})
            init_data = dev.json().get("data", {}).get("init_data")
            headers = {"Authorization": f"TMA {init_data}"}

            me = client.get("/api/v1/me", headers=headers)
            user_id = me.json().get("data", {}).get("id")
            client.patch(
                "/api/v1/me/profile",
                headers=headers,
                json={"aba_account": "111111", "aba_name": "E2E"},
            )
            otp_req = client.post("/auth/otp/request", json={"user_id": user_id, "phone": "081111111"})
            code = otp_req.json().get("dev_code")
            challenge_id = otp_req.json().get("challenge_id")
            client.post(
                "/auth/otp/verify",
                json={"user_id": user_id, "phone": "081111111", "code": code, "challenge_id": challenge_id},
            )

            emp = client.post(
                "/api/v1/salary-loan/employment",
                headers=headers,
                json={"factory_id": factory_id, "employee_no": "E300", "pay_cycle": "monthly", "pay_method": "transfer"},
            )
            employment_id = emp.json().get("data", {}).get("id")

            order = client.post(
                "/api/v1/salary-loan/orders",
                headers=headers,
                json={"employment_id": employment_id, "principal": 100, "tenor_days": 14},
            )
            order_id = order.json().get("data", {}).get("id")

            client.post(
                f"/api/admin/salary-loan/employments/{employment_id}/verify",
                headers=admin_headers,
                json={"verify_status": "verified", "verify_notes": "ok"},
            )
            client.post(
                f"/api/admin/salary-loan/orders/{order_id}/decision",
                headers=admin_headers,
                json={"decision": "approve", "approved_principal": 100, "fee": 5, "interest": 3, "decision_notes": ""},
            )
            client.post(
                f"/api/admin/salary-loan/orders/{order_id}/disburse",
                headers=admin_headers,
                json={"disbursement_ref": "TX999"},
            )

            payment_id = "pay_001"
            body = (
                '{'
                f'"event":"repayment.paid","order_id":"{order_id}","payment_id":"{payment_id}","amount":108'
                '}'
            ).encode("utf-8")
            ts = str(int(time.time()))
            sig = _sign("whsec_test", ts, body)
            res = client.post(
                "/khmerx/webhooks/salary-loan/repayment",
                data=body,
                headers={"X-KHX-Timestamp": ts, "X-KHX-Signature": sig, "Content-Type": "application/json"},
            )
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.json().get("status"), "processed")

            res2 = client.post(
                "/khmerx/webhooks/salary-loan/repayment",
                data=body,
                headers={"X-KHX-Timestamp": ts, "X-KHX-Signature": sig, "Content-Type": "application/json"},
            )
            self.assertEqual(res2.status_code, 200)
            self.assertEqual(res2.json().get("status"), "skipped")

            o = client.get(f"/api/admin/salary-loan/orders/{order_id}", headers=admin_headers)
            self.assertEqual(o.status_code, 200)
            self.assertEqual(o.json().get("order", {}).get("status"), "completed")

            ledger = o.json().get("ledger", [])
            fee_lines = [x for x in ledger if x.get("event_type") == "REPAY" and x.get("account") == "fee_receivable"]
            int_lines = [x for x in ledger if x.get("event_type") == "REPAY" and x.get("account") == "interest_receivable"]
            pri_lines = [x for x in ledger if x.get("event_type") == "REPAY" and x.get("account") == "loan_receivable"]
            self.assertTrue(any(abs(float(x.get("cr_amount")) - 5.0) < 0.001 and x.get("external_ref") == payment_id for x in fee_lines))
            self.assertTrue(any(abs(float(x.get("cr_amount")) - 3.0) < 0.001 and x.get("external_ref") == payment_id for x in int_lines))
            self.assertTrue(any(abs(float(x.get("cr_amount")) - 100.0) < 0.001 and x.get("external_ref") == payment_id for x in pri_lines))

        try:
            if os.path.exists(db_path):
                os.remove(db_path)
        except Exception:
            pass

