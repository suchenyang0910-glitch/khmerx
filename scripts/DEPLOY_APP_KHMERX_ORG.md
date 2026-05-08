# 部署 app.khmerx.org（Mini App 静态站点）

当前多语言未生效的常见原因：线上仍在服务旧的前端构建产物（`index.html` 仍引用旧 hash 的 `/assets/index-*.js`）。

## 1) 快速判断线上是否已更新

在浏览器打开 `https://app.khmerx.org/`，找到 `index.html` 里引用的 JS：
- `/assets/index-XXXX.js`

再检查 JS 是否包含关键字（任意一种方法都行）：
- DevTools → Sources 搜索 `khx_lang`
- DevTools → Console：
  - `fetch('/assets/index-XXXX.js').then(r=>r.text()).then(t=>t.includes('khx_lang'))`

如果返回 `false`，说明线上仍是旧包（没有多语言逻辑）。

## 2) 构建 Mini App

在服务器或 CI 环境执行（推荐）：

```bash
bash scripts/deploy-miniapp-build.sh
```

或 Windows PowerShell：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/deploy-miniapp-build.ps1
```

构建产物目录：`frontend/miniapp/dist`

## 3) 发布 dist 到 app.khmerx.org

按你当前的静态托管方式把 `frontend/miniapp/dist/` 发布出去：

- Nginx/静态目录：将 `dist/` 同步到站点根目录
- Cloudflare Pages：Build output directory 指向 `dist`（或 `frontend/miniapp/dist`）并触发 redeploy

## 4) 上线后验证

- 打开 `https://app.khmerx.org/`
- Console 执行 `localStorage.getItem('khx_lang')`，首次应为 `km`
- Network 任意 API 请求 Headers 应包含 `X-Lang: km`

