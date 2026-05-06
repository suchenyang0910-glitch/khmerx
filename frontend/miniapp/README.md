# KhmerX Mini App（Telegram Mini App）

## 本地启动（推荐流程）

### 1) 启动后端

确保后端 `.env` 至少包含：
- `BOT_TOKENS=...`（Telegram Bot token）
- `DEV_TMA_ENABLED=true`（本地生成 initData）

启动（示例用 3040）：
```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 3040
```

验证后端可用（浏览器打开应返回 JSON）：
- `http://127.0.0.1:3040/auth/dev-tma`

### 2) 启动 Mini App

```bash
pnpm dev -- --host 127.0.0.1 --port 5173
```

打开：
- `http://localhost:5173/`

## 本地登录与验证

### 本地调试登录

在本地浏览器环境没有 Telegram `initData` 时：
- App 会自动调用 `/auth/dev-tma` 生成测试账号并完成登录。

如果提示无法登录，可在错误页直接切换：
- `切到 3040` / `切到 3030`

### 正式手机号验证（方案 A）

在 Telegram 内打开 Mini App 时，可用“Telegram 联系人授权”完成手机号验证：
- ProfileSetup 页点击 `使用 Telegram 验证手机号`

## 可选：本地代理端口

默认代理后端为 `http://127.0.0.1:3040`。

如果你想改代理目标，可在运行 dev 前设置：
- `VITE_DEV_PROXY_TARGET=http://127.0.0.1:3030`

