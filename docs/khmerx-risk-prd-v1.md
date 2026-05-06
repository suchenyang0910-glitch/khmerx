# KhmerX 风控系统 PRD V1（P2P ABA 微借贷优先）

## 1. 风控系统目标

核心目标只有 4 个：

- 降低坏账
- 防止刷单、骗贷、恶意接单
- 保护平台不碰资金、不背债务
- 让 OpenClaw 自动盯盘，提前发现异常

一句话：

- 风控系统不是为了“拦住所有风险”，而是为了让风险可识别、可分级、可处理。

## 2. 风控总架构

数据与控制链路：

- 用户行为
  - 创建挂单、接单、上传凭证、确认收款、还款、取消、发起 dispute
- 风控规则引擎
  - 每个业务动作前做校验（允许/拦截/转人工/限流）
- 信用分系统
  - 以行为为事件驱动，记录增减分
- 风险等级系统
  - 用户层风险等级（normal/watch/flagged/restricted/blocked）
- 交易状态控制
  - 对交易状态流转做硬约束
- OpenClaw 自动盯盘
  - 定时监控与建议/自动化动作
- 管理员人工复核
  - 仲裁 dispute、放行/封禁、调分、处理异常交易

## 3. 风险等级设计

### 3.1 用户风险等级

| 等级 | 状态 | 说明 | 处理 |
|---|---|---|---|
| normal | 正常 | 可正常借款/放款 | 正常使用 |
| watch | 观察 | 有轻微异常 | 降低额度 |
| flagged | 风险 | 多次异常行为 | 限制挂单/接单 |
| restricted | 受限 | 严重异常 | 只能还款，不能新交易 |
| blocked | 封禁 | 欺诈/恶意违约 | 禁止交易 |

### 3.2 动作与权限约束（最小可上线）

- `normal`：允许创建挂单、接单、上传凭证、确认收款、还款、发起 dispute。
- `watch`：允许上述动作，但降低额度/限制频率（见第 6 章）。
- `flagged`：限制创建挂单/接单；允许还款与 dispute。
- `restricted`：只能还款与 dispute；禁止任何新交易相关动作（创建挂单/接单/确认收款等）。
- `blocked`：禁止交易相关动作；允许查看历史与提交申诉（如保留）。

## 4. 信用分系统

### 4.1 初始分

- 新用户默认信用分：650

### 4.2 信用等级

| 分数 | 等级 | 借款额度 | 利率 |
|---|---|---|---|
| 800+ | A | 高 | 低 |
| 700-799 | B | 中高 | 中低 |
| 600-699 | C | 中低 | 中 |
| 500-599 | D | 低 | 高 |
| <500 | E | 禁止借款 | 禁止 |

## 5. 信用分变动规则

| 行为 | 分数变化 |
|---|---:|
| 按时还款 | +10 |
| 提前还款 | +5 |
| 完成首单 | +15 |
| 取消挂单 | -5 |
| 匹配后取消 | -10 |
| 放款人接单后未打款 | -20 |
| 借款人确认收款后逾期 | -20 |
| 逾期超过 7 天 | -50 |
| 仲裁失败 | -50 |
| 恶意欺诈 | -100 |
| 管理员确认黑名单 | 直接 blocked |

落地要求：

- 每一次分数变化必须写入 `risk_logs`（含 old/new 分数、old/new 风险等级、原因与触发来源）。
- 分数变化后必须同步刷新 `credit_level`（A/B/C/D/E）。

## 6. 借款额度风控

### 6.1 默认额度规则

| 用户类型 | 最大借款额度 |
|---|---|
| 新用户 | $100-$300 |
| 手机认证 | $500 |
| KYC 认证 | $1,000 |
| 老用户 A 级 | $2,000+ |
| 风险用户 | $0-$100 |

### 6.2 额度计算公式

- 可借额度 = 基础额度 × 信用等级系数 × 风险系数

示例：

- 基础额度 $500
- 信用等级 B = 1.2
- 风险 normal = 1.0
- 可借额度 = 500 × 1.2 × 1.0 = $600

### 6.3 额度落地要求（MVP）

- 创建挂单前必须校验：`amount <= max_borrow_amount`。
- 当 `credit_level=E` 或 `risk_level in (restricted, blocked)` 时，直接禁止借款。

## 7. 核心风控规则（P2P MVP 必须）

### 7.1 新用户限制

注册未满 7 天：

- 最大借款 $300
- 每天最多创建 1 个挂单
- 必须绑定 ABA 姓名和手机号

### 7.2 高频挂单限制

- 24 小时内创建挂单 ≥ 3 次 → 标记 `watch`
- 24 小时内创建挂单 ≥ 5 次 → 标记 `flagged`，禁止继续挂单 24h

### 7.3 连续取消限制

- 连续取消 3 次 → 禁止创建挂单 24h，信用分 -10
- 连续取消 5 次 → `restricted`

### 7.4 放款人接单不打款

接单后 24h 未上传 ABA 打款凭证：

- 交易 `cancelled`
- 放款人信用分 -20
- 24h 禁止接单

### 7.5 借款人逾期

到期未还：

- `repayment_schedules.status = overdue`
- 用户 `risk_level = watch`
- 信用分 -20

逾期 ≥ 7 天：

