import { useEffect, useMemo, useState } from "react"
import { Link } from "react-router-dom"
import Card from "@/components/ui/Card"
import Badge from "@/components/ui/Badge"
import { useAuthStore } from "@/stores/authStore"
import { ArrowRight, HandCoins, Lock, Megaphone, ShoppingCart, Smartphone } from "lucide-react"
import { fetchAnnouncements } from "@/api/v1"
import type { Announcement } from "@/api/types"
import { useI18n } from "@/i18n"

function scoreToLevel(score: number) {
  if (score >= 800) return "A"
  if (score >= 700) return "B"
  if (score >= 600) return "C"
  return "D"
}

export default function Home() {
  const { t } = useI18n()
  const MAX_BORROW_CAP = 800
  const NEW_USER_BORROW_CAP = 500
  const user = useAuthStore((s) => s.user)
  const risk = useAuthStore((s) => s.risk)
  const refresh = useAuthStore((s) => s.refreshMe)
  const [ann, setAnn] = useState<Announcement[]>([])

  useEffect(() => {
    refresh()
  }, [refresh])

  useEffect(() => {
    fetchAnnouncements().then(setAnn).catch(() => setAnn([]))
  }, [])

  const creditLevel = useMemo(() => scoreToLevel(user?.credit_score || 650), [user?.credit_score])
  const maxBorrow = useMemo(() => {
    const base = risk?.max_borrow_amount ?? MAX_BORROW_CAP
    const capped = Math.min(base, MAX_BORROW_CAP)
    const isNew = (user?.total_borrowed || 0) <= 0
    return isNew ? Math.min(capped, NEW_USER_BORROW_CAP) : capped
  }, [MAX_BORROW_CAP, NEW_USER_BORROW_CAP, risk?.max_borrow_amount, user?.total_borrowed])

  const isNewUser = (user?.total_borrowed || 0) <= 0

  return (
    <div data-testid="page-home" className="space-y-4">
      {ann.length ? (
        <Card className="p-4">
          <div className="flex items-start justify-between gap-3">
            <div>
              <div className="text-sm font-semibold text-zinc-900">{t("home.announcement")}</div>
              <div className="mt-1 text-sm text-zinc-700">{ann[0].title}</div>
              <div className="mt-1 line-clamp-2 text-xs text-zinc-500">{ann[0].body}</div>
              {ann[0].link_url ? (
                <a className="mt-2 inline-block text-sm text-blue-600" href={ann[0].link_url} target="_blank" rel="noreferrer">
                  {t("home.viewDetail")} <ArrowRight className="inline h-4 w-4" />
                </a>
              ) : null}
            </div>
            <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-blue-50 text-blue-700">
              <Megaphone className="h-5 w-5" />
            </div>
          </div>
        </Card>
      ) : null}

      <div data-testid="credit-card" className="rounded-2xl bg-gradient-to-r from-blue-600 to-cyan-500 p-4 text-white shadow-sm">
        <div className="flex items-start justify-between gap-3">
          <div>
            <div className="text-xs opacity-90">{t("home.creditScore")}</div>
            <div className="mt-1 text-2xl font-bold tabular-nums">{user?.credit_score ?? 650}</div>
            <div className="mt-2 flex flex-wrap gap-2">
              <Badge tone="zinc">{t("home.creditLevel")} {creditLevel}</Badge>
              <Badge tone="zinc">{t("home.risk")} {risk?.risk_level || user?.risk_level || "normal"}</Badge>
            </div>
          </div>
          <div className="text-right">
            <div className="text-xs opacity-90">{t("home.borrowLimit")}</div>
            <div className="mt-1 text-2xl font-bold tabular-nums">${Math.round(maxBorrow)}</div>
            <div className="mt-2 text-xs text-white/90">{t("home.activeLoans", { count: user?.active_loans || 0 })}</div>
          </div>
        </div>
        <div className="mt-3 text-xs text-white/90">
          {t("borrow.platformCap", { cap: MAX_BORROW_CAP })}
          {isNewUser ? ` ${t("borrow.newUserCap", { cap: NEW_USER_BORROW_CAP })}` : ""}
        </div>
        <div className="mt-2">
          <Link to="/credit" className="text-sm text-white underline">
            {t("home.viewCredit")} <ArrowRight className="inline h-4 w-4" />
          </Link>
        </div>
      </div>

      <div data-testid="home-grid" className="grid grid-cols-2 gap-3">
        <Link data-testid="entry-loan" to="/borrow" className="rounded-2xl bg-white p-4 shadow-sm">
          <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-blue-50 text-blue-700">
            <HandCoins className="h-5 w-5" />
          </div>
          <div className="mt-3 text-sm font-semibold text-zinc-900">{t("services.loan.title")}</div>
          <div className="mt-1 text-xs text-zinc-500">{t("home.fastToAccount")}</div>
        </Link>
        <Link data-testid="entry-lease" to="/catalog/lease" className="rounded-2xl bg-white p-4 shadow-sm">
          <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-blue-50 text-blue-700">
            <Smartphone className="h-5 w-5" />
          </div>
          <div className="mt-3 text-sm font-semibold text-zinc-900">{t("services.lease.title")}</div>
          <div className="mt-1 text-xs text-zinc-500">{t("home.rentalDesc")}</div>
        </Link>
        <Link data-testid="entry-installment" to="/catalog/installment" className="rounded-2xl bg-white p-4 shadow-sm">
          <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-blue-50 text-blue-700">
            <ShoppingCart className="h-5 w-5" />
          </div>
          <div className="mt-3 text-sm font-semibold text-zinc-900">{t("services.installment.title")}</div>
          <div className="mt-1 text-xs text-zinc-500">{t("home.installmentDesc")}</div>
        </Link>
        <Link data-testid="entry-pledge" to="/apply/pledge" className="rounded-2xl bg-white p-4 shadow-sm">
          <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-blue-50 text-blue-700">
            <Lock className="h-5 w-5" />
          </div>
          <div className="mt-3 text-sm font-semibold text-zinc-900">{t("services.pledge.title")}</div>
          <div className="mt-1 text-xs text-zinc-500">{t("home.pawnDesc")}</div>
        </Link>
      </div>

      <Card className="p-4">
        <div className="flex items-center justify-between">
          <div>
            <div className="text-sm font-semibold text-zinc-900">{t("home.myOrders")}</div>
            <div className="mt-1 text-sm text-zinc-600">{t("home.myOrdersDesc")}</div>
          </div>
          <Link to="/orders" className="text-sm text-blue-600">
            {t("home.viewDetail")} <ArrowRight className="inline h-4 w-4" />
          </Link>
        </div>
      </Card>
    </div>
  )
}
