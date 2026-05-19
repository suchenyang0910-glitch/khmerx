from __future__ import annotations

import hashlib
import hmac
import logging
import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import config
from app.models.phone_otp import PhoneOtpChallenge
from app.models.user import User
from app.services.sms import send_sms


logger = logging.getLogger(__name__)


def _utcnow() -> datetime:
    return datetime.utcnow()


def normalize_phone(phone: str) -> str:
    p = (phone or "").strip().replace(" ", "")
    if len(p) < 8:
        raise HTTPException(status_code=400, detail="Invalid phone number")
    return p


def _pepper_bytes() -> bytes:
    secret = (config.OTP_SECRET or "").strip()
    if not secret:
        return b""
    return secret.encode()


def _hash_code(*, salt_hex: str, code: str) -> str:
    salt = bytes.fromhex(salt_hex)
    pepper = _pepper_bytes()
    data = code.encode() if not pepper else (code + ":").encode() + pepper
    digest = hashlib.pbkdf2_hmac("sha256", data, salt, 120_000)
    return digest.hex()


def _generate_code() -> str:
    return f"{secrets.randbelow(1000000):06d}"


@dataclass
class OtpRequestResult:
    challenge_id: str
    dev_code: str | None


def request_phone_otp(db: Session, *, user: User, phone: str) -> OtpRequestResult:
    phone_n = normalize_phone(phone)

    now = _utcnow()
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    daily = (
        db.query(PhoneOtpChallenge)
        .filter(PhoneOtpChallenge.user_id == user.id)
        .filter(PhoneOtpChallenge.created_at >= start)
        .count()
    )
    if daily >= config.OTP_DAILY_LIMIT:
        raise HTTPException(status_code=429, detail="OTP daily limit reached")

    recent = (
        db.query(PhoneOtpChallenge)
        .filter(PhoneOtpChallenge.user_id == user.id)
        .filter(PhoneOtpChallenge.phone == phone_n)
        .filter(PhoneOtpChallenge.verified_at.is_(None))
        .order_by(PhoneOtpChallenge.sent_at.desc())
        .first()
    )
    if recent and (now - recent.sent_at).total_seconds() < config.OTP_RESEND_MIN_SECONDS:
        return OtpRequestResult(challenge_id=str(recent.id), dev_code=None)

    code = _generate_code()
    salt_hex = secrets.token_hex(16)
    code_hash = _hash_code(salt_hex=salt_hex, code=code)
    row = PhoneOtpChallenge(
        user_id=user.id,
        phone=phone_n,
        code_hash=code_hash,
        salt=salt_hex,
        sent_at=now,
        expires_at=now + timedelta(seconds=config.OTP_CODE_TTL_SECONDS),
        attempts=0,
    )
    db.add(row)
    db.commit()
    db.refresh(row)

    dev_mode = bool(config.OTP_DEV_MODE) or not bool((config.SMS_PROVIDER or "").strip())
    if not dev_mode:
        try:
            send_sms(
                to=phone_n,
                body=f"KhmerX 验证码：{code}（{config.OTP_CODE_TTL_SECONDS // 60}分钟内有效）",
            )
        except Exception:
            logger.exception("OTP SMS send failed")
            raise HTTPException(status_code=503, detail="OTP 短信发送失败，请稍后重试")

    dev_code = code if dev_mode else None
    return OtpRequestResult(challenge_id=str(row.id), dev_code=dev_code)


def verify_phone_otp(db: Session, *, user: User, phone: str, code: str) -> None:
    phone_n = normalize_phone(phone)
    code_n = (code or "").strip()
    if len(code_n) != 6 or not code_n.isdigit():
        raise HTTPException(status_code=400, detail="Invalid code")

    now = _utcnow()
    row = (
        db.query(PhoneOtpChallenge)
        .filter(PhoneOtpChallenge.user_id == user.id)
        .filter(PhoneOtpChallenge.phone == phone_n)
        .filter(PhoneOtpChallenge.verified_at.is_(None))
        .order_by(PhoneOtpChallenge.sent_at.desc())
        .first()
    )
    if not row:
        raise HTTPException(status_code=400, detail="OTP not found")
    if row.expires_at < now:
        raise HTTPException(status_code=400, detail="OTP expired")
    if row.attempts >= config.OTP_MAX_VERIFY_ATTEMPTS:
        raise HTTPException(status_code=429, detail="Too many attempts")

    expected = _hash_code(salt_hex=row.salt, code=code_n)
    ok = hmac.compare_digest(expected, row.code_hash)
    row.attempts = int(row.attempts or 0) + 1
    if not ok:
        db.commit()
        raise HTTPException(status_code=400, detail="Invalid code")

    row.verified_at = now
    user.phone = phone_n
    user.phone_verified_at = datetime.now(timezone.utc)
    if user.verification_level == "unverified":
        user.verification_level = "phone"
    db.commit()
