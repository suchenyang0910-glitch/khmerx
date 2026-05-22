import { test, expect } from "@playwright/test"
import { bootstrapTmaSession, devInitData, ensureProfileCompleted } from "./helpers"


test.describe("Borrow page", () => {
  test("borrow submit button stays stable", async ({ page, request }) => {
    const initData = await devInitData(request)
    await ensureProfileCompleted(request, initData)
    await bootstrapTmaSession(page, initData)

    await page.goto("/borrow")
    await expect(page.getByTestId("page-borrow")).toBeVisible()

    const btn = page.getByTestId("borrow-submit")
    await expect(btn).toBeVisible()

    await expect.poll(async () => await btn.isDisabled(), { timeout: 10_000 }).toBe(false)
    await page.waitForTimeout(800)

    const states: boolean[] = []
    for (let i = 0; i < 15; i += 1) {
      states.push(await btn.isDisabled())
      await page.waitForTimeout(100)
    }

    expect(new Set(states).size).toBe(1)
    expect(states[0]).toBe(false)
  })
})

