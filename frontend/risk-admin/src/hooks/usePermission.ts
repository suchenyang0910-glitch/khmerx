import { useMemo } from 'react'
import { useRbacStore } from '@/stores/rbacStore'

export function useHasPermission(permKey: string) {
  const permissions = useRbacStore((s) => s.permissions)
  return useMemo(() => permissions.includes(permKey), [permissions, permKey])
}

