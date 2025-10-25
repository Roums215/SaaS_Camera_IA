import api from './api'
import { User, LoginCredentials, RegisterData } from '../types'

export const authService = {
  async login(credentials: LoginCredentials): Promise<{ user: User; token: string }> {
    // FastAPI OAuth2 expects form data
    const formData = new URLSearchParams()
    formData.append('username', credentials.username)
    formData.append('password', credentials.password)

    const { data } = await api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })

    const token = data.access_token

    // Get user info
    const { data: user } = await api.get<User>('/auth/me', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    return { user, token }
  },

  async register(data: RegisterData): Promise<User> {
    const { data: user } = await api.post<User>('/auth/register', data)
    return user
  },

  async getCurrentUser(): Promise<User> {
    const { data } = await api.get<User>('/auth/me')
    return data
  },

  async logout(): Promise<void> {
    await api.post('/auth/logout')
  },
}
