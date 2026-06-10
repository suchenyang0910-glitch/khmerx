# Debug Session: telegram-login-500 [OPEN]

## Symptom
- Production `POST /auth/telegram-login` returns 500.
- Static assets, `/health`, and CORS preflight are healthy.
- Local malformed requests produce expected 401/422 instead of 500.

## Hypotheses
1. `verify_telegram_init_data(...)` throws an uncaught exception for real Telegram `init_data`.
2. Active bot token resolution returns an unexpected value set in production and crashes verification flow.
3. Database access during active token lookup fails intermittently in production.
4. Request payload shape is valid enough to pass schema validation but contains edge-case content that breaks downstream parsing.
5. Exception handling around `/auth/telegram-login` is incomplete, so a recoverable auth failure is surfacing as 500.

## Evidence Plan
- Add instrumentation at route entry, token resolution, verification start/end, and exception boundary.
- Reproduce against production-equivalent request path.
- Compare failing trace with expected 401/422 local outcomes.

## Status
- Session opened.
- Instrumentation added to `app/routes/auth.py` and `app/services/auth.py`.
- Debug server running with session `telegram-login-500`.
- Awaiting runtime evidence from one failing `/auth/telegram-login` request.
