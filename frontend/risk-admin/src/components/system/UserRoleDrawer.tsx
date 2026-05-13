import Drawer from '@/components/Drawer'
import type { Role } from '@/api/types'

export default function UserRoleDrawer(props: {
  open: boolean
  title: string
  roles: Role[]
  roleKeys: string[]
  canAdmin: boolean
  saving: boolean
  onClose: () => void
  onChangeRoleKeys: (keys: string[]) => void
  onSave: () => void
}) {
  return (
    <Drawer open={props.open} title={props.title} onClose={props.onClose}>
      <div className="space-y-3">
        <div className="rounded-lg border border-zinc-200 p-3">
          <div className="text-sm font-medium">选择角色</div>
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
          onClick={props.onSave}
          disabled={!props.canAdmin || props.saving}
          className="inline-flex h-9 w-full items-center justify-center rounded-lg bg-zinc-900 px-3 text-sm font-medium text-white transition hover:bg-zinc-800 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {props.saving ? '保存中…' : props.canAdmin ? '保存' : '需要 system.admin 权限'}
        </button>
      </div>
    </Drawer>
  )
}

