"""用户认证路由 — KhmerX 登录 + ABA 微借贷扩展"""
import uuid
import logging
import hashlib
import hmac
import json
import time
from urllib.parse import urlencode
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.database import get_db
from app.schemas import TelegramLoginRequest, UserOut
from app.services.auth import verify_telegram_init_data, login_or_register
from app.services.bot_accounts import get_active_bot_tokens
from app.config import BOT_TOKENS, DEV_TMA_ENABLED
from app.models.user import User
from app.risk.models import DeviceFingerprint
from app.risk.relations import RelationService
from app.i18n import localize_auth, t
from app.services.otp import request_phone_otp, verify_phone_otp

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/dev-tma")
def dev_tma(
    tg_id: int = Query(10001),
    first_name: str = Query("Dev"),
    username: str = Query("dev"),
):
    if not DEV_TMA_ENABLED:
        raise HTTPException(status_code=404, detail="Not Found")

    token = BOT_TOKENS[0] if BOT_TOKENS else ""
    if not token:
        raise HTTPException(status_code=500, detail="Bot token not configured")

    auth_date = int(time.time())
    user_json = json.dumps(
        {"id": tg_id, "first_name": first_name, "username": username},
        ensure_ascii=False,
        separators=(",", ":"),
    )

    data = {
        "auth_date": str(auth_date),
        "query_id": hashlib.sha256(f"{tg_id}:{auth_date}".encode()).hexdigest(),
        "user": user_json,
    }

    data_check_string = "\n".join(f"{k}={data[k]}" for k in sorted(data.keys()))
    secret_key = hmac.new(b"WebAppData", token.encode(), hashlib.sha256).digest()
    data["hash"] = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    return {"ok": True, "data": {"init_data": urlencode(data)}}


# ── Pydantic schemas ─────────────────────────────────────────────

class PhoneVerifyRequest(BaseModel):
    user_id: str = Field(..., description="User UUID")
    phone: str = Field(..., min_length=8, max_length=20, description="手机号")


class OtpRequestRequest(BaseModel):
    user_id: str = Field(..., description="User UUID")
    phone: str = Field(..., min_length=8, max_length=20, description="手机号")


class OtpVerifyRequest(BaseModel):
    user_id: str = Field(..., description="User UUID")
    phone: str = Field(..., min_length=8, max_length=20, description="手机号")
    code: str = Field(..., min_length=4, max_length=10, description="OTP code")


class KycVerifyRequest(BaseModel):
    user_id: str = Field(..., description="User UUID")
    document_url: str = Field(..., description="KYC 文件 URL")


class AbaBindRequest(BaseModel):
    user_id: str = Field(..., description="User UUID")
    aba_account: str = Field(..., min_length=6, max_length=32, description="ABA 银行账号")
    aba_name: str = Field(..., min_length=1, max_length=128, description="ABA 账户名")


class DeviceFingerprintUpsertRequest(BaseModel):
    user_id: str = Field(..., description="User UUID")
    device_id: str = Field(default="", description="设备ID")
    ip_hash: str = Field(default="", description="IP Hash")
    user_agent_hash: str = Field(default="", description="UA Hash")
    fingerprint_hash: str = Field(default="", description="设备指纹Hash")


class BindAgentRequest(BaseModel):
    user_id: str = Field(..., description="User UUID")
    agent_id: str = Field(..., description="Agent UUID")


# ── Helper ────────────────────────────────────────────────────────

