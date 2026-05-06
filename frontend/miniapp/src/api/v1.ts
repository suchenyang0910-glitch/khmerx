import { apiV1 } from "@/api/client"
import type { Announcement, Notification } from "@/api/types"

export async function fetchAnnouncements() {
  const res = await apiV1.get<{ ok: boolean; data: Announcement[] }>("/announcements")
  return res.data.data
}

export async function fetchNotifications() {
  const res = await apiV1.get<{ ok: boolean; data: Notification[] }>("/notifications")
  return res.data.data
}

export async function markNotificationRead(notificationId: string) {
  const res = await apiV1.post<{ ok: boolean; data: { id: string; read: boolean } }>(`/notifications/${notificationId}/read`)
  return res.data.data
}

export type NotificationSettings = {
  repayment_reminders: boolean
  dispute_updates: boolean
}

export async function fetchNotificationSettings() {
  const res = await apiV1.get<{ ok: boolean; data: NotificationSettings }>("/notifications/settings")
  return res.data.data
}

export async function updateNotificationSettings(input: Partial<NotificationSettings>) {
  const res = await apiV1.put<{ ok: boolean; data: NotificationSettings }>("/notifications/settings", input)
  return res.data.data
}
