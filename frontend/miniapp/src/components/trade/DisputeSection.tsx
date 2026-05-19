import { useMemo, useState } from "react"
import Card from "@/components/ui/Card"
import Button from "@/components/ui/Button"
import Input from "@/components/ui/Input"
import Modal from "@/components/ui/Modal"
import { apiV1 } from "@/api/client"
import type { Dispute } from "@/api/types"
import { AlertTriangle, Flag } from "lucide-react"
import { errorMessage } from "@/utils/errors"
import { useI18n } from "@/i18n"

export default function DisputeSection({
  tradeId,
  tradeStatus,
  disputes,
  submitting,
  onCreated,
  onError,
  setSubmitting,
}: {
  tradeId: string
  tradeStatus: string
  disputes: Dispute[]
  submitting: boolean
  setSubmitting: (v: boolean) => void
  onCreated: () => Promise<void>
  onError: (msg: string) => void
}) {
  const { t } = useI18n()
  const [open, setOpen] = useState(false)
  const [evidenceOpen, setEvidenceOpen] = useState(false)
  const [reason, setReason] = useState("")
  const [evidenceUrl, setEvidenceUrl] = useState("")
  const [evidenceNote, setEvidenceNote] = useState("")

  const active = useMemo(() => {
    return disputes.find((d) => String(d.trade_id) === String(tradeId)) || null
  }, [disputes, tradeId])

  return (
    <>
      <Card className="p-4">
        <div className="flex items-start justify-between gap-3">
          <div>
            <div className="text-sm font-semibold text-zinc-900">{t("dispute.title")}</div>
            <div className="mt-1 text-sm text-zinc-600">{t("dispute.desc")}</div>
            {active ? <div className="mt-2 text-xs text-zinc-500">{t("dispute.current", { status: active.status })}</div> : null}
          </div>
          <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-amber-50 text-amber-800">
            <Flag className="h-5 w-5" />
          </div>
        </div>
        <div className="mt-3">
          <div className="grid grid-cols-2 gap-2">
            <Button
              variant="secondary"
              className="w-full"
              disabled={tradeStatus === "completed" || Boolean(active)}
              onClick={() => setOpen(true)}
            >
              {t("dispute.open")}
            </Button>
            <Button
              variant="secondary"
              className="w-full"
              disabled={!active}
              onClick={() => setEvidenceOpen(true)}
            >
              {t("dispute.addEvidence")}
            </Button>
          </div>
        </div>
      </Card>

      <Modal open={open} title={t("dispute.open")} onClose={() => setOpen(false)}>
        <div className="space-y-3">
          <div className="rounded-2xl bg-amber-50 p-3 text-sm text-amber-900">
            <div className="flex items-start gap-2">
              <AlertTriangle className="mt-0.5 h-4 w-4" />
              <div>
                <div className="font-semibold">{t("dispute.warnTitle")}</div>
                <div className="mt-1 text-xs">{t("dispute.warnDesc")}</div>
              </div>
            </div>
          </div>
          <Input value={reason} onChange={(e) => setReason(e.target.value)} placeholder={t("dispute.reason")}
          />
          <Button
            className="w-full"
            disabled={submitting || reason.trim().length < 2}
            onClick={async () => {
              setSubmitting(true)
              try {
                await apiV1.post("/disputes", { trade_id: tradeId, dispute_type: "trade", reason: reason.trim() })
                setOpen(false)
                setReason("")
                await onCreated()
              } catch (e: unknown) {
                onError(errorMessage(e, t("dispute.openFailed")))
              } finally {
                setSubmitting(false)
              }
            }}
          >
            {submitting ? t("borrow.submitting") : t("dispute.submit")}
          </Button>
        </div>
      </Modal>

      <Modal open={evidenceOpen} title={t("dispute.addEvidence")} onClose={() => setEvidenceOpen(false)}>
        <div className="space-y-3">
          <div className="rounded-2xl bg-zinc-50 p-3 text-sm text-zinc-700">
            <div className="font-semibold">{t("dispute.suggest")}</div>
            <div className="mt-1 text-xs">{t("dispute.suggestDesc")}</div>
          </div>
          <Input value={evidenceUrl} onChange={(e) => setEvidenceUrl(e.target.value)} placeholder={t("dispute.evidenceUrl")} />
          <Input value={evidenceNote} onChange={(e) => setEvidenceNote(e.target.value)} placeholder={t("dispute.evidenceNote")} />
          <Button
            className="w-full"
            disabled={!active || submitting || evidenceUrl.trim().length < 6}
            onClick={async () => {
              if (!active) return
              setSubmitting(true)
              try {
                await apiV1.post(`/disputes/${active.id}/evidence`, {
                  evidence_type: "proof",
                  file_url: evidenceUrl.trim(),
                  text_note: evidenceNote.trim() || undefined,
                  metadata: {},
                })
                setEvidenceOpen(false)
                setEvidenceUrl("")
                setEvidenceNote("")
                await onCreated()
              } catch (e: unknown) {
                onError(errorMessage(e, t("dispute.submitFailed")))
              } finally {
                setSubmitting(false)
              }
            }}
          >
            {submitting ? t("borrow.submitting") : t("dispute.submitEvidence")}
          </Button>
        </div>
      </Modal>
    </>
  )
}
