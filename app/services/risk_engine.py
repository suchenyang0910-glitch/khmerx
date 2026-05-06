"""
最小风控引擎

规则：
1. 连续取消限制 — 同一用户连续取消 > MAX_CANCEL_LIMIT 次，限制下单 24h
2. 卖家延迟发货 — 订单 escrowed > SELLER_DELIVERY_HOURS 未发货，标记 + 自动退款
3. 高频不支付 — 高频率创建订单不支付，标记观察
4. 新用户大额审核 — 新用户首单 > NEW_USER_MAX_AMOUNT 需人工审核
"""
import logging
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.config import (
    MAX_CANCEL_LIMIT,
    CANCEL_BAN_HOURS,
    MAX_PENDING_ORDERS,
    NEW_USER_MAX_AMOUNT,
    SELLER_DELIVERY_HOURS,
)
from app.models.user import User
from app.models.order import Order

logger = logging.getLogger(__name__)


class RiskEngine:

    def __init__(self, db: Session):
        self.db = db

    # ── 规则 1: 连续取消限制 ──────────────────────────────────
    def check_cancel_limit(self, user: User) -> tuple[bool, str]:
        """
        检查用户是否被限制下单。
        返回 (blocked: bool, reason: str)
        """
        now = datetime.now(timezone.utc)

        # 检查是否在封禁期内
        if user.cancel_banned_until and user.cancel_banned_until > now:
            remaining = (user.cancel_banned_until - now).total_seconds() / 3600
            return True, f"连续取消受限，剩余 {remaining:.0f} 小时后恢复"

        # 检查连续取消次数
        if user.consecutive_cancels >= MAX_CANCEL_LIMIT:
            # 设置封禁
            user.cancel_banned_until = now + timedelta(hours=CANCEL_BAN_HOURS)
            user.consecutive_cancels = 0
            self.db.commit()
            return True, f"连续取消超过 {MAX_CANCEL_LIMIT} 次，限制下单 {CANCEL_BAN_HOURS} 小时"

        return False, ""

    # ── 记录取消 ──────────────────────────────────────────────
    def record_cancel(self, user: User):
        """记录一次取消行为"""
        user.consecutive_cancels = (user.consecutive_cancels or 0) + 1
        self.db.commit()
        logger.info(f"Risk: user {user.tg_id} cancel count → {user.consecutive_cancels}")

    # ── 取消封禁到期后重置 ────────────────────────────────────
    def reset_cancel_ban(self, user: User):
        """封禁到期后调用"""
        user.consecutive_cancels = 0
        user.cancel_banned_until = None
        self.db.commit()

    # ── 规则 2: 卖家延迟发货 ──────────────────────────────────
    def check_seller_delivery(self, order: Order) -> tuple[bool, str]:
        """
        检查卖家是否超时未发货。
        订单 escrowed 状态超过 SELLER_DELIVERY_HOURS 小时。
        """
        if order.status != "escrowed":
            return False, ""

        if not order.deliver_deadline:
            return False, ""

        now = datetime.now(timezone.utc)
        if now > order.deliver_deadline:
            seller = self.db.query(User).filter(User.id == order.seller_id).first()
            if seller:
                seller.risk_level = "flagged"
                self.db.commit()
            return True, f"卖家超时未发货（已超过 {SELLER_DELIVERY_HOURS} 小时）"

        return False, ""

    # ── 规则 3: 高频不支付 ────────────────────────────────────
    def check_frequent_nonpayment(self, user: User) -> tuple[bool, str]:
        """
        检查用户是否有大量未支付订单。
        """
        pending_count = self.db.query(Order).filter(
            Order.buyer_id == user.id,
            Order.status == "pending_payment",
        ).count()

        if pending_count >= MAX_PENDING_ORDERS:
            user.risk_level = "flagged"
            self.db.commit()
            return True, f"待支付订单超过 {MAX_PENDING_ORDERS} 个，已标记观察"

        return False, ""

    # ── 规则 4: 新用户大额审核 ────────────────────────────────
    def check_new_user_large_order(self, user: User, amount: float) -> tuple[bool, str]:
        """
        新用户（订单数量 < 3）首单金额超过阈值，需要人工审核。
        """
        if user.order_count and user.order_count >= 3:
            return False, ""

        if amount > NEW_USER_MAX_AMOUNT:
            user.risk_level = "flagged"
            self.db.commit()
            return True, f"新用户首单 ${amount:.2f} > ${NEW_USER_MAX_AMOUNT:.2f}，需人工审核"

        return False, ""

    # ── 下单前完整检查 ────────────────────────────────────────
    def pre_order_check(self, buyer: User, amount: float) -> tuple[bool, str]:
        """
        下单前执行全部风控检查。
        返回 (passed: bool, reason: str)
        """
        # 规则 1: 连续取消限制
        blocked, reason = self.check_cancel_limit(buyer)
        if blocked:
            return True, reason

        # 规则 3: 高频不支付
        blocked, reason = self.check_frequent_nonpayment(buyer)
        if blocked:
            return True, reason

        # 规则 4: 新用户大额
        blocked, reason = self.check_new_user_large_order(buyer, amount)
        if blocked:
            return True, reason

        return False, ""
