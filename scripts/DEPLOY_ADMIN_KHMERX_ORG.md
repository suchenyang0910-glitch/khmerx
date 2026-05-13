# 部署 admin.khmerx.org（风控管理后台）

管理后台前端会请求同域的两条反代路径：

- `https://admin.khmerx.org/api-auth/*` → `auth-service`（默认 `127.0.0.1:8081`）
- `https://admin.khmerx.org/api-risk/*` → `risk-engine-service`（默认 `127.0.0.1:8082`）

## 1) 服务器侧 Nginx 反代（推荐）

将站点 `server {}` 中加入以下两段 location，并确保静态站点可回退到 `index.html`：

```nginx
location / {
  try_files $uri $uri/ /index.html;
}

location /api-auth/ {
  rewrite ^/api-auth/?(.*)$ /$1 break;
  proxy_pass http://127.0.0.1:8081;
}

location /api-risk/ {
  rewrite ^/api-risk/?(.*)$ /$1 break;
  proxy_pass http://127.0.0.1:8082;
}
```

## 2) Docker 部署（可选）

前端目录已提供 `Dockerfile` 与 `nginx.conf`：

```bash
cd frontend/risk-admin
docker build -t khmerx-risk-admin:latest .
docker run -d --name khmerx-risk-admin -p 8080:8080 khmerx-risk-admin:latest
```

默认反代目标为宿主机 `127.0.0.1:8081/8082`，确保两服务在同机运行且端口可达。

## 3) 线上排错

打开浏览器 DevTools → Network：

- 检查 `POST /api-auth/auth/token` 的状态码
  - `404`：反代未配置或路径未匹配
  - `502/504`：上游 `auth-service` 不通
  - `401`：数据库里没有该 `merchant_id/api_key` 或账号被禁用

如果是 `401`，先在数据库确认：

```sql
select merchant_id, status from merchant_center.merchants where merchant_id='m_demo';
```

