import { test, expect } from "@playwright/test"
import { bootstrapTmaSession, devInitData, ensureProfileCompleted } from "./helpers"

test.describe("KhmerX Mini App smoke", () => {
  test("tabs and core pages render", async ({ page, request }) => {
    const initData = await devInitData(request)
    await ensureProfileCompleted(request, initData)
    await bootstrapTmaSession(page, initData)

    await page.goto("/")
    await expect(page.getByTestId("tabbar")).toBeVisible()
    await expect(page.getByTestId("page-home")).toBeVisible()
    await expect(page.getByTestId("credit-card")).toBeVisible()
    await expect(page.getByTestId("home-grid")).toBeVisible()

    const credit = await page.getByTestId("credit-card").boundingBox()
    const grid = await page.getByTestId("home-grid").boundingBox()
    expect(credit && grid).toBeTruthy()
    if (credit && grid) expect(grid.y).toBeGreaterThan(credit.y)

    await page.getByTestId("tab-services").click()
    await expect(page.getByTestId("page-services")).toBeVisible()
    await expect(page.getByTestId("services-list")).toBeVisible()

    await page.getByTestId("tab-orders").click()
    await expect(page.getByTestId("page-orders")).toBeVisible()

    await page.getByTestId("tab-credit").click()
    await expect(page.getByTestId("page-credit")).toBeVisible()

    await page.getByTestId("tab-me").click()
    await expect(page.getByTestId("page-me")).toBeVisible()
  })

  test("visual snapshots", async ({ page, request }) => {
    const initData = await devInitData(request)
    await ensureProfileCompleted(request, initData)
    await bootstrapTmaSession(page, initData)

    await page.goto("/")
    await expect(page).toHaveScreenshot("home.png", { fullPage: true })

    await page.goto("/services")
    await expect(page).toHaveScreenshot("services.png", { fullPage: true })

    await page.goto("/orders")
    await expect(page).toHaveScreenshot("orders.png", { fullPage: true })

    await page.goto("/credit")
    await expect(page).toHaveScreenshot("credit.png", { fullPage: true })

    await page.goto("/me")
    await expect(page).toHaveScreenshot("me.png", { fullPage: true })
  })
})
