import { useEffect, useMemo, useState } from "react"
import { useNavigate } from "react-router-dom"
import Card from "@/components/ui/Card"
import Button from "@/components/ui/Button"
import Input from "@/components/ui/Input"
import Badge from "@/components/ui/Badge"
import { apiV1 } from "@/api/client"
import { useAuthStore } from "@/stores/authStore"
import { scoreToLevel } from "@/utils/credit"
import { errorMessage } from "@/utils/errors"

type CalcResultV1 = {
  amount: number
  term_days: number
  rate_percent: number
  interest: number
  received_amount: number
  repay_amount: number
  mode: string
}

function clamp(n: number, min: number, max: number) {
  return Math.max(min, Math.min(max, n))
}

export default function Borrow() {
  const nav = useNavigate()
  const user = useAuthStore((s) => s.user)
  const risk = useAuthStore((s) => s.risk)

  const creditLevel = useMemo(() => scoreToLevel(user?.credit_score || 650), [user?.credit_score])
  const maxBorrow = useMemo(() => {
    const base = risk?.max_borrow_amount ?? (creditLevel === "A" ? 500 : creditLevel === "B" ? 300 : creditLevel === "C" ? 200 : 100)
    const isNew = (user?.total_borrowed || 0) <= 0
    return isNew ? Math.min(base, 100) : base
  }, [creditLevel, risk?.max_borrow_amount, user?.total_borrowed])

  const suggested = useMemo(() => {
    const s = Math.floor((maxBorrow * 0.8) / 10) * 10
    return clamp(s || 50, 10, Math.floor(maxBorrow))
  }, [maxBorrow])

  const [amount, setAmount] = useState<number>(suggested)
  const [term, setTerm] = useState<7 | 14 | 30>(7)
  const [calc, setCalc] = useState<CalcResultV1 | null>(null)
  const [loadingCalc, setLoadingCalc] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  const [err, setErr] = useState<string | null>(null)
  const isNewUser = (user?.total_borrowed || 0) <= 0

  useEffect(() => {
    setAmount(suggested)
  }, [suggested])

  useEffect(() => {
    let cancelled = false
    const run = async () => {
      if (!user) return
      setLoadingCalc(true)
      setErr(null)
      try {
        const res = await apiV1.post<{ ok: boolean; data: CalcResultV1 }>("/p2p/calculate", {
          amount,
          term_days: term,
        })
        if (!cancelled) setCalc(res.data.data)
      } catch (e: unknown) {
        if (!cancelled) setErr(errorMessage(e, "试算失败"))
      } finally {
        if (!cancelled) setLoadingCalc(false)
      }
    }
    run()
    return () => {
      cancelled = true
    }
  }, [amount, creditLevel, term, user])

  const receive = calc?.received_amount ?? 0
  const repay = calc?.repay_amount ?? 0
  const interest = calc?.interest ?? 0

  const canSubmit = Boolean(user) && !submitting && amount > 0 && amount <= maxBorrow && Boolean(calc)
  const limited = amount > maxBorrow

  return (
    <div className="space-y-4">
      <Card className="p-4">
        <div className="flex items-center justify-between">
          <div>
            <div className="text-xs text-zinc-500">可借额度</div>
            <div className="mt-1 text-2xl font-bold text-zinc-900">${Math.round(maxBorrow)}</div>
          </div>
          <div className="text-right">
            <div className="text-xs text-zinc-500">信用等级</div>
            <div className="mt-1 text-2xl font-bold text-zinc-900">{creditLevel}</div>
          </div>
        </div>
        <div className="mt-3 flex flex-wrap gap-2">
          {isNewUser ? <Badge tone="blue">新用户首单建议 ≤ $100</Badge> : <Badge tone="green">按时还款可提升额度</Badge>}
          <Badge tone="zinc">推荐借款：${suggested}</Badge>
        </div>
      </Card>

      <Card className="p-4">
        <div className="flex items-center justify-between">
          <div className="text-sm font-semibold text-zinc-900">金额</div>
          {limited ? <Badge tone="red">超过额度</Badge> : <Badge tone="zinc">$ {amount}</Badge>}
        </div>

        <div className="mt-3">
          <input
            type="range"
            min={10}
            max={Math.max(10, Math.floor(maxBorrow))}
            step={10}
            value={clamp(amount, 10, Math.floor(maxBorrow))}
            onChange={(e) => setAmount(Number(e.target.value))}
            className="w-full"
          />
        </div>

        <div className="mt-3">
          <Input
            type="number"
            value={amount}
            onChange={(e) => setAmount(Number(e.target.value || 0))}
            placeholder="输入金额"
            min={0}
          />
        </div>

        <div className="mt-3 flex gap-2">
          {[7, 14, 30].map((d) => (
            <Button
              key={d}
              variant={term === d ? "primary" : "secondary"}
              className="flex-1"
              onClick={() => setTerm(d as 7 | 14 | 30)}
            >
              {d}天
            </Button>
          ))}
        </div>
      </Card>

      <Card className="p-4">
        <div className="text-sm font-semibold text-zinc-900">关键说明（避免纠纷）</div>
        <div className="mt-2 grid grid-cols-3 gap-2">
          <div className="rounded-2xl bg-blue-50 p-3">
            <div className="text-xs text-zinc-600">到账金额</div>
            <div className="mt-1 text-base font-semibold text-zinc-900">${receive.toFixed(2)}</div>
          </div>
          <div className="rounded-2xl bg-zinc-50 p-3">
            <div className="text-xs text-zinc-600">利息</div>
            <div className="mt-1 text-base font-semibold text-zinc-900">${interest.toFixed(2)}</div>
          </div>
          <div className="rounded-2xl bg-amber-50 p-3">
            <div className="text-xs text-zinc-600">到期需还</div>
            <div className="mt-1 text-base font-semibold text-zinc-900">${repay.toFixed(2)}</div>
          </div>
        </div>

        <div className="mt-3 rounded-2xl bg-white p-3 text-sm text-zinc-700 border border-zinc-100">
          你借 <span className="font-semibold">${amount.toFixed(0)}</span>，实际到账 <span className="font-semibold">${receive.toFixed(2)}</span>，到期需还 <span className="font-semibold">${repay.toFixed(2)}</span>。
        </div>

        <div className="mt-3 text-xs text-zinc-500">
          提示：按时还款可提升信用与额度；逾期会降低信用并影响后续借款。
        </div>
      </Card>

      {err ? (
        <div className="rounded-2xl bg-red-50 p-3 text-sm text-red-700">{err}</div>
      ) : null}

      <Button
        className="w-full"
        disabled={!canSubmit || loadingCalc || limited}
        onClick={async () => {
          if (!user) return
          setSubmitting(true)
          setErr(null)
          try {
            await apiV1.post("/offers", { amount, term_days: term, note: "" })
            nav("/trades")
          } catch (e: unknown) {
            setErr(errorMessage(e, "创建失败"))
          } finally {
            setSubmitting(false)
          }
        }}
      >
        {submitting ? "提交中…" : "立即借款（发布挂单）"}
      </Button>
    </div>
  )
}
