import { useEffect, useMemo, useState } from "react"
import { fetchConfig, upsertConfig } from "@/api/admin"
import type { AdminConfigItem } from "@/api/types"
import { Card } from "@/components/ui/Card"
import { Button } from "@/components/ui/Button"

const presets = [
  {
    key: "home_slots",
    label: "首页配置（公告/活动位）",
    defaultValue: { banners: [], shortcuts: [] },
  },
  {
    key: "limits",
    label: "限额与期限",
    defaultValue: { min_amount: 10, max_amount: 500, term_days: [7, 14, 30], max_active_trades_default: 1 },
  },
  {
    key: "fees",
    label: "费率配置",
    defaultValue: { platform_fee_percent: 0, aba_fee_tip: "" },
  },
  {
    key: "support",
    label: "客服与帮助链接",
    defaultValue: { telegram_support: "https://t.me/KhmerXBot", faq_url: "https://khmerx.org/zh/faq" },
  },
]

export default function Config() {
  const [rows, setRows] = useState<AdminConfigItem[]>([])
  const [selectedKey, setSelectedKey] = useState(presets[0].key)
  const [text, setText] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [ok, setOk] = useState<string | null>(null)

  const current = useMemo(() => {
    const preset = presets.find((p) => p.key === selectedKey) || presets[0]
    const existing = rows.find((r) => r.key === selectedKey)
    return { preset, existing }
  }, [rows, selectedKey])

  async function reload() {
    setLoading(true)
    setError(null)
    try {
      const data = await fetchConfig()
      setRows(data)
    } catch {
      setError("加载失败")
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    reload()
  }, [])

  useEffect(() => {
    const { existing, preset } = current
    const v = existing?.value ?? preset.defaultValue
    setText(JSON.stringify(v, null, 2))
    setOk(null)
    setError(null)
  }, [current])

  return (
    <div>
      <div className="mb-5">
        <div className="text-xl font-semibold">运营配置</div>
        <div className="mt-1 text-sm text-zinc-400">以 Key-Value 方式配置运营参数</div>
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <Card>
          <div className="text-sm font-semibold">配置项</div>
          <div className="mt-3 space-y-2">
            {presets.map((p) => (
              <button
                key={p.key}
                className={`w-full rounded-xl border px-3 py-2 text-left text-sm transition ${selectedKey === p.key ? "border-blue-700 bg-blue-950/40" : "border-zinc-800 hover:bg-zinc-900/40"}`}
                onClick={() => setSelectedKey(p.key)}
              >
                <div className="font-medium text-zinc-100">{p.label}</div>
                <div className="mt-1 font-mono text-xs text-zinc-500">{p.key}</div>
              </button>
            ))}
          </div>
          <div className="mt-4 flex items-center gap-2">
            <Button variant="secondary" onClick={reload} disabled={loading}>
              {loading ? "刷新中..." : "刷新"}
            </Button>
          </div>
        </Card>

        <Card>
          <div className="flex items-start justify-between gap-3">
            <div>
              <div className="text-sm font-semibold">编辑</div>
              <div className="mt-1 text-xs text-zinc-500">key: {selectedKey}</div>
            </div>
            <Button
              onClick={async () => {
                setError(null)
                setOk(null)
                try {
                  const parsed = JSON.parse(text) as Record<string, unknown>
                  await upsertConfig({ key: selectedKey, value: parsed })
                  await reload()
                  setOk("已保存")
                } catch {
                  setError("保存失败（检查 JSON 格式）")
                }
              }}
            >
              保存
            </Button>
          </div>
          <textarea
            className="mt-4 min-h-[360px] w-full rounded-xl border border-zinc-800 bg-zinc-950 px-3 py-2 font-mono text-xs outline-none focus:border-blue-600"
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
          {error ? <div className="mt-3 rounded-xl border border-red-900 bg-red-950 px-3 py-2 text-sm text-red-200">{error}</div> : null}
          {ok ? <div className="mt-3 rounded-xl border border-green-900 bg-green-950 px-3 py-2 text-sm text-green-200">{ok}</div> : null}
        </Card>
      </div>
    </div>
  )
}

