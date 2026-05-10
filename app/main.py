"""KhmerX API — 柬埔寨最可信的手机与资产交易平台"""
import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.staticfiles import StaticFiles

from app.config import HOST, PORT, CORS_ORIGINS, validate_runtime_config
from app.database import init_db
from app.routes import auth, products, orders, inspections, webhooks, p2p, rates, telegram_bot
from app.routes import interest_rates
from app.risk.router import router as risk_router
from app.disputes.router import router as disputes_router
from app.ops.router import router as ops_router
from app.admin.router import router as admin_router
from app.openclaw.router import router as openclaw_router
from fastapi import Request

from app.api_v1.errors import ApiError
from app.api_v1.responses import fail
from app.api_v1.router import router as api_v1_router

# ── Logging ──────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


# ── Lifespan ─────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 KhmerX API starting...")
    try:
        validate_runtime_config()
    except Exception:
        logger.error("Config validation failed; continuing startup", exc_info=True)
    init_db()
    logger.info("✅ Database tables ready")
    from app.scheduler.runner import start_scheduler

    app.state.scheduler = start_scheduler()
    yield
    scheduler = getattr(app.state, "scheduler", None)
    if scheduler:
        scheduler.shutdown()
    logger.info("👋 KhmerX API shutting down")


# ── App ──────────────────────────────────────────────────────────
app = FastAPI(
    title="KhmerX API",
    description="KhmerX — ABA កម្ចីប្រាក់ | ABA 微借贷平台",
    version="0.1.0",
    lifespan=lifespan,
)


@app.exception_handler(ApiError)
async def api_error_handler(request: Request, exc: ApiError):
    if request.url.path.startswith("/api/v1"):
        return JSONResponse(
            status_code=exc.status_code,
            content=fail(exc.code, exc.message, exc.details),
        )
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

# CORS — 允许 Mini App 访问
default_origins = [
    "https://khmerx.org",
    "https://app.khmerx.org",
    "https://admin.khmerx.org",
    "https://api.khmerx.org",
]

allow_origin_regex = r"^https?://(localhost|127\\.0\\.0\\.1)(:\\d+)?$|^https://([a-z0-9-]+\\.)*khmerx\\.org$"
origins = CORS_ORIGINS
if not origins:
    origins = default_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=allow_origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Middleware: 解析 lang 查询参数 ──────────────────────────────
@app.middleware("http")
async def add_lang_header(request: Request, call_next):
    """
    从 query 或 header 提取 lang 参数，注入到 request.state.lang
    优先使用 header X-Lang，其次 query param lang
    """
    lang = request.headers.get("X-Lang", "")
    if not lang:
        lang = request.query_params.get("lang", "km")
    if lang not in ("km", "en", "cn"):
        lang = "km"
    request.state.lang = lang
    response = await call_next(request)
    return response


# ── Routes ───────────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(inspections.router)
app.include_router(webhooks.router)
app.include_router(telegram_bot.router)
app.include_router(p2p.router)
app.include_router(rates.router)
app.include_router(interest_rates.router)
app.include_router(risk_router)
app.include_router(disputes_router)
app.include_router(ops_router)
app.include_router(admin_router)
app.include_router(api_v1_router)
app.include_router(openclaw_router)


upload_dir = os.getenv("UPLOAD_DIR", "./uploads/proofs")
os.makedirs(upload_dir, exist_ok=True)
app.mount("/proofs", StaticFiles(directory=upload_dir), name="proofs")


@app.get("/health")
async def health():
    return {"status": "ok", "service": "khmerx-api"}


# ── Main ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=True)
