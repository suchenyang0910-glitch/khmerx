# KhmerX 全产品需求文档（PRD）V1

域名
- 官网：`https://khmerx.org`
- Mini App：`https://app.khmerx.org`
- API：`https://api.khmerx.org`
- 后台：`https://admin.khmerx.org`

产品定位
- KhmerX 是「金融 + 本地信任 + 现代科技」的 Telegram Mini App 闭环系统：借款人发布借款单、出借人接单打款、双方凭证确认、按期还款、异常争议仲裁、风控可视化与运营后台。

官网定位（关键）
- 官网不是“贷款平台官网”，而是：
  - KhmerX：柬埔寨本地 ABA 小额周转信息服务平台
  - 强调：可信、简单、本地化
  - 目标：SEO/GEO 可被 Google 与 AI 搜索理解，并引导用户打开 Telegram Mini App

关键原则（不可违背）
- 一个用户只绑定一个 `global_user_id`（以 `tg_id` 识别用户，跨 Bot/入口不丢账户）
- Mini App 鉴权不绑死单一 Bot Token（支持主 Bot/备用 Bot 切换）
- 所有 Bot 共用同一套用户数据库
- 不向陌生人主动私聊；不批量拉人进群
- 所有通知必须用户主动触发或订阅
- 每个 Bot 有清晰业务用途（主用/备用/管理员）

---

## 1. 目标与范围

### 1.1 业务目标
- 上线后可跑通「借款→出借→打款→确认→还款→完成」闭环
- 降低纠纷：强制展示到账金额/费用说明，交易状态与下一步提示明确
- 提升转化：首次引导+资料完善门槛+倒计时压迫感+推荐金额

### 1.2 成功指标（MVP）
- 关键漏斗：打开 Mini App → 完成资料 → 创建借款单 → 被接单 → 借款确认收款 → 完成还款
- 纠纷率：`dispute / trades` 低于阈值（由运营定义）
- 超时率：`matched` 后 24h 未打款的比例持续下降

### 1.3 范围
包含
- 官网：多语言（km/en/zh）落地页体系、借款流程/费用/风险解释、FAQ、联系入口、合规声明、t.me Mini App 入口
- Mini App：首页/借款/出借/交易/我的 + 首次引导 + 资料完善 + 争议入口 + 还款提醒
- API：TMA 鉴权、用户资料、借款试算、挂单、撮合、交易流程、凭证上传、争议、通知（MVP 可空）
- 后台：运营看板/交易管理/风控事件/人工审核/仲裁管理/利率矩阵（分阶段）
- Bot：主入口 + 备用入口（可选管理员 Bot）

不包含（MVP）
- 平台实际“碰钱/托管资金”（平台只记录信息与凭证，不做资金托管）
- 批量触达/群发/主动私聊

---

## 2. 用户角色

### 2.1 角色定义
- 借款人（Borrower）：发布借款单、确认收款、上传还款凭证
- 出借人（Lender）：接单、上传打款凭证、确认收到还款
- 业务员（Agent，可选）：邀请用户、查看名下数据与佣金
- 管理员（Admin）：后台处理风控/审核/仲裁/配置

### 2.2 身份与账号
- 账号唯一识别：`tg_id`
- 平台用户唯一：`global_user_id`（产品语义），MVP 可用用户主键代替
- 多入口/多 Bot：只要 `tg_id` 不变，用户账户不变

---

## 3. Mini App 信息架构

### 3.1 底部 Tab
- 首页 / 借款 / 出借 / 交易 / 我的

### 3.2 首次进入门槛
- 首次引导（3屏）：
  1) 什么是 KhmerX
  2) 如何借钱/出借
  3) 安全与合规说明（平台不兜底、只提供信息与撮合）
- 资料完善（强制）：手机号 + ABA 账号 + ABA 姓名
  - 未完成资料：禁止借款/出借关键动作

---

## 4. 核心闭环（用户路径）

### 4.1 借款路径
进入 → 自动登录 → 完成资料 → 试算 → 发布借款单 → 等待匹配 → 对方打款 → 确认收款 → 还款 → 完成

### 4.2 出借路径
进入 → 自动登录 → 完成资料 → 浏览市场 → 查看详情 → 风险确认 → 接单 → 打款并上传凭证 → 等对方确认 → 等还款 → 确认收款 → 完成

