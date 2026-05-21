# KhmerX Credit OS 页面设计（Desktop-first）

## 全局设计规范（适用于所有页面）
### Layout
- 桌面优先：1200px 内容最大宽度（数据表格/工作台可放宽到 1440px），左右留白自适应。
- 栅格：12 栏 CSS Grid + 局部 Flexbox；列表页以“左侧筛选/右侧表格”为主。
- 断点：
  - ≥1280：完整三栏能力（侧边栏 + 内容 + 详情抽屉/侧栏）
  - 1024–1279：侧边栏可折叠；详情使用抽屉
  - <1024：仅保证可用（不作为主要设计目标）

### Meta Information（默认）
- title：KhmerX Credit OS
- description：统一用户、风控、账本、订单、设备的运营管理平台。
- OG：og:title=KhmerX Credit OS；og:type=website

### Global Styles（Design Tokens）
- Colors
  - Background: #0B1220（深色工作台底）
  - Surface/Card: #111A2E
  - Primary: #2F6BFF
  - Success: #16A34A
  - Warning: #F59E0B
  - Danger: #EF4444
  - Text Primary: #E5E7EB
  - Text Muted: #94A3B8
  - Border: rgba(148,163,184,0.2)
- Typography
  - H1 20/28 semibold；H2 16/24 semibold；Body 14/20；Caption 12/16
  - 数字/金额采用等宽字体（tabular-nums）
- Buttons
  - Primary：实心主色；hover 加亮 6%
  - Secondary：描边；hover 背景加深
  - Danger：红色；高风险动作必须二次确认
- Links
  - 默认主色；hover 下划线；在表格中使用“弱链接”样式避免抢占注意力
- Motion
  - 抽屉/弹窗 180ms ease-out；列表筛选 120ms

### 通用组件库（跨页复用）
- AppShell：顶部栏（租户/组织、账号、快捷搜索）+ 左侧导航（模块入口）+ 内容区
- DataTable：列配置、排序、分页、列显隐、导出按钮（若有权限）
- FilterBar：关键词、状态、多选枚举、时间范围
- DetailDrawer：右侧抽屉显示详情与操作记录
- AuditTimeline：按时间倒序展示关键动作（含操作者、时间、字段差异）

---

## 1) 登录/访问控制页
### Layout
- 居中单卡片布局（Flexbox），背景使用品牌渐变/暗色纹理。

### Meta
- title：登录 - KhmerX Credit OS
- description：登录并进入 Credit OS 管理平台。

### Page Structure
- Header（简化）：Logo + 系统名
- Login Card：表单区 + 错误提示区 + 帮助信息

### Sections & Components
1. 登录表单
   - 输入：账号（邮箱/用户名/手机号，按你现有后端实现）+ 密码
   - 操作：登录按钮（loading 状态）；回车提交
   - 安全：连续失败提示；不暴露具体账号是否存在
2. 会话与权限提示
   - 登录成功后若需要选择租户/组织：弹出选择器（Modal）后进入 /app

---

## 2) 平台工作台（首页）
### Layout
- AppShell + 内容区上下分段：上方 KPI Cards，下方“待办 + 最近查询/活动”。

### Meta
- title：工作台 - KhmerX Credit OS
- description：关键指标概览与跨域待办处理入口。

### Page Structure
- 左侧导航：工作台、用户、风控、订单、账本、设备、系统
- 顶部栏：全局搜索、租户/组织切换（如适用）、账号菜单

### Sections & Components
1. KPI 概览区（Cards Grid）
   - 指标卡：订单量、风险命中、待复核、入账异常（具体口径由你们统一定义）
   - 点击进入对应列表页并预置筛选条件
2. 待办列表（DataTable 精简版）
   - 类型：复核待办、异常订单、对账差异
   - 行为：点击行打开 DetailDrawer
3. 最近活动/审计摘要
   - 展示最近 20 条关键动作摘要；点击跳转到系统审计

---

## 3) 用户与主体中心
### Layout
- 上方 FilterBar + 下方 DataTable；详情使用右侧 DetailDrawer。

### Meta
- title：用户中心 - KhmerX Credit OS
- description：统一用户档案、关系链路与风险标签。

### Page Structure
- 列表区：用户列表
- 详情抽屉：用户详情 Tab（基础信息/关联订单/关联设备/风险标签/审计）

### Sections & Components
1. 用户列表
   - 筛选：关键词（姓名/手机号/证件号）、状态、风险标签、时间范围
   - 列：用户ID、姓名、手机号、状态、风险标签、最近订单时间
2. 用户详情抽屉
   - 基础信息：结构化字段展示
   - 关联订单：嵌入子表格，跳转订单中心
   - 关联设备：嵌入子表格，跳转设备中心
   - 风险标签：只读展示（如需修改需受权限控制）
   - 审计：AuditTimeline

---

