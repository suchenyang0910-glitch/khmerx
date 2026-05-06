"""验机路由"""
import uuid
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import InspectionCreate, InspectionOut
from app.models.inspection import Inspection
from app.models.product import Product

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/inspections", tags=["inspections"])


@router.post("", response_model=InspectionOut)
async def create_inspection(req: InspectionCreate, inspector_id: str = "", db: Session = Depends(get_db)):
    """提交验机报告"""
    try:
        pid = uuid.UUID(req.product_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid product_id")

    product = db.query(Product).filter(Product.id == pid).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    inspector_uuid = None
    if inspector_id:
        try:
            inspector_uuid = uuid.UUID(inspector_id)
        except ValueError:
            pass

    inspection = Inspection(
        product_id=pid,
        inspector_id=inspector_uuid,
        condition=req.condition,
        battery_health=req.battery_health,
        result=req.result,
        notes=req.notes,
        video_url=req.video_url,
    )
    db.add(inspection)

    # 验机通过则标记为已验证
    if req.result == "pass":
        product.is_verified = True

    db.commit()
    db.refresh(inspection)
    logger.info(f"Inspection created: {inspection.id} - result={req.result}")
    return inspection


@router.get("/{product_id}", response_model=list[InspectionOut])
async def get_inspections(product_id: str, db: Session = Depends(get_db)):
    """查询商品的所有验机报告"""
    try:
        pid = uuid.UUID(product_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid product_id")

    inspections = db.query(Inspection).filter(
        Inspection.product_id == pid
    ).order_by(Inspection.created_at.desc()).all()
    return inspections
