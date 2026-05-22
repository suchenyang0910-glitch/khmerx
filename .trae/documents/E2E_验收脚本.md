# KhmerX 端到端验收脚本（本地）

## 目标
- 验证 Mini App：薪资贷入口、申请、订单详情与还款凭证上传
- 验证 运营后台（薪资贷）：工厂管理、在职验证、审核、放款、还款凭证核销

## 前置条件
- 安装 Python 以及依赖（项目现有测试可运行）
- 已安装 pnpm

## 1. 启动后端

在项目根目录执行（PowerShell）：

```powershell
$env:DATABASE_URL = "sqlite+pysqlite:///./khmerx_e2e.db"
$env:ADMIN_USERNAME = "admin"
$env:ADMIN_PASSWORD = "pass"
$env:ADMIN_JWT_SECRET = "secret"
python -m app.main
```

默认监听 `http://localhost:3030`。

## 2. 启动运营后台（薪资贷）

```powershell
pnpm -C frontend/risk-admin install
$env:VITE_CORE_BASE_URL = "http://localhost:3030"
pnpm -C frontend/risk-admin dev
```

浏览器打开输出的地址，访问 `/#/ops-login`，使用 `ADMIN_USERNAME/ADMIN_PASSWORD` 登录。

验收点：
- 左侧仅显示：`薪资贷审核`
- `工厂库`可新增工厂
- `订单审核`可打开订单抽屉，完成：在职验证 → 审核通过（填写 fee/interest）→ 放款（填写流水号）
- 在抽屉里可对还款凭证执行：通过 / 驳回

## 3. 启动 Mini App（薪资贷）

```powershell
pnpm -C frontend/miniapp install
pnpm -C frontend/miniapp dev
```

验收流程：
- 进入 `Services`，点击 `Salary advance / 工资预支`
- 填写就业信息与借款金额，提交后进入订单详情页
- 订单放款后，在订单详情页上传还款凭证
- 回到运营后台抽屉里审核凭证通过，订单状态进入 `repaying/completed`

## 4. 自动化测试与类型检查

```powershell
python -m pytest -q
pnpm -C frontend/risk-admin run check
pnpm -C frontend/risk-admin run lint
pnpm -C frontend/miniapp run check
pnpm -C frontend/miniapp run e2e
pnpm -C frontend/website run check
```
