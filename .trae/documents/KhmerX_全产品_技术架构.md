# KhmerX 全产品技术文档（Architecture）V1

域名
- 官网：`https://khmerx.org`
- Mini App：`https://app.khmerx.org`
- API：`https://api.khmerx.org`
- 后台：`https://admin.khmerx.org`

API Base（生产）
- `https://api.khmerx.org/api/v1`

---

## 1. 实际技术栈（与仓库一致）

后端
- FastAPI（Python）
- SQLAlchemy 2.x（ORM）
- 数据库：PostgreSQL（生产）/ SQLite（开发与测试）

前端
- Mini App：React + Vite + TS + Tailwind（`frontend/miniapp`）
- Admin：React + Vite + TS + Tailwind（`frontend/admin`）

官网（建议 V1，偏 SEO/SSG）
- 推荐：Next.js + Tailwind + i18n（/km /en /zh）+ SSG
- 托管：Cloudflare + Vercel 或 VPS Nginx
- 原因：SEO 强、多语言友好、加载快、易扩展 Blog

---

## 2. 总体架构

```mermaid
graph TD
  TG[Telegram Client] --> MA[Mini App app.khmerx.org]
  WEB[Website khmerx.org (/km /en /zh)] --> API[FastAPI api.khmerx.org]
  MA --> API
  ADM[Admin admin.khmerx.org] --> API
  API --> DB[(PostgreSQL)]
  API --> FS[(Proof Storage: /proofs)]
```

要点
- Mini App 不依赖 Bot Token 做“会话”，而是使用每次请求携带 `telegram_init_data` 的 TMA 认证方式。
- 后端校验 `initData` 时支持多 Bot token（主/备用），以便 Bot 容灾切换。
- 业务数据统一落库（users/offers/trades/repayments/disputes/risk）。

---

## 3. 认证设计（TMA）

### 3.1 Header 规范
- `Authorization: tma <telegram_init_data>`
- `X-Lang: cn | km`

### 3.2 校验流程
1) 解析 `initData`（querystring）
2) 提取 `hash`，对其余字段按 key 排序拼接 `data_check_string`
3) 对每个可用 Bot token：
   - `secret_key = HMAC_SHA256("WebAppData", bot_token)`
   - `expected_hash = HMAC_SHA256(secret_key, data_check_string)`
   - 任意一个 token 匹配即通过
4) 校验 `auth_date` 是否过期（默认 24h）
5) 解析 `user` JSON，使用 `tg_id` upsert 用户（一个 tg_id 对应一个用户）

### 3.3 多 Bot token 来源
- 数据库（优先）：`bot_accounts` 中 `status=active` 的 token 列表，优先 `is_primary=true`
- 环境变量（兜底）：`BOT_TOKENS=tokenA,tokenB`

