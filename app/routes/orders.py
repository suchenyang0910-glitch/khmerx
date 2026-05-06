"""订单路由 — MVP 核心"""
import uuid
import logging
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import (
    OrderCreateRequest,
    OrderConfirmRequest,
    OrderCancelRequest,
    OrderDisputeRequest,
    OrderOut,
)
from app.models.order import Order
from app.models.product import Product
from app.models.user import User
from app.services.settlecore_adapter import (
    create_payment_order,
    release_escrow,
    refund_escrow,
    dispute_escrow,
)
from app.services.risk_engine import RiskEngine
from app.config import SELLER_DELIVERY_HOURS

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/create", response_model=OrderOut)
async def create_order(req: OrderCreateRequest, buyer_id: str, db: Session = Depends(get_db)):
    """
    创建订单：
    1. 风控检查
    2. 创建订单记录（pending_payment）
    3. 调用 SettleCore 创建托管单，获取收款地址
    4. 返回订单信息
    """
    try:
        pid = uuid.UUID(req.product_id)
        bid = uuid.UUID(buyer_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID")

    # 查商品
    product = db.query(Product).filter(Product.id == pid).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.status != "on_sale":
        raise HTTPException(status_code=400, detail="Product is not available")

    # 查用户
    buyer = db.query(User).filter(User.id == bid).first()
    if not buyer:
        raise HTTPException(status_code=404, detail="Buyer not found")

    # 自己不能买自己的商品
    if product.owner_id == bid:
        raise HTTPException(status_code=400, detail="Cannot buy your own product")

    # ⚡ 风控检查
    risk = RiskEngine(db)
    blocked, reason = risk.pre_order_check(buyer, product.price)
    if blocked:
        raise HTTPException(status_code=403, detail=f"风险检查未通过: {reason}")

    # 创建订单
    order = Order(
        product_id=pid,
        buyer_id=bid,
        seller_id=product.owner_id,
        amount=product.price,
        status="pending_payment",
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    # 调用 SettleCore Merchant API 创建支付订单
    try:
        payment = await create_payment_order(str(order.id), order.amount)
        if payment.get("success"):
            order.settlecore_escrow_id = str(payment.get("order_uuid", ""))
            order.pay_address = payment.get("payment_address", "")
            order.pay_amount = order.amount
            order.pay_status = "pending"
        else:
            logger.error(f"SettleCore payment creation returned error: {payment}")
        db.commit()
        db.refresh(order)
    except Exception as e:
        logger.error(f"SettleCore payment creation failed for order {order.id}: {e}")
        # 订单保留，走手动处理

    logger.info(f"Order created: {order.id} - product {product.title}")
    return order


@router.get("/{order_id}", response_model=OrderOut)
async def get_order(order_id: str, db: Session = Depends(get_db)):
    """订单详情"""
    try:
        oid = uuid.UUID(order_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid order_id")
    order = db.query(Order).filter(Order.id == oid).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.get("", response_model=list[OrderOut])
async def list_orders(
    user_id: str = "",
    role: str = "buyer",  # buyer / seller
    status: str = "",
    db: Session = Depends(get_db),
):
    """获取用户订单列表"""
    if not user_id:
        return []

    try:
        uid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user_id")

    query = db.query(Order)
    if role == "buyer":
        query = query.filter(Order.buyer_id == uid)
    else:
        query = query.filter(Order.seller_id == uid)

    if status:
        query = query.filter(Order.status == status)

    query = query.order_by(Order.created_at.desc())
    return query.all()


@router.post("/confirm")
async def confirm_order(req: OrderConfirmRequest, db: Session = Depends(get_db)):
    """
    买家确认收货：
    1. 校验订单状态为 escrowed
    2. 调用 SettleCore release
    3. 更新订单状态
    """
    try:
        oid = uuid.UUID(req.order_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid order_id")

    order = db.query(Order).filter(Order.id == oid).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status != "escrowed":
        raise HTTPException(status_code=400, detail=f"Order status is {order.status}, not escrowed")

    if order.settlecore_escrow_id:
        try:
            result = await release_escrow(order.settlecore_escrow_id)
            order.pay_status = "released"
            order.settlement_status = "released"
        except Exception as e:
            logger.error(f"Release failed for order {order.id}: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to release funds: {e}")

    order.status = "completed"
    order.updated_at = datetime.now(timezone.utc)

    # 商品标记已售
    product = db.query(Product).filter(Product.id == order.product_id).first()
    if product:
        product.status = "sold"

    # 更新买家订单计数
    buyer = db.query(User).filter(User.id == order.buyer_id).first()
    if buyer:
        buyer.order_count = (buyer.order_count or 0) + 1

    db.commit()

    logger.info(f"Order confirmed: {order.id}")
    return {"status": "ok", "order_id": str(order.id), "new_status": "completed"}


@router.post("/cancel")
async def cancel_order(req: OrderCancelRequest, user_id: str = "", db: Session = Depends(get_db)):
    """
    取消订单（仅 pending_payment 状态可取消）:
    1. 更新状态
    2. 记录取消到风控
    """
    try:
        oid = uuid.UUID(req.order_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid order_id")

    order = db.query(Order).filter(Order.id == oid).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status != "pending_payment":
        raise HTTPException(status_code=400, detail=f"Order status is {order.status}, cannot cancel")

    order.status = "cancelled"
    order.updated_at = datetime.now(timezone.utc)

    # 记录取消行为
    if user_id:
        try:
            uid = uuid.UUID(user_id)
            buyer = db.query(User).filter(User.id == uid).first()
            if buyer:
                risk = RiskEngine(db)
                risk.record_cancel(buyer)
        except (ValueError, Exception):
            pass

    db.commit()
    logger.info(f"Order cancelled: {order.id}")
    return {"status": "ok", "order_id": str(order.id), "new_status": "cancelled"}


@router.post("/dispute")
async def dispute_order(req: OrderDisputeRequest, db: Session = Depends(get_db)):
    """发起纠纷"""
    try:
        oid = uuid.UUID(req.order_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid order_id")

    order = db.query(Order).filter(Order.id == oid).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status not in ("escrowed", "shipped"):
        raise HTTPException(status_code=400, detail=f"Order status is {order.status}, can only dispute escrowed/shipped orders")

    order.status = "disputed"
    order.notes = req.reason
    order.updated_at = datetime.now(timezone.utc)

    if order.settlecore_escrow_id:
        try:
            await dispute_escrow(order.settlecore_escrow_id)
        except Exception as e:
            logger.error(f"Dispute failed for order {order.id}: {e}")

    db.commit()
    logger.info(f"Order disputed: {order.id}")
    return {"status": "ok", "order_id": str(order.id), "new_status": "disputed"}


@router.post("/ship")
async def mark_shipped(order_id: str, db: Session = Depends(get_db)):
    """
    卖家标记已发货（人工触发，后续可改为自动）
    """
    try:
        oid = uuid.UUID(order_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid order_id")

    order = db.query(Order).filter(Order.id == oid).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status != "escrowed":
        raise HTTPException(status_code=400, detail=f"Order status is {order.status}, cannot ship")

    now = datetime.now(timezone.utc)
    order.status = "shipped"
    order.shipped_at = now
    order.deliver_deadline = now + timedelta(hours=SELLER_DELIVERY_HOURS)
    order.updated_at = now
    db.commit()

    logger.info(f"Order marked shipped: {order.id}")
    return {"status": "ok", "order_id": str(order.id), "new_status": "shipped"}
