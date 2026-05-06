$ErrorActionPreference = "Stop"

$BaseUrl = $env:KHX_BASE_URL
if (-not $BaseUrl) { $BaseUrl = "http://localhost:3030" }

$Username = $env:ADMIN_USERNAME
if (-not $Username) { $Username = "admin" }

$Password = $env:ADMIN_PASSWORD
if (-not $Password) { $Password = "pass" }

Write-Host "BaseUrl: $BaseUrl"

$login = Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/admin/login" -ContentType "application/json" -Body (@{ username = $Username; password = $Password } | ConvertTo-Json)
$token = $login.token
if (-not $token) { throw "login failed" }

$headers = @{ Authorization = "Bearer $token" }

$overview = Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/admin/reports/overview" -Headers $headers
Write-Host "overview ok: users.total=$($overview.users.total)"

$trends = Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/admin/reports/trends" -Headers $headers
Write-Host "trends ok: users_new.points=$($trends.users_new.values.Count)"

$cfgBody = @{ key = "limits"; value = @{ min_amount = 10; max_amount = 500; term_days = @(7,14,30); max_active_trades_default = 1 } } | ConvertTo-Json -Depth 8
$cfg = Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/admin/config" -Headers $headers -ContentType "application/json" -Body $cfgBody
Write-Host "config upsert ok: key=$($cfg.key)"

$audit = Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/admin/audit-logs?limit=10&resource_type=app_config" -Headers $headers
if (-not $audit) { throw "audit logs missing" }
Write-Host "audit logs ok: count=$($audit.Count)"

$outDir = Join-Path (Get-Location) "artifacts"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

Invoke-WebRequest -Method Get -Uri "$BaseUrl/api/admin/exports/users.csv" -Headers $headers -OutFile (Join-Path $outDir "users.csv") | Out-Null
Invoke-WebRequest -Method Get -Uri "$BaseUrl/api/admin/exports/orders.csv" -Headers $headers -OutFile (Join-Path $outDir "orders.csv") | Out-Null
Invoke-WebRequest -Method Get -Uri "$BaseUrl/api/admin/exports/risk-events.csv" -Headers $headers -OutFile (Join-Path $outDir "risk_events.csv") | Out-Null

Write-Host "csv exported to $outDir"
Write-Host "E2E OK"
