import { test, expect } from "@playwright/test"
import { devInitData } from "./helpers"


test.describe("New user first run", () => {
  test("first-run can finish onboarding then boot", async ({ page, request }) => {
    const initData = await devInitData(request)

    await page.addInitScript(
      ({ initData }) => {
        localStorage.clear()
        localStorage.setItem("khx_tma_init_data", initData)
        localStorage.setItem("khx_lang", "km")
        localStorage.setItem("khx_lang_selected_v2", "1")
        localStorage.setItem("khx_onboarding_done", "1")
      },
      { initData },
    )

    await page.goto("/")
    await expect(page.getByTestId("profile-required")).toBeVisible({ timeout: 15_000 })
    await page.getByTestId("profile-required-cta").click()
    await expect(page.getByTestId("page-setup")).toBeVisible({ timeout: 15_000 })
  })
})
