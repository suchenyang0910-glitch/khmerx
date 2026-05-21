# 全局设计规范

## 用户端（Telegram Mini App / TMA）统一规范
- 主题：完全跟随 Telegram `themeParams`（bg/text/hint/link/button/secondary_bg），并监听 themeChanged 动态刷新。
- 导航：一级页用底部 TabBar（自绘，≤5）；二级页统一启用 Telegram `BackButton` 返回。
- 主操作：表单提交/确认等关键动作优先使用 Telegram `MainButton`（随校验显示、禁用、更新文案）。
- 动效：以 120–200ms 轻量过渡为主（淡入/位移），低端机默认关闭复杂动效。
- 错误/离线：全局 ErrorBanner + OfflineBar；离线时禁用提交、允许草稿本地暂存与恢复。
- 权限：手机号/联系人按需弹出授权（失败提供手动录入兜底），并在 UI 明确用途与最小化采集。

## 后台端（Web / Desktop-first）补充
- 颜色 Token（后台默认浅色）：Primary #2563EB；Danger #DC2626；Warning #F59E0B；Success #16A34A
- 排版：标题 20/16；正文 14；辅助 12；数字等宽（用于金额/指标）。
- 状态：按钮 hover 亮度 +6%；disabled 40% 透明；表格行 hover 背景 #F1F5F9。

---

# Mini App（5 模块）页面设计

## 1）首页（模块1）
- Layout：纵向栈式布局（Flex column）；顶部吸顶导航 + 内容滚动。
- Meta：Title「KhmerX」；Description「在 Telegram 内完成核心操作」。
- Page Structure：
  1. 顶部栏：Logo/产品名 + 账号状态 pill（正常/受限/冻结）。
  2. 公告/活动 Banner：可左右滑动卡片；点击跳转。
  3. 快捷入口区：2~4 个主按钮（进入交易/订单/资产/客服）。
  4. 风控提示卡：当 riskLevel>=medium 显示；展示原因摘要 + 行动按钮。

## 2）交易/下单（模块2）
- Layout：移动端单栏为主（TMA）；顶部信息区 + 表单区；主提交动作使用 Telegram MainButton。
- Sections & Components：
  - 报价区：价格、更新时间、费率、限额；支持刷新（下拉刷新/按钮）。
  - 下单表单：金额/数量输入、即时校验提示；确认前弹出确认 Popup（含关键费用摘要）。
  - 风控拦截：ErrorBanner/Alert 展示原因摘要 + 可复制错误码；提供「联系客服」与「返回（BackButton）」。

## 3）订单（模块3）
- Layout：TMA 以“列表 → 详情”push 跳转为主；详情页启用 Telegram BackButton。
- Sections：
  - 筛选条：状态 tabs（横向滚动）+ 时间范围（轻量选择器）。
  - 订单列表：卡片/列表项，突出状态、金额与下一步动作。
  - 订单详情：状态时间线、关键字段（订单号一键复制）、失败原因/处理建议；必要时在底部用 MainButton 给出下一步。

## 4）资产（模块4）
- Layout：总览卡片 + 流水表。
- Sections：
  - 余额总览：总资产、可用/冻结；资产分组列表。
  - 流水：类型筛选（充值/提现/交易等）、时间筛选；空态引导。

## 5）我的（模块5）
- Layout：信息卡 + 操作列表。
- Sections：
  - 用户信息：Telegram 头像/昵称、用户ID、绑定/认证状态。
  - 操作项：帮助中心、联系客服、关于/协议、退出（如允许）。

---

# 运营后台页面设计（Desktop-first）

## A）后台登录
- Layout：居中卡片（max-width 420px）+ 背景插画/渐变。
- Components：账号/密码输入、登录按钮、错误提示（含锁定/验证码占位）。

## B）后台总览（仪表盘）
- Layout：CSS Grid 12 栅格；上方 KPI 卡片，下方趋势与列表。
- Sections：
  - KPI 卡：DAU、新增、下单量、成交金额、成功率、风险命中数。
  - 趋势图：按天/小时切换（折线/柱状）。
  - 异常摘要：待处理风险事件、异常订单、Top 失败原因。

## C）用户管理
- Layout：左侧筛选栏 + 右侧表格；点击行进入抽屉详情。
- Components：搜索（ID/TelegramID）、筛选（风险等级/时间）、用户详情抽屉（标签、订单摘要、处置记录）。

## D）订单管理
- Layout：表格为主；详情抽屉含状态时间线。
- Components：多条件筛选（状态/时间/金额区间）；失败原因字段高亮；备注与处置操作区。

## E）风控中心
- Layout：上方规则 tabs（规则/事件）；下方表格 + 右侧详情。
- Components：
  - 风险事件：严重级别颜色编码；处置按钮（标记已处理/备注/指派）。
  - 规则配置：规则表单（名称、启停、阈值/条件 JSON 展示、动作）；命中统计小图。

## F）配置与报表
- Layout：表单分组（公告/活动/限额费率）+ 导出任务列表。
- Components：配置项变更需二次确认；导出支持时间范围与进度状态。