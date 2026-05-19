import { useEffect, useMemo, useState } from "react"
import Modal from "@/components/ui/Modal"
import Input from "@/components/ui/Input"
import Button from "@/components/ui/Button"
import { useI18n } from "@/i18n"

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
  const { t } = useI18n()
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
        <Input value={url} onChange={(e) => setUrl(e.target.value)} placeholder={t("proof.url")} />
        <Input
          type="number"
          value={amount}
          onChange={(e) => setAmount(Number(e.target.value || 0))}
          placeholder={t("proof.amount")}
          min={0}
        />
        <Input value={note} onChange={(e) => setNote(e.target.value)} placeholder={t("proof.note")} />
        <Button className="w-full" disabled={!can || submitting} onClick={() => onSubmit({ url: url.trim(), amount, note: note.trim() })}>
          {submitting ? t("borrow.submitting") : t("proof.confirm")}
        </Button>
        <div className="text-xs text-zinc-500">{t("proof.hint")}</div>
      </div>
    </Modal>
  )
}
