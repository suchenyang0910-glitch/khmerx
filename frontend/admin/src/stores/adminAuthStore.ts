import { create } from "zustand"

type AdminAuthState = {
  token: string | null
  username: string | null
  setAuth: (auth: { token: string; username: string }) => void
  logout: () => void
}

const storageKey = "khmerx_admin_auth"

function loadAuth(): Pick<AdminAuthState, "token" | "username"> {
  try {
    const raw = localStorage.getItem(storageKey)
    if (!raw) return { token: null, username: null }
    const parsed = JSON.parse(raw) as { token?: string; username?: string }
    return { token: parsed.token ?? null, username: parsed.username ?? null }
  } catch {
    return { token: null, username: null }
  }
}

function saveAuth(token: string | null, username: string | null) {
  if (!token || !username) {
    localStorage.removeItem(storageKey)
    return
  }
  localStorage.setItem(storageKey, JSON.stringify({ token, username }))
}

export const useAdminAuthStore = create<AdminAuthState>((set) => {
  const initial = loadAuth()
  return {
    token: initial.token,
    username: initial.username,
    setAuth: ({ token, username }) => {
      saveAuth(token, username)
      set({ token, username })
    },
    logout: () => {
      saveAuth(null, null)
      set({ token: null, username: null })
    },
  }
})

