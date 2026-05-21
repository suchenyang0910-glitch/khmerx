import { expect, type Page, type APIRequestContext } from "@playwright/test"

export const BACKEND_BASE = "http://127.0.0.1:3030"

export async function devInitData(request: APIRequestContext) {
  const tgId = 90000000 + Math.floor(Math.random() * 1000000)
  const res = await request.get(`${BACKEND_BASE}/auth/dev-tma`, { params: { tg_id: tgId } })
  expect(res.ok()).toBeTruthy()
  const body = await res.json()
  const initData = body?.data?.init_data
  expect(typeof initData).toBe("string")
  expect(initData.length).toBeGreaterThan(10)
  return initData as string
}

export async function ensureProfileCompleted(request: APIRequestContext, initData: string) {
  const loginRes = await request.post(`${BACKEND_BASE}/auth/telegram-login`, { data: { init_data: initData } })
  expect(loginRes.ok()).toBeTruthy()
  const u = await loginRes.json()
  const userId = u?.id
  expect(typeof userId).toBe("string")

  const auth = { Authorization: `TMA ${initData}` }
  const abaAccount = String(800000 + Math.floor(Math.random() * 100000))
  const abaName = "E2E"
  const p1 = await request.patch(`${BACKEND_BASE}/api/v1/me/profile`, {
    headers: auth,
    data: { aba_account: abaAccount, aba_name: abaName },
  })
  expect(p1.ok()).toBeTruthy()

  const phone = "0" + String(8000000 + Math.floor(Math.random() * 1000000))
  const otpReq = await request.post(`${BACKEND_BASE}/auth/otp/request`, {
    data: { user_id: userId, phone },
  })
  expect(otpReq.ok()).toBeTruthy()
  const otp = await otpReq.json()
  const code = otp?.dev_code
  const challengeId = otp?.challenge_id
  expect(typeof code).toBe("string")
  expect(typeof challengeId).toBe("string")

  const otpVerify = await request.post(`${BACKEND_BASE}/auth/otp/verify`, {
    data: { user_id: userId, phone, code, challenge_id: challengeId },
  })
  expect(otpVerify.ok()).toBeTruthy()

  return { userId: userId as string, phone, abaAccount, abaName }
}

export async function bootstrapTmaSession(page: Page, initData: string) {
  await page.addInitScript(
    ({ initData }) => {
      localStorage.setItem("khx_lang_selected_v2", "1")
      localStorage.setItem("khx_lang", "en")
      localStorage.setItem("khx_onboarding_done", "1")
      localStorage.setItem("khx_tma_init_data", initData)
      localStorage.removeItem("khx_dev_api_base")
    },
    { initData },
  )
}
