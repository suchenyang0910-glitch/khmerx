import { useEffect, useMemo, useState } from "react"
import { useNavigate } from "react-router-dom"
import Card from "@/components/ui/Card"
import Button from "@/components/ui/Button"
import Input from "@/components/ui/Input"
import { useI18n } from "@/i18n"
import { createSalaryEmployment, createSalaryLoanOrder, fetchSalaryFactories } from "@/api/v1"
import type { SalaryFactory } from "@/api/types"
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

  async function onSubmit() {
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

              <Button
                data-testid="salary-apply-submit"
                disabled={submitting || !factoryId}
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
    </div>
  )
}

