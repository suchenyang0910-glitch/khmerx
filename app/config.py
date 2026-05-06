import os

from dotenv import load_dotenv

load_dotenv()


def _split_csv(value: str) -> list[str]:
    return [v.strip() for v in (value or "").split(",") if v.strip()]


BOT_TOKENS = _split_csv(os.getenv("BOT_TOKENS", ""))
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
if BOT_TOKEN and not BOT_TOKENS:
    BOT_TOKENS = [BOT_TOKEN]

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./khmerx.db")

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "3030"))

WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")
MINI_APP_URL = os.getenv("MINI_APP_URL", "")

CORS_ORIGINS = _split_csv(os.getenv("CORS_ORIGINS", ""))

DEV_TMA_ENABLED = os.getenv("DEV_TMA_ENABLED", "false").lower() == "true"

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "")
ADMIN_JWT_SECRET = os.getenv("ADMIN_JWT_SECRET", "")

OPENCLAW_API_KEY = os.getenv("OPENCLAW_API_KEY", "")

SETTLECORE_BASE_URL = os.getenv("SETTLECORE_BASE_URL", "https://settlecore.org/api")
SETTLECORE_ENABLED = os.getenv("SETTLECORE_ENABLED", "false").lower() == "true"
SETTLECORE_API_KEY = os.getenv("SETTLECORE_API_KEY", "")
SETTLECORE_MERCHANT_ID = int(os.getenv("SETTLECORE_MERCHANT_ID", "0"))
SETTLECORE_PLATFORM_WALLET_ID = os.getenv("SETTLECORE_PLATFORM_WALLET_ID", "")

ABA_LENDING_ENABLED = os.getenv("ABA_LENDING_ENABLED", "true").lower() == "true"
PLATFORM_FEE_RATE = float(os.getenv("PLATFORM_FEE_RATE", "0.01"))
ADVANCE_PAY_HOURS = int(os.getenv("ADVANCE_PAY_HOURS", "24"))
DEFAULT_CREDIT_SCORE = int(os.getenv("DEFAULT_CREDIT_SCORE", "650"))
OVERDUE_DAYS_LIMIT = int(os.getenv("OVERDUE_DAYS_LIMIT", "7"))

OTP_DEV_MODE = os.getenv("OTP_DEV_MODE", "false").lower() == "true"
OTP_SECRET = os.getenv("OTP_SECRET", "")
OTP_CODE_TTL_SECONDS = int(os.getenv("OTP_CODE_TTL_SECONDS", "300"))
OTP_RESEND_MIN_SECONDS = int(os.getenv("OTP_RESEND_MIN_SECONDS", "60"))
OTP_MAX_VERIFY_ATTEMPTS = int(os.getenv("OTP_MAX_VERIFY_ATTEMPTS", "6"))
OTP_DAILY_LIMIT = int(os.getenv("OTP_DAILY_LIMIT", "10"))

SMS_PROVIDER = os.getenv("SMS_PROVIDER", "")
SMS_FROM = os.getenv("SMS_FROM", "")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")

NOTIFY_MAX_PER_TYPE_PER_DAY = int(os.getenv("NOTIFY_MAX_PER_TYPE_PER_DAY", "3"))

MAX_CANCEL_LIMIT = int(os.getenv("MAX_CANCEL_LIMIT", "3"))
CANCEL_BAN_HOURS = int(os.getenv("CANCEL_BAN_HOURS", "24"))
MAX_PENDING_ORDERS = int(os.getenv("MAX_PENDING_ORDERS", "5"))
NEW_USER_MAX_AMOUNT = float(os.getenv("NEW_USER_MAX_AMOUNT", "500.0"))
SELLER_DELIVERY_HOURS = int(os.getenv("SELLER_DELIVERY_HOURS", "48"))
