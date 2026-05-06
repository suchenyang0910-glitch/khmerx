"""SettleCore Webhook 回调 — 支付适配层"""
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import SettlecoreWebhook
from app.services.settlecore_adapter import handle_webhook

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/khmerx/webhooks", tags=["webhooks"])

# 幂等性缓存（内存，重启后丢失但在线期间足够用）
PROCESSED_EVENTS = set()


@router.post("/settlecore")
async def settlecore_webhook(payload: dict, db: Session = Depends(get_db)):
    """
    接收 SettleCore Merchant Webhook 回调。

    回调示例:
    {
        "event": "payment.paid",
        "order_id": "khmerx-order-uuid",
        "tx_hash": "tx_hash_here",
        "amount": 100.0,
        "status": "paid"
    }
    """
    event = payload.get("event", "")
    order_id = payload.get("order_id", "")

    if not event or not order_id:
        raise HTTPException(status_code=400, detail="Missing event or order_id")

    # 幂等校验
    idem_key = f"{order_id}:{event}"
    if idem_key in PROCESSED_EVENTS:
        logger.info(f"Webhook duplicate skipped: {idem_key}")
        return {"status": "skipped", "message": "already processed"}

    PROCESSED_EVENTS.add(idem_key)

    # 处理回调（新 adapter 不需要 db 参数）
    result = await handle_webhook(payload)
    logger.info(f"Webhook processed: {event} → {result}")
    return result