def _get_user(db: Session, user_id_str: str) -> User:
    try:
        uid = uuid.UUID(user_id_str)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user_id")
    user = db.query(User).filter(User.id == uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ── TG 登录（原接口） ────────────────────────────────────────────

@router.post("/telegram-login")
async def telegram_login(
    req: TelegramLoginRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    """TG Mini App 登录 — 验证 initData 签名并登录/注册"""
    tokens = []
    try:
        tokens = get_active_bot_tokens(db)
    except Exception:
        tokens = []

    for t in BOT_TOKENS:
        if t and t not in tokens:
            tokens.append(t)

    tg_user = verify_telegram_init_data(req.init_data, tokens)
    if not tg_user:
        raise HTTPException(status_code=401, detail="Invalid Telegram init data")

    user = login_or_register(db, tg_user)
    lang = getattr(request.state, "lang", "km")
    return localize_auth({
        "id": str(user.id),
        "global_user_id": str(user.id),
        "tg_id": user.tg_id,
        "name": user.name,
        "photo_url": user.photo_url or "",
        "role": user.role,
        "risk_level": user.risk_level,
        "credit_score": user.credit_score,
        "verification_level": user.verification_level,
        "phone": user.phone or "",
        "phone_verified": bool(user.phone_verified_at),
        "aba_account": user.aba_account or "",
        "aba_name": user.aba_name or "",
        "total_borrowed": user.total_borrowed,
        "total_repaid": user.total_repaid,
        "active_loans": user.active_loans,
        "created_at": user.created_at.isoformat(),
    }, lang)


@router.get("/me")
async def get_me(
    user_id: str,
    request: Request,
    db: Session = Depends(get_db),
):
    """获取当前用户信息"""
    user = _get_user(db, user_id)
    lang = getattr(request.state, "lang", "km")
    return localize_auth({
        "id": str(user.id),
        "global_user_id": str(user.id),
        "tg_id": user.tg_id,
        "name": user.name,
        "photo_url": user.photo_url or "",
        "role": user.role,
        "risk_level": user.risk_level,
        "credit_score": user.credit_score,
        "verification_level": user.verification_level,
        "phone": user.phone or "",
        "phone_verified": bool(user.phone_verified_at),
        "aba_account": user.aba_account or "",
        "aba_name": user.aba_name or "",
        "total_borrowed": user.total_borrowed,
        "total_repaid": user.total_repaid,
        "active_loans": user.active_loans,
        "created_at": user.created_at.isoformat(),
    }, lang)


# ── OTP：请求验证码 ───────────────────────────────────────────

@router.post("/otp/request")
async def request_otp(
    req: OtpRequestRequest,
    db: Session = Depends(get_db),
):
    user = _get_user(db, req.user_id)
    res = request_phone_otp(db, user=user, phone=req.phone)
    payload = {"status": "ok", "challenge_id": res.challenge_id}
    if res.dev_code is not None:
        payload["dev_code"] = res.dev_code
    return payload


@router.post("/otp/verify")
async def verify_otp(
    req: OtpVerifyRequest,
    db: Session = Depends(get_db),
):
    user = _get_user(db, req.user_id)
    verify_phone_otp(db, user=user, phone=req.phone, code=req.code)
    return {"status": "ok", "verification_level": user.verification_level, "phone": user.phone or ""}


# ── 兼容端点：verify/phone（旧） ───────────────────────────────

@router.post("/verify/phone")
async def verify_phone(
    req: PhoneVerifyRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    """提交手机号验证"""
    user = _get_user(db, req.user_id)

    from app import config

    if not config.OTP_DEV_MODE:
        raise HTTPException(status_code=400, detail="Use /auth/otp/request and /auth/otp/verify")

    user.phone = req.phone.strip()
    user.phone_verified_at = datetime.utcnow()
    if user.verification_level == "unverified":
        user.verification_level = "phone"
    db.commit()
    return {"status": "ok", "verification_level": user.verification_level, "phone": user.phone}


# ── 新端点：提交 KYC ────────────────────────────────────────────

@router.post("/verify/kyc")
async def verify_kyc(
    req: KycVerifyRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    """提交 KYC 文件 URL（本阶段先 log，后续加 OCR）"""
    user = _get_user(db, req.user_id)

    # TODO: 接入 OCR 验证文档
    logger.info(
        f"User {user.id} submitted KYC document: {req.document_url}"
    )

    # 升级验证等级
    if user.verification_level == "phone":
        user.verification_level = "kyc"
    elif user.verification_level == "unverified":
        # 需要先验证手机号
        raise HTTPException(
            status_code=400,
            detail="Please verify your phone number first"
        )
    elif user.verification_level in ("kyc", "full"):
        user.verification_level = "full"

    db.commit()

    return {
        "status": "ok",
        "verification_level": user.verification_level,
        "document_url": req.document_url,
        "message": "KYC document submitted, will be reviewed",
    }


# ── 新端点：绑定 ABA ─────────────────────────────────────────────

@router.post("/aba/bind")
async def bind_aba(
    req: AbaBindRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    """绑定 ABA 银行账户"""
    user = _get_user(db, req.user_id)

    if not user.phone_verified_at:
        raise HTTPException(
            status_code=400,
            detail="Please verify your phone number before binding ABA account"
        )

    user.aba_account = req.aba_account.strip()
    user.aba_name = req.aba_name.strip()

    # 如果已有 kyc 验证，升为 full
    if user.verification_level == "kyc":
        user.verification_level = "full"

    db.commit()

    logger.info(
        f"User {user.id} bound ABA: {req.aba_account} ({req.aba_name})"
    )

    return {
        "status": "ok",
        "aba_account": req.aba_account,
        "aba_name": req.aba_name,
        "verification_level": user.verification_level,
    }


@router.post("/device")
async def upsert_device_fingerprint(
    req: DeviceFingerprintUpsertRequest,
    db: Session = Depends(get_db),
):
    user = _get_user(db, req.user_id)

    fp = DeviceFingerprint(
        user_id=user.id,
        tg_id=user.tg_id,
        device_id=req.device_id.strip() or None,
        ip_hash=req.ip_hash.strip() or None,
        user_agent_hash=req.user_agent_hash.strip() or None,
        fingerprint_hash=req.fingerprint_hash.strip() or None,
    )
    db.add(fp)
    db.commit()
    db.refresh(fp)

    RelationService(db).build_relations_for_user(user.id)

    return {"status": "ok", "device_fingerprint_id": fp.id}


@router.post("/agent/bind")
async def bind_agent(
    req: BindAgentRequest,
    db: Session = Depends(get_db),
):
    user = _get_user(db, req.user_id)
    if user.agent_id:
        raise HTTPException(status_code=400, detail="agent_id already bound")

    agent = _get_user(db, req.agent_id)
    if agent.role != "agent":
        raise HTTPException(status_code=400, detail="target user is not an agent")

    user.agent_id = agent.id
    user.inviter_id = agent.id
    db.commit()

    from app.risk.relations import RelationService

    RelationService(db).build_relations_for_user(user.id)

    return {"status": "ok", "agent_id": str(agent.id)}


# ── 新端点：查询信用分 ───────────────────────────────────────────

@router.get("/credit-score")
async def get_credit_score(
    request: Request,
    user_id: str = Query(..., description="User UUID"),
    db: Session = Depends(get_db),
):
    """查看我的信用分"""
    user = _get_user(db, user_id)
    lang = getattr(request.state, "lang", "km")

    return {
        "user_id": str(user.id),
        "name": user.name,
        "credit_score": user.credit_score,
        "verification_level": user.verification_level,
        "total_borrowed": user.total_borrowed,
        "total_repaid": user.total_repaid,
        "active_loans": user.active_loans,
        "monthly_referrals": user.monthly_referrals,
        "_label": {
            "credit_score": t("credit_score", lang),
            "aba_account": t("aba_account", lang),
            "aba_name": t("aba_name", lang),
        },
        "lang": lang,
    }


class LangPreferenceRequest(BaseModel):
    user_id: str = Field(..., description="User UUID")
    lang: str = Field(..., min_length=2, max_length=8, description="语言偏好: km/cn")


@router.post("/lang")
async def set_lang(
    req: LangPreferenceRequest,
    db: Session = Depends(get_db),
):
    """设置用户语言偏好"""
    user = _get_user(db, req.user_id)
    if req.lang not in ("km", "cn"):
        raise HTTPException(status_code=400, detail="Language must be 'km' or 'cn'")
    user.preferred_lang = req.lang
    db.commit()
    return {
        "status": "ok",
        "preferred_lang": req.lang,
        "message": f"Language set to {'ភាសាខ្មែរ' if req.lang == 'km' else '中文'}",
    }


print("=== Task 3.3 done ===")
