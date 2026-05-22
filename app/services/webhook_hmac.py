from __future__ import annotations

import hmac
import hashlib
import time


def sign_body(secret: str, timestamp: str, body: bytes) -> str:
    key = (secret or "").encode("utf-8")
    msg = timestamp.encode("utf-8") + b"." + body
    return hmac.new(key, msg, hashlib.sha256).hexdigest()


def verify_signature(
    *,
    secret: str,
    timestamp: str | None,
    signature: str | None,
    body: bytes,
    max_skew_seconds: int = 300,
) -> tuple[bool, str]:
    if not secret:
        return False, "webhook secret not configured"
    if not timestamp or not signature:
        return False, "missing signature headers"

    try:
        ts = int(str(timestamp).strip())
    except Exception:
        return False, "invalid timestamp"

    now = int(time.time())
    if abs(now - ts) > max_skew_seconds:
        return False, "timestamp out of range"

    expected = sign_body(secret, str(ts), body)
    if not hmac.compare_digest(expected, (signature or "").strip().lower()):
        return False, "signature mismatch"

    return True, "ok"

