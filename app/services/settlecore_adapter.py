"""
KhmerX → SettleCore Merchant API 对接层

对接方式：SettleCore Merchant API (Bearer Token)
- POST /merchant/payment/create    → 创建支付订单，获取 TRC20 收款地址
- POST /merchant/withdraw          → 放款给卖家（提现）
- Webhook: KhmerX 接收 SettleCore 回调

Mock 模式（SETTLECORE_ENABLED=false）用于本地开发
"""
import uuid
import logging
from datetime import datetime, timezone, timedelta
from typing import Optional
import httpx

from app.config import (
    SETTLECORE_BASE_URL,
    SETTLECORE_ENABLED,
    SETTLECORE_API_KEY,
)

logger = logging.getLogger(__name__)

# ── Mock 模式数据 ──
MOCK_PAYMENTS: dict = {}
MOCK_COUNTER = 0


def _headers() -> dict:
    """SettleCore Merchant API 认证头"""
    if not SETTLECORE_API_KEY:
        logger.warning("SETTLECORE_API_KEY not set")
        return {}
    return {"Authorization": f"Bearer {SETTLECORE_API_KEY}"}


async def _sc_post(path: str, payload: dict, timeout: int = 15) -> dict:
    """向 SettleCore Merchant API 发 POST"""
    if not SETTLECORE_ENABLED:
        logger.info(f"[MOCK] POST {path}: {payload}")
        return _mock_create_payment(payload)

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{SETTLECORE_BASE_URL}{path}",
            json=payload,
            headers=_headers(),
            timeout=timeout,
        )
        if resp.status_code == 401:
            logger.error("SettleCore: API Key rejected (401)")
            raise PermissionError("SettleCore API Key 无效，请检查 SETTLECORE_API_KEY")
        resp.raise_for_status()
        return resp.json()


# ── Mock 实现 ──
def _mock_create_payment(payload: dict) -> dict:
    global MOCK_COUNTER
    MOCK_COUNTER += 1
    order_id = payload.get("order_id", f"mock-{MOCK_COUNTER}")
    mock = {
        "success": True,
        "order_uuid": MOCK_COUNTER + 100,
        "payment_address": f"T{uuid.uuid4().hex[:24].upper()}MOCK",
        "payment_url": None,
        "channel_payment_id": None,
        "status": "pending",
        "qr_code": f"scpay://merchant/{MOCK_COUNTER + 100}",
        "expires_at": (datetime.now(timezone.utc) + timedelta(hours=2)).isoformat(),
        "_mock": True,
    }
    MOCK_PAYMENTS[order_id] = mock
    logger.info(f"[MOCK] Created payment order_id={order_id}")
    return mock


def _mock_query_payment(order_id: str) -> dict:
    mock = MOCK_PAYMENTS.get(order_id)
    if mock:
        return {"status": mock.get("status", "pending"), "payment_address": mock.get("payment_address", "")}
    return {"status": "not_found"}


# ═══════════════════════════════════════════════════
# 对外接口
# ═══════════════════════════════════════════════════

async def create_payment_order(order_id: str, amount: float, currency: str = "USDT") -> dict:
    """
    创建 SettleCore 支付订单
    返回 { success, order_uuid, payment_address, status, expires_at }
    """
    payload = {
        "amount": amount,
        "currency": currency,
        "order_id": order_id,
    }
    return await _sc_post("/merchant/payment/create", payload)


async def check_payment_status(order_uuid: int) -> dict:
    """
    查询支付状态
    返回 { status, ... }
    注：SettleCore merchant API 暂未有公开查询接口，走 webhook 方式
    """
    if not SETTLECORE_ENABLED:
        return _mock_query_payment(str(order_uuid))
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{SETTLECORE_BASE_URL}/merchant/payment/{order_uuid}",
                headers=_headers(),
                timeout=10,
            )
            if resp.status_code == 200:
                return resp.json()
    except Exception as e:
        logger.warning(f"check_payment_status failed: {e}")
    return {"status": "unknown"}


