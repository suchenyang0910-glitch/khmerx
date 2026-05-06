"""商品路由"""
import uuid
import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.database import get_db
from app.schemas import ProductCreate, ProductOut
from app.models.product import Product
from app.models.user import User

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductOut])
async def list_products(
    source: Optional[str] = Query(None, description="Filter by source: stock / user"),
    category: Optional[str] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, description="Search by title"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    """商品列表 — 支持筛选和搜索，stock 优先排列"""
    query = db.query(Product).filter(Product.status.in_(["on_sale", "locked"]))

    if source:
        query = query.filter(Product.source == source)
    if category:
        query = query.filter(Product.category == category)
    if search:
        query = query.filter(Product.title.ilike(f"%{search}%"))

    # 排序：stock 优先，然后按创建时间倒序
    query = query.order_by(
        # stock 排前面
        Product.source == "stock",
        Product.created_at.desc(),
    )

    products = query.offset(offset).limit(limit).all()
    return products


@router.get("/{product_id}", response_model=ProductOut)
async def get_product(product_id: str, db: Session = Depends(get_db)):
    """商品详情"""
    try:
        pid = uuid.UUID(product_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid product_id")
    product = db.query(Product).filter(Product.id == pid).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("", response_model=ProductOut)
async def create_product(req: ProductCreate, user_id: str, db: Session = Depends(get_db)):
    """发布商品"""
    try:
        uid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user_id")

    user = db.query(User).filter(User.id == uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    product = Product(
        title=req.title,
        description=req.description,
        price=req.price,
        owner_id=uid,
        source=req.source,
        category=req.category,
        images=req.images,
        video_url=req.video_url,
        contact_info=req.contact_info,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    logger.info(f"Product created: {product.id} - {product.title}")
    return product
