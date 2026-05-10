import os
import logging
from typing import Any

import httpx
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.config import BOT_TOKENS
from app.database import get_db
from app.services.bot_accounts import get_active_bot_tokens

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/telegram", tags=["telegram"])


def _allowed_bot_tokens(db: Session) -> set[str]:
    tokens = set([t.strip() for t in BOT_TOKENS if (t or "").strip()])
    try:
        for t in get_active_bot_tokens(db):
            if (t or "").strip():
                tokens.add(t.strip())
    except Exception:
        pass
    return tokens


def _start_intro_text() -> str:
    km = (os.getenv("TG_START_INTRO_KM") or "").strip()
    en = (os.getenv("TG_START_INTRO_EN") or "").strip()
    cn = (os.getenv("TG_START_INTRO_CN") or "").strip()

    if not km:
        km = (
            "សូមស្វាគមន៍មកកាន់ KhmerX\n"
            "KhmerX ជាវេទិកា P2P មីក្រូកម្ចី/មីក្រូហិរញ្ញវត្ថុ សម្រាប់កម្ពុជា (ABA + Telegram Mini App)។\n"
            "អ្នកអាចបង្ហោះសំណើខ្ចី ប្រៀបធៀបលក្ខខណ្ឌ និងបញ្ចប់ប្រតិបត្តិការតាម ABA ដោយមានភាពច្បាស់លាស់។"
        )

    if not en:
        en = (
            "Welcome to KhmerX\n"
            "KhmerX is a Cambodia-focused P2P micro‑lending information platform (ABA + Telegram Mini App).\n"
            "Publish a borrowing request, match lenders, and complete ABA transfers with transparent terms."
        )

    if not cn:
        cn = (
            "欢迎使用 KhmerX\n"
            "KhmerX 是面向柬埔寨的 P2P 微借贷信息平台（ABA + Telegram Mini App）。\n"
            "你可以发布借款需求、匹配出借人，并通过 ABA 转账完成交易，条款透明可追溯。"
        )

    links = []
    site = (os.getenv("KHMERX_SITE_URL") or "https://khmerx.org").strip()
    app_url = (os.getenv("KHMERX_MINIAPP_URL") or "https://app.khmerx.org").strip()
    if site:
        links.append(f"Website: {site}")
    if app_url:
        links.append(f"Mini App: {app_url}")

    parts = [km, "", en, "", cn]
    if links:
        parts += ["", "\n".join(links)]
    return "\n".join(parts).strip()


def _start_intro_keyboard() -> dict:
    site = (os.getenv("KHMERX_SITE_URL") or "https://khmerx.org").strip()
    app_url = (os.getenv("KHMERX_MINIAPP_URL") or "https://app.khmerx.org").strip()

    miniapp_btn_text = (os.getenv("TG_START_BTN_MINIAPP") or "").strip() or "Open Mini App / 打开 Mini App / បើក Mini App"
    website_btn_text = (os.getenv("TG_START_BTN_WEBSITE") or "").strip() or "Website / 官网 / គេហទំព័រ"

    keyboard = []
    if app_url:
        keyboard.append([
            {
                "text": miniapp_btn_text,
                "web_app": {"url": app_url},
            }
        ])
    if site:
        keyboard.append([
            {
                "text": website_btn_text,
                "url": site,
            }
        ])

    return {"inline_keyboard": keyboard}


async def _send_telegram_message(*, bot_token: str, chat_id: int, text: str, reply_markup: dict | None = None) -> None:
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload: dict[str, Any] = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }
    if reply_markup is not None:
        payload["reply_markup"] = reply_markup
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(url, json=payload)
        r.raise_for_status()
        data = r.json()
        if not (isinstance(data, dict) and data.get("ok") is True):
            raise RuntimeError(f"telegram sendMessage failed: {data}")


@router.post("/webhook/{bot_token}")
async def telegram_webhook(bot_token: str, request: Request, db: Session = Depends(get_db)):
    allowed = _allowed_bot_tokens(db)
    if bot_token not in allowed:
        return {"ok": True}

    try:
        update = await request.json()
    except Exception:
        return {"ok": True}

    msg = None
    if isinstance(update, dict):
        msg = update.get("message") or update.get("edited_message")

    if not isinstance(msg, dict):
        return {"ok": True}

    text = (msg.get("text") or "").strip()
    if not text.startswith("/start"):
        return {"ok": True}

    chat = msg.get("chat")
    chat_id = chat.get("id") if isinstance(chat, dict) else None
    if not isinstance(chat_id, int):
        return {"ok": True}

    intro = _start_intro_text()
    keyboard = _start_intro_keyboard()

    if (os.getenv("TELEGRAM_SEND_DISABLED") or "").lower() == "true":
        return {"ok": True, "sent": False, "dry_run": True}

    try:
        await _send_telegram_message(bot_token=bot_token, chat_id=chat_id, text=intro, reply_markup=keyboard)
        return {"ok": True, "sent": True}
    except Exception:
        logger.error("telegram /start reply failed", exc_info=True)
        return {"ok": True, "sent": False}
