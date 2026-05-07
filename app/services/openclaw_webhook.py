from __future__ import annotations

import hashlib
import hmac
import json
from datetime import datetime, timezone

import httpx

from app import config


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sign(payload: dict) -> str:
    secret = (config.OPENCLAW_WEBHOOK_SECRET or "").encode()
    if not secret:
        return ""
    body = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode()
    return hmac.new(secret, body, hashlib.sha256).hexdigest()


def push_risk_event(payload: dict) -> None:
    if not config.OPENCLAW_WEBHOOK_ENABLED:
        raise RuntimeError("OPENCLAW_WEBHOOK_ENABLED is false")
    if not config.OPENCLAW_WEBHOOK_URL:
        raise RuntimeError("OPENCLAW_WEBHOOK_URL not configured")

    envelope = {
        "type": "khmerx.risk_event",
        "sent_at": _utcnow_iso(),
        "data": payload,
    }
    sig = _sign(envelope)
    headers = {"Content-Type": "application/json"}
    if sig:
        headers["X-OpenClaw-Signature"] = sig

    with httpx.Client(timeout=float(config.OPENCLAW_WEBHOOK_TIMEOUT_SECONDS)) as client:
        res = client.post(config.OPENCLAW_WEBHOOK_URL, json=envelope, headers=headers)
    if res.status_code >= 400:
        raise RuntimeError("openclaw webhook failed")

