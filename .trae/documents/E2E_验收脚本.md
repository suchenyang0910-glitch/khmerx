# KhmerX 端到端验收脚本（本地）

## 目标
- 验证运营后台：登录、报表总览与趋势、运营配置、CSV 导出

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

## 2. 启动运营后台

```powershell
pnpm -C frontend/admin install
pnpm -C frontend/admin dev
```

浏览器打开输出的地址，使用 `ADMIN_USERNAME/ADMIN_PASSWORD` 登录。

验收点：
- 左侧出现：`报表`、`配置`、`风控事件`、`争议`、`公告`
- `报表`页面能展示区间指标与 5 条趋势折线（sparklines）
- `CSV 导出`三个按钮可下载文件
- `配置`页面可保存 JSON，并刷新后仍能读取

## 3. 一键 E2E（脚本）

确保后端已启动后，执行：

```powershell
$env:KHX_BASE_URL = "http://localhost:3030"
$env:ADMIN_USERNAME = "admin"
$env:ADMIN_PASSWORD = "pass"
pwsh ./scripts/e2e-admin.ps1
```

产物：
- `./artifacts/users.csv`
- `./artifacts/orders.csv`
- `./artifacts/risk_events.csv`

## 4. 自动化测试与类型检查

```powershell
python -m pytest -q
pnpm -C frontend/admin run check
pnpm -C frontend/miniapp run check
pnpm -C frontend/website run check
```