- `trade.status = defaulted`
- 用户 `risk_level = restricted`
- 信用分 -50

### 7.6 多账号风险

识别维度：

- `tg_id`
- `phone`
- `aba_account`
- `device_id`
- `ip_hash`
- `fingerprint_hash`

规则：

- 同一个 `aba_account` 绑定多个 TG 账号 → `flagged`
- 同一个设备注册多个账号 → `watch/flagged`
- 同一个手机号重复绑定 → `blocked` 或人工审核

### 7.7 金额异常

- 新用户借款 > $300 → 人工审核
- 单笔借款 > $500 → 人工审核
- 短时间连续借款 → `flagged`

### 7.8 交易争议（dispute）

- 任一方发起 `dispute` → 交易状态锁定，禁止继续状态流转
- admin 人工处理
- 仲裁失败方：信用分 -50，`risk_level = flagged`

## 8. 数据库新增/强化表（PostgreSQL）

### 8.1 `user_risk_profiles`

```sql
CREATE TABLE user_risk_profiles (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT NOT NULL,
  risk_level VARCHAR(30) DEFAULT 'normal',
  credit_score INT DEFAULT 650,
  credit_level VARCHAR(10) DEFAULT 'C',
  max_borrow_amount NUMERIC(12,2) DEFAULT 300,
  max_active_trades INT DEFAULT 1,
  cancel_count INT DEFAULT 0,
  overdue_count INT DEFAULT 0,
  default_count INT DEFAULT 0,
  dispute_lost_count INT DEFAULT 0,
  is_blocked BOOLEAN DEFAULT FALSE,
  block_reason TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### 8.2 `risk_logs`

```sql
CREATE TABLE risk_logs (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT,
  trade_id BIGINT,
  event_type VARCHAR(50),
  score_change INT DEFAULT 0,
  old_score INT,
  new_score INT,
  old_risk_level VARCHAR(30),
  new_risk_level VARCHAR(30),
  reason TEXT,
  created_by VARCHAR(30) DEFAULT 'system',
  created_at TIMESTAMP DEFAULT NOW()
);
```

### 8.3 `device_fingerprints`

```sql
CREATE TABLE device_fingerprints (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT NOT NULL,
  tg_id BIGINT,
  device_id VARCHAR(255),
  ip_hash VARCHAR(255),
  user_agent_hash VARCHAR(255),
  fingerprint_hash VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW()
);
```

### 8.4 `risk_rules`

```sql
CREATE TABLE risk_rules (
  id BIGSERIAL PRIMARY KEY,
  code VARCHAR(100) UNIQUE NOT NULL,
  name VARCHAR(255),
  rule_type VARCHAR(50),
  threshold_value NUMERIC(12,2),
  action VARCHAR(50),
  score_delta INT,
  enabled BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT NOW()
);
```

## 9. 风控 API（可上线版）

### 9.1 用户风控

- `GET /risk/users/{user_id}`
- `POST /risk/users/{user_id}/block`
- `POST /risk/users/{user_id}/unblock`
- `POST /risk/users/{user_id}/adjust-score`

### 9.2 交易风控

- `POST /risk/check/create-offer`
- `POST /risk/check/match-offer`
- `POST /risk/check/confirm-lend`
- `POST /risk/check/repay`

### 9.3 风控日志

- `GET /risk/logs`
- `GET /risk/logs?user_id=`
- `GET /risk/logs?trade_id=`

### 9.4 管理后台

- `GET /admin/risk/dashboard`
- `GET /admin/risk/flagged-users`
- `GET /admin/risk/overdue-trades`
- `GET /admin/risk/disputes`

## 10. OpenClaw 自动盯盘需求

### 10.1 每 5 分钟检查

- 新增高风险用户
- 即将逾期订单
- 已逾期订单
- 24h 未打款交易
- 高频挂单用户
- 多账号嫌疑

### 10.2 OpenClaw 输出动作

- 低风险：只记录 `risk_logs`
- 中风险：标记 `watch/flagged`、发送提醒、降低额度
- 高风险：冻结新交易、通知管理员、生成处理建议

### 10.3 每日风控报告

每日自动生成：

- 今日新增用户
- 今日挂单数
- 今日成交数
- 今日逾期数
- 今日坏账数
- 高风险用户列表
- 需要人工处理交易

## 11. 风控触发点

| 业务动作 | 是否检查风控 |
|---|---|
| 用户注册 | ✅ |
| 创建挂单 | ✅ |
| 放款人接单 | ✅ |
| 上传凭证 | ✅ |
| 确认收款 | ✅ |
| 还款 | ✅ |
| 发起 dispute | ✅ |
| 取消交易 | ✅ |
| 管理员改信用分 | ✅ |

## 12. MVP 必须先做的风控（第一版只做这 8 个）

1) 新用户额度限制
2) 连续取消限制
3) 接单不打款惩罚
4) 逾期自动标记
5) 逾期 7 天违约
6) 信用分动态变化
7) 多账号基础识别
8) OpenClaw 每日风控报告

## 13. 最终判断（优先级结论）

- KhmerX 的核心竞争力不在“借钱页面”，而在：谁敢借、能借多少、什么时候必须拦住。

优先顺序：

- PostgreSQL 风控表
- Risk Engine
- Scheduler
- OpenClaw 自动盯盘
- Mini App 风控展示