async def get_merchant_balance() -> dict:
    """
    查询商户余额
    返回 { balance, currency }
    """
    if not SETTLECORE_ENABLED:
        return {"balance": 9999.0, "currency": "USDT", "_mock": True}

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{SETTLECORE_BASE_URL}/merchant/balance",
            headers=_headers(),
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()


# ═══════════════════════════════════════════════════
# Webhook 处理器 — 处理 SettleCore 回调
# ═══════════════════════════════════════════════════

async def handle_webhook(payload: dict) -> dict:
    """
    处理 SettleCore merchant webhook 回调
    期待的 payload 格式:
    {
        "event": "payment.paid",
        "order_id": "khmerx-order-uuid",
        "tx_hash": "...",
        "amount": 100.0,
        "status": "paid"
    }
    返回 { status, order_id, new_status }
    """
    from app.database import SessionLocal
    from app.models.order import Order
    from app.models.product import Product

    event = payload.get("event", "")
    order_id_str = payload.get("order_id", "")
    tx_hash = payload.get("tx_hash", "")

    if not order_id_str:
        return {"status": "error", "message": "missing order_id"}

    db = SessionLocal()
    try:
        order = db.query(Order).filter(Order.id == order_id_str).first()
        if not order:
            logger.warning(f"Webhook: order not found {order_id_str}")
            return {"status": "error", "message": "order not found"}

        logger.info(f"Webhook received: event={event}, order={order_id_str}, tx={tx_hash}")

        if event == "payment.paid":
            if order.status not in ("pending_payment",):
                return {"status": "skipped", "message": f"order status is {order.status}"}
            order.status = "escrowed"
            order.pay_status = "paid"
            order.settlecore_tx_hash = tx_hash or order.settlecore_tx_hash
            # 锁定商品
            product = db.query(Product).filter(Product.id == order.product_id).first()
            if product and product.status == "on_sale":
                product.status = "locked"

        elif event == "escrow.released":
            order.status = "completed"
            order.pay_status = "released"
            product = db.query(Product).filter(Product.id == order.product_id).first()
            if product:
                product.status = "sold"

        elif event == "escrow.refunded":
            order.status = "refunded"
            order.pay_status = "refunded"
            product = db.query(Product).filter(Product.id == order.product_id).first()
            if product:
                product.status = "on_sale"

        elif event == "escrow.disputed":
            order.pay_status = "disputed"

        else:
            logger.warning(f"Unknown webhook event: {event}")
            return {"status": "error", "message": f"unknown event: {event}"}

        order.updated_at = datetime.now(timezone.utc)
        db.commit()
        logger.info(f"Webhook processed: {event} -> status={order.status}")
        return {"status": "ok", "order_id": str(order.id), "new_status": order.status}

    except Exception as e:
        db.rollback()
        logger.error(f"Webhook handler error: {e}")
        return {"status": "error", "message": str(e)}
    finally:
        db.close()


# ═══════════════════════════════════════════════════
# 旧 P2P 接口（已废弃，保留 stub 防止导入报错）
# ═══════════════════════════════════════════════════

async def ensure_khmerx_user_in_settlecore(db, user_id: str, tg_id: int) -> dict:
    """已废弃 — KhmerX 不再对接 SettleCore USDT P2P"""
    logger.warning(f"ensure_khmerx_user_in_settlecore called (deprecated): user_id={user_id}")
    return {}


async def get_payment_address(user_id: str) -> dict:
    """已废弃"""
    return {"deposit_address": ""}


async def transfer_from_platform_to_seller(address: str, amount: float) -> dict:
    """已废弃"""
    return {"tx_hash": "", "status": "deprecated"}


async def get_deposit_status(user_id, since=None) -> list:
    """已废弃"""
    return []


async def release_escrow(escrow_id: str) -> dict:
    """已废弃"""
    return {"success": False, "message": "SettleCore deprecated"}


async def refund_escrow(escrow_id: str) -> dict:
    """已废弃"""
    return {"success": False, "message": "SettleCore deprecated"}


async def dispute_escrow(escrow_id: str) -> dict:
    """已废弃"""
    return {"success": False, "message": "SettleCore deprecated"}
