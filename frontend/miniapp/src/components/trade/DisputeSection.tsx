import { useMemo, useState } from "react"
import Card from "@/components/ui/Card"
import Button from "@/components/ui/Button"
import Input from "@/components/ui/Input"
import Modal from "@/components/ui/Modal"
import { apiV1 } from "@/api/client"
import type { Dispute } from "@/api/types"
import { AlertTriangle, Flag } from "lucide-react"
import { errorMessage } from "@/utils/errors"

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
            <div className="text-sm font-semibold text-zinc-900">争议/仲裁</div>
            <div className="mt-1 text-sm text-zinc-600">凭证与确认存在分歧时可发起争议。</div>
            {active ? <div className="mt-2 text-xs text-zinc-500">当前争议状态：{active.status}</div> : null}
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
              发起争议
            </Button>
            <Button
              variant="secondary"
              className="w-full"
              disabled={!active}
              onClick={() => setEvidenceOpen(true)}
            >
              补充证据
            </Button>
          </div>
        </div>
      </Card>

      <Modal open={open} title="发起争议" onClose={() => setOpen(false)}>
        <div className="space-y-3">
          <div className="rounded-2xl bg-amber-50 p-3 text-sm text-amber-900">
            <div className="flex items-start gap-2">
              <AlertTriangle className="mt-0.5 h-4 w-4" />
              <div>
                <div className="font-semibold">请先确认你已尝试沟通与核对凭证</div>
                <div className="mt-1 text-xs">争议将记录在案并影响信用评估。</div>
              </div>
            </div>
          </div>
          <Input value={reason} onChange={(e) => setReason(e.target.value)} placeholder="请输入争议原因" />
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
                onError(errorMessage(e, "发起失败"))
              } finally {
                setSubmitting(false)
              }
            }}
          >
            {submitting ? "提交中…" : "提交争议"}
          </Button>
        </div>
      </Modal>

      <Modal open={evidenceOpen} title="补充证据" onClose={() => setEvidenceOpen(false)}>
        <div className="space-y-3">
          <div className="rounded-2xl bg-zinc-50 p-3 text-sm text-zinc-700">
            <div className="font-semibold">建议提交</div>
            <div className="mt-1 text-xs">转账截图/聊天记录/收款记录等能证明事实的材料。</div>
          </div>
          <Input value={evidenceUrl} onChange={(e) => setEvidenceUrl(e.target.value)} placeholder="证据 URL（可粘贴）" />
          <Input value={evidenceNote} onChange={(e) => setEvidenceNote(e.target.value)} placeholder="说明（可选）" />
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
                onError(errorMessage(e, "提交失败"))
              } finally {
                setSubmitting(false)
              }
            }}
          >
            {submitting ? "提交中…" : "提交证据"}
          </Button>
        </div>
      </Modal>
    </>
  )
}
