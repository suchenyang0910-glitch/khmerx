import { useEffect, useMemo, useState } from "react"
import { useParams } from "react-router-dom"
import Card from "@/components/ui/Card"
import Button from "@/components/ui/Button"
import Input from "@/components/ui/Input"
import { useI18n } from "@/i18n"
import { fetchSalaryLoanOrderDetail, uploadSalaryLoanRepaymentProof } from "@/api/v1"
import type { SalaryLoanOrderDetail } from "@/api/types"
import { errorMessage } from "@/utils/errors"

function money(n: number) {
  if (!Number.isFinite(n)) return "0"
  return n % 1 === 0 ? n.toFixed(0) : n.toFixed(2)
}

export default function SalaryLoanOrderDetailPage() {
  const { t } = useI18n()
  const { orderId } = useParams()
  const [loading, setLoading] = useState(true)
  const [err, setErr] = useState<string | null>(null)
  const [data, setData] = useState<SalaryLoanOrderDetail | null>(null)

  const [file, setFile] = useState<File | null>(null)
  const [amount, setAmount] = useState<string>("")
  const [note, setNote] = useState<string>("")
  const [uploading, setUploading] = useState(false)
  const [uploadedUrl, setUploadedUrl] = useState<string | null>(null)

  useEffect(() => {
    if (!orderId) return
    let cancelled = false
    setLoading(true)
    setErr(null)
    fetchSalaryLoanOrderDetail(orderId)
      .then((d) => {
        if (cancelled) return
        setData(d)
        const due = d.schedules?.[0]?.due_amount
        if (typeof due === "number" && Number.isFinite(due)) setAmount(String(due))
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
  }, [orderId, t])

  const status = data?.order.status || ""
  const totalDue = useMemo(() => {
    if (!data) return 0
    const s = data.schedules?.[0]
    return s ? Number(s.due_amount || 0) : Number(data.order.principal) + Number(data.order.fee) + Number(data.order.interest)
  }, [data])

  const canUpload = useMemo(() => {
    if (!data) return false
    return ["disbursed", "repaying", "overdue"].includes(data.order.status)
  }, [data])

  async function onUpload() {
    if (!orderId || !file) return
    setUploading(true)
    setErr(null)
    setUploadedUrl(null)
    try {
      const n = Number(amount)
      if (!Number.isFinite(n) || n <= 0) throw new Error(t("salary.order.invalidPayAmount"))
      const res = await uploadSalaryLoanRepaymentProof(orderId, { amount: n, note, file })
      setUploadedUrl(res.url)
      setFile(null)
    } catch (e: unknown) {
      setErr(errorMessage(e, t("common.requestFailed")))
    } finally {
      setUploading(false)
    }
  }

  return (
    <div data-testid="page-salary-order" className="space-y-4">
      <div className="text-base font-semibold text-zinc-900">{t("salary.order.title")}</div>

      {loading ? (
        <div className="space-y-3">
          <div className="h-28 animate-pulse rounded-2xl bg-white" />
          <div className="h-52 animate-pulse rounded-2xl bg-white" />
        </div>
      ) : err ? (
        <Card className="p-4">
          <div className="text-sm font-semibold text-zinc-900">{t("common.requestFailed")}</div>
          <div className="mt-2 text-sm text-zinc-600">{err}</div>
        </Card>
      ) : !data ? (
        <Card className="p-4">
          <div className="text-sm text-zinc-700">{t("common.empty")}</div>
        </Card>
      ) : (
        <>
          <Card className="p-4" data-testid="salary-order-summary">
            <div className="flex items-start justify-between gap-3">
              <div>
                <div className="text-sm font-semibold text-zinc-900">{t("salary.order.no", { id: data.order.id.slice(0, 8) })}</div>
                <div className="mt-1 text-xs text-zinc-500">{t("salary.order.status", { status })}</div>
                {data.order.due_date ? <div className="mt-1 text-xs text-zinc-500">{t("salary.order.due", { date: data.order.due_date })}</div> : null}
              </div>
              <div className="text-right">
                <div className="text-sm font-bold text-zinc-900">${money(Number(data.order.principal))}</div>
                <div className="mt-1 text-xs text-zinc-500">{t("salary.order.totalDue", { amount: money(totalDue) })}</div>
              </div>
            </div>

            {data.factory ? (
              <div className="mt-3 rounded-xl bg-zinc-50 p-3">
                <div className="text-xs font-medium text-zinc-700">{t("salary.order.factory")}</div>
                <div className="mt-1 text-sm text-zinc-900">{data.factory.name}</div>
                {data.employment.employee_no ? <div className="mt-1 text-xs text-zinc-500">{t("salary.order.employeeNo", { no: data.employment.employee_no })}</div> : null}
              </div>
            ) : null}
          </Card>

          <Card className="p-4" data-testid="salary-order-schedules">
            <div className="text-sm font-semibold text-zinc-900">{t("salary.order.schedule")}</div>
            <div className="mt-3 space-y-2">
              {data.schedules.length === 0 ? (
                <div className="text-sm text-zinc-600">{t("salary.order.schedulePending")}</div>
              ) : (
                data.schedules.map((s) => (
                  <div key={s.id} className="flex items-center justify-between rounded-xl border border-zinc-200 bg-white p-3">
                    <div>
                      <div className="text-sm font-medium text-zinc-900">{t("salary.order.installment", { no: s.installment_no })}</div>
                      <div className="mt-1 text-xs text-zinc-500">{t("salary.order.due", { date: s.due_date })}</div>
                      <div className="mt-1 text-xs text-zinc-500">{t("salary.order.scheduleStatus", { status: s.status })}</div>
                    </div>
                    <div className="text-right">
                      <div className="text-sm font-semibold text-zinc-900">${money(Number(s.due_amount))}</div>
                      {Number(s.paid_amount) > 0 ? <div className="mt-1 text-xs text-zinc-500">{t("salary.order.paid", { amount: money(Number(s.paid_amount)) })}</div> : null}
                    </div>
                  </div>
                ))
              )}
            </div>
          </Card>

          <Card className="p-4" data-testid="salary-order-repay">
            <div className="text-sm font-semibold text-zinc-900">{t("salary.order.repay")}</div>
            <div className="mt-2 text-sm text-zinc-600">{t("salary.order.repayDesc")}</div>

            {!canUpload ? (
              <div className="mt-3 rounded-xl bg-zinc-50 p-3 text-sm text-zinc-700">{t("salary.order.repayNotReady")}</div>
            ) : (
              <div className="mt-3 space-y-3">
                <div>
                  <div className="text-xs font-medium text-zinc-700">{t("salary.order.payAmount")}</div>
                  <Input inputMode="decimal" value={amount} onChange={(e) => setAmount(e.target.value)} />
                </div>
                <div>
                  <div className="text-xs font-medium text-zinc-700">{t("salary.order.note")}</div>
                  <Input value={note} onChange={(e) => setNote(e.target.value)} placeholder={t("salary.order.notePh")} />
                </div>
                <div>
                  <div className="text-xs font-medium text-zinc-700">{t("salary.order.proof")}</div>
                  <input
                    type="file"
                    accept="image/*"
                    onChange={(e) => setFile(e.target.files?.[0] || null)}
                    className="mt-1 block w-full text-sm text-zinc-700 file:mr-3 file:rounded-lg file:border-0 file:bg-zinc-100 file:px-3 file:py-2 file:text-sm file:font-medium hover:file:bg-zinc-200"
                  />
                  {file ? <div className="mt-1 text-xs text-zinc-500">{file.name}</div> : null}
                </div>

                <Button data-testid="salary-upload-proof" disabled={!file || uploading} onClick={onUpload} className="w-full">
                  {uploading ? t("common.loading") : t("salary.order.upload")}
                </Button>
                {uploadedUrl ? <div className="text-xs text-emerald-600">{t("salary.order.uploaded")}</div> : null}
              </div>
            )}
          </Card>
        </>
      )}
    </div>
  )
}

