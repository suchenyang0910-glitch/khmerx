import "./index.css"

const year = new Date().getFullYear()
for (const el of document.querySelectorAll<HTMLElement>("[data-year]")) {
  el.textContent = String(year)
}