### 4.3 异常路径
- 24h 未打款：订单超时 → 自动取消/提示 → 允许重新发单
- 凭证与收款争议：进入争议状态 → 补充证据 → 管理员仲裁 → 风控扣分/限制
- 逾期：标记 `overdue` → 提醒与信用影响展示 → 催收任务（后台/催收员）

---

## 5. 页面级需求（可直接给前端）

---

## 5.0 官网（khmerx.org）需求（SEO/GEO 版本）

### 5.0.1 官网目标
- 建立信任
- 承接 Google 搜索流量
- 引导用户打开 Telegram Mini App
- 解释借款流程、费用、风险（减少纠纷）
- 支持高棉语/英语/中文

### 5.0.2 多语言 URL 结构
- 默认主站：`/km`
- 英文：`/en`
- 中文：`/zh`

示例
- `https://khmerx.org/km`
- `https://khmerx.org/en`
- `https://khmerx.org/zh`

### 5.0.3 官网页面规划（V1）
- 首页：`/{locale}`
- 借款说明：`/{locale}/borrow`
- 出借说明：`/{locale}/lend`
- 费用说明：`/{locale}/fees`
- 安全与风控：`/{locale}/safety`
- 常见问题：`/{locale}/faq`
- 关于我们：`/{locale}/about`
- 联系我们：`/{locale}/contact`
- 博客（V2）：`/{locale}/blog`

### 5.0.4 首页结构（必须包含）
- 首屏 Hero
  - 标题：KhmerX / ABA 小额周转，更简单
  - 副标题：通过 Telegram Mini App 发布小额借款需求，使用 ABA 转账完成交易
  - CTA：打开 Mini App（t.me 深链）/ 了解如何借款
- 核心卖点：ABA 转账、小额短期、Telegram 操作、信用记录、透明费用
- 借款流程（5 步）
- 费用透明示例（必须）：借款 $100 → 费用 $10 → 到账 $90 → 到期还 $100
- 信用与额度：新用户小额度、按时还款提升、逾期影响
- 安全说明：平台不保管资金、ABA 转账、凭证记录、争议处理
- FAQ
- 合规声明（Footer 必须）

### 5.0.5 合规文案（Footer 必须）
- KhmerX 是本地用户之间的小额周转信息服务与信用记录工具。
- 平台不承诺放款成功，不承诺收益，不吸收存款，不提供担保。
- 所有交易请用户自行确认风险。

### 5.0.6 SEO 关键词规划（V1）
高棉语（示例）
- ខ្ចីលុយតាម ABA
- ខ្ចីប្រាក់ខ្នាតតូច
- ខ្ចីលុយភ្នំពេញ
- ប្រាក់កម្ចីខ្លី

英文（示例）
- ABA micro loan Cambodia
- small loan Cambodia
- short term loan Phnom Penh
- borrow money via ABA
- Telegram loan Cambodia

中文（示例）
- 柬埔寨小额借款
- 金边小额周转
- ABA借款
- 柬埔寨Telegram借款
- 柬埔寨短期借款

### 5.0.7 GEO / AI 搜索可理解性（每页必须回答）
- KhmerX 是什么？
- 服务谁？
- 在什么地区？
- 解决什么问题？
- 怎么使用？
- 是否支持 ABA？
- 是否支持 Telegram？

首页建议结构化介绍（需出现在可抓取正文中）
- EN：KhmerX is a Cambodia-focused micro lending information platform that helps local users publish small short-term borrowing requests and complete transactions through ABA transfer and Telegram Mini App.
- CN：KhmerX 是面向柬埔寨本地用户的小额周转信息服务平台，用户可以通过 Telegram Mini App 发布借款需求，并使用 ABA 转账完成交易。

### 5.1 首页 Dashboard
目标：让用户立刻知道“我能借多少 / 我有没有待还 / 我下一步做什么”。

控件
- 顶部：Logo、语言切换（cn/km）、通知入口
- 信用额度卡：信用分/等级/可借额度/风险状态 +「查看信用详情」
- 主操作按钮：「我要借钱」「我要出借」
- 当前任务卡（动态）：
  - 无交易：提示 +「创建第一笔借款」
  - 待打款：倒计时 +「查看交易」
  - 待还款：到期提示 +「立即还款」

状态
- loading / error / ready
- 当前任务：none / need_lend / need_repay / dispute

点击后的动作
- 借钱：跳转 Borrow
- 出借：跳转 Lend
- 查看信用详情：跳转 Credit
- 通知：跳转 Notifications

异常提示
- 登录失效：提示从 Telegram 重新打开
- 风控限制：显示原因与恢复方式

