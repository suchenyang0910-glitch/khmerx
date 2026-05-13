import { cn } from '@/lib/utils'
import { useMemo, useState } from 'react'
import UsersPanel from '@/components/system/UsersPanel'
import RolesPanel from '@/components/system/RolesPanel'
import AuditPanel from '@/components/system/AuditPanel'
import { useHasPermission } from '@/hooks/usePermission'
import { useRbacStore } from '@/stores/rbacStore'

type TabKey = 'users' | 'roles' | 'audit' | 'access'

function TabButton(props: { active: boolean; onClick: () => void; children: React.ReactNode }) {
  return (
    <button
      type="button"
      onClick={props.onClick}
      className={cn(
        'inline-flex h-9 items-center rounded-lg px-3 text-sm transition',
        props.active ? 'bg-zinc-900 text-white' : 'text-zinc-700 hover:bg-zinc-100'
      )}
    >
      {props.children}
    </button>
  )
}

export default function System() {
  const canReadAudit = useHasPermission('audit.read')
  const actorId = useRbacStore((s) => s.actorId)
  const roles = useRbacStore((s) => s.roles)
  const permissions = useRbacStore((s) => s.permissions)
  const [tab, setTab] = useState<TabKey>(canReadAudit ? 'audit' : 'users')

  const visibleTabs = useMemo(() => {
    const t: TabKey[] = ['users', 'roles', 'access']
    if (canReadAudit) t.splice(2, 0, 'audit')
    return t
  }, [canReadAudit])

  return (
    <div className="space-y-4">
      <div>
        <div className="text-base font-semibold">系统管理</div>
        <div className="text-xs text-zinc-500">用户/角色/权限与审计日志</div>
      </div>

      <div className="flex flex-wrap items-center gap-2">
        <TabButton active={tab === 'users'} onClick={() => setTab('users')}>
          用户管理
        </TabButton>
        <TabButton active={tab === 'roles'} onClick={() => setTab('roles')}>
          角色与权限
        </TabButton>
        {visibleTabs.includes('audit') ? (
          <TabButton active={tab === 'audit'} onClick={() => setTab('audit')}>
            审计日志
          </TabButton>
        ) : null}
        <TabButton active={tab === 'access'} onClick={() => setTab('access')}>
          登录与访问
        </TabButton>
      </div>

      <div className="rounded-2xl border border-zinc-200 bg-white p-4 text-sm text-zinc-700 shadow-sm">
        <div>当前登录：<span className="font-mono text-xs">{actorId || '—'}</span></div>
        <div className="mt-1">角色：{roles.length ? roles.join(', ') : '—'}</div>
        <div className="mt-1">权限：{permissions.length ? permissions.join(', ') : '—'}</div>
      </div>

      {tab === 'users' ? <UsersPanel /> : null}
      {tab === 'roles' ? <RolesPanel /> : null}
      {tab === 'audit' ? <AuditPanel /> : null}
      {tab === 'access' ? (
        <div className="rounded-2xl border border-zinc-200 bg-white p-6 text-sm text-zinc-600 shadow-sm">
          当前登录方式为商户 API Key（JWT principal=merchantId）。如需“管理员账号+密码/SSO”，下一步可在 auth-service 扩展用户认证并将 actorId 切换为 adminUserId。
        </div>
      ) : null}
    </div>
  )
}
