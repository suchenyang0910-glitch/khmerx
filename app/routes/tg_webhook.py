"""Telegram Bot Webhook — Mini App & command handler"""
import json
import logging
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.database import get_db

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/webhook", tags=["telegram-webhook"])

UPDATE_QUEUE = []


@router.post("/tg")
async def telegram_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Receive Telegram Bot updates (messages, callback queries).

    Current: log all updates for future command processing.
    """
    try:
        body = await request.json()
        logger.info(f"TG update: {json.dumps(body, ensure_ascii=False)[:500]}")

        # Queue the update for processing
        UPDATE_QUEUE.append(body)
        # Keep queue bounded
        if len(UPDATE_QUEUE) > 100:
            UPDATE_QUEUE.pop(0)

        update_id = body.get("update_id", 0)
        return {"ok": True, "update_id": update_id}
    except Exception as e:
        logger.error(f"TG webhook error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/tg")
async def telegram_webhook_get():
    """GET endpoint for webhook verification"""
    return {"status": "ok", "message": "Telegram webhook active"}