实现位置
- `initData` 校验：[auth.py](file:///d:/projects/khmerx/app/services/auth.py)
- V1 鉴权依赖：[auth.py](file:///d:/projects/khmerx/app/api_v1/auth.py)
- bot accounts 获取：[bot_accounts.py](file:///d:/projects/khmerx/app/services/bot_accounts.py)

---

## 4. API 设计（V1）

### 4.1 统一返回
成功：
```json
{ "ok": true, "data": {}, "message": "success" }
```
失败：
```json
{ "ok": false, "error": { "code": "RISK_REJECTED", "message": "当前额度不足", "details": {} } }
```

### 4.2 核心错误码
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

### 4.3 MVP 必须接口（已提供 /api/v1）
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
- `GET /notifications`（MVP 可返回空）

实现位置
- 路由集合：[router.py](file:///d:/projects/khmerx/app/api_v1/router.py)

---

## 5. 权限矩阵（避免越权）

原则
- 客户端不允许通过传入 `user_id` 来“代表别人操作”。
- 服务端以 `Authorization: tma <initData>` 推导当前用户（tg_id→user），再做角色与资源归属校验。

矩阵（V1）
| 能力 | Borrower | Lender | Agent | Admin |
|---|---:|---:|---:|---:|
| GET /me | ✓ | ✓ | ✓ | ✓ |
| PATCH /me/profile | ✓ | ✓ | ✓ | ✓ |
| GET /offers | ✓ | ✓ | ✓ | ✓ |
| POST /offers | ✓ | - | - | ✓ |
| POST /offers/{id}/match | - | ✓ | - | ✓ |
| POST /trades/{id}/confirm-lend | - | ✓ | - | ✓ |
| POST /trades/{id}/confirm-receive | ✓ | - | - | ✓ |
| POST /trades/{id}/repay | ✓ | - | - | ✓ |
| POST /trades/{id}/confirm-repayment | - | ✓ | - | ✓ |
| POST /disputes | ✓ | ✓ | - | ✓ |
| POST /disputes/{id}/evidence | ✓ | ✓ | - | ✓ |

---

## 6. 状态机与幂等

幂等建议（V1）
- `match`：同一 offer 只能创建 1 个 trade；重复请求应返回已匹配状态
- `confirm-lend`：重复上传同一 proof，保持最后一次为准或拒绝（需定口径）
- `confirm-receive`：只允许从 lend_confirmed 到 repayment_confirmed
- `repay`：schedule 只允许从 pending/overdue 到 paid_pending
- `confirm-repayment`：只允许从 paid_pending 到 paid

---

## 7. 争议模型（Dispute）

类型（dispute_type）
- lend_not_received / repay_not_received / wrong_amount / fake_proof / other

状态
- open / reviewing / resolved / rejected

裁决结果（resolution_result）
- borrower_win / lender_win / both_fault / cancel_trade / manual_continue

---

## 8. 风控原因字段规范（reasons/actions）

目的
- 前端可直接展示“为什么被限制/如何恢复”，且可多语言。

建议结构
- reasons：数组（按优先级降序）
  - code：稳定枚举（如 NEW_USER_LIMIT/OVERDUE_COUNT/PROFILE_INCOMPLETE/RELATION_RISK）
  - message：已本地化文案
  - severity：info/warn/error
  - metadata：数值（逾期次数、限制天数等）
- actions：数组
  - code：BIND_PROFILE/REPAY_ON_TIME/WAIT_REVIEW
  - message：已本地化文案

---

## 9. 官网 SEO/GEO 交付物清单（技术）

必须
- `hreflang`：/km /en /zh
- `canonical`
- `robots.txt`
- `sitemap.xml`（按语言）
- JSON-LD：Organization、WebSite、FAQPage（FAQ页）
- 每页正文包含“是什么/服务谁/地区/怎么用/ABA/Telegram/风险声明”结构化段落

---

## 5. 领域模型与数据口径

### 5.1 核心实体
- User：以 `tg_id` 唯一；资料字段 phone/ABA；角色 user/agent/admin
- Offer（p2p_offers）：借款挂单（pending→matched/cancelled）
- Trade（p2p_trades）：交易（matched→lend_confirmed→repayment_confirmed→repaying→completed；异常 overdue/dispute/cancelled）
- RepaymentSchedule：还款计划（pending/paid_pending/paid/overdue）
- Dispute：争议（open/reviewing/resolved）
- Risk：风险档案/风险事件/风险日志

### 5.2 交易状态机
- `matched`：等待放款人打款（24h 倒计时）
- `lend_confirmed`：放款人已上传打款凭证
- `repayment_confirmed`：借款人确认收款
- `repaying`：还款中
- `completed`：完成
- `overdue/defaulted`：逾期/违约
- `dispute`：争议中

---

## 6. 数据库结构

### 6.1 生产“最终结构”（greenfield）
- 完整 SQL：`docs/khmerx-postgres-v1-schema.sql`

### 6.2 当前仓库实现（说明）
- 当前代码使用 UUID 作为多数主键（适合服务端与分布式），并兼容 SQLite 测试。
- 生产如果采用 BIGSERIAL 的 greenfield 结构，需要进行一次“主键类型迁移/适配层”工程；建议在 MVP 阶段保持 UUID 方案一致，等稳定后再做数据库结构升级。

---

## 7. 部署与配置

### 7.1 必要环境变量
- `DATABASE_URL`（PostgreSQL 生产）
- `BOT_TOKENS`（多 Bot token，逗号分隔）或使用 `bot_accounts` 表
- `CORS_ORIGINS=https://khmerx.org,https://app.khmerx.org,https://admin.khmerx.org`
- `UPLOAD_DIR=./uploads/proofs`
- `UPLOAD_BASE_URL=https://api.khmerx.org`

示例见：`.env.example`

### 7.3 官网（SEO/GEO）实现要点
- URL：`/km` 为主站，`/en`、`/zh` 为语言版本
- Head：每页必须设置 `title/description/canonical/hreflang`
- 结构化数据：建议全站插入 JSON-LD（Organization + WebSite + FAQPage（FAQ页））
- 站点地图：`sitemap.xml`（按语言生成）
- 抓取策略：`robots.txt`（允许抓取静态页面，屏蔽非公开管理路径）
- 文案原则：每页明确回答“是什么/服务谁/地区/怎么用/ABA/Telegram/风险声明”

### 7.4 入口与深链
- 官网 CTA 必须指向 Telegram Mini App：`https://t.me/KhmerXBot/app`
- 支持 agent 邀请：`https://t.me/KhmerXBot/app?startapp=<invite_code>`

### 7.2 Proof 静态访问
- 上传：`POST /api/v1/uploads/proof`
- 访问：`https://api.khmerx.org/proofs/<file>`

---

## 10. 定时任务与自动化（V1.1 必做）

目标
- 把“超时/逾期/提醒”从人工操作变成可审计的自动化，降低事故率。

任务清单
- Trade 超时
  - 扫描 `matched` 且 `advance_pay_deadline < now` 的交易
  - 动作：标记 `cancelled` 并写入风险日志（cancel_count +1）
- Repayment 逾期
  - 扫描到期未还的 `repayment_schedules`
  - 动作：schedule 标记 `overdue`，trade 可联动标记 `overdue`
- 通知生成（仅用户订阅）
  - 到期前 24h/48h 生成 App 内通知
  - 争议状态变化生成通知

实现建议
- 本地/开发：`SCHEDULER_ENABLED=false` 可禁用
- 生产：使用独立 worker（cron/queue）或启用 APScheduler（需显式依赖与监控）

---

## 11. 管理员审计日志（V1.1 必做）

记录范围
- 封禁/解封
- 调分/改风控规则
- 仲裁裁决
- 改利率矩阵/运营配置

字段建议
- admin_id、action、target_type、target_id、before/after、reason、created_at

---

## 8. 安全与合规

必须执行
- 任何 Bot Token 泄露视为事故：立即 BotFather 重置并替换
- `.env` 永不提交（仓库已加入 `.gitignore`）
- 不主动私聊用户、不群发（通知仅用户触发/订阅）
