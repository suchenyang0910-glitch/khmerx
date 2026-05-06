# KhmerX 风控系统落地说明 V1（P2P 优先）

## 1. SQL 初始化

- PostgreSQL 初始化脚本：`migrations/001_risk_system_init.sql`

说明：当前后端用户/交易主键为 UUID，因此该迁移脚本使用 UUID 作为 `user_id/trade_id/offer_id`。

## 2. 风控模块代码结构

- 目录：`app/risk/`
- 核心文件：
  - `models.py`：`user_risk_profiles` / `risk_logs` / `risk_events` / `risk_rules` / `disputes`
  - `service.py`：档案创建、扣分、封禁、事件写入
  - `engine.py`：CreateOffer/MatchOffer/逾期/超时 等核心判断
  - `router.py`：对外 API（含 OpenClaw 盯盘接口）

## 3. 风控 API（含 OpenClaw）

基础风控检查：

- `POST /risk/check/create-offer`
- `POST /risk/check/match-offer`

事件入口（给 scheduler 或业务回调触发）：

- `POST /risk/events/repayment-overdue`
- `POST /risk/events/repayment-paid`

OpenClaw 盯盘接口：

- `GET /risk/events/pending?limit=50`
- `POST /risk/events/{event_id}/handled?handled_by=openclaw`
- `GET /risk/dashboard`
- `GET /risk/flagged-users`
- `GET /risk/logs?user_id=&trade_id=&limit=100`

争议/仲裁：

- `POST /disputes?user_id=`
- `POST /disputes/evidence?user_id=`
- `POST /disputes/resolve?admin_id=`
- `GET /disputes/my?user_id=`

管理员动作：

- `POST /risk/users/{user_id}/block?reason=&hours=&admin_id=`
- `POST /risk/users/{user_id}/unblock?admin_id=`
- `POST /risk/users/adjust-score?admin_id=`

## 4. OpenClaw Prompt（建议）

你是 KhmerX 风控运营员。

每 5 分钟执行一次：

1) 请求 `GET /risk/events/pending`
2) 按 `severity` 处理：
   - `high`：立即通知管理员
   - `medium`：生成处理建议
   - `low`：记录观察
3) 对以下事件重点分析：
   - `repayment_defaulted`
   - `repayment_overdue`
   - `lender_no_pay_timeout`
   - `new_user_large_amount`
   - `offer_frequency_watch`
   - `daily_risk_summary`
4) 每次处理后调用 `POST /risk/events/{id}/handled`

## 5. Scheduler 定时任务

- 目录：`app/scheduler/`
- 启动：应用启动时自动启动（可用环境变量 `SCHEDULER_ENABLED=false` 关闭）

任务：

- 放款 24h 超时取消：每 5 分钟
- 还款逾期检查：每 30 分钟
- 临时封禁自动解封：每 10 分钟
- 生成每日风控摘要：23:55（UTC）

## 6. 关系图谱与反刷规则

- 设备指纹上报：`POST /auth/device`
- 匹配拦截：同手机号/同 ABA 直接拒绝；关系分 > 80 直接拒绝并生成人工审核单
- 信用增长：若借款人与放款人存在任意关系边（或重复/互借），不加信用分
