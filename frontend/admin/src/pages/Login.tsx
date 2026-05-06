import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { adminLogin } from "@/api/admin"
import { useAdminAuthStore } from "@/stores/adminAuthStore"
import { Button } from "@/components/ui/Button"
import { Card } from "@/components/ui/Card"

export default function Login() {
  const nav = useNavigate()
  const setAuth = useAdminAuthStore((s) => s.setAuth)
  const [username, setUsername] = useState("admin")
  const [password, setPassword] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  return (
    <div className="min-h-screen bg-zinc-950 px-5 py-10 text-zinc-100">
      <div className="mx-auto max-w-md">
        <div className="mb-6">
          <div className="text-2xl font-semibold">KhmerX Admin</div>
          <div className="mt-1 text-sm text-zinc-400">使用管理员账号登录</div>
        </div>
        <Card>
          <form
            className="space-y-4"
            onSubmit={async (e) => {
              e.preventDefault()
              setError(null)
              setLoading(true)
              try {
                const res = await adminLogin({ username, password })
                setAuth({ token: res.token, username: res.username })
                nav("/", { replace: true })
              } catch (err) {
                setError("登录失败：用户名或密码不正确，或服务未配置")
              } finally {
                setLoading(false)
              }
            }}
          >
            <div>
              <div className="text-sm text-zinc-300">用户名</div>
              <input
                className="mt-2 w-full rounded-xl border border-zinc-800 bg-zinc-950 px-3 py-2 text-sm outline-none focus:border-blue-600"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                autoComplete="username"
              />
            </div>
            <div>
              <div className="text-sm text-zinc-300">密码</div>
              <input
                className="mt-2 w-full rounded-xl border border-zinc-800 bg-zinc-950 px-3 py-2 text-sm outline-none focus:border-blue-600"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                autoComplete="current-password"
              />
            </div>
            {error ? <div className="rounded-xl border border-red-900 bg-red-950 px-3 py-2 text-sm text-red-200">{error}</div> : null}
            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? "登录中..." : "登录"}
            </Button>
          </form>
        </Card>
        <div className="mt-4 text-xs text-zinc-500">API Base: {import.meta.env.VITE_ADMIN_API_BASE_URL || "https://api.khmerx.org/api/admin"}</div>
      </div>
    </div>
  )
}

