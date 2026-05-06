# KhmerX API V1

Base URL: `https://api.khmerx.org/api/v1`

相关域名
- 官网：`https://khmerx.org`
- Mini App：`https://app.khmerx.org`
- API：`https://api.khmerx.org`
- 后台：`https://admin.khmerx.org`

## 认证
- Header: `Authorization: tma <telegram_init_data>`
- Header: `X-Lang: cn | km`

说明：服务端以 `tg_id` 识别用户，并映射为 `global_user_id`（账户唯一标识）。

## 统一返回
成功：
```json
{ "ok": true, "data": {}, "message": "success" }
```

失败：
```json
{ "ok": false, "error": { "code": "RISK_REJECTED", "message": "当前额度不足", "details": {} } }
```

## 核心错误码
- `AUTH_REQUIRED`
- `PROFILE_INCOMPLETE`
- `ABA_REQUIRED`
- `RISK_REJECTED`
- `MANUAL_REVIEW_REQUIRED`
- `OFFER_NOT_FOUND`
- `TRADE_NOT_FOUND`
- `INVALID_STATUS`
- `DISPUTE_LOCKED`
- `UPLOAD_FAILED`
- `PERMISSION_DENIED`

## MVP 必须接口（已提供 /api/v1）
- `GET /me`
- `PATCH /me/profile`
- `GET /me/credit`
- `POST /p2p/calculate`
- `POST /offers`
- `GET /offers`
- `GET /offers/{offer_id}`
- `POST /offers/{offer_id}/cancel`
- `POST /offers/{offer_id}/match`
- `GET /trades`
- `GET /trades/{trade_id}`
- `POST /trades/{trade_id}/confirm-lend`
- `POST /trades/{trade_id}/confirm-receive`
- `POST /trades/{trade_id}/repay`
- `POST /trades/{trade_id}/confirm-repayment`
- `POST /uploads/proof`
- `POST /disputes`
- `POST /disputes/{dispute_id}/evidence`
- `GET /disputes/{dispute_id}`
- `GET /notifications`
