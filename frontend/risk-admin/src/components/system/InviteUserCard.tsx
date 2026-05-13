import type { Role } from '@/api/types'

export default function InviteUserCard(props: {
  roles: Role[]
  canAdmin: boolean
  email: string
  displayName: string
  roleKeys: string[]
  inviting: boolean
  onChangeEmail: (v: string) => void
  onChangeDisplayName: (v: string) => void
  onChangeRoleKeys: (keys: string[]) => void
  onSubmit: () => void
}) {
  return (
    <div>
      <div className="text-sm font-medium">邀请用户</div>
      <div className="mt-2 grid gap-2">
        <input
          value={props.email}
          onChange={(e) => props.onChangeEmail(e.target.value)}
          className="h-9 w-full rounded-lg border border-zinc-200 bg-white px-3 text-sm outline-none transition focus:border-zinc-400"
          placeholder="email"
        />
        <input
          value={props.displayName}
          onChange={(e) => props.onChangeDisplayName(e.target.value)}
          className="h-9 w-full rounded-lg border border-zinc-200 bg-white px-3 text-sm outline-none transition focus:border-zinc-400"
          placeholder="显示名（可空）"
        />
        <div className="rounded-lg border border-zinc-200 p-2">
          <div className="text-xs text-zinc-500">角色</div>
          <div className="mt-2 space-y-1">
            {props.roles.map((r) => (
              <label key={r.roleId} className="flex cursor-pointer items-center gap-2 text-sm">
                <input
                  type="checkbox"
                  checked={props.roleKeys.includes(r.roleKey)}
                  onChange={(e) => {
                    props.onChangeRoleKeys(
                      e.target.checked
                        ? [...props.roleKeys, r.roleKey]
                        : props.roleKeys.filter((k) => k !== r.roleKey)
                    )
                  }}
                  disabled={!props.canAdmin}
                />
                <span className="text-zinc-800">{r.roleName}</span>
                <span className="text-xs text-zinc-500">({r.roleKey})</span>
              </label>
            ))}
          </div>
        </div>
        <button
          type="button"
          onClick={props.onSubmit}
          disabled={!props.canAdmin || props.inviting || !props.email}
          className="inline-flex h-9 items-center justify-center rounded-lg bg-zinc-900 px-3 text-sm font-medium text-white transition hover:bg-zinc-800 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {props.inviting ? '提交中…' : props.canAdmin ? '创建用户' : '需要 system.admin 权限'}
        </button>
      </div>
    </div>
  )
}

