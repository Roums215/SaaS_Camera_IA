import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { detectionService } from '../services/detectionService'
import { format } from 'date-fns'
import { Filter } from 'lucide-react'

export default function DetectionsPage() {
  const [minConfidence, setMinConfidence] = useState<number>(0)
  const [cameraFilter, setCameraFilter] = useState<string>('')

  const { data: detections, isLoading } = useQuery({
    queryKey: ['detections', minConfidence, cameraFilter],
    queryFn: () => detectionService.getDetections({
      min_confidence: minConfidence > 0 ? minConfidence / 100 : undefined,
      camera_id: cameraFilter ? parseInt(cameraFilter) : undefined,
    }),
  })

  return (
    <div className="px-4 py-6 sm:px-0">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Detections</h1>
        <p className="mt-2 text-sm text-gray-600">
          Review all detection events from your cameras
        </p>
      </div>

      {/* Filters */}
      <div className="card mb-6">
        <div className="flex items-center space-x-4">
          <Filter className="h-5 w-5 text-gray-400" />
          <div className="flex-1 grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Min Confidence
              </label>
              <input
                type="range"
                min="0"
                max="100"
                value={minConfidence}
                onChange={(e) => setMinConfidence(parseInt(e.target.value))}
                className="w-full"
              />
              <span className="text-sm text-gray-500">{minConfidence}%</span>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Camera ID (Optional)
              </label>
              <input
                type="text"
                value={cameraFilter}
                onChange={(e) => setCameraFilter(e.target.value)}
                placeholder="Enter camera ID"
                className="input"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Detections List */}
      {isLoading ? (
        <div className="text-center py-12">
          <p className="text-gray-500">Loading detections...</p>
        </div>
      ) : detections && detections.length > 0 ? (
        <div className="card overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  ID
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Camera
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Type
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Confidence
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Time
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {detections.map((detection) => (
                <tr key={detection.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    #{detection.id}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    Camera {detection.camera_id}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {detection.detection_type}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    <span
                      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        detection.confidence > 0.8
                          ? 'bg-green-100 text-green-800'
                          : detection.confidence > 0.5
                          ? 'bg-yellow-100 text-yellow-800'
                          : 'bg-red-100 text-red-800'
                      }`}
                    >
                      {(detection.confidence * 100).toFixed(1)}%
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    {detection.is_false_positive ? (
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                        False Positive
                      </span>
                    ) : detection.reviewed ? (
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                        Reviewed
                      </span>
                    ) : (
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                        Pending
                      </span>
                    )}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {format(new Date(detection.created_at), 'MMM d, yyyy HH:mm')}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="text-center py-12 card">
          <p className="text-gray-500">No detections found</p>
        </div>
      )}
    </div>
  )
}
