# KhmerX 运营结构 V1（Agent + Collector + Operator）

## 1. 角色定义（系统口径）

| 角色 | users.role | users.sub_role | 核心职责 |
|---|---|---|---|
| 借款方 | user | borrower | 需求端 |
| 出借方 | user | lender | 资金端 |
| 两栖用户 | user | both | 同时借/贷 |
| 平台方 | admin | - | 风控/仲裁/利率/封号/数据 |
| 业务员 | agent | - | 拉新/转化/维护/线下背书 |
| 催收员 | collector | - | 逾期处理/催收执行 |

数据字段：

- `users.agent_id`：用户绑定的业务员（首次绑定后不允许修改）
- `users.inviter_id`：邀请人（可与 agent 同值）
- `users.commission_rate`：业务员佣金比例（默认可用 2%）

## 2. 资金关系

- 交易资金来源：`p2p_trades.fund_source` = `user|platform|agent_pool`

## 3. 核心约束（防乱、防串单、防内外勾结）

强规则：

- 同一个 `agent_id` 下的用户禁止互借（撮合时直接拒绝）
- 同手机号/同 ABA 禁止互借

收益规则：

- 佣金延迟结算：先生成 `pending`，交易完成后才 `settled`
- 若借贷双方存在关系边（same_aba/same_phone/same_device/same_ip/repeated_trade/mutual_trade），不产生佣金

信用规则：

- 信用加分在“放款人确认收到还款”时触发
- 若借贷双方存在关系边或重复/互借边，不加信用分

## 4. 佣金系统（V1）

表：`agent_commissions`、`agent_stats`

- 生成时机：借款人确认收款后生成 `pending`（仅借款佣金 V1）
- 结算时机：交易完成（最后一期确认收款）后 `settled`

## 5. 催收系统（V1）

表：`collection_tasks`

- 逾期 3 天：自动生成催收任务（`pending`）
- 逾期 7 天：任务优先级 `high`

## 6. 接口（最小运营能力）

用户绑定业务员：

- `POST /auth/agent/bind`

业务员看板：

- `GET /ops/agent/dashboard?agent_id=`
- `GET /ops/agent/commissions?agent_id=&status=pending|settled`

催收任务：

- `GET /ops/collector/tasks?collector_id=&status=pending|assigned|in_progress|closed`
- `POST /ops/collector/tasks/{task_id}/assign?admin_id=&assigned_to=`
- `POST /ops/collector/tasks/{task_id}/close?collector_id=&note=`

## 7. 迁移文件

- `migrations/004_operator_agent_collector.sql`

