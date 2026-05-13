import { useCallback, useEffect, useMemo, useState } from 'react'
import { getErrorMessage, requestJson } from '@/api/http'
import type { Permission, Role } from '@/api/types'
import { cn } from '@/lib/utils'
import { useHasPermission } from '@/hooks/usePermission'

export default function RolesPanel() {
  const canAdmin = useHasPermission('system.admin')
  const [roles, setRoles] = useState<Role[]>([])
  const [permissions, setPermissions] = useState<Permission[]>([])
  const [selectedRoleId, setSelectedRoleId] = useState<string | null>(null)
  const [workingKeys, setWorkingKeys] = useState<string[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [saving, setSaving] = useState(false)

  const selectedRole = useMemo(() => roles.find((r) => r.roleId === selectedRoleId) || null, [roles, selectedRoleId])

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const [rolesResp, permsResp] = await Promise.all([
        requestJson<Role[]>('/api-risk/system/roles'),
        requestJson<Permission[]>('/api-risk/system/permissions'),
      ])
      setRoles(rolesResp)
      setPermissions(permsResp)
      if (!selectedRoleId && rolesResp.length > 0) {
        setSelectedRoleId(rolesResp[0].roleId)
        setWorkingKeys(rolesResp[0].permissionKeys || [])
      }
    } catch (e: unknown) {
      setError(getErrorMessage(e))
    } finally {
      setLoading(false)
    }
  }, [selectedRoleId])

  useEffect(() => {
    load()
  }, [load])

  useEffect(() => {
    if (!selectedRole) return
    setWorkingKeys(selectedRole.permissionKeys || [])
  }, [selectedRole])

  const groups = useMemo(() => {
    const buckets: Record<string, Permission[]> = {}
    for (const p of permissions) {
      const prefix = p.permKey.includes('.') ? p.permKey.split('.')[0] : 'other'
      buckets[prefix] = buckets[prefix] || []
      buckets[prefix].push(p)
    }
    return Object.entries(buckets).sort((a, b) => a[0].localeCompare(b[0]))
  }, [permissions])

  async function save() {
    if (!canAdmin || !selectedRoleId) return
    setSaving(true)
    setError(null)
    try {
      await requestJson(`/api-risk/system/roles/${encodeURIComponent(selectedRoleId)}/permissions`, {
        method: 'POST',
        body: JSON.stringify({ permissionKeys: workingKeys }),
      })
      await load()
    } catch (e: unknown) {
      setError(getErrorMessage(e))
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="rounded-2xl border border-zinc-200 bg-white p-4 shadow-sm">
      <div className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <div className="text-sm font-medium">角色与权限</div>
          <div className="text-xs text-zinc-500">配置角色权限矩阵，并用于前端路由/按钮保护</div>
        </div>
        <button
          type="button"
          onClick={save}
          disabled={!canAdmin || saving || !selectedRoleId}
          className="inline-flex h-9 items-center rounded-lg bg-zinc-900 px-3 text-sm font-medium text-white transition hover:bg-zinc-800 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {saving ? '保存中…' : canAdmin ? '保存权限' : '需要 system.admin 权限'}
        </button>
      </div>

      {error ? <div className="mt-3 rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">{error}</div> : null}

      <div className="mt-4 grid gap-3 md:grid-cols-3">
        <div className="rounded-xl border border-zinc-200">
          <div className="border-b border-zinc-200 bg-zinc-50 px-3 py-2 text-xs font-medium text-zinc-500">角色</div>
          <div className="max-h-[520px] overflow-auto p-2">
            {roles.map((r) => (
              <button
                key={r.roleId}
                type="button"
                onClick={() => setSelectedRoleId(r.roleId)}
                className={cn(
                  'flex w-full items-center justify-between rounded-lg px-3 py-2 text-left text-sm transition',
                  r.roleId === selectedRoleId ? 'bg-zinc-900 text-white' : 'text-zinc-700 hover:bg-zinc-100'
                )}
              >
                <span className="truncate">{r.roleName}</span>
                <span className={cn('ml-2 text-xs', r.roleId === selectedRoleId ? 'text-white/80' : 'text-zinc-500')}>
                  {r.roleKey}
                </span>
              </button>
            ))}
            {!loading && roles.length === 0 ? <div className="p-3 text-sm text-zinc-500">暂无角色</div> : null}
          </div>
        </div>

        <div className="md:col-span-2 rounded-xl border border-zinc-200">
          <div className="border-b border-zinc-200 bg-zinc-50 px-3 py-2 text-xs font-medium text-zinc-500">
            权限
          </div>
          <div className="max-h-[520px] overflow-auto p-3">
            {selectedRole ? (
              <div className="mb-3 text-sm text-zinc-700">
                当前角色：<span className="font-medium text-zinc-900">{selectedRole.roleName}</span>
                <span className="ml-2 text-xs text-zinc-500">({selectedRole.roleKey})</span>
              </div>
            ) : null}

            <div className="space-y-4">
              {groups.map(([group, perms]) => (
                <div key={group} className="rounded-xl border border-zinc-200 p-3">
                  <div className="text-xs font-medium text-zinc-500">{group}</div>
                  <div className="mt-2 grid gap-2 md:grid-cols-2">
                    {perms.map((p) => (
                      <label key={p.permKey} className="flex cursor-pointer items-center gap-2 text-sm">
                        <input
                          type="checkbox"
                          checked={workingKeys.includes(p.permKey)}
                          onChange={(e) => {
                            setWorkingKeys((prev) => {
                              if (e.target.checked) return [...prev, p.permKey]
                              return prev.filter((k) => k !== p.permKey)
                            })
                          }}
                          disabled={!canAdmin}
                        />
                        <span className="text-zinc-800">{p.permName}</span>
                        <span className="text-xs text-zinc-500">{p.permKey}</span>
                      </label>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

