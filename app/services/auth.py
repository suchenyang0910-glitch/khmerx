"""
Telegram Mini App 登录验证

流程：
1. 前端获取 window.Telegram.WebApp.initData
2. POST 到后端的 /auth/telegram-login
3. 后端验证 initData 签名（使用 Bot Token）
4. 验证通过 → 创建或登录用户
5. 返回用户信息（含 role）
"""
import hmac
import hashlib
import json
import logging
import os
import urllib.request
from urllib.parse import parse_qsl, unquote
from typing import Optional, Sequence
from sqlalchemy.orm import Session

from app.models.user import User

logger = logging.getLogger(__name__)


def _debug_emit(hypothesis_id: str, location: str, msg: str, data: dict | None = None) -> None:
    _url = "http://127.0.0.1:7777/event"
    _session = "telegram-login-500"
    _env_path = os.path.join(".dbg", "telegram-login-500.env")
    try:
        with open(_env_path, "r", encoding="utf-8") as _f:
            for _line in _f:
                if _line.startswith("DEBUG_SERVER_URL="):
                    _url = _line.split("=", 1)[1].strip() or _url
                elif _line.startswith("DEBUG_SESSION_ID="):
                    _session = _line.split("=", 1)[1].strip() or _session
    except Exception:
        pass
    try:
        _payload = json.dumps({
            "sessionId": _session,
            "runId": "pre-fix",
            "hypothesisId": hypothesis_id,
            "location": location,
            "msg": msg,
            "data": data or {},
        }).encode()
        urllib.request.urlopen(urllib.request.Request(_url, data=_payload, headers={"Content-Type": "application/json"}), timeout=0.8).read()
    except Exception:
        pass


def verify_telegram_init_data(init_data: str, bot_tokens: Sequence[str]) -> Optional[dict]:
    """
    验证 Telegram Mini App 的 initData 签名。

    参考: https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app

    返回解密后的用户数据 dict，验证失败返回 None。
    """
    try:
        if not bot_tokens:
            # #region debug-point B:no-bot-tokens
            _debug_emit("B", "app/services/auth.py:verify_telegram_init_data:no_tokens", "[DEBUG] no bot tokens configured", {})
            # #endregion
            logger.error("TG auth: no bot tokens configured")
            return None

        raw = (init_data or "").strip()
        if ("hash=" not in raw) and ("%3D" in raw or "%26" in raw):
            raw = unquote(raw)

        parsed = dict(parse_qsl(raw, keep_blank_values=True))
        data_dict = {k: v for k, v in parsed.items()}
        # #region debug-point D:parsed-init-data
        _debug_emit(
            "D",
            "app/services/auth.py:verify_telegram_init_data:parsed",
            "[DEBUG] telegram init data parsed",
            {
                "raw_len": len(raw),
                "field_count": len(data_dict),
                "has_hash": "hash" in data_dict,
                "keys": sorted(list(data_dict.keys()))[:12],
            },
        )
        # #endregion

        # 提取 hash
        received_hash = data_dict.pop("hash", None)
        if not received_hash:
            # #region debug-point D:missing-hash
            _debug_emit("D", "app/services/auth.py:verify_telegram_init_data:missing_hash", "[DEBUG] missing hash in init data", {})
            # #endregion
            logger.warning("TG auth: no hash in initData")
            return None

        # 构建 data_check_string
        sorted_keys = sorted(data_dict.keys())
        data_check_parts = [f"{k}={data_dict[k]}" for k in sorted_keys]
        data_check_string = "\n".join(data_check_parts)

        hash_ok = False
        for token in bot_tokens:
            secret_key = hmac.new(
                b"WebAppData",
                token.encode(),
                hashlib.sha256,
            ).digest()

            expected_hash = hmac.new(
                secret_key,
                data_check_string.encode(),
                hashlib.sha256,
            ).hexdigest()

            if hmac.compare_digest(expected_hash, received_hash):
                hash_ok = True
                break

        if not hash_ok:
            # #region debug-point A:hash-mismatch
            _debug_emit("A", "app/services/auth.py:verify_telegram_init_data:hash_mismatch", "[DEBUG] hash mismatch", {"token_count": len(bot_tokens)})
            # #endregion
            logger.warning("TG auth: hash mismatch")
            return None

        # 可选：检查 auth_date 是否过期（默认 24 小时内有效）
        auth_date = data_dict.get("auth_date")
        if auth_date:
            import time
            now = time.time()
            if now - int(auth_date) > 86400:  # 24h
                # #region debug-point A:auth-date-expired
                _debug_emit("A", "app/services/auth.py:verify_telegram_init_data:auth_date_expired", "[DEBUG] auth_date expired", {"auth_date": auth_date})
                # #endregion
                logger.warning("TG auth: auth_date expired")
                return None

        # 解析 user
        user_str = data_dict.get("user")
        if user_str:
            try:
                user_data = json.loads(unquote(user_str))
                # #region debug-point A:user-json-ok
                _debug_emit(
                    "A",
                    "app/services/auth.py:verify_telegram_init_data:user_json_ok",
                    "[DEBUG] user json parsed",
                    {
                        "has_id": bool(user_data.get("id")) if isinstance(user_data, dict) else False,
                        "keys": sorted(list(user_data.keys()))[:12] if isinstance(user_data, dict) else [],
                    },
                )
                # #endregion
                return user_data
            except json.JSONDecodeError:
                # #region debug-point D:user-json-error
                _debug_emit("D", "app/services/auth.py:verify_telegram_init_data:user_json_error", "[DEBUG] failed to parse user json", {"user_len": len(user_str)})
                # #endregion
                logger.error("TG auth: failed to parse user JSON")
                return None

        # #region debug-point D:missing-user
        _debug_emit("D", "app/services/auth.py:verify_telegram_init_data:missing_user", "[DEBUG] init data missing user field", {"keys": sorted(list(data_dict.keys()))[:12]})
        # #endregion
        return None

    except Exception as e:
        # #region debug-point A:verify-exception
        _debug_emit("A", "app/services/auth.py:verify_telegram_init_data:exception", "[DEBUG] verify function caught exception", {"error_type": type(e).__name__, "error_text": str(e)[:300]})
        # #endregion
        logger.error(f"TG verify error: {e}")
        return None


