from __future__ import annotations

from fastapi import Depends, Header
from sqlalchemy.orm import Session

from app.api_v1.errors import ApiError
from app.config import BOT_TOKENS
from app.database import get_db
from app.models.user import User
from app.services.auth import login_or_register, verify_telegram_init_data
from app.services.bot_accounts import get_active_bot_tokens


def get_current_user_tma(
    authorization: str | None = Header(default=None, alias="Authorization"),
    db: Session = Depends(get_db),
) -> User:
    if not authorization:
        raise ApiError(code="AUTH_REQUIRED", message="未登录", status_code=401)

    value = authorization.strip()
    if not value.lower().startswith("tma "):
        raise ApiError(code="AUTH_REQUIRED", message="未登录", status_code=401)

    init_data = value[4:].strip()
    if not init_data:
        raise ApiError(code="AUTH_REQUIRED", message="未登录", status_code=401)

    tokens = []
    try:
        tokens = get_active_bot_tokens(db)
    except Exception:
        tokens = []
    if not tokens:
        tokens = BOT_TOKENS

    tg_user = verify_telegram_init_data(init_data, tokens)
    if not tg_user:
        raise ApiError(code="AUTH_REQUIRED", message="未登录", status_code=401)

    return login_or_register(db, tg_user)


def ensure_profile_completed(user: User) -> None:
    phone_missing = not bool(user.phone_verified_at)
    aba_missing = not bool(user.aba_account and user.aba_name)
    if not (phone_missing or aba_missing):
        return

    if aba_missing and not phone_missing:
        raise ApiError(
            code="ABA_REQUIRED",
            message="未绑定 ABA",
            details={"aba_required": True},
            status_code=403,
        )

    raise ApiError(
        code="PROFILE_INCOMPLETE",
        message="资料未完善",
        details={
            "phone_required": phone_missing,
            "aba_required": aba_missing,
        },
        status_code=403,
    )
