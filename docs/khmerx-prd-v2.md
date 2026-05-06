# KhmerX 完整需求文档 V2（可上线版）

## 1. 项目核心定位（重新收敛）

### 1.1 项目本质

- KhmerX 是柬埔寨 ABA 微借贷的 P2P 借贷撮合 + 风控平台。
- 平台不触碰资金：资金流转仅发生在放款人与借款人之间，通过 ABA 转账完成。
- 平台的价值来自规则、风控、信用体系与运营自动化。

### 1.2 核心机制

- 人对人 ABA 转账 + 平台规则约束（匹配、定价、凭证确认、还款计划、风控、争议处理）。

### 1.3 收益模型

- 撮合费：交易额的 1%–5%（可配置）。
- 风控罚金：对违约/争议失败/欺诈等行为的惩罚性扣分与平台侧处罚（不从资金中扣款；以信用体系与平台使用权限约束为主）。

### 1.4 护城河

- 风控系统：风险识别、限制与自动处置。
- 信用体系：信用分、信用等级、额度与价格联动。
- 自动运营：OpenClaw 驱动的盯盘、预警、提醒、策略建议与自动化操作。

### 1.5 MVP 上线目标

- 跑通借贷闭环（唯一主流程）并稳定运行。
- 控制违约率（defaulted） < 10%。

### 1.6 MVP 范围与不做（明确约束）

- 只围绕：P2P + 风控 + Mini App + OpenClaw + Telegram Bot（通知/入口）。
- 不做：USDT P2P、不做任何加密支付、不做 SettleCore 对接、不做二手商品交易（Products/Orders/Inspections 模块）、不做验机/验货服务。

## 2. 系统总架构（核心模块）

- Mini App：用户主要入口（Telegram WebApp）。
- Backend（FastAPI）：业务 API、权限、状态机、风控与定时任务入口。
- PostgreSQL：核心数据存储。
- Risk Engine：风控规则执行与信用分变更。
- Scheduler：超时取消、逾期标记、还款提醒、周期性信用更新等。
- OpenClaw：AI 运营与自动风控（盯盘、预警、建议、自动化动作）。
- Telegram Bot：通知 + 打开 Mini App 的入口。

## 3. P2P 核心业务（最终确认版）

### 3.1 唯一主流程

1) 借款人发布需求（创建挂单）
2) 系统定价（利率 + 费率）
3) 挂单进入市场
4) 放款人接单（匹配）
5) 放款人 ABA 转账
6) 上传凭证
7) 借款人确认收款
8) 进入还款期
9) 分期还款
10) 放款人确认
11) 完成

### 3.2 关键业务约束

- 平台不持有资金、不生成链上交易、不代付。
- 资金凭证以“上传凭证 + 双方确认 + 平台记录”为准。
- 所有关键动作均需要权限校验与状态机校验。

## 4. 核心数据结构（PostgreSQL 版）

> 说明：以下为“可上线版”数据结构的业务字段集合，具体数据类型、索引与约束以实现时的数据库迁移为准。

### 4.1 `users`（强化版）

- `id`
- `tg_id`
- `name`
- `role`：`user` / `admin`
- `credit_score`
- `credit_level`：`A` / `B` / `C` / `D`
- `aba_account`
- `aba_name`
- `phone`
- `verification_level`
- `total_borrowed`
- `total_repaid`
- `total_defaulted`
- `risk_level`：`normal` / `flagged` / `blocked`
- `created_at`

业务约束建议：

- `tg_id` 唯一。
- `role`、`credit_level`、`risk_level` 使用枚举或 check constraint。

### 4.2 `p2p_offers`（挂单）

- `id`
- `borrower_id`
- `amount`
- `term_days`
- `rate`
- `fee`
- `status`：`pending` / `matched` / `cancelled` / `expired`
- `created_at`

业务约束建议：

- `term_days` 仅允许：`7/14/21/30`。
- `amount > 0`。

### 4.3 `p2p_trades`（交易）

- `id`
- `offer_id`
- `borrower_id`
- `lender_id`
- `amount`
- `rate`
- `fee`
- `status`：见第 5 章状态机
- `lend_deadline`（放款截止时间，默认创建后 24h）
- `created_at`

业务约束建议：

- `offer_id` 唯一（一个挂单只产生一笔交易）。
- `borrower_id` 必须等于挂单的 `borrower_id`。

