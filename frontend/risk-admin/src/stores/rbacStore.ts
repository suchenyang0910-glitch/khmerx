import { create } from 'zustand'

type RbacState = {
  actorId: string | null
  roles: string[]
  permissions: string[]
  hydrated: boolean
  setMe: (payload: { actorId: string; roles: string[]; permissions: string[] }) => void
  clear: () => void
}

export const useRbacStore = create<RbacState>((set) => ({
  actorId: null,
  roles: [],
  permissions: [],
  hydrated: false,
  setMe: (payload) =>
    set({
      actorId: payload.actorId,
      roles: payload.roles,
      permissions: payload.permissions,
      hydrated: true,
    }),
  clear: () => set({ actorId: null, roles: [], permissions: [], hydrated: false }),
}))

