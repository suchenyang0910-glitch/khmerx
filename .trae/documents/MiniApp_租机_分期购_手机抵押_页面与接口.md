# MiniApp：租机 / 分期购 / 手机抵押

## 目标
在 Telegram Mini App 内新增三类业务入口与闭环：
- 租机（lease）
- 分期购（installment）
- 手机抵押（pledge）

实现：入口 → 申请表单 → 我的申请列表 → 申请详情，并接入后端 FastAPI + Postgres 落库与查询。

## 页面结构（路由）
- `/services`：业务入口聚合页（三卡片）
- `/apply/:bizType`：提交申请表单（bizType ∈ lease/installment/pledge）
- `/applications`：我的申请（列表 + 业务类型筛选）
- `/applications/:applicationId`：申请详情

入口放置：
- 首页 `Home` 新增“更多服务”卡片（直达三类申请）
- 我的页 `Me` 新增“我的申请”入口（直达列表）

## 表单字段（MVP）
通用字段（全部业务）：
- `full_name`：姓名
- `phone`：手机号（只读，来自已绑定手机号）
- `city`：城市/区域
- `device_model`：手机型号
- `amount`：金额（字符串，后端可二次校验为数值）
- `notes`：备注

分期购（installment）额外：
- `down_payment`：首付
- `term_months`：分期月数（3/6/12/18/24）

租机（lease）额外：
- `term_months`：租期月数（3/6/12/18/24）

手机抵押（pledge）额外：
- `imei`：IMEI
- `condition`：机况（good/fair/poor）
- `locked`：是否锁机（yes/no）
- `term_days`：周期（7/14/30）

## 后端数据结构（Postgres）
表：`finance_applications`
- `id` uuid
- `user_id` uuid
- `biz_type` varchar(32)
- `status` varchar(32) 默认 `submitted`
- `payload` jsonb（存上述字段）
- `created_at`/`updated_at`

## 后端 API（/api/v1）
所有接口使用 TMA 鉴权（`Authorization: TMA <initData>`），并要求资料完整：手机号已验证 + 已绑定 ABA。

- `POST /api/v1/applications`
  - body: `{ biz_type: "lease"|"installment"|"pledge", payload: {...} }`
  - 返回：创建后的申请对象
- `GET /api/v1/applications`
  - query: `biz_type?` `status?` `limit?` `offset?`
  - 返回：当前用户申请列表（倒序）
- `GET /api/v1/applications/{applicationId}`
  - 返回：申请详情（仅本人可见）

## 风控与拦截（MVP）
- `ensure_profile_completed(user)`：未完善资料禁止提交申请
- `RiskService.get_or_create_profile(user.id).is_blocked`：被风控封禁则禁止提交

