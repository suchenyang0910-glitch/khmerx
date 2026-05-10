from decimal import Decimal


MAX_BORROW_AMOUNT_CAP = Decimal("800.00")


def credit_level_from_score(score: int) -> str:
    if score >= 800:
        return "A"
    if score >= 700:
        return "B"
    if score >= 600:
        return "C"
    if score >= 500:
        return "D"
    return "E"


def max_borrow_amount_by_level(level: str) -> Decimal:
    mapping = {
        "A": Decimal("2000.00"),
        "B": Decimal("1000.00"),
        "C": Decimal("500.00"),
        "D": Decimal("200.00"),
        "E": Decimal("0.00"),
    }
    raw = mapping.get(level, Decimal("0.00"))
    return min(raw, MAX_BORROW_AMOUNT_CAP)


def normalize_risk_level(score: int, current_level: str = "normal") -> str:
    if score < 500:
        return "blocked"
    if score < 550:
        return "restricted"
    if score < 600:
        return "flagged"
    if score < 650:
        return "watch"
    return current_level

