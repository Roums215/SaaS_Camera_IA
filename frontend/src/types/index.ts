export interface User {
  id: number
  email: string
  username: string
  full_name?: string
  is_active: boolean
  is_superuser: boolean
  role: 'admin' | 'user' | 'viewer'
  created_at: string
  last_login?: string
}

export interface Camera {
  id: number
  name: string
  description?: string
  source: string
  source_type: 'webcam' | 'rtsp' | 'http' | 'file'
  is_active: boolean
  fps: number
  resolution_width: number
  resolution_height: number
  detection_enabled: boolean
  confidence_threshold: number
  alert_cooldown_seconds: number
  owner_id: number
  created_at: string
  updated_at?: string
  last_detection?: string
}

export interface Detection {
  id: number
  camera_id: number
  detection_type: string
  confidence: number
  bbox_x1?: number
  bbox_y1?: number
  bbox_x2?: number
  bbox_y2?: number
  metadata?: Record<string, any>
  image_path?: string
  video_path?: string
  is_false_positive: boolean
  reviewed: boolean
  created_at: string
}

export interface Alert {
  id: number
  detection_id: number
  user_id: number
  title: string
  message: string
  severity: 'low' | 'medium' | 'high' | 'critical'
  status: 'pending' | 'acknowledged' | 'resolved' | 'false_alarm'
  notified: boolean
  notification_sent_at?: string
  created_at: string
  acknowledged_at?: string
  resolved_at?: string
}

export interface LoginCredentials {
  username: string
  password: string
}

export interface RegisterData {
  email: string
  username: string
  password: string
  full_name?: string
}

export interface CameraStats {
  camera_id: number
  total_detections: number
  detections_today: number
  last_detection?: string
  average_confidence?: number
}

export interface DetectionFrame {
  camera_id: number
  frame_data: string
  detections: Array<{
    bbox: {
      x1: number
      y1: number
      x2: number
      y2: number
    }
    confidence: number
    class_id: number
    class_name: string
    detection_type: string
  }>
  timestamp: string
  has_suspicious_activity: boolean
}