### 5.2 借款 Borrow
目标：10 秒创建借款单，0 纠纷。

控件
- 额度卡：可借额度/信用等级
- 金额输入：步进器 + 输入框 + 滑块（50→max）
- 期限选择：7/14/30（新用户默认只显示 7）
- 费用计算卡（强制）：借款金额 / 平台费或利息 / 实际到账 / 到期应还
- 风险提示卡：按时还款提升额度、逾期影响信用
- 提交按钮：「确认发布借款」

状态
- profile_incomplete（提示先绑定）
- calculating
- submit_ready
- submitting

点击后的动作
- 发布借款：二次确认（展示四件套）→ `POST /offers` → 成功进入交易页

异常提示
- 超额：自动回到最大额度并提示
- 未绑定 ABA：提示 `ABA_REQUIRED`
- 风控拒绝：提示 `RISK_REJECTED` 并展示原因

### 5.3 出借 Lend
目标：放款人 3 秒看懂风险和收益，10 秒决定。

控件
- 顶部筛选：稳健/推荐/高收益
- LoanCard：金额、预计收益、期限、信用等级、完成单、逾期次数、风险标签
- 操作：「查看详情」「立即出借」

状态
- loading / empty / ready

点击后的动作
- 查看详情：进入 LendConfirm
- 立即出借：进入 LendConfirm 并聚焦风险确认

异常提示
- 已被接单：提示刷新列表

### 5.4 出借确认 LendConfirm
目标：防误操作，明确收益与风险。

控件
- 摘要：出借金额、预计收益、到期收回
- 借款人风险信息：信用等级、风险等级、历史逾期/完成单
- 勾选框：我已确认风险
- 按钮：确认出借

点击后的动作
- 勾选后二次确认 → `POST /offers/{id}/match`（confirm_risk=true）→ 成功跳转 TradeDetail

异常提示
- 需要人工审核：`MANUAL_REVIEW_REQUIRED`
- 风控拒绝：`RISK_REJECTED`

### 5.5 交易列表 Trades
目标：快速找到“现在需要我做的那一笔”。

控件
- 过滤：active/completed/overdue/dispute + role=borrower/lender
- 条目：金额/状态/下一步/倒计时

点击后的动作
- 进入 TradeDetail

### 5.6 交易详情 TradeDetail（核心）
目标：用户永远知道“我在哪一步 / 下一步做什么 / 还有多久”。

控件
- 状态进度条：匹配→打款→确认→还款→完成
- 当前状态卡：当前状态文案 + 下一步提示 + 倒计时
- ABA 信息：账号+姓名
- 操作区（动态按钮）：上传打款凭证/确认收款/上传还款凭证/确认收到还款
- 还款计划：期数/到期/金额/状态（未还/已还/逾期）
- 争议入口：发起争议/补充证据/查看进度

倒计时规则
- matched：24h 打款倒计时

异常提示
- 状态不允许：`INVALID_STATUS`
- 争议锁定：`DISPUTE_LOCKED`

### 5.7 我的 Profile
目标：资料维护 + 信用成长路径 + 风控解释。

模块
- 头像/昵称
- 信用概览：信用分/等级/额度
- 风控解释：为什么额度变化/如何提升
- 资料：手机号、ABA 账号、ABA 姓名
- 语言切换、退出登录
- 业务员入口（role=agent）

---

## 6. 通知策略（符合原则）
- 通知仅来自：用户操作触发（发布/接单/确认/上传）或用户显式订阅
- MVP：Mini App 内消息列表为主（后端接口可先返回空，后续补齐）

---

## 7. Bot 策略（容灾）
- Bot A：主入口（正常使用）
- Bot B：备用入口（A 异常时切换）
- Bot C：管理员/通知（可选）

切换规则
- 后端维护 active bot 列表；前端入口更新为备用 Bot
- 用户重新从 Bot B 打开 Mini App 后，仍通过 `tg_id` 找回原账户

---

## 8. 合规与风控（用户可见）
- 风控限制必须解释原因（不可只提示“不可操作”）
- 争议与仲裁流程透明（状态：open/reviewing/resolved）
- 平台声明：不兜底、不托管资金，仅记录凭证与风控信息

---

## 9. 资金与责任边界（必须写死）

