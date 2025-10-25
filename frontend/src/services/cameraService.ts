import api from './api'
import { Camera, CameraStats } from '../types'

export const cameraService = {
  async getCameras(): Promise<Camera[]> {
    const { data } = await api.get<Camera[]>('/cameras/')
    return data
  },

  async getCamera(id: number): Promise<Camera> {
    const { data } = await api.get<Camera>(`/cameras/${id}`)
    return data
  },

  async createCamera(camera: Partial<Camera>): Promise<Camera> {
    const { data } = await api.post<Camera>('/cameras/', camera)
    return data
  },

  async updateCamera(id: number, camera: Partial<Camera>): Promise<Camera> {
    const { data } = await api.put<Camera>(`/cameras/${id}`, camera)
    return data
  },

  async deleteCamera(id: number): Promise<void> {
    await api.delete(`/cameras/${id}`)
  },

  async startCamera(id: number): Promise<void> {
    await api.post(`/cameras/${id}/start`)
  },

  async stopCamera(id: number): Promise<void> {
    await api.post(`/cameras/${id}/stop`)
  },

  async getCameraStats(id: number): Promise<CameraStats> {
    const { data } = await api.get<CameraStats>(`/cameras/${id}/stats`)
    return data
  },
}
