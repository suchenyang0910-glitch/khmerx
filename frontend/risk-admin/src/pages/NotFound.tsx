import { Link } from 'react-router-dom'

export default function NotFound() {
  return (
    <div className="mx-auto max-w-xl rounded-2xl border border-zinc-200 bg-white p-6 text-center shadow-sm">
      <div className="text-base font-semibold">页面不存在</div>
      <div className="mt-2 text-sm text-zinc-600">请从侧边栏进入可用功能页面</div>
      <Link
        to="/"
        className="mt-4 inline-flex rounded-lg bg-zinc-900 px-3 py-2 text-sm font-medium text-white transition hover:bg-zinc-800"
      >
        返回控制台
      </Link>
    </div>
  )
}

