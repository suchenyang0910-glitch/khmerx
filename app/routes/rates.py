"""汇率路由 — 管理 USD/KHR 汇率"""
import uuid
import logging
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.rate import Rate
from app.i18n import t, fmt_amount

logger = logging.getLogger(__name__)
router = APIRouter(tags=["rates"])


@router.post("/admin/rates/set")
async def set_rate(
    request: Request,
    buy_rate: float,
    sell_rate: float,
    source: str = "admin",
    db: Session = Depends(get_db),
):
    """管理员设置当天汇率"""
    if buy_rate <= 0 or sell_rate <= 0:
        raise HTTPException(status_code=400, detail="Rates must be positive")
    if buy_rate > sell_rate:
        raise HTTPException(status_code=400, detail="buy_rate must be <= sell_rate")

    today = datetime.now(timezone.utc).date()
    rate = Rate(
        currency_pair="USD/KHR",
        buy_rate=buy_rate,
        sell_rate=sell_rate,
        source=source,
        rate_date=today,
    )
    db.add(rate)
    db.commit()
    db.refresh(rate)

    lang = getattr(request.state, "lang", "cn")

    logger.info(f"Rate set: USD/KHR buy={buy_rate} sell={sell_rate} source={source}")
    return {
        "status": "ok",
        "currency_pair": "USD/KHR",
        "buy_rate": buy_rate,
        "sell_rate": sell_rate,
        "_labels": {
            "buy": f"{t('price', lang)} (Buy)",
            "sell": f"{t('price', lang)} (Sell)",
        },
        "source": source,
        "rate_date": today.isoformat(),
        "lang": lang,
    }


@router.get("/rates/current")
async def get_current_rate(
    request: Request,
    db: Session = Depends(get_db),
):
    """获取当天最新汇率"""
    today = datetime.now(timezone.utc).date()
    rate = db.query(Rate).filter(
        Rate.currency_pair == "USD/KHR",
        Rate.rate_date == today
    ).order_by(Rate.created_at.desc()).first()

    lang = getattr(request.state, "lang", "cn")

    if not rate:
        # 返回默认汇率
        return {
            "currency_pair": "USD/KHR",
            "buy_rate": 4050.0,
            "sell_rate": 4100.0,
            "source": "default",
            "rate_date": today.isoformat(),
            "_labels": {
                "note": t("no_rate_warning", lang),
            },
            "lang": lang,
        }

    return {
        "currency_pair": rate.currency_pair,
        "buy_rate": rate.buy_rate,
        "sell_rate": rate.sell_rate,
        "source": rate.source,
        "rate_date": rate.rate_date.isoformat(),
        "lang": lang,
    }
