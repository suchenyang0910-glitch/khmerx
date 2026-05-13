# KX-AIRE (MVP)

## 模块

- `auth-service`：商户 API Key 换取 JWT；提供 `/auth/token`、`/auth/me`
- `risk-engine-service`：基于规则表 `risk_engine.risk_rules` 的风控评估；提供 `/risk/check`

## 依赖

- PostgreSQL 16
- Redis

## 环境变量

- `DB_HOST` `DB_PORT` `DB_NAME` `DB_USER` `DB_PASSWORD`
- `REDIS_HOST` `REDIS_PORT` `REDIS_DB_AUTH` `REDIS_DB_RISK`
- `JWT_SECRET_BASE64` `JWT_EXPIRATION_MS`

默认 `DB_NAME` 为 `kx_aire`，并使用 `Schema` 进行隔离：`merchant_center`、`risk_engine` 等。

## 数据库初始化

在目标数据库执行：

```bash
psql -h localhost -U postgres -d kx_aire -f kx-aire/sql/init.sql
psql -h localhost -U postgres -d kx_aire -f kx-aire/sql/seed_mvp.sql
```

## 接口

### auth-service

- `POST /auth/token`

请求体：

```json
{ "merchantId": "m_demo", "apiKey": "demo_key" }
```

响应体：

```json
{ "accessToken": "...", "tokenType": "Bearer", "expiresInMs": 86400000 }
```

### risk-engine-service

- `POST /risk/check`（需要 `Authorization: Bearer <token>`）
 - `GET /risk/rules?scenarioType=...`（需要 `Authorization: Bearer <token>`）
 - `POST /risk/rules/reload?scenarioType=...`（需要 `Authorization: Bearer <token>`）
 - `GET /risk/events?scenarioType=&status=&keyword=&page=&pageSize=`（需要 `Authorization: Bearer <token>`）
 - `GET /risk/events/{eventId}`（需要 `Authorization: Bearer <token>`）
 - `POST /risk/events/{eventId}/dispositions`（需要 `Authorization: Bearer <token>`）
 - `GET /system/audit?page=&pageSize=&actorId=&action=&objectType=&objectId=`（需要 `Authorization: Bearer <token>`）
 - `GET /system/me`（需要 `Authorization: Bearer <token>`）
 - `GET /system/users?page=&pageSize=&keyword=`（需要 `Authorization: Bearer <token>`）
 - `POST /system/users`（需要 `Authorization: Bearer <token>`）
 - `POST /system/users/{userId}/status`（需要 `Authorization: Bearer <token>`）
 - `POST /system/users/{userId}/roles`（需要 `Authorization: Bearer <token>`）
 - `GET /system/roles`（需要 `Authorization: Bearer <token>`）
 - `GET /system/permissions`（需要 `Authorization: Bearer <token>`）
 - `POST /system/roles/{roleId}/permissions`（需要 `Authorization: Bearer <token>`）

请求体：

```json
{
  "orderId": "o_001",
  "userId": "u_001",
  "scenarioType": "phone_rental",
  "applyAmount": 500.0,
  "userAgeDays": 2,
  "offers24hCount": 1,
  "activeTradesCount": 0,
  "blacklistHits": 0,
  "phone": "85512345678",
  "idNumber": "KHM-ID-XXX",
  "deviceId": "device-xxx",
  "ipAddress": "1.2.3.4"
}
```

规则表达式使用 Spring Expression Language，可引用变量：

- `applyAmount`
- `userAgeDays`
- `offers24hCount`
- `activeTradesCount`
- `blacklistHits`
- `scenarioType`
- `merchantId`
- `userId`
- `orderId`

