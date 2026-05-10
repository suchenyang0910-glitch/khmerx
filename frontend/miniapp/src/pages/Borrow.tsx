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
import { useI18n } from "@/i18n"

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
  const { t } = useI18n()
  const user = useAuthStore((s) => s.user)
  const risk = useAuthStore((s) => s.risk)

  const MAX_BORROW_CAP = 800
  const NEW_USER_BORROW_CAP = 500

  const creditLevel = useMemo(() => scoreToLevel(user?.credit_score || 650), [user?.credit_score])
  const maxBorrow = useMemo(() => {
    const base = risk?.max_borrow_amount ?? MAX_BORROW_CAP
    const isNew = (user?.total_borrowed || 0) <= 0
    const capped = Math.min(base, MAX_BORROW_CAP)
    return isNew ? Math.min(capped, NEW_USER_BORROW_CAP) : capped
  }, [MAX_BORROW_CAP, NEW_USER_BORROW_CAP, risk?.max_borrow_amount, user?.total_borrowed])

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
        if (!cancelled) setErr(errorMessage(e, t("borrow.calcFailed")))
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
            <div className="text-xs text-zinc-500">{t("borrow.max")}</div>
            <div className="mt-1 text-2xl font-bold text-zinc-900">${Math.round(maxBorrow)}</div>
          </div>
          <div className="text-right">
            <div className="text-xs text-zinc-500">{t("borrow.creditLevel")}</div>
            <div className="mt-1 text-2xl font-bold text-zinc-900">{creditLevel}</div>
          </div>
        </div>
        <div className="mt-3 flex flex-wrap gap-2">
          {isNewUser ? <Badge tone="blue">{t("borrow.newUserFirst")}</Badge> : <Badge tone="green">{t("borrow.onTimeMore")}</Badge>}
          <Badge tone="zinc">{t("borrow.suggest")}: ${suggested}</Badge>
        </div>
      </Card>

      <Card className="p-4">
        <div className="text-sm text-zinc-700">
          {t("borrow.platformCap", { cap: MAX_BORROW_CAP })}
          {isNewUser ? ` ${t("borrow.newUserCap", { cap: NEW_USER_BORROW_CAP })}` : ""} {t("borrow.largeAmountContact")}{" "}
          <a className="text-blue-600" href="https://t.me/KhmerXBot" target="_blank" rel="noreferrer">
            {t("borrow.telegramBot")}
          </a>
        </div>
      </Card>

      <Card className="p-4">
        <div className="flex items-center justify-between">
          <div className="text-sm font-semibold text-zinc-900">{t("borrow.amount")}</div>
          {limited ? <Badge tone="red">{t("borrow.overLimit")}</Badge> : <Badge tone="zinc">$ {amount}</Badge>}
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
            placeholder={t("borrow.enterAmount")}
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
              {d}{t("borrow.days")}
            </Button>
          ))}
        </div>
      </Card>

      <Card className="p-4">
        <div className="text-sm font-semibold text-zinc-900">{t("borrow.keyInfo")}</div>
        <div className="mt-2 grid grid-cols-3 gap-2">
          <div className="rounded-2xl bg-blue-50 p-3">
            <div className="text-xs text-zinc-600">{t("borrow.receive")}</div>
            <div className="mt-1 text-base font-semibold text-zinc-900">${receive.toFixed(2)}</div>
          </div>
          <div className="rounded-2xl bg-zinc-50 p-3">
            <div className="text-xs text-zinc-600">{t("borrow.interest")}</div>
            <div className="mt-1 text-base font-semibold text-zinc-900">${interest.toFixed(2)}</div>
          </div>
          <div className="rounded-2xl bg-amber-50 p-3">
            <div className="text-xs text-zinc-600">{t("borrow.repayAtEnd")}</div>
            <div className="mt-1 text-base font-semibold text-zinc-900">${repay.toFixed(2)}</div>
          </div>
        </div>

        <div className="mt-3 rounded-2xl bg-white p-3 text-sm text-zinc-700 border border-zinc-100">
          {t("borrow.summary", {
            amount: amount.toFixed(0),
            receive: receive.toFixed(2),
            repay: repay.toFixed(2),
          })}
        </div>

        <div className="mt-3 text-xs text-zinc-500">
          {t("borrow.tip")}
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
            setErr(errorMessage(e, t("borrow.createFailed")))
          } finally {
            setSubmitting(false)
          }
        }}
      >
        {submitting ? t("borrow.submitting") : t("borrow.submit")}
      </Button>
    </div>
  )
}
