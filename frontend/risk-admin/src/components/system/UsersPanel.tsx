import { useCallback, useEffect, useMemo, useState } from 'react'
import { getErrorMessage, requestJson } from '@/api/http'
import type { AdminUser, PageResponse, Role } from '@/api/types'
import { useRbacStore } from '@/stores/rbacStore'
import { useHasPermission } from '@/hooks/usePermission'
import InviteUserCard from '@/components/system/InviteUserCard'
import UserRoleDrawer from '@/components/system/UserRoleDrawer'
import UsersTable from '@/components/system/UsersTable'

export default function UsersPanel() {
  const canAdmin = useHasPermission('system.admin')
  const actorId = useRbacStore((s) => s.actorId)

  const [keyword, setKeyword] = useState('')
  const [page, setPage] = useState(1)
  const [pageSize] = useState(20)
  const [data, setData] = useState<PageResponse<AdminUser> | null>(null)
  const [roles, setRoles] = useState<Role[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const [inviteEmail, setInviteEmail] = useState('')
  const [inviteName, setInviteName] = useState('')
  const [inviteRoleKeys, setInviteRoleKeys] = useState<string[]>([])
  const [inviting, setInviting] = useState(false)

  const [editUser, setEditUser] = useState<AdminUser | null>(null)
  const [editRoleKeys, setEditRoleKeys] = useState<string[]>([])
  const [savingRoles, setSavingRoles] = useState(false)

  const totalPages = useMemo(() => {
    const total = data?.total || 0
    return Math.max(1, Math.ceil(total / pageSize))
  }, [data?.total, pageSize])

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const qs = new URLSearchParams()
      if (keyword.trim()) qs.set('keyword', keyword.trim())
      qs.set('page', String(page))
      qs.set('pageSize', String(pageSize))
      const [usersResp, rolesResp] = await Promise.all([
        requestJson<PageResponse<AdminUser>>(`/api-risk/system/users?${qs.toString()}`),
        requestJson<Role[]>('/api-risk/system/roles'),
      ])
      setData(usersResp)
      setRoles(rolesResp)
    } catch (e: unknown) {
      setError(getErrorMessage(e))
    } finally {
      setLoading(false)
    }
  }, [keyword, page, pageSize])

  useEffect(() => {
    load()
  }, [load])

  async function invite() {
    if (!canAdmin) return
    setInviting(true)
    setError(null)
    try {
      await requestJson('/api-risk/system/users', {
        method: 'POST',
        body: JSON.stringify({ email: inviteEmail, displayName: inviteName, roleKeys: inviteRoleKeys }),
      })
      setInviteEmail('')
      setInviteName('')
      setInviteRoleKeys([])
      setPage(1)
      await load()
    } catch (e: unknown) {
      setError(getErrorMessage(e))
    } finally {
      setInviting(false)
    }
  }

  async function toggleStatus(u: AdminUser) {
    if (!canAdmin) return
    setError(null)
    try {
      await requestJson(`/api-risk/system/users/${encodeURIComponent(u.userId)}/status`, {
        method: 'POST',
        body: JSON.stringify({ status: u.status === 1 ? 0 : 1 }),
      })
      await load()
    } catch (e: unknown) {
      setError(getErrorMessage(e))
    }
  }

  async function saveUserRoles() {
    if (!canAdmin || !editUser) return
    setSavingRoles(true)
    setError(null)
    try {
      await requestJson(`/api-risk/system/users/${encodeURIComponent(editUser.userId)}/roles`, {
        method: 'POST',
        body: JSON.stringify({ roleKeys: editRoleKeys }),
      })
      setEditUser(null)
      await load()
    } catch (e: unknown) {
      setError(getErrorMessage(e))
    } finally {
      setSavingRoles(false)
    }
  }

  return (
    <div className="space-y-3">
      <div className="rounded-2xl border border-zinc-200 bg-white p-4 shadow-sm">
        <div className="flex flex-wrap items-end justify-between gap-3">
          <div>
            <div className="text-sm font-medium">用户管理</div>
            <div className="text-xs text-zinc-500">管理后台用户、启停与角色分配</div>
          </div>
          <div className="flex items-center gap-2">
            <input
              value={keyword}
              onChange={(e) => setKeyword(e.target.value)}
              className="h-9 w-72 rounded-lg border border-zinc-200 bg-white px-3 text-sm outline-none transition focus:border-zinc-400"
              placeholder="搜索 userId / email / 名称"
            />
            <button
              type="button"
              onClick={() => {
                setPage(1)
                load()
              }}
              className="inline-flex h-9 items-center rounded-lg bg-zinc-900 px-3 text-sm font-medium text-white transition hover:bg-zinc-800"
            >
              查询
            </button>
          </div>
        </div>

        {error ? <div className="mt-3 rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">{error}</div> : null}

        <div className="mt-4 grid gap-3 md:grid-cols-3">
          <div className="md:col-span-1">
            <InviteUserCard
              roles={roles}
              canAdmin={canAdmin}
              email={inviteEmail}
              displayName={inviteName}
              roleKeys={inviteRoleKeys}
              inviting={inviting}
              onChangeEmail={setInviteEmail}
              onChangeDisplayName={setInviteName}
              onChangeRoleKeys={setInviteRoleKeys}
              onSubmit={invite}
            />
          </div>

          <div className="md:col-span-2">
            <UsersTable
              users={data?.items || []}
              loading={loading}
              canAdmin={canAdmin}
              actorId={actorId}
              onEditRoles={(u) => {
                setEditUser(u)
                setEditRoleKeys(u.roleKeys || [])
              }}
              onToggleStatus={toggleStatus}
            />

            <div className="mt-3 flex items-center justify-between">
              <div className="text-xs text-zinc-500">第 {page} / {totalPages} 页（共 {data?.total ?? 0} 条）</div>
              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => setPage((p) => Math.max(1, p - 1))}
                  disabled={page <= 1}
                  className="inline-flex h-9 items-center rounded-lg border border-zinc-200 bg-white px-3 text-sm text-zinc-700 transition hover:bg-zinc-50 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  上一页
                </button>
                <button
                  type="button"
                  onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                  disabled={page >= totalPages}
                  className="inline-flex h-9 items-center rounded-lg border border-zinc-200 bg-white px-3 text-sm text-zinc-700 transition hover:bg-zinc-50 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  下一页
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <UserRoleDrawer
        open={!!editUser}
        title={editUser ? `修改角色：${editUser.email}` : '修改角色'}
        roles={roles}
        roleKeys={editRoleKeys}
        canAdmin={canAdmin}
        saving={savingRoles}
        onClose={() => setEditUser(null)}
        onChangeRoleKeys={setEditRoleKeys}
        onSave={saveUserRoles}
      />
    </div>
  )
}
