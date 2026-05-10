import "./index.css"

const path = window.location.pathname.replace(/\/+$/, "")
if (path === "" || path === "/" || path === "/index.html") {
  window.location.replace("/km")
}

const year = new Date().getFullYear()
for (const el of document.querySelectorAll<HTMLElement>("[data-year]")) {
  el.textContent = String(year)
}
