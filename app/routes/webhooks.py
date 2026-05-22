"""Webhook 回调 — 支付适配层"""
import logging
import json
import uuid

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app import config
from app.database import get_db
from app.schemas import SettlecoreWebhook
from app.services.salary_loan_payments import apply_repayment
from app.services.settlecore_adapter import handle_webhook
from app.services.webhook_hmac import verify_signature
from app.models.salary_loan_order import SalaryLoanOrder

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


@router.post("/salary-loan/repayment")
async def salary_loan_repayment_webhook(request: Request, db: Session = Depends(get_db)):
    body = await request.body()
    ok_sig, reason = verify_signature(
        secret=config.SALARY_LOAN_WEBHOOK_SECRET,
        timestamp=request.headers.get("X-KHX-Timestamp"),
        signature=request.headers.get("X-KHX-Signature"),
        body=body,
        max_skew_seconds=config.SALARY_LOAN_WEBHOOK_MAX_SKEW_SECONDS,
    )
    if not ok_sig:
        raise HTTPException(status_code=401, detail=reason)

    try:
        payload = json.loads(body.decode("utf-8") or "{}")
    except Exception:
        raise HTTPException(status_code=400, detail="invalid json")

    order_id = (payload.get("order_id") or "").strip()
    payment_id = (payload.get("payment_id") or payload.get("tx_id") or "").strip()
    amount = payload.get("amount")

    if not order_id or not payment_id or amount is None:
        raise HTTPException(status_code=400, detail="missing order_id/payment_id/amount")

    try:
        oid = uuid.UUID(order_id)
    except Exception:
        raise HTTPException(status_code=400, detail="invalid order_id")

    o = db.query(SalaryLoanOrder).filter(SalaryLoanOrder.id == oid).first()
    if not o:
        raise HTTPException(status_code=404, detail="order not found")

    result = apply_repayment(db, order=o, amount=float(amount), external_ref=payment_id)
    if not result.get("ok"):
        raise HTTPException(status_code=400, detail=result.get("message") or "failed")

    db.commit()
    return result
