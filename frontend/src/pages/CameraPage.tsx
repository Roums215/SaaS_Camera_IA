import { useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { AlertTriangle, Activity } from 'lucide-react'
import { cameraService } from '../services/cameraService'
import { useWebSocket } from '../hooks/useWebSocket'

export default function CameraPage() {
  const { id } = useParams<{ id: string }>()
  const cameraId = parseInt(id!)

  const { data: camera, isLoading } = useQuery({
    queryKey: ['camera', cameraId],
    queryFn: () => cameraService.getCamera(cameraId),
  })

  const { data: stats } = useQuery({
    queryKey: ['camera-stats', cameraId],
    queryFn: () => cameraService.getCameraStats(cameraId),
    refetchInterval: 10000,
  })

  const { frame, isConnected, error } = useWebSocket(cameraId)

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <p className="text-gray-500">Loading camera...</p>
      </div>
    )
  }

  if (!camera) {
    return (
      <div className="flex items-center justify-center h-96">
        <p className="text-gray-500">Camera not found</p>
      </div>
    )
  }

  return (
    <div className="px-4 py-6 sm:px-0">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">{camera.name}</h1>
        <p className="mt-2 text-sm text-gray-600">{camera.description}</p>
      </div>

      {/* Connection Status */}
      <div className="mb-4 flex items-center space-x-2">
        <div
          className={`h-3 w-3 rounded-full ${
            isConnected ? 'bg-green-500' : 'bg-red-500'
          }`}
        />
        <span className="text-sm font-medium">
          {isConnected ? 'Connected' : 'Disconnected'}
        </span>
      </div>

      {error && (
        <div className="mb-4 bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-sm text-red-800">{error}</p>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Video Stream */}
        <div className="lg:col-span-2">
          <div className="card">
            <h2 className="text-xl font-bold mb-4">Live Stream</h2>
            <div className="relative bg-black rounded-lg overflow-hidden" style={{ paddingBottom: '56.25%' }}>
              {frame ? (
                <>
                  <img
                    src={`data:image/jpeg;base64,${frame.frame_data}`}
                    alt="Camera feed"
                    className="absolute inset-0 w-full h-full object-contain"
                  />
                  {frame.has_suspicious_activity && (
                    <div className="absolute top-4 left-4 bg-red-600 text-white px-4 py-2 rounded-lg flex items-center space-x-2 animate-pulse">
                      <AlertTriangle className="h-5 w-5" />
                      <span className="font-bold">SUSPICIOUS ACTIVITY DETECTED</span>
                    </div>
                  )}
                  {frame.detections.length > 0 && (
                    <div className="absolute top-4 right-4 bg-black bg-opacity-75 text-white px-3 py-2 rounded-lg">
                      <p className="text-sm font-medium">
                        {frame.detections.length} detection(s)
                      </p>
                    </div>
                  )}
                </>
              ) : (
                <div className="absolute inset-0 flex items-center justify-center text-white">
                  <p>Waiting for stream...</p>
                </div>
              )}
            </div>
          </div>

          {/* Detections */}
          {frame && frame.detections.length > 0 && (
            <div className="mt-6 card">
              <h3 className="text-lg font-bold mb-4">Current Detections</h3>
              <div className="space-y-2">
                {frame.detections.map((detection, idx) => (
                  <div
                    key={idx}
                    className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                  >
                    <div>
                      <p className="font-medium">{detection.class_name}</p>
                      <p className="text-sm text-gray-500">
                        {detection.detection_type}
                      </p>
                    </div>
                    <span className="text-sm font-medium text-primary-600">
                      {(detection.confidence * 100).toFixed(1)}%
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Stats & Info */}
        <div className="space-y-6">
          {/* Camera Info */}
          <div className="card">
            <h3 className="text-lg font-bold mb-4">Camera Information</h3>
            <dl className="space-y-2 text-sm">
              <div>
                <dt className="text-gray-500">Status</dt>
                <dd className="font-medium">
                  {camera.is_active ? 'Active' : 'Inactive'}
                </dd>
              </div>
              <div>
                <dt className="text-gray-500">Source Type</dt>
                <dd className="font-medium">{camera.source_type}</dd>
              </div>
              <div>
                <dt className="text-gray-500">Resolution</dt>
                <dd className="font-medium">
                  {camera.resolution_width}x{camera.resolution_height}
                </dd>
              </div>
              <div>
                <dt className="text-gray-500">FPS</dt>
                <dd className="font-medium">{camera.fps}</dd>
              </div>
              <div>
                <dt className="text-gray-500">Confidence Threshold</dt>
                <dd className="font-medium">
                  {(camera.confidence_threshold * 100).toFixed(0)}%
                </dd>
              </div>
            </dl>
          </div>

          {/* Statistics */}
          {stats && (
            <div className="card">
              <h3 className="text-lg font-bold mb-4 flex items-center">
                <Activity className="h-5 w-5 mr-2" />
                Statistics
              </h3>
              <dl className="space-y-3">
                <div>
                  <dt className="text-sm text-gray-500">Total Detections</dt>
                  <dd className="text-2xl font-bold text-gray-900">
                    {stats.total_detections}
                  </dd>
                </div>
                <div>
                  <dt className="text-sm text-gray-500">Detections Today</dt>
                  <dd className="text-2xl font-bold text-gray-900">
                    {stats.detections_today}
                  </dd>
                </div>
                {stats.average_confidence && (
                  <div>
                    <dt className="text-sm text-gray-500">Avg. Confidence</dt>
                    <dd className="text-2xl font-bold text-gray-900">
                      {(stats.average_confidence * 100).toFixed(1)}%
                    </dd>
                  </div>
                )}
              </dl>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
