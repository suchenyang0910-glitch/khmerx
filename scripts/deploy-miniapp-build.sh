#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

cd frontend/miniapp
if command -v pnpm >/dev/null 2>&1; then
  pnpm install --frozen-lockfile
  pnpm build
else
  npm ci
  npm run build
fi

echo "OK: built frontend/miniapp/dist"

