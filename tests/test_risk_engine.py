import unittest
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from uuid import uuid4

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models.user import User
from app.risk.engine import RiskEngine
from app.risk.schemas import CreateOfferRiskInput
from app.risk.service import RiskService


class TestRiskEngine(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite+pysqlite:///:memory:")
        Base.metadata.create_all(bind=self.engine)
        Session = sessionmaker(bind=self.engine)
        self.db = Session()

    def tearDown(self):
        self.db.close()

    def test_new_user_large_amount_requires_manual_review(self):
        user = User(
            id=uuid4(),
            tg_id=123,
            name="u",
            credit_score=650,
            created_at=datetime.now(timezone.utc) - timedelta(days=1),
        )
        self.db.add(user)
        self.db.commit()

        service = RiskService(self.db)
        engine = RiskEngine(service)

        decision = engine.check_create_offer(
            CreateOfferRiskInput(
                user_id=user.id,
                amount=Decimal("301.00"),
                term_days=7,
                user_age_days=1,
                active_trades_count=0,
                offers_24h_count=0,
            )
        )

        self.assertFalse(decision.allowed)
        self.assertTrue(decision.require_manual_review)
        self.assertEqual(decision.action, "manual_review")

    def test_high_frequency_offer_blocks_24h(self):
        user = User(
            id=uuid4(),
            tg_id=124,
            name="u2",
            credit_score=650,
            created_at=datetime.now(timezone.utc) - timedelta(days=30),
        )
        self.db.add(user)
        self.db.commit()

        service = RiskService(self.db)
        engine = RiskEngine(service)

        decision = engine.check_create_offer(
            CreateOfferRiskInput(
                user_id=user.id,
                amount=Decimal("100.00"),
                term_days=7,
                user_age_days=30,
                active_trades_count=0,
                offers_24h_count=5,
            )
        )

        self.assertFalse(decision.allowed)
        profile = service.get_or_create_profile(user.id)
        self.assertTrue(profile.is_blocked)


if __name__ == "__main__":
    unittest.main()

