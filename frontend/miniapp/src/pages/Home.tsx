import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import Badge from "@/components/ui/Badge";
import { useAuthStore } from "@/stores/authStore";
import { ArrowRight, Megaphone, ShieldCheck } from "lucide-react";
import { fetchAnnouncements } from "@/api/v1";
import type { Announcement } from "@/api/types";
import { useI18n } from "@/i18n";

function scoreToLevel(score: number) {
  if (score >= 800) return "A"
  if (score >= 700) return "B"
  if (score >= 600) return "C"
  return "D"
}

export default function Home() {
  const { t } = useI18n()
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
    if (risk?.max_borrow_amount != null) return risk.max_borrow_amount
    return creditLevel === "A" ? 500 : creditLevel === "B" ? 300 : creditLevel === "C" ? 200 : 100
  }, [creditLevel, risk?.max_borrow_amount])

  const isNewUser = (user?.total_borrowed || 0) <= 0

  return (
    <div className="space-y-4">
      {ann.length ? (
        <Card className="p-4">
          <div className="flex items-start justify-between gap-3">
            <div>
              <div className="text-sm font-semibold text-zinc-900">{t("home.announcement")}</div>
              <div className="mt-1 text-sm text-zinc-700">{ann[0].title}</div>
              <div className="mt-1 text-xs text-zinc-500 line-clamp-2">{ann[0].body}</div>
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
      <div className="rounded-2xl bg-gradient-to-r from-blue-600 to-cyan-500 p-4 text-white shadow-sm">
        <div className="flex items-center justify-between">
          <div>
            <div className="text-xs opacity-90">{t("home.creditLevel")}</div>
            <div className="mt-1 text-2xl font-bold">{creditLevel}</div>
          </div>
          <div className="text-right">
            <div className="text-xs opacity-90">{t("home.creditScore")}</div>
            <div className="mt-1 text-2xl font-bold">{user?.credit_score ?? 650}</div>
          </div>
        </div>
        <div className="mt-3 flex items-center justify-between rounded-2xl bg-white/15 px-3 py-2">
          <div className="text-sm">{t("home.borrowLimit")}</div>
          <div className="text-lg font-semibold">${Math.round(maxBorrow)}</div>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <Link to="/borrow">
          <Button className="w-full">{t("home.borrowNow")}</Button>
        </Link>
        <Link to="/lend">
          <Button variant="secondary" className="w-full">{t("home.lendNow")}</Button>
        </Link>
      </div>

      <Card className="p-4">
        <div className="flex items-start justify-between gap-3">
          <div>
            <div className="text-sm font-semibold text-zinc-900">{t("home.whyCanBorrow")}</div>
            <div className="mt-1 text-sm text-zinc-600">{t("home.whyDesc")}</div>
          </div>
          <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-blue-50 text-blue-700">
            <ShieldCheck className="h-5 w-5" />
          </div>
        </div>
        <div className="mt-3 flex flex-wrap gap-2">
          {isNewUser ? <Badge tone="blue">{t("home.newUserSuggest")}</Badge> : <Badge tone="green">{t("home.oldUserMore")}</Badge>}
          <Badge tone="zinc">{t("home.onTimeImprove")}</Badge>
          <Badge tone={(risk?.risk_level && ["flagged", "restricted", "blocked"].includes(risk.risk_level)) ? "yellow" : "green"}>
            {t("home.risk")}：{risk?.risk_level || user?.risk_level || "normal"}
          </Badge>
        </div>
      </Card>

      <Card className="p-4">
        <div className="flex items-center justify-between">
          <div>
            <div className="text-sm font-semibold text-zinc-900">{t("home.successTips")}</div>
            <div className="mt-1 text-sm text-zinc-600">{t("home.successDesc")}</div>
          </div>
          <Link to="/borrow" className="text-sm text-blue-600">
            {t("home.goCreate")} <ArrowRight className="inline h-4 w-4" />
          </Link>
        </div>
      </Card>
    </div>
  );
}