### 9.1 平台责任声明（必须在官网 Footer + Mini App 关键页出现）
- KhmerX 是本地用户之间的小额周转信息服务与信用记录工具。
- 平台不承诺放款成功，不承诺收益，不吸收存款，不提供担保。
- 所有转账通过 ABA 完成，平台不直接保管用户资金。
- 用户须自行确认风险；平台仅提供撮合信息、凭证记录与争议处理流程。

### 9.2 强制勾选/二次确认规则
必须二次确认（弹窗确认 + 关键金额/风险摘要同屏）：
- 发布借款
- 确认出借（必须勾选“我已确认风险”）
- 借款人确认收款
- 借款人提交还款
- 放款人确认收到还款
- 发起争议

---

## 10. 状态机与超时策略（上线事故高发点）

### 10.1 Offer 状态
- `pending`：可被接单
- `matched`：已匹配，不可重复接单
- `cancelled`：借款人取消
- `expired`：超时未匹配（可选）
- `reviewing`：人工审核中（可选）
- `rejected`：审核拒绝（可选）

### 10.2 Trade 状态（核心）
- `matched` → `lend_confirmed` → `repayment_confirmed` → `repaying` → `completed`
- 异常：`overdue` / `defaulted` / `dispute` / `cancelled`

### 10.3 状态-动作-权限（最小可上线口径）
| trade.status | 当前状态文案 | 下一步提示 | Borrower 可操作 | Lender 可操作 | 系统动作 |
|---|---|---|---|---|---|
| matched | 等待放款人打款 | 24h 内完成 ABA 转账并上传凭证 | 查看倒计时/发起争议（可选） | 上传打款凭证 | 24h 超时：自动取消或标记超时 |
| lend_confirmed | 放款人已上传凭证 | 借款人确认是否收到款 | 确认收到 / 发起争议 | 等待 | 可设置确认超时提醒 |
| repayment_confirmed | 已确认收款 | 请按期还款 | 上传还款凭证 | 查看还款计划 | 进入还款中展示 |
| repaying | 还款中 | 请按期还款，逾期影响信用 | 上传还款凭证 | 确认收到还款 | 到期未还：标记 overdue |
| overdue | 已逾期 | 立即还款避免进一步扣分 | 立即还款 / 发起争议 | 查看/发起催收（后台） | 逾期累计：可升级 defaulted |
| dispute | 争议处理中 | 等待平台处理，可补充证据 | 补充证据 | 补充证据 | 锁定交易关键操作 |
| completed | 已完成 | 可查看记录 | 查看明细 | 查看明细 | 结算佣金/更新信用 |

### 10.4 超时策略（MVP 必须）
- 放款超时：`matched` 后 `24h` 未上传打款凭证 → 自动取消交易并回退/关闭 offer（口径需一致）
- 到期提醒：还款到期前 `24h` / `48h` 在 App 内提示（符合“用户触发或订阅”原则，可由用户在 App 勾选订阅）
- 逾期升级：逾期超过 `OVERDUE_DAYS_LIMIT`（默认 7 天）可升级 `defaulted`

---

## 11. 争议与仲裁 SOP（纠纷核心）

### 11.1 可发起争议类型（dispute_type）
- `lend_not_received`：借款人称未收到款
- `repay_not_received`：放款人称未收到还款
- `wrong_amount`：金额不一致
- `fake_proof`：疑似伪造凭证
- `other`：其他

### 11.2 证据要求（最小）
- 截图/照片（ABA 转账记录）
- 金额与时间
- 备注说明

### 11.3 仲裁时限与状态
- `open`：已提交
- `reviewing`：平台审核中
- `resolved`：已裁决
- `rejected`：不受理（资料不足/恶意）

### 11.4 裁决结果（resolution_result）
- `borrower_win` / `lender_win` / `both_fault` / `cancel_trade` / `manual_continue`

### 11.5 裁决后的联动
- 更新信用分/风险等级（扣分原因必须可见）
- 必要时：限制额度、限制交易、封禁

---

## 12. 风控可视化标准（避免投诉）

### 12.1 用户端必须展示
- 当前 `risk_level` / `credit_score` / `credit_level` / `max_borrow_amount`
- “为什么我被限制/额度变化”的原因列表（reasons）
- “如何恢复/如何提升额度”的行动列表（actions）

### 12.2 原因字段规范（最小）
原因必须满足：可翻译（cn/km/en）、可排序（优先级）、可追溯（对应 risk_log/event）。
示例 reasons：
- 新用户首单额度限制
- 有 1 次逾期记录，额度已收紧
- 资料未完善（缺手机号/ABA）
- 关系风险较高，需要人工审核

---