### 4.4 `repayment_schedules`（还款）

- `id`
- `trade_id`
- `period`
- `due_at`
- `principal`
- `interest`
- `total`
- `status`：`pending` / `paid` / `overdue`

### 4.5 `interest_rate_matrix`（利率）

- `term_days`
- `credit_level`
- `monthly_rate`

业务约束建议：

- (`term_days`, `credit_level`) 组合唯一。

### 4.6 `disputes`（新增，关键）

- `id`
- `trade_id`
- `raised_by`（发起人 user_id）
- `reason`
- `evidence_urls`（数组或 JSON）
- `status`
- `resolution_note`
- `created_at`

目标：

- 为凭证争议、未收到款、恶意投诉等提供可追踪、可仲裁的闭环。

### 4.7 `risk_logs`（新增）

- `id`
- `user_id`
- `action`（如：score_change、flagged、blocked、rule_hit）
- `score_change`
- `reason`
- `created_at`

目标：

- 记录每一次风控动作与信用分变化，支撑运营审计与 OpenClaw 盯盘。

## 5. 状态机（最终锁定）

### 5.1 挂单状态机（`p2p_offers.status`）

- `pending` → `matched` → 转交易（创建 `p2p_trades`，挂单进入不可再匹配状态）
- `pending` → `cancelled`（借款人取消）
- `pending` → `expired`（创建后 24h 未匹配，系统自动过期）

触发：

- 借款人新建：进入 `pending`
- 放款人匹配：进入 `matched`
- 借款人取消：进入 `cancelled`
- 定时任务：进入 `expired`

### 5.2 交易状态机（`p2p_trades.status`）

主链路：

- `matched`（已匹配，等待放款）
  - → `lend_confirmed`（放款人确认已打款/上传凭证）
    - → `repayment_confirmed`（借款人确认收款）
      - → `repaying`（还款中）
        - → `completed`（所有期已还清）

异常分支：

- `matched` → `cancelled`（放款超 24h 未确认打款）
- `repaying` / `repayment_confirmed` → `defaulted`（逾期 ≥ 7 天，整笔违约）
- 任意关键节点 → `dispute`（进入争议处理，详见第 6 章）

## 6. 风控系统（核心升级）

本章对应的风控完整细则见：`docs/khmerx-risk-prd-v1.md`。

### 6.1 信用分机制（必须上线）

- 初始信用分：650

行为与分数变化（以 `risk_logs` 记录）：

- `+10`：正常还款
- `+5`：提前还款
- `-20`：逾期
- `-50`：违约
- `-10`：取消订单
- `-100`：欺诈或争议仲裁失败

落地要求：

- 所有分数变化必须通过统一的风控/积分服务执行，且写入 `risk_logs`。
- 分数变化后必须实时更新 `credit_level`（A/B/C/D）。

### 6.2 信用等级（定价与额度联动）

- A：800+
- B：700–799
- C：600–699
- D：<600

影响：

- 利率：由 `interest_rate_matrix` 按 `term_days + credit_level` 定价。
- 借款上限：由信用等级与风控状态决定（MVP 可先做“新用户 > 500 审核”与“blocked 禁止下单/接单”）。

### 6.3 核心风控规则（MVP 必须生效）

- 连续取消 3 次：封禁 24h（`risk_level` 可升到 `flagged` 或临时冻结下单权限）。
- 新用户借款 > $500：进入人工审核（MVP 先做 admin 标记与放行/拒绝）。
- 放款超 24h：交易自动取消。
- 逾期 7 天：整笔标记 `defaulted`。
- 高频操作：标记风险（`flagged`）。
- dispute 失败：信用降级/扣分并记录。

### 6.4 风控动作（状态）

- `normal` → `flagged` → `blocked`

要求：

- `blocked` 用户禁止创建挂单与接单。
- `flagged` 用户可能触发人工审核、额度限制或更高利率（MVP 可先只做“限制关键操作 + 运营列表可见”）。

### 6.5 争议（dispute）处理

目标：

- 在不触碰资金的前提下，提供“凭证争议 + 风控仲裁 + 信用处置”的闭环。

最小流程：

- 用户发起 dispute（上传证据）
- 管理员仲裁（支持：成立/不成立/需要补充材料）
- 形成 `resolution_note`，并触发信用分变化与风控状态变化

## 7. 定时任务系统（必须）

Scheduler 任务与频率：

