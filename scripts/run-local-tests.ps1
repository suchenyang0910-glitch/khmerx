$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

$Artifacts = Join-Path $Root "artifacts"
New-Item -ItemType Directory -Force -Path $Artifacts | Out-Null

if (-not $env:DATABASE_URL) {
  $stamp = Get-Date -Format "yyyyMMdd_HHmmss"
  $env:DATABASE_URL = "sqlite:///./artifacts/khmerx_local_${stamp}.db"
}
if (-not $env:SCHEDULER_ENABLED) { $env:SCHEDULER_ENABLED = "false" }
if (-not $env:BOT_TOKENS) { $env:BOT_TOKENS = "test-bot-token" }
if (-not $env:OTP_DEV_MODE) { $env:OTP_DEV_MODE = "true" }
if (-not $env:OTP_SECRET) { $env:OTP_SECRET = "dev-otp-secret" }

if (-not $env:ADMIN_USERNAME) { $env:ADMIN_USERNAME = "admin" }
if (-not $env:ADMIN_PASSWORD) { $env:ADMIN_PASSWORD = "pass" }
if (-not $env:ADMIN_JWT_SECRET) { $env:ADMIN_JWT_SECRET = "dev-secret" }

if (-not $env:KHX_BASE_URL) { $env:KHX_BASE_URL = "http://127.0.0.1:3030" }
if (-not $env:KHX_ROOT) { $env:KHX_ROOT = "http://127.0.0.1:3030" }
if (-not $env:KHX_V1_BASE) { $env:KHX_V1_BASE = "http://127.0.0.1:3030/api/v1" }
if (-not $env:KHX_TEST_BOT_TOKEN) { $env:KHX_TEST_BOT_TOKEN = "test-bot-token" }

Write-Host "Starting backend..."
$server = Start-Process -FilePath python -ArgumentList "-m","uvicorn","app.main:app","--host","127.0.0.1","--port","3030","--log-level","warning" -PassThru

try {
  Start-Sleep -Seconds 2
  Write-Host "Running Mini App TMA flow test..."
  python scripts/local_tma_flow_test.py
  if ($LASTEXITCODE -ne 0) { throw "local_tma_flow_test failed" }

  Write-Host "Running V1.1 automation test..."
  python scripts/local_v11_automation_test.py
  if ($LASTEXITCODE -ne 0) { throw "local_v11_automation_test failed" }

  Write-Host "Running Admin E2E test..."
  powershell -ExecutionPolicy Bypass -File scripts/e2e-admin.ps1
  if ($LASTEXITCODE -ne 0) { throw "e2e-admin failed" }

  Write-Host "ALL LOCAL TESTS OK"
}
finally {
  if ($server -and -not $server.HasExited) {
    Write-Host "Stopping backend..."
    Stop-Process -Id $server.Id -Force
  }
}
