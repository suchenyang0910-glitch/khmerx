import unittest
from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models.p2p_trade import P2PTrade
from app.models.user import User
from app.ops.service import AgentService


class TestAgentCommission(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite+pysqlite:///:memory:")
        Base.metadata.create_all(bind=self.engine)
        Session = sessionmaker(bind=self.engine)
        self.db = Session()

    def tearDown(self):
        self.db.close()

    def test_create_and_settle_commission(self):
        agent = User(id=uuid4(), tg_id=1, name="a", role="agent", commission_rate=2)
        borrower = User(id=uuid4(), tg_id=2, name="b", role="user", agent_id=agent.id)
        lender = User(id=uuid4(), tg_id=3, name="l", role="user")
        self.db.add_all([agent, borrower, lender])
        self.db.commit()

        trade = P2PTrade(
            id=uuid4(),
            offer_id=uuid4(),
            borrower_id=borrower.id,
            lender_id=lender.id,
            amount=100.0,
            term_days=7,
            rate=10.0,
            fee=1.0,
            total_repayable=100.0,
            status="repayment_confirmed",
            created_at=datetime.now(timezone.utc),
        )
        self.db.add(trade)
        self.db.commit()

        svc = AgentService(self.db)
        c = svc.create_borrow_commission_pending(trade)
        self.assertIsNotNone(c)
        self.assertEqual(c.status, "pending")

        svc.settle_commissions_for_trade(trade.id)
        self.db.refresh(c)
        self.assertEqual(c.status, "settled")


if __name__ == "__main__":
    unittest.main()

