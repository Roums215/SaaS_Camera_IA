import api from './api'
import { Alert } from '../types'

export const alertService = {
  async getAlerts(status?: string): Promise<Alert[]> {
    const { data } = await api.get<Alert[]>('/alerts/', {
      params: { status_filter: status },
    })
    return data
  },

  async getAlert(id: number): Promise<Alert> {
    const { data } = await api.get<Alert>(`/alerts/${id}`)
    return data
  },

  async acknowledgeAlert(id: number): Promise<void> {
    await api.post(`/alerts/${id}/acknowledge`)
  },

  async resolveAlert(id: number): Promise<void> {
    await api.post(`/alerts/${id}/resolve`)
  },

  async getUnreadCount(): Promise<number> {
    const { data } = await api.get<{ unread_count: number }>('/alerts/unread/count')
    return data.unread_count
  },
}
