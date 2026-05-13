"""SettleCore Unified Risk API Client"""
import os
import requests
import logging
from typing import Any

logger = logging.getLogger(__name__)

BASE_URL = os.getenv("SETTLECORE_RISK_API", "https://adminapi.settlecore.org/risk/v1")
TIMEOUT = int(os.getenv("SETTLECORE_RISK_TIMEOUT", "5"))


def _call(method: str, path: str, body: dict | None = None) -> dict[str, Any] | None:
    base = BASE_URL.rstrip("/")
    url = base + "/" + path.lstrip("/")
    try:
        if method == "GET":
            r = requests.get(url, timeout=TIMEOUT)
        else:
            r = requests.post(url, json=body, timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        logger.warning(f"SettleCore risk API call failed: {method} {path} -- {e}")
        return None


def check_create_offer(khmerx_uuid: str, amount: float, term_days: int) -> dict[str, Any] | None:
    return _call("POST", "/check/create-offer", {"khmerx_uuid": khmerx_uuid, "amount": str(amount), "term_days": term_days})


def check_match_offer(borrower_uuid: str, lender_uuid: str, amount: float) -> dict[str, Any] | None:
    return _call("POST", "/check/match-offer", {"borrower_khmerx_uuid": borrower_uuid, "lender_khmerx_uuid": lender_uuid, "amount": str(amount)})


def report_overdue(khmerx_uuid: str, trade_id: str, overdue_days: int) -> dict[str, Any] | None:
    return _call("POST", "/events/repayment-overdue", {"khmerx_uuid": khmerx_uuid, "trade_id": trade_id, "overdue_days": overdue_days})


def report_paid(khmerx_uuid: str, trade_id: str, early: bool = False) -> dict[str, Any] | None:
    return _call("POST", "/events/repayment-paid", {"khmerx_uuid": khmerx_uuid, "trade_id": trade_id, "early": early})


def get_score(khmerx_uuid: str) -> dict[str, Any] | None:
    return _call("GET", f"/score/{khmerx_uuid}")


def adjust_score(khmerx_uuid: str, score_delta: int, reason: str) -> dict[str, Any] | None:
    return _call("POST", "/score/adjust", {"khmerx_uuid": khmerx_uuid, "score_delta": score_delta, "reason": reason})
