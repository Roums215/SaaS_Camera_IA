import api from './api'
import { Detection } from '../types'

export const detectionService = {
  async getDetections(params?: {
    camera_id?: number
    detection_type?: string
    min_confidence?: number
    start_date?: string
    end_date?: string
  }): Promise<Detection[]> {
    const { data } = await api.get<Detection[]>('/detections/', { params })
    return data
  },

  async getDetection(id: number): Promise<Detection> {
    const { data } = await api.get<Detection>(`/detections/${id}`)
    return data
  },

  async updateDetection(id: number, update: Partial<Detection>): Promise<Detection> {
    const { data } = await api.put<Detection>(`/detections/${id}`, update)
    return data
  },

  async deleteDetection(id: number): Promise<void> {
    await api.delete(`/detections/${id}`)
  },

  async getDetectionStats(days: number = 7): Promise<any> {
    const { data } = await api.get('/detections/stats/summary', {
      params: { days },
    })
    return data
  },
}
