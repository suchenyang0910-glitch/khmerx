import { useEffect, useMemo, useState } from "react"
import Modal from "@/components/ui/Modal"
import Input from "@/components/ui/Input"
import Button from "@/components/ui/Button"

export default function ProofSheet({
  open,
  title,
  defaultUrl,
  defaultAmount,
  defaultNote,
  onClose,
  onSubmit,
  submitting,
}: {
  open: boolean
  title: string
  defaultUrl?: string
  defaultAmount?: number
  defaultNote?: string
  submitting: boolean
  onClose: () => void
  onSubmit: (input: { url: string; amount: number; note: string }) => void
}) {
  const [url, setUrl] = useState(defaultUrl || "")
  const [amount, setAmount] = useState<number>(defaultAmount ?? 0)
  const [note, setNote] = useState(defaultNote || "")

  useEffect(() => {
    if (!open) return
    setUrl(defaultUrl || "")
    setAmount(defaultAmount ?? 0)
    setNote(defaultNote || "")
  }, [defaultAmount, defaultNote, defaultUrl, open])

  const can = useMemo(() => url.trim().length >= 1 && amount > 0, [amount, url])

  return (
    <Modal open={open} title={title} onClose={onClose}>
      <div className="space-y-3">
        <Input value={url} onChange={(e) => setUrl(e.target.value)} placeholder="凭证 URL（可粘贴）" />
        <Input
          type="number"
          value={amount}
          onChange={(e) => setAmount(Number(e.target.value || 0))}
          placeholder="金额（必填）"
          min={0}
        />
        <Input value={note} onChange={(e) => setNote(e.target.value)} placeholder="备注（可选）" />
        <Button className="w-full" disabled={!can || submitting} onClick={() => onSubmit({ url: url.trim(), amount, note: note.trim() })}>
          {submitting ? "提交中…" : "确认"}
        </Button>
        <div className="text-xs text-zinc-500">为避免纠纷：请确保凭证清晰、金额与时间可辨认。</div>
      </div>
    </Modal>
  )
}
