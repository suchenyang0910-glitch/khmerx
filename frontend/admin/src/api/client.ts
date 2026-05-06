import axios from "axios"
import { useAdminAuthStore } from "@/stores/adminAuthStore"

const baseURL = import.meta.env.VITE_ADMIN_API_BASE_URL || "https://api.khmerx.org/api/admin"

export const adminApi = axios.create({
  baseURL,
  timeout: 20000,
})

adminApi.interceptors.request.use((config) => {
  const token = useAdminAuthStore.getState().token
  if (token) {
    config.headers = {
      ...(config.headers as any),
      Authorization: `Bearer ${token}`,
    } as any
  }
  return config
})