- 每分钟：检查放款超时（24h）并自动取消交易
- 每小时：检查逾期并将对应期标记为 `overdue`
- 每天：发送还款提醒（到期前 24h）
- 每周：信用评分更新（例如：周期性纠偏/清理临时标记/运营复核；MVP 先保留入口与日志）

## 8. Mini App（前端完整需求）

### 8.1 技术栈

- React + Vite + Tailwind
- Telegram WebApp SDK

### 8.2 语言与本地化

- 默认高棉语 `km`，支持中文 `cn`。
- 后端所有 API 支持 `?lang=km|cn` 与 `X-Lang`。
- 前端所有文案必须可本地化，且与后端错误码/提示一致。

### 8.3 页面结构（5 大核心）

1) Dashboard

- 信用分与信用等级
- 当前借款与还款倒计时
- 快捷入口（发布借款/进入市场/查看交易）

2) 市场

- 挂单列表（金额/期限/利率/状态）
- 筛选（金额/期限/利率）
- 接单（匹配）

3) 发布借款

- 输入金额
- 选择期限（7/14/21/30）
- 自动算利率与平台费
- 提交挂单

4) 交易详情（核心页面）

- 双方信息与 ABA 账号
- 上传凭证（放款凭证、还款凭证）
- 状态流程条
- 还款计划（分期表、每期状态）

5) 我的

- 个人信息与 ABA 绑定
- 历史记录（交易/还款）
- 语言切换（km/cn）

### 8.4 权限与登录

- Telegram WebApp 首次打开即自动注册并建立会话。
- 普通用户不可访问任何 admin 能力。

## 9. OpenClaw 接入（自动运营核心）

### 9.1 OpenClaw 角色

- AI Operator（盯盘系统）：基于平台数据做监控、预警、建议与自动化动作。

### 9.2 接入点（数据输入）

- `p2p_trades`
- `p2p_offers`
- `repayment_schedules`
- `risk_logs`
- `disputes`

### 9.3 自动行为（MVP 先做可控闭环）

实时盯盘：

- 长时间未匹配挂单
- 高利率异常
- 高频取消用户

自动处理（建议分级）：

- 生成建议：如降利率建议、提醒运营介入
- 自动标记：对用户/交易打上 `flagged`（可配置是否需要 admin 确认）
- 自动扣分：仅对明确规则命中（如逾期、违约、取消上限、dispute 失败）执行

自动催收：

- 到期前：Telegram 提醒
- 逾期：强提醒 + 风险升级（`flagged/blocked`）

AI 推荐（放款侧）：

- 推荐高收益订单
- 推荐低风险借款人

约束：

- OpenClaw 不可触碰资金；所有动作必须可审计（写入 `risk_logs` 或运营日志）。

## 10. Telegram Bot（最小功能）

- 打开 Mini App
- 交易提醒
- 还款提醒
- 风控警告
- dispute 通知

## 11. 上线验收标准（必须全部满足）

- 完整借贷流程跑通（创建挂单→匹配→放款凭证→收款确认→还款→完成）
- PostgreSQL 替换成功（核心数据落库正确，读写正常）
- 风控规则生效（取消上限、超时取消、逾期/违约、标记风险、dispute 处置）
- Mini App 可操作（5 个核心页面可用，关键动作可完成）
- Telegram 登录正常（首次打开自动注册/鉴权稳定）
- 还款提醒正常（到期前 24h）
- 逾期自动标记（期级别 overdue 与交易级别 defaulted）
- dispute 流程可用（发起、证据、仲裁、结果落库、信用处置）

## 12. 关键口径与数据定义（避免扯皮）

- “违约率”= `defaulted` 的交易数 /（周期内到期的交易数）
- “逾期”= 任一还款期 `status=overdue`
- “新用户”= `total_borrowed=0` 或 `created_at` 距今小于配置阈值（实现时选其一并写入配置）
- “放款超时”= 当前时间 > `lend_deadline` 且仍未进入 `lend_confirmed`

## 13. 风险与待决策（上线前必须定稿）

- dispute 的 `status` 枚举与仲裁 SLA（例如 24h 内必须处理）
- 新用户大额审核的处理方式（拦截挂单、允许挂单但不允许匹配、或允许匹配但需 admin 放行）
- flagged/blocked 的具体限制清单（仅下单/接单，还是包括查看市场/上传凭证）
- 凭证存储方式（URL/对象存储）与保留策略