## 13. 资料完善与修改规则（交易会崩点）

### 13.1 必填字段
- `phone`、`aba_account`、`aba_name`

### 13.2 修改规则
- 修改 ABA 信息：建议加入“二次验证/人工确认”策略（MVP 可先限制为不可修改或仅在无进行中交易时可修改）
- 进行中交易的 ABA 信息：必须锁定以交易创建时的收款信息为准（避免中途改资料造成纠纷）

---

## 14. 费用/利息模型口径（必须统一）

MVP 采用“透明示例 + 同口径字段返回”。
必须对齐 4 个金额字段：
- `amount`：借款金额
- `interest`（或服务费/利息）：平台规则计算出的费用
- `received_amount`：实际到账（用于解决砍头息纠纷）
- `repay_amount`：到期应还

官网与 Mini App 必须提供同一示例：借款 $100 → 费用 $10 → 到账 $90 → 到期还 $100（示例按你当前模型）

---

## 15. 通知策略（必须符合原则）

原则
- 只允许用户触发或订阅，不主动私聊陌生人
- 优先 App 内通知列表（Notifications）

通知类型（建议）
- offer_created / offer_matched
- lend_proof_uploaded / receive_confirm_required
- repayment_due_24h / repayment_overdue
- dispute_created / dispute_updated / dispute_resolved

订阅点（最小）
- 用户在“我的-通知设置”中开启：还款提醒、争议更新

---

## 16. 数据埋点与运营看板（上线后可迭代）

关键事件（MVP）
- `app_open`
- `onboarding_completed`
- `profile_completed`
- `offer_created`
- `offer_matched`
- `lend_proof_uploaded`
- `receive_confirmed`
- `repay_proof_uploaded`
- `repay_confirmed`
- `dispute_created`

必须能形成漏斗
打开 Mini App → 完成资料 → 创建借款 → 被接单 → 确认收款 → 完成还款

---

## 17. 上线验收用例（E2E 必跑）

测试账号
- 账号 A：借款人
- 账号 B：出借人

验收步骤（必须逐条对照）
1) A 登录并完成资料（phone + ABA）
2) A 借款试算：金额/期限变化自动更新四件套
3) A 发布 7 天 $100 借款单（二次确认弹窗）
4) B 在市场列表看到该单，进入确认页勾选风险并接单
5) B 上传打款凭证（状态从 matched → lend_confirmed）
6) A 确认收款（状态 lend_confirmed → repayment_confirmed）
7) A 上传还款凭证（schedule 状态 paid_pending）
8) B 确认收到还款（schedule paid，若全部已还 trade → completed）
9) 检查信用变化、风控日志、交易列表归档、通知列表记录

超时验收
- matched 24h 未打款：系统应自动取消/回退并给出明确提示

---

## 18. 下一阶段需求（V1.1 / V2 Roadmap）

目标：在不改变“信息服务平台、不碰钱、不主动私聊”的前提下，提升安全性、可控性与运营效率。

### 18.1 必做（V1.1，上线后 1–2 周）
- 手机号真实性校验（OTP）
  - 触发：绑定/修改手机号
  - 约束：未通过 OTP 不允许借款/出借关键动作
- 自动超时与状态推进
  - `matched` 超时自动取消
  - 还款计划到期自动标记 `overdue`
  - `overdue` 超过阈值可升级 `defaulted`
- 通知订阅与频控
  - 用户主动开启：还款提醒、争议更新
  - 频控：每用户每类型每天最多 N 条
- 争议仲裁的后台工作流
  - 受理/驳回
  - 证据补齐提醒
  - 裁决结果落库 + 风控联动
- 管理员审计日志
  - 记录：谁在何时对谁做了什么（调分/封禁/裁决/改配置）

### 18.2 可选（V1.2，盈利与规模化）
- 平台资金池控制
  - 每日放款上限、单人敞口、单业务员敞口
  - 资金池状态 healthy/cautious/freeze
- 自动撮合推荐（lender feed）
  - 稳健/推荐/高收益三类 feed
  - 排序：收益分 + 信用分 + 成交概率 - 风险分
- 业务员系统完善
  - 邀请码绑定、佣金释放条件（完成还款后释放）、冻结规则（坏账惩罚）

### 18.3 官网 SEO 扩展（V2）
- 博客/知识库（按语言生成）
- 城市/场景 Landing Pages（Phnom Penh/Siem Reap 等）
- 每页结构化问答（FAQPage），增强 GEO 可理解性
