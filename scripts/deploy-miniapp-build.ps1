$ErrorActionPreference = "Stop"

$root = (Resolve-Path (Join-Path $PSScriptRoot ".."))
Set-Location $root

Set-Location (Join-Path $root "frontend/miniapp")

if (Get-Command pnpm -ErrorAction SilentlyContinue) {
  pnpm install --frozen-lockfile
  pnpm build
} else {
  npm ci
  npm run build
}

Write-Host "OK: built frontend/miniapp/dist"

