import type { AdminUser } from '@/api/types'
import RoleChips from '@/components/system/RoleChips'

export default function UsersTable(props: {
  users: AdminUser[]
  loading: boolean
  canAdmin: boolean
  actorId: string | null
  onEditRoles: (u: AdminUser) => void
  onToggleStatus: (u: AdminUser) => void
}) {
  return (
    <div className="overflow-hidden rounded-xl border border-zinc-200">
      <table className="w-full text-sm">
        <thead className="bg-zinc-50 text-xs text-zinc-500">
          <tr>
            <th className="px-3 py-2 text-left font-medium">用户</th>
            <th className="px-3 py-2 text-left font-medium">角色</th>
            <th className="px-3 py-2 text-left font-medium">状态</th>
            <th className="px-3 py-2 text-right font-medium">操作</th>
          </tr>
        </thead>
        <tbody>
          {props.users.map((u) => (
            <tr key={u.userId} className="border-t border-zinc-200">
              <td className="px-3 py-2">
                <div className="text-zinc-900">{u.displayName || u.email}</div>
                <div className="text-xs text-zinc-500">{u.email}</div>
                <div className="text-xs text-zinc-500">{u.userId === props.actorId ? '当前登录' : ''}</div>
              </td>
              <td className="px-3 py-2">
                <RoleChips roles={u.roleKeys || []} />
              </td>
              <td className="px-3 py-2">
                <span className={u.status === 1 ? 'text-emerald-700' : 'text-zinc-500'}>{u.status === 1 ? '启用' : '停用'}</span>
              </td>
              <td className="px-3 py-2 text-right">
                <div className="inline-flex items-center gap-2">
                  <button
                    type="button"
                    onClick={() => props.onEditRoles(u)}
                    disabled={!props.canAdmin}
                    className="inline-flex h-8 items-center rounded-lg border border-zinc-200 bg-white px-2 text-xs text-zinc-700 transition hover:bg-zinc-50 disabled:cursor-not-allowed disabled:opacity-50"
                  >
                    角色
                  </button>
                  <button
                    type="button"
                    onClick={() => props.onToggleStatus(u)}
                    disabled={!props.canAdmin || u.userId === props.actorId}
                    className="inline-flex h-8 items-center rounded-lg border border-zinc-200 bg-white px-2 text-xs text-zinc-700 transition hover:bg-zinc-50 disabled:cursor-not-allowed disabled:opacity-50"
                  >
                    {u.status === 1 ? '停用' : '启用'}
                  </button>
                </div>
              </td>
            </tr>
          ))}
          {!props.loading && props.users.length === 0 ? (
            <tr>
              <td className="px-3 py-10 text-center text-sm text-zinc-500" colSpan={4}>
                暂无数据
              </td>
            </tr>
          ) : null}
        </tbody>
      </table>
    </div>
  )
}