def verify_telegram_contact_response(response: str, bot_tokens: Sequence[str]) -> Optional[dict]:
    try:
        if not bot_tokens:
            logger.error("TG contact: no bot tokens configured")
            return None

        parsed = dict(parse_qsl(response, keep_blank_values=True))
        data_dict = {k: v for k, v in parsed.items()}

        received_hash = data_dict.pop("hash", None)
        if not received_hash:
            logger.warning("TG contact: no hash")
            return None

        sorted_keys = sorted(data_dict.keys())
        data_check_string = "\n".join([f"{k}={data_dict[k]}" for k in sorted_keys])

        hash_ok = False
        for token in bot_tokens:
            secret_key = hmac.new(b"WebAppData", token.encode(), hashlib.sha256).digest()
            expected_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
            if hmac.compare_digest(expected_hash, received_hash):
                hash_ok = True
                break

        if not hash_ok:
            logger.warning("TG contact: hash mismatch")
            return None

        contact_raw = data_dict.get("contact")
        if not contact_raw:
            logger.warning("TG contact: missing contact")
            return None

        try:
            contact = json.loads(unquote(contact_raw))
        except json.JSONDecodeError:
            logger.error("TG contact: invalid contact json")
            return None

        return contact
    except Exception as e:
        logger.error(f"TG contact verify error: {e}")
        return None


def login_or_register(db: Session, tg_user: dict) -> User:
    """
    根据 TG 用户数据查找或创建用户。
    """
    tg_id = tg_user.get("id")
    if not tg_id:
        raise ValueError("TG user data missing 'id'")

    user = db.query(User).filter(User.tg_id == tg_id).first()
    if user:
        # 更新信息
        user.name = tg_user.get("first_name", "") + " " + tg_user.get("last_name", "")
        if tg_user.get("username"):
            user.name = tg_user["username"]
        user.photo_url = tg_user.get("photo_url", "")
        db.commit()
        logger.info(f"TG login: existing user {tg_id} → {user.name}")
        return user

    # 创建新用户
    name = tg_user.get("first_name", "") + " " + tg_user.get("last_name", "")
    if tg_user.get("username"):
        name = tg_user["username"]

    user = User(
        tg_id=tg_id,
        name=name.strip(),
        photo_url=tg_user.get("photo_url", ""),
        role="user",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    logger.info(f"TG register: new user {tg_id} → {user.id}")
    return user
