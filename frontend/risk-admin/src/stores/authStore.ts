import { create } from 'zustand'

type AuthState = {
  token: string | null
  merchantId: string | null
  setSession: (token: string, merchantId: string) => void
  logout: () => void
}

const TOKEN_KEY = 'risk_admin_token'
const MERCHANT_KEY = 'risk_admin_merchant_id'

export const useAuthStore = create<AuthState>((set) => ({
  token: localStorage.getItem(TOKEN_KEY),
  merchantId: localStorage.getItem(MERCHANT_KEY),
  setSession: (token, merchantId) => {
    localStorage.setItem(TOKEN_KEY, token)
    localStorage.setItem(MERCHANT_KEY, merchantId)
    set({ token, merchantId })
  },
  logout: () => {
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(MERCHANT_KEY)
    set({ token: null, merchantId: null })
  },
}))

