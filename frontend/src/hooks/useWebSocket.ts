import { useEffect, useRef, useState } from 'react'
import { useAuthStore } from '../stores/authStore'
import { DetectionFrame } from '../types'

const WS_BASE_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/api/v1/ws'

export function useWebSocket(cameraId: number) {
  const [frame, setFrame] = useState<DetectionFrame | null>(null)
  const [isConnected, setIsConnected] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const wsRef = useRef<WebSocket | null>(null)
  const { token } = useAuthStore()

  useEffect(() => {
    if (!token || !cameraId) return

    const ws = new WebSocket(`${WS_BASE_URL}/stream/${cameraId}?token=${token}`)

    ws.onopen = () => {
      console.log('WebSocket connected')
      setIsConnected(true)
      setError(null)
    }

    ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data)

        if (message.type === 'frame') {
          setFrame(message.data)
        } else if (message.type === 'alert') {
          console.log('Alert received:', message)
          // You can handle alerts here (e.g., show toast notification)
        } else if (message.type === 'error') {
          setError(message.message)
        }
      } catch (err) {
        console.error('Error parsing WebSocket message:', err)
      }
    }

    ws.onerror = (event) => {
      console.error('WebSocket error:', event)
      setError('WebSocket connection error')
    }

    ws.onclose = () => {
      console.log('WebSocket disconnected')
      setIsConnected(false)
    }

    wsRef.current = ws

    return () => {
      if (wsRef.current) {
        wsRef.current.close()
      }
    }
  }, [cameraId, token])

  return { frame, isConnected, error }
}