## 4) 风控中心
### Layout
- 二级 Tab：策略与规则 / 决策记录 / 复核队列。

### Meta
- title：风控中心 - KhmerX Credit OS
- description：策略规则配置、决策链路沉淀与人工复核。

### Page Structure
- Tab 1：策略与规则（左列表 + 右编辑/详情）
- Tab 2：决策记录（表格 + 详情抽屉）
- Tab 3：复核队列（表格 + 复核面板）

### Sections & Components
1. 策略与规则
   - 列表：策略名称、版本、状态、更新时间
   - 详情：规则集展示（可折叠），变更原因输入，启停按钮
2. 决策记录
   - 表格列：决策ID、订单ID、策略版本、结果、命中数、时间
   - 详情抽屉：输入特征摘要、命中规则列表、输出结果、链路审计
3. 复核队列
   - 行为：通过/拒绝/要求补充信息（若你们流程允许）
   - 每次操作必须写入“结论 + 理由”，并产出审计记录

---

## 5) 订单中心
### Layout
- FilterBar + DataTable；订单详情用抽屉，抽屉内包含风控与账本联动信息。

### Meta
- title：订单中心 - KhmerX Credit OS
- description：统一订单视图与全链路追溯（风控/账本/设备）。

### Page Structure
- 订单列表
- 订单详情抽屉（概览/风控/账本/设备/审计 Tabs）

### Sections & Components
1. 订单列表
   - 筛选：模块标识（moduleA-D）、状态、时间范围、用户关键词
   - 列：订单ID、模块、用户、金额、状态、风控结果、创建时间
2. 订单详情抽屉
   - 概览：关键字段与状态流转时间线
   - 风控：关联决策记录与命中摘要
   - 账本：关联分录列表（只读为主，敏感操作需权限）
   - 设备：关联设备与绑定历史
   - 审计：AuditTimeline
3. 异常处理
   - 异常标记/备注
   - 冲正/更正入口（如果账本已闭环；高风险动作二次确认）

---

## 6) 账本中心
### Layout
- 左侧二级导航：账户 / 分录 / 对账；右侧内容区。

### Meta
- title：账本中心 - KhmerX Credit OS
- description：账户与分录管理、对账与导出。

### Page Structure
- 账户列表：余额概览
- 分录列表：强检索与可导出
- 对账面板：差异列表 + 处理记录

### Sections & Components
1. 账户
   - 列：账户名/类型、余额、更新时间
   - 点击进入账户详情（抽屉）查看最近分录
2. 分录
   - 筛选：订单ID、用户ID、类型、时间范围、金额区间
   - 导出：仅对有权限角色显示，导出结果写入对象存储并可下载
3. 对账
   - 展示对账批次、差异条目、处理状态
   - 处理动作：标记已确认/待追踪，并记录处理意见

---

## 7) 设备中心
### Layout
- FilterBar + DataTable；设备详情抽屉（档案/绑定/事件/审计）。

### Meta
- title：设备中心 - KhmerX Credit OS
- description：设备档案、绑定关系与设备事件处置。

### Page Structure
- 设备列表
- 设备详情抽屉

### Sections & Components
1. 设备列表
   - 筛选：IMEI/序列号、状态、是否绑定、时间范围
   - 列：设备ID、IMEI、状态、当前绑定用户/订单、更新时间
2. 设备详情抽屉
   - 档案：基础字段
   - 绑定：绑定历史表格（bound_at/unbound_at）
   - 事件：设备相关风险事件列表与处置记录
   - 审计：AuditTimeline

---

## 8) 系统设置与迁移中心
### Layout
- 左侧二级导航：组织与权限 / 参数与字典 / 审计 / 迁移任务。

### Meta
- title：系统与迁移 - KhmerX Credit OS
- description：RBAC、参数字典、审计与迁移批次编排。

### Page Structure
- RBAC 管理：组织/角色/权限矩阵
- 参数字典：枚举与口径配置
- 审计：全域审计检索与导出
- 迁移任务：批次列表 + 批次详情（步骤、进度、对账报告）

### Sections & Components
1. 组织与权限（RBAC）
   - 组织列表、角色列表
   - 权限矩阵：按模块/页面/动作粒度勾选（至少支持读/写/导出/审批类动作）
2. 参数与字典
   - 枚举项管理：状态值、原因码、策略结果码等
   - 变更需审计记录
3. 审计中心
   - FilterBar：操作者、对象类型（用户/订单/设备/规则/分录）、时间范围、关键词
   - DataTable：事件列表；详情抽屉展示字段差异
4. 迁移任务
   - 创建迁移批次：选择模块（A-D）、范围（时间/ID段）、映射模板、校验规则
   - 执行与重试：展示每步成功/失败、失败原因、重试按钮
   - 对账报告：迁移前后关键口径差异（订单数/金额/分录数/风控结果分布等）