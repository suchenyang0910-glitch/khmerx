import unittest
from decimal import Decimal

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models.interest_rate import InterestRateMatrix
from app.services.interest_calculator import InterestCalculator


class TestCutInterestCalculator(unittest.TestCase):
    def test_examples(self):
        cases = [
            (7, Decimal("10"), Decimal("10.00"), Decimal("90.00"), Decimal("100.00")),
            (14, Decimal("18"), Decimal("18.00"), Decimal("82.00"), Decimal("100.00")),
            (30, Decimal("30"), Decimal("30.00"), Decimal("70.00"), Decimal("100.00")),
        ]

        for term_days, rate_percent, interest, received, repay in cases:
            result = InterestCalculator.calc_cut_interest_loan(100, term_days, rate_percent)
            self.assertEqual(result.interest, interest)
            self.assertEqual(result.received_amount, received)
            self.assertEqual(result.repay_amount, repay)

    def test_real_rate_and_apr(self):
        result = InterestCalculator.calc_cut_interest_loan(100, 7, 10)
        self.assertEqual(result.real_rate_percent, Decimal("11.11"))
        self.assertEqual(result.apr_percent, Decimal("579.37"))

    def test_invalid_term_days(self):
        with self.assertRaises(ValueError):
            InterestCalculator.calc_cut_interest_loan(100, 21, 10)

    def test_rate_lookup_in_db(self):
        engine = create_engine("sqlite+pysqlite:///:memory:")
        Base.metadata.create_all(bind=engine)
        Session = sessionmaker(bind=engine)
        db = Session()
        try:
            db.add(
                InterestRateMatrix(
                    term_days=7,
                    credit_level="C",
                    rate_percent=Decimal("10.00"),
                    mode="cut_interest",
                    enabled=True,
                )
            )
            db.commit()

            rate = InterestCalculator.get_cut_interest_rate_percent(db, 7, "C")
            self.assertEqual(rate, Decimal("10.00"))
        finally:
            db.close()


if __name__ == "__main__":
    unittest.main()

