from __future__ import annotations

from dataclasses import dataclass

import httpx

from app import config


@dataclass
class SmsSendResult:
    provider: str
    message_id: str | None


def send_sms(*, to: str, body: str) -> SmsSendResult:
    provider = (config.SMS_PROVIDER or "").strip().lower()
    if not provider:
        raise RuntimeError("SMS provider not configured")
    if provider == "twilio":
        return _send_twilio(to=to, body=body)
    raise RuntimeError("Unsupported SMS provider")


def _send_twilio(*, to: str, body: str) -> SmsSendResult:
    sid = (config.TWILIO_ACCOUNT_SID or "").strip()
    token = (config.TWILIO_AUTH_TOKEN or "").strip()
    from_ = (config.SMS_FROM or "").strip()
    if not sid or not token or not from_:
        raise RuntimeError("Twilio not configured")

    url = f"https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json"
    with httpx.Client(timeout=15.0) as client:
        res = client.post(
            url,
            auth=(sid, token),
            data={"To": to, "From": from_, "Body": body},
        )
    if res.status_code >= 400:
        raise RuntimeError("SMS send failed")
    data = res.json() if res.content else {}
    return SmsSendResult(provider="twilio", message_id=data.get("sid"))

