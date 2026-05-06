from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid


# ── Auth ─────────────────────────────────────────────────────────
class TelegramLoginRequest(BaseModel):
    init_data: str = Field(..., description="Telegram WebApp initData string")


class UserOut(BaseModel):
    id: uuid.UUID
    global_user_id: Optional[uuid.UUID] = None
    tg_id: int
    name: str
    photo_url: str = ""
    role: str = "user"
    risk_level: str = "normal"
    created_at: datetime

    class Config:
        from_attributes = True


# ── Product ──────────────────────────────────────────────────────
class ProductCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str = ""
    price: float = Field(..., gt=0)
    category: str = "phone"
    images: str = ""
    video_url: str = ""
    contact_info: str = ""
    source: str = "user"


class ProductOut(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    price: float
    status: str
    owner_id: uuid.UUID
    source: str
    is_verified: bool
    images: str
    video_url: str
    contact_info: str
    category: str
    created_at: datetime

    class Config:
        from_attributes = True


# ── Order ────────────────────────────────────────────────────────
class OrderCreateRequest(BaseModel):
    product_id: str = Field(..., description="Product UUID")


class OrderConfirmRequest(BaseModel):
    order_id: str = Field(..., description="Order UUID")


class OrderCancelRequest(BaseModel):
    order_id: str = Field(..., description="Order UUID")


class OrderDisputeRequest(BaseModel):
    order_id: str = Field(..., description="Order UUID")
    reason: str = ""


class OrderOut(BaseModel):
    id: uuid.UUID
    product_id: uuid.UUID
    buyer_id: uuid.UUID
    seller_id: uuid.UUID
    amount: float
    status: str
    settlecore_escrow_id: Optional[str] = None
    pay_address: Optional[str] = None
    pay_amount: Optional[float] = None
    pay_status: str = "created"
    settlement_status: str = ""
    settlecore_tx_hash: Optional[str] = None
    shipped_at: Optional[datetime] = None
    notes: str = ""
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ── Inspection ───────────────────────────────────────────────────
class InspectionCreate(BaseModel):
    product_id: str
    condition: str = ""
    battery_health: int = 0
    result: str = "pass"
    notes: str = ""
    video_url: str = ""


class InspectionOut(BaseModel):
    id: uuid.UUID
    product_id: uuid.UUID
    inspector_id: Optional[uuid.UUID] = None
    condition: str
    battery_health: int
    result: str
    notes: str
    video_url: str
    created_at: datetime

    class Config:
        from_attributes = True


# ── SettleCore Webhook ───────────────────────────────────────────
class SettlecoreWebhook(BaseModel):
    event: str  # payment.paid / escrow.released / escrow.refunded / escrow.disputed
    escrow_id: str
    order_id: str
    tx_hash: Optional[str] = None
    amount: Optional[float] = None
    status: Optional[str] = None
