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
from urllib.parse import parse_qsl, unquote
from typing import Optional, Sequence
from sqlalchemy.orm import Session

from app.models.user import User

logger = logging.getLogger(__name__)


def verify_telegram_init_data(init_data: str, bot_tokens: Sequence[str]) -> Optional[dict]:
    """
    验证 Telegram Mini App 的 initData 签名。

    参考: https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app

    返回解密后的用户数据 dict，验证失败返回 None。
    """
    try:
        if not bot_tokens:
            logger.error("TG auth: no bot tokens configured")
            return None

        parsed = dict(parse_qsl(init_data, keep_blank_values=True))
        data_dict = {k: v for k, v in parsed.items()}

        # 提取 hash
        received_hash = data_dict.pop("hash", None)
        if not received_hash:
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
            logger.warning("TG auth: hash mismatch")
            return None

        # 可选：检查 auth_date 是否过期（默认 24 小时内有效）
        auth_date = data_dict.get("auth_date")
        if auth_date:
            import time
            now = time.time()
            if now - int(auth_date) > 86400:  # 24h
                logger.warning("TG auth: auth_date expired")
                return None

        # 解析 user
        user_str = data_dict.get("user")
        if user_str:
            try:
                user_data = json.loads(unquote(user_str))
                return user_data
            except json.JSONDecodeError:
                logger.error("TG auth: failed to parse user JSON")
                return None

        return None

    except Exception as e:
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
