# 本地测试（推荐）

目标：用一套脚本在本地跑通 API/Mini App/Admin 的核心闭环。

## 一键运行

在仓库根目录执行：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run-local-tests.ps1
```

该脚本会自动：
- 启动后端（本地 SQLite、关闭 scheduler、OTP 开发模式）
- 跑 Mini App TMA 闭环脚本
- 跑 V1.1 自动化（超时取消/逾期推进/通知生成）脚本
- 跑后台 E2E 脚本（报表/配置/导出）

## 单独运行（可选）

1) 启动后端
```powershell
$env:DATABASE_URL='sqlite:///./khmerx_local.db'
$env:SCHEDULER_ENABLED='false'
$env:BOT_TOKENS='test-bot-token'
$env:OTP_DEV_MODE='true'
$env:OTP_SECRET='dev-otp-secret'
$env:ADMIN_USERNAME='admin'
$env:ADMIN_PASSWORD='pass'
$env:ADMIN_JWT_SECRET='dev-secret'
python -m uvicorn app.main:app --host 127.0.0.1 --port 3030 --log-level warning
```

2) Mini App 闭环（TMA）
```powershell
python scripts/local_tma_flow_test.py
```

3) 自动化（超时/逾期/通知）
```powershell
python scripts/local_v11_automation_test.py
```

4) 后台验收
```powershell
powershell -ExecutionPolicy Bypass -File scripts/e2e-admin.ps1
```

