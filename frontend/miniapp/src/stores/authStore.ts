import { create } from "zustand"
import axios from "axios"
import { api, apiV1 } from "@/api/client"
import type { AppUser, UserRiskProfile } from "@/api/types"
import { errorMessage } from "@/utils/errors"

type AuthState = {
  user: AppUser | null
  risk: UserRiskProfile | null
  booting: boolean
  error: string | null
  onboardingDone: boolean
  initData: string
  setOnboardingDone: (done: boolean) => void
  bootstrap: (initData: string) => Promise<void>
  refreshMe: () => Promise<void>
  requestPhoneOtp: (phone: string) => Promise<{ challenge_id: string; dev_code?: string }>
  verifyPhoneOtp: (phone: string, code: string) => Promise<void>
  updateAba: (aba_account: string, aba_name: string) => Promise<void>
}

function readOnboardingFlag() {
  return localStorage.getItem("khx_onboarding_done") === "1"
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  risk: null,
  booting: true,
  error: null,
  onboardingDone: readOnboardingFlag(),
  initData: localStorage.getItem("khx_tma_init_data") || "",
  setOnboardingDone: (done) => {
    localStorage.setItem("khx_onboarding_done", done ? "1" : "0")
    set({ onboardingDone: done })
  },
  bootstrap: async (initData: string) => {
    set({ booting: true, error: null })
    try {
      if (!initData) {
        set({ booting: false, error: "请从 Telegram 打开 KhmerX Mini App" })
        return
      }

      localStorage.setItem("khx_tma_init_data", initData)
      set({ initData })

      let user: AppUser
      try {
        const res = await api.post<AppUser>("/auth/telegram-login", { init_data: initData })
        user = res.data
      } catch (e: unknown) {
        const host = window.location.hostname
        if (host !== "localhost" && host !== "127.0.0.1") throw e

        const bases = [
          localStorage.getItem("khx_dev_api_base") || "",
          "http://127.0.0.1:3040",
          "http://127.0.0.1:3030",
        ].filter(Boolean)

        let lastErr: unknown = e
        for (const base of bases) {
          try {
            const r = await axios.post<AppUser>(`${base}/auth/telegram-login`, { init_data: initData }, { timeout: 20000 })
            localStorage.setItem("khx_dev_api_base", base)
            user = r.data
            lastErr = null
            break
          } catch (err) {
            lastErr = err
          }
        }
        if (lastErr) throw lastErr
      }

      set({ user })

      try {
        const riskRes = await api.get<UserRiskProfile>(`/risk/users/${user.id}`)
        set({ risk: riskRes.data })
      } catch (e: unknown) {
        const host = window.location.hostname
        if (host !== "localhost" && host !== "127.0.0.1") throw e
        const base = localStorage.getItem("khx_dev_api_base") || "http://127.0.0.1:3040"
        const riskRes = await axios.get<UserRiskProfile>(`${base}/risk/users/${user.id}`, { timeout: 20000 })
        set({ risk: riskRes.data })
      }

      set({ booting: false })
    } catch (e: unknown) {
      const msg = errorMessage(e, "登录失败")
      if (axios.isAxiosError(e) && !e.response) {
        const origin = window.location.origin
        const base = (api.defaults.baseURL || "").toString()
        set({
          booting: false,
          error: `Network Error：无法连接到 API。\nOrigin: ${origin}\nAPI: ${base}\n请检查：api 域名/证书是否可用、CORS 是否放行该 Origin、服务器是否可达。`,
        })
        return
      }
      set({ booting: false, error: msg })
    }
  },
  refreshMe: async () => {
    const user = get().user
    if (!user) return

    const me = await apiV1.get<{ ok: boolean; data: AppUser }>("/me")
    set({ user: me.data.data })

    const riskRes = await api.get<UserRiskProfile>(`/risk/users/${user.id}`)
    set({ risk: riskRes.data })
  },
  requestPhoneOtp: async (phone: string) => {
    const user = get().user
    if (!user) throw new Error("missing user")
    const res = await api.post<{ status: string; challenge_id: string; dev_code?: string }>(
      "/auth/otp/request",
      { user_id: user.id, phone },
    )
    return { challenge_id: res.data.challenge_id, dev_code: res.data.dev_code }
  },
  verifyPhoneOtp: async (phone: string, code: string) => {
    const user = get().user
    if (!user) throw new Error("missing user")
    await api.post(
      "/auth/otp/verify",
      { user_id: user.id, phone, code },
    )
    await get().refreshMe()
  },
  updateAba: async (aba_account: string, aba_name: string) => {
    const user = get().user
    if (!user) return
    await api.post(
      "/auth/aba/bind",
      { user_id: user.id, aba_account, aba_name },
    )
    await get().refreshMe()
  },
}))
