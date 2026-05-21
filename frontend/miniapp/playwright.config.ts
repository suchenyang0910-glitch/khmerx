import { defineConfig } from "@playwright/test"
import path from "path"
import { fileURLToPath } from "url"

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)
const repoRoot = path.resolve(__dirname, "..", "..")

export default defineConfig({
  testDir: "./e2e",
  fullyParallel: true,
  retries: 0,
  timeout: 60_000,
  expect: {
    timeout: 10_000,
    toHaveScreenshot: {
      maxDiffPixelRatio: 0.01,
    },
  },
  use: {
    baseURL: "http://127.0.0.1:5173",
    viewport: { width: 390, height: 844 },
    locale: "en-US",
    timezoneId: "UTC",
    colorScheme: "light",
    screenshot: "only-on-failure",
    trace: "retain-on-failure",
    video: "retain-on-failure",
  },
  projects: [
    {
      name: "chromium",
      use: { browserName: "chromium" },
    },
  ],
  webServer: [
    {
      command: "python -m uvicorn app.main:app --host 127.0.0.1 --port 3030 --log-level warning",
      url: "http://127.0.0.1:3030/health",
      cwd: repoRoot,
      reuseExistingServer: true,
      env: {
        DATABASE_URL: "sqlite:///./khmerx_e2e.db",
        SCHEDULER_ENABLED: "false",
        BOT_TOKENS: "test-bot-token",
        DEV_TMA_ENABLED: "true",
        OTP_DEV_MODE: "true",
      },
    },
    {
      command: "pnpm -C frontend/miniapp dev -- --host 127.0.0.1 --port 5173",
      url: "http://127.0.0.1:5173/",
      cwd: repoRoot,
      reuseExistingServer: true,
      env: {
        VITE_DEV_PROXY_TARGET: "http://127.0.0.1:3030",
      },
    },
  ],
  outputDir: "test-results",
  reporter: [["list"], ["html", { open: "never" }]],
})
