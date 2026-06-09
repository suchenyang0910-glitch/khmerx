import { useEffect, useMemo, useState } from "react"
import { useNavigate } from "react-router-dom"
import Card from "@/components/ui/Card"
import Button from "@/components/ui/Button"
import Input from "@/components/ui/Input"
import Modal from "@/components/ui/Modal"
import { useI18n } from "@/i18n"
import { calculateSalaryLoanQuote, createSalaryEmployment, createSalaryLoanOrder, fetchSalaryFactories } from "@/api/v1"
import type { SalaryFactory, SalaryLoanQuote } from "@/api/types"
import { errorMessage } from "@/utils/errors"

type PayCycle = "monthly" | "biweekly" | "daily"
type PayMethod = "transfer" | "cash"

export default function SalaryLoanApply() {
  const { t } = useI18n()
  const navigate = useNavigate()

  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [err, setErr] = useState<string | null>(null)
  const [factories, setFactories] = useState<SalaryFactory[]>([])

  const [factoryId, setFactoryId] = useState("")
  const [employeeNo, setEmployeeNo] = useState("")
  const [joinDate, setJoinDate] = useState<string>("")
  const [salaryAmount, setSalaryAmount] = useState<string>("")
  const [salaryPayDay, setSalaryPayDay] = useState<string>("")
  const [payCycle, setPayCycle] = useState<PayCycle>("monthly")
  const [payMethod, setPayMethod] = useState<PayMethod>("transfer")
  const [principal, setPrincipal] = useState<string>("80")
  const [tenorDays, setTenorDays] = useState<string>("14")
  const [quote, setQuote] = useState<SalaryLoanQuote | null>(null)
  const [quoteLoading, setQuoteLoading] = useState(false)
  const [confirmOpen, setConfirmOpen] = useState(false)

  useEffect(() => {
    let cancelled = false
    setLoading(true)
    setErr(null)
    fetchSalaryFactories()
      .then((rows) => {
        if (cancelled) return
        setFactories(rows)
        if (rows.length > 0) setFactoryId(rows[0].id)
      })
      .catch((e: unknown) => {
        if (!cancelled) setErr(errorMessage(e, t("common.requestFailed")))
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [t])

  const factoryLabel = useMemo(() => {
    const f = factories.find((x) => x.id === factoryId)
    return f ? f.name : ""
  }, [factories, factoryId])

  useEffect(() => {
    let cancelled = false
    async function run() {
      const p = Number(principal)
      const term = Number(tenorDays)
      if (!factoryId || !Number.isFinite(p) || p < 30 || p > 5000 || ![7, 14, 30].includes(term)) {
        setQuote(null)
        return
      }
      setQuoteLoading(true)
      try {
        const data = await calculateSalaryLoanQuote({
          factory_id: factoryId,
          principal: p,
          tenor_days: term,
          join_date: joinDate || null,
          salary_amount: salaryAmount ? Number(salaryAmount) : null,
          salary_pay_day: salaryPayDay ? Number(salaryPayDay) : null,
          pay_cycle: payCycle,
          pay_method: payMethod,
        })
        if (!cancelled) setQuote(data)
      } catch {
        if (!cancelled) setQuote(null)
      } finally {
        if (!cancelled) setQuoteLoading(false)
      }
    }
    void run()
    return () => {
      cancelled = true
    }
  }, [factoryId, joinDate, payCycle, payMethod, principal, salaryAmount, salaryPayDay, tenorDays])

  async function submitConfirmed() {
    setSubmitting(true)
    setErr(null)
    try {
      const p = Number(principal)
      const term = Number(tenorDays)
      if (!Number.isFinite(p) || p <= 0) throw new Error(t("salary.apply.invalidAmount"))
      if (![7, 14, 30].includes(term)) throw new Error(t("salary.apply.invalidTerm"))
      if (!factoryId) throw new Error(t("salary.apply.factoryRequired"))

      const emp = await createSalaryEmployment({
        factory_id: factoryId,
        employee_no: employeeNo.trim(),
        join_date: joinDate ? joinDate : null,
        salary_amount: salaryAmount ? Number(salaryAmount) : null,
        salary_pay_day: salaryPayDay ? Number(salaryPayDay) : null,
        pay_cycle: payCycle,
        pay_method: payMethod,
      })
      const order = await createSalaryLoanOrder({ employment_id: emp.id, principal: p, tenor_days: term })
      navigate(`/salary-loan/order/${order.id}`)
    } catch (e: unknown) {
      setErr(errorMessage(e, t("common.requestFailed")))
    } finally {
      setSubmitting(false)
    }
  }

  async function onSubmit() {
    try {
      const p = Number(principal)
      const term = Number(tenorDays)
      if (!Number.isFinite(p) || p <= 0) throw new Error(t("salary.apply.invalidAmount"))
      if (![7, 14, 30].includes(term)) throw new Error(t("salary.apply.invalidTerm"))
      if (!factoryId) throw new Error(t("salary.apply.factoryRequired"))
      setConfirmOpen(true)
    } catch (e: unknown) {
      setErr(errorMessage(e, t("common.requestFailed")))
    }
  }

  return (
    <div data-testid="page-salary-apply" className="space-y-4">
      <div className="text-base font-semibold text-zinc-900">{t("salary.apply.title")}</div>

      {loading ? (
        <div className="space-y-3">
          <div className="h-40 animate-pulse rounded-2xl bg-white" />
          <div className="h-48 animate-pulse rounded-2xl bg-white" />
        </div>
      ) : (
        <>
          {err ? (
            <Card className="p-4">
              <div className="text-sm font-semibold text-zinc-900">{t("common.requestFailed")}</div>
              <div className="mt-2 text-sm text-zinc-600">{err}</div>
            </Card>
          ) : null}

          <Card className="p-4">
            <div className="text-sm font-semibold text-zinc-900">{t("salary.apply.section.employment")}</div>
            <div className="mt-3 space-y-3">
              <div>
                <div className="text-xs font-medium text-zinc-700">{t("salary.apply.factory")}</div>
                <select
                  value={factoryId}
                  onChange={(e) => setFactoryId(e.target.value)}
                  className="mt-1 h-12 w-full rounded-xl border border-zinc-200 bg-white px-3 text-sm outline-none focus:ring-2 focus:ring-blue-200"
                >
                  {factories.map((f) => (
                    <option key={f.id} value={f.id}>
                      {f.name}
                    </option>
                  ))}
                </select>
                {factoryLabel ? <div className="mt-1 text-xs text-zinc-500">{factoryLabel}</div> : null}
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <div className="text-xs font-medium text-zinc-700">{t("salary.apply.employeeNo")}</div>
                  <Input value={employeeNo} onChange={(e) => setEmployeeNo(e.target.value)} placeholder={t("salary.apply.employeeNoPh")} />
                </div>
                <div>
                  <div className="text-xs font-medium text-zinc-700">{t("salary.apply.joinDate")}</div>
                  <Input type="date" value={joinDate} onChange={(e) => setJoinDate(e.target.value)} />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <div className="text-xs font-medium text-zinc-700">{t("salary.apply.payCycle")}</div>
                  <select
                    value={payCycle}
                    onChange={(e) => setPayCycle(e.target.value as PayCycle)}
                    className="mt-1 h-12 w-full rounded-xl border border-zinc-200 bg-white px-3 text-sm outline-none focus:ring-2 focus:ring-blue-200"
                  >
                    <option value="monthly">{t("salary.apply.payCycle.monthly")}</option>
                    <option value="biweekly">{t("salary.apply.payCycle.biweekly")}</option>
                    <option value="daily">{t("salary.apply.payCycle.daily")}</option>
                  </select>
                </div>
                <div>
                  <div className="text-xs font-medium text-zinc-700">{t("salary.apply.payMethod")}</div>
                  <select
                    value={payMethod}
                    onChange={(e) => setPayMethod(e.target.value as PayMethod)}
                    className="mt-1 h-12 w-full rounded-xl border border-zinc-200 bg-white px-3 text-sm outline-none focus:ring-2 focus:ring-blue-200"
                  >
                    <option value="transfer">{t("salary.apply.payMethod.transfer")}</option>
                    <option value="cash">{t("salary.apply.payMethod.cash")}</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <div className="text-xs font-medium text-zinc-700">{t("salary.apply.salaryAmount")}</div>
                  <Input
                    inputMode="decimal"
                    value={salaryAmount}
                    onChange={(e) => setSalaryAmount(e.target.value)}
                    placeholder={t("salary.apply.salaryAmountPh")}
                  />
                </div>
                <div>
                  <div className="text-xs font-medium text-zinc-700">{t("salary.apply.payDay")}</div>
                  <Input inputMode="numeric" value={salaryPayDay} onChange={(e) => setSalaryPayDay(e.target.value)} placeholder="15" />
                </div>
              </div>
            </div>
          </Card>

          <Card className="p-4">
            <div className="text-sm font-semibold text-zinc-900">{t("salary.apply.section.loan")}</div>
            <div className="mt-3 space-y-3">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <div className="text-xs font-medium text-zinc-700">{t("salary.apply.principal")}</div>
                  <Input inputMode="decimal" value={principal} onChange={(e) => setPrincipal(e.target.value)} placeholder="80" />
                </div>
                <div>
                  <div className="text-xs font-medium text-zinc-700">{t("salary.apply.tenor")}</div>
                  <select
                    value={tenorDays}
                    onChange={(e) => setTenorDays(e.target.value)}
                    className="mt-1 h-12 w-full rounded-xl border border-zinc-200 bg-white px-3 text-sm outline-none focus:ring-2 focus:ring-blue-200"
                  >
                    <option value="7">7 {t("salary.apply.days")}</option>
                    <option value="14">14 {t("salary.apply.days")}</option>
                    <option value="30">30 {t("salary.apply.days")}</option>
                  </select>
                </div>
              </div>

              <div className="rounded-2xl border border-zinc-200 bg-zinc-50 p-3">
                <div className="text-sm font-semibold text-zinc-900">{t("salary.apply.previewTitle")}</div>
                {quoteLoading ? (
                  <div className="mt-2 text-sm text-zinc-500">{t("common.loading")}</div>
                ) : quote ? (
                  <>
                    <div className="mt-3 grid grid-cols-2 gap-3 text-sm">
                      <div className="rounded-xl bg-white p-3">
                        <div className="text-xs text-zinc-500">{t("salary.apply.previewFee")}</div>
                        <div className="mt-1 font-semibold text-zinc-900">${quote.fee.toFixed(2)}</div>
                      </div>
                      <div className="rounded-xl bg-white p-3">
                        <div className="text-xs text-zinc-500">{t("salary.apply.previewInterest")}</div>
                        <div className="mt-1 font-semibold text-zinc-900">${quote.interest.toFixed(2)}</div>
                      </div>
                      <div className="rounded-xl bg-white p-3">
                        <div className="text-xs text-zinc-500">{t("salary.apply.previewReceive")}</div>
                        <div className="mt-1 font-semibold text-zinc-900">${quote.disbursement_amount.toFixed(2)}</div>
                      </div>
                      <div className="rounded-xl bg-white p-3">
                        <div className="text-xs text-zinc-500">{t("salary.apply.previewTotalDue")}</div>
                        <div className="mt-1 font-semibold text-zinc-900">${quote.total_due.toFixed(2)}</div>
                      </div>
                    </div>
                    <div className="mt-2 text-xs text-zinc-500">
                      {t("salary.apply.previewSummary", {
                        score: quote.risk_score,
                        feeRate: `${(quote.fee_rate * 100).toFixed(1)}%`,
                        interestRate: `${(quote.interest_rate * 100).toFixed(1)}%`,
                      })}
                    </div>
                    <div className="mt-1 text-xs text-zinc-500">{quote.note}</div>
                  </>
                ) : (
                  <div className="mt-2 text-sm text-zinc-500">{t("salary.apply.previewEmpty")}</div>
                )}
              </div>

              <Button
                data-testid="salary-apply-submit"
                disabled={submitting || !factoryId || !quote}
                onClick={onSubmit}
                className="w-full"
              >
                {submitting ? t("common.loading") : t("salary.apply.submit")}
              </Button>
              <div className="text-xs text-zinc-500">{t("salary.apply.note")}</div>
            </div>
          </Card>
        </>
      )}

      <Modal open={confirmOpen} title={t("salary.apply.confirmTitle")} onClose={() => setConfirmOpen(false)}>
        <div className="space-y-3">
          <div className="rounded-2xl bg-zinc-50 p-3 text-sm text-zinc-700">
            <div>{t("salary.apply.confirmFactory", { factory: factoryLabel || "-" })}</div>
            <div className="mt-1">{t("salary.apply.confirmPrincipal", { amount: Number(principal || "0").toFixed(2) })}</div>
            <div className="mt-1">{t("salary.apply.confirmTenor", { days: Number(tenorDays || "0") })}</div>
          </div>
          {quote ? (
            <div className="rounded-2xl border border-zinc-200 p-3 text-sm">
              <div className="flex items-center justify-between">
                <span className="text-zinc-500">{t("salary.apply.previewFee")}</span>
                <span className="font-medium text-zinc-900">${quote.fee.toFixed(2)}</span>
              </div>
              <div className="mt-2 flex items-center justify-between">
                <span className="text-zinc-500">{t("salary.apply.previewInterest")}</span>
                <span className="font-medium text-zinc-900">${quote.interest.toFixed(2)}</span>
              </div>
              <div className="mt-2 flex items-center justify-between">
                <span className="text-zinc-500">{t("salary.apply.previewReceive")}</span>
                <span className="font-medium text-zinc-900">${quote.disbursement_amount.toFixed(2)}</span>
              </div>
              <div className="mt-2 flex items-center justify-between">
                <span className="text-zinc-500">{t("salary.apply.previewTotalDue")}</span>
                <span className="font-semibold text-zinc-900">${quote.total_due.toFixed(2)}</span>
              </div>
            </div>
          ) : null}
          <div className="text-xs text-zinc-500">{t("salary.apply.confirmNote")}</div>
          <div className="flex gap-2">
            <Button variant="secondary" className="flex-1" onClick={() => setConfirmOpen(false)}>
              {t("common.retry")}
            </Button>
            <Button
              className="flex-1"
              disabled={submitting}
              onClick={() => {
                setConfirmOpen(false)
                void submitConfirmed()
              }}
            >
              {submitting ? t("common.loading") : t("salary.apply.confirmSubmit")}
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  )
}
