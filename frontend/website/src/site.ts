import "./index.css"

const path = window.location.pathname.replace(/\/+$/, "")
if (path === "" || path === "/" || path === "/index.html") {
  window.location.replace("/km")
}

const localeMatch = path.match(/^\/(km|en|zh)(\/.*)?$/)
const currentLocale = (localeMatch?.[1] || "km") as "km" | "en" | "zh"
const rest = (localeMatch?.[2] || "")

for (const a of document.querySelectorAll<HTMLAnchorElement>("a[data-lang]")) {
  const targetLocale = a.dataset.lang as "km" | "en" | "zh" | undefined
  if (targetLocale !== "km" && targetLocale !== "en" && targetLocale !== "zh") continue
  const next = `/${targetLocale}${rest}`
  a.href = next

  a.classList.remove("bg-slate-100")
  a.classList.remove("hover:bg-slate-100")
  if (targetLocale === currentLocale) {
    a.classList.add("bg-slate-100")
  } else {
    a.classList.add("hover:bg-slate-100")
  }
}

const year = new Date().getFullYear()
for (const el of document.querySelectorAll<HTMLElement>("[data-year]")) {
  el.textContent = String(year)
}
