import os
import sys
import unittest
from datetime import date, timedelta

from fastapi.testclient import TestClient


class TestSalaryLoanQuoteAndCollection(unittest.TestCase):
    def test_quote_and_collection_event_flow(self):
        db_path = "./test_salary_loan_quote_and_collection.db"
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
        import app.database
        from app.models.salary_loan_order import SalaryLoanOrder
        from app.models.salary_loan_repayment import SalaryLoanRepaymentSchedule
        from app.scheduler.jobs import check_salary_loan_overdue

        with TestClient(app.main.app) as client:
            admin_login = client.post("/api/admin/login", json={"username": "admin", "password": "pass"})
            self.assertEqual(admin_login.status_code, 200)
            admin_headers = {"Authorization": f"Bearer {admin_login.json().get('token')}"}

            created_factory = client.post(
                "/api/admin/salary-loan/factories",
                headers=admin_headers,
                json={"name": "Factory C", "location": "PP", "risk_level": "B", "default_rate": 0.1, "is_active": True},
            )
            self.assertEqual(created_factory.status_code, 200)
            factory_id = created_factory.json().get("id")

            dev = client.get("/auth/dev-tma", params={"tg_id": 90345678})
            self.assertEqual(dev.status_code, 200)
            init_data = dev.json().get("data", {}).get("init_data")
            headers = {"Authorization": f"TMA {init_data}"}

            me = client.get("/api/v1/me", headers=headers)
            user_id = me.json().get("data", {}).get("id")
            client.patch(
                "/api/v1/me/profile",
                headers=headers,
                json={"aba_account": "666666", "aba_name": "QuoteFlow"},
            )
            otp_req = client.post("/auth/otp/request", json={"user_id": user_id, "phone": "086666666"})
            code = otp_req.json().get("dev_code")
            challenge_id = otp_req.json().get("challenge_id")
            client.post(
                "/auth/otp/verify",
                json={"user_id": user_id, "phone": "086666666", "code": code, "challenge_id": challenge_id},
            )

            quote = client.post(
                "/api/v1/salary-loan/calculate",
                headers=headers,
                json={
                    "factory_id": factory_id,
                    "principal": 120,
                    "tenor_days": 14,
                    "join_date": "2024-01-01",
                    "pay_cycle": "monthly",
                    "pay_method": "transfer",
                },
            )
            self.assertEqual(quote.status_code, 200)
            quote_data = quote.json().get("data", {})
            self.assertEqual(quote_data.get("principal"), 120)
            self.assertTrue(float(quote_data.get("total_due", 0)) > 120)

            emp = client.post(
                "/api/v1/salary-loan/employment",
                headers=headers,
                json={"factory_id": factory_id, "employee_no": "E300", "pay_cycle": "monthly", "pay_method": "transfer"},
            )
            self.assertEqual(emp.status_code, 200)
            employment_id = emp.json().get("data", {}).get("id")

            order = client.post(
                "/api/v1/salary-loan/orders",
                headers=headers,
                json={"employment_id": employment_id, "principal": 120, "tenor_days": 14},
            )
            self.assertEqual(order.status_code, 200)
            order_id = order.json().get("data", {}).get("id")

            client.post(
                f"/api/admin/salary-loan/employments/{employment_id}/verify",
                headers=admin_headers,
                json={"verify_status": "verified", "verify_notes": "ok"},
            )
            client.post(
                f"/api/admin/salary-loan/orders/{order_id}/decision",
                headers=admin_headers,
                json={"decision": "approve", "approved_principal": 120, "fee": 12, "interest": 3},
            )
            client.post(
                f"/api/admin/salary-loan/orders/{order_id}/disburse",
                headers=admin_headers,
                json={"disbursement_ref": "TX-COLLECT"},
            )

            SessionLocal = app.database.get_session_local()
            db = SessionLocal()
            try:
                order_model = db.query(SalaryLoanOrder).filter(SalaryLoanOrder.id == order_id).first()
                schedule = db.query(SalaryLoanRepaymentSchedule).filter(SalaryLoanRepaymentSchedule.order_id == order_model.id).first()
                yesterday = date.today() - timedelta(days=1)
                order_model.due_date = yesterday
                schedule.due_date = yesterday
                db.commit()
                check_salary_loan_overdue(db)
                db.commit()
            finally:
                db.close()

            rows = client.get("/api/admin/salary-loan/collections?status=open", headers=admin_headers)
            self.assertEqual(rows.status_code, 200)
            rows_data = rows.json()
            self.assertEqual(len(rows_data), 1)
            case_id = rows_data[0]["id"]

            detail = client.get(f"/api/admin/salary-loan/collections/{case_id}", headers=admin_headers)
            self.assertEqual(detail.status_code, 200)
            self.assertEqual(detail.json()["case"]["status"], "open")

            event = client.post(
                f"/api/admin/salary-loan/collections/{case_id}/events",
                headers=admin_headers,
                json={
                    "channel": "call",
                    "result": "ptp",
                    "reason_code": "promise_to_pay",
                    "note": "borrower promised repayment tomorrow",
                    "ptp_date": (date.today() + timedelta(days=1)).isoformat(),
                    "ptp_amount": 50,
                },
            )
            self.assertEqual(event.status_code, 200)

            detail_after = client.get(f"/api/admin/salary-loan/collections/{case_id}", headers=admin_headers)
            self.assertEqual(detail_after.status_code, 200)
            self.assertEqual(len(detail_after.json()["events"]), 1)

        try:
            if os.path.exists(db_path):
                os.remove(db_path)
        except Exception:
            pass
