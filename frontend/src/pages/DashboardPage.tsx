import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { Plus, Play, Square, Trash2, Edit } from 'lucide-react'
import toast from 'react-hot-toast'
import { cameraService } from '../services/cameraService'
import { detectionService } from '../services/detectionService'
import { Camera } from '../types'

export default function DashboardPage() {
  const [showAddModal, setShowAddModal] = useState(false)
  const navigate = useNavigate()
  const queryClient = useQueryClient()

  const { data: cameras, isLoading } = useQuery({
    queryKey: ['cameras'],
    queryFn: cameraService.getCameras,
  })

  const { data: stats } = useQuery({
    queryKey: ['detection-stats'],
    queryFn: () => detectionService.getDetectionStats(7),
  })

  const startCameraMutation = useMutation({
    mutationFn: cameraService.startCamera,
    onSuccess: () => {
      toast.success('Camera started')
      queryClient.invalidateQueries({ queryKey: ['cameras'] })
    },
    onError: () => toast.error('Failed to start camera'),
  })

  const stopCameraMutation = useMutation({
    mutationFn: cameraService.stopCamera,
    onSuccess: () => {
      toast.success('Camera stopped')
      queryClient.invalidateQueries({ queryKey: ['cameras'] })
    },
    onError: () => toast.error('Failed to stop camera'),
  })

  const deleteCameraMutation = useMutation({
    mutationFn: cameraService.deleteCamera,
    onSuccess: () => {
      toast.success('Camera deleted')
      queryClient.invalidateQueries({ queryKey: ['cameras'] })
    },
    onError: () => toast.error('Failed to delete camera'),
  })

  return (
    <div className="px-4 py-6 sm:px-0">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-2 text-sm text-gray-600">
          Monitor and manage your AI-powered security cameras
        </p>
      </div>

      {/* Stats */}
      {stats && (
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-4 mb-8">
          <div className="card">
            <h3 className="text-sm font-medium text-gray-500">Total Detections (7d)</h3>
            <p className="mt-2 text-3xl font-bold text-gray-900">{stats.total_detections}</p>
          </div>
          <div className="card">
            <h3 className="text-sm font-medium text-gray-500">Average Confidence</h3>
            <p className="mt-2 text-3xl font-bold text-gray-900">
              {(stats.average_confidence * 100).toFixed(1)}%
            </p>
          </div>
          <div className="card">
            <h3 className="text-sm font-medium text-gray-500">False Positives</h3>
            <p className="mt-2 text-3xl font-bold text-gray-900">{stats.false_positives}</p>
          </div>
          <div className="card">
            <h3 className="text-sm font-medium text-gray-500">Active Cameras</h3>
            <p className="mt-2 text-3xl font-bold text-gray-900">
              {cameras?.filter((c) => c.is_active).length || 0}
            </p>
          </div>
        </div>
      )}

      {/* Cameras List */}
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Cameras</h2>
        <button
          onClick={() => setShowAddModal(true)}
          className="btn btn-primary inline-flex items-center"
        >
          <Plus className="h-5 w-5 mr-2" />
          Add Camera
        </button>
      </div>

      {isLoading ? (
        <div className="text-center py-12">
          <p className="text-gray-500">Loading cameras...</p>
        </div>
      ) : cameras && cameras.length > 0 ? (
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {cameras.map((camera) => (
            <div key={camera.id} className="card hover:shadow-lg transition-shadow">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">{camera.name}</h3>
                  <p className="text-sm text-gray-500">{camera.source_type}</p>
                </div>
                <span
                  className={`px-2 py-1 text-xs rounded-full ${
                    camera.is_active
                      ? 'bg-green-100 text-green-800'
                      : 'bg-gray-100 text-gray-800'
                  }`}
                >
                  {camera.is_active ? 'Active' : 'Inactive'}
                </span>
              </div>

              {camera.description && (
                <p className="text-sm text-gray-600 mb-4">{camera.description}</p>
              )}

              <div className="flex items-center justify-between pt-4 border-t border-gray-200">
                <button
                  onClick={() => navigate(`/camera/${camera.id}`)}
                  className="text-sm text-primary-600 hover:text-primary-700 font-medium"
                >
                  View Stream
                </button>

                <div className="flex space-x-2">
                  {camera.is_active ? (
                    <button
                      onClick={() => stopCameraMutation.mutate(camera.id)}
                      className="p-2 text-gray-400 hover:text-red-600"
                      title="Stop"
                    >
                      <Square className="h-4 w-4" />
                    </button>
                  ) : (
                    <button
                      onClick={() => startCameraMutation.mutate(camera.id)}
                      className="p-2 text-gray-400 hover:text-green-600"
                      title="Start"
                    >
                      <Play className="h-4 w-4" />
                    </button>
                  )}
                  <button
                    onClick={() => {
                      if (confirm('Are you sure you want to delete this camera?')) {
                        deleteCameraMutation.mutate(camera.id)
                      }
                    }}
                    className="p-2 text-gray-400 hover:text-red-600"
                    title="Delete"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-12 card">
          <p className="text-gray-500">No cameras found. Add your first camera to get started!</p>
        </div>
      )}

      {/* Add Camera Modal */}
      {showAddModal && (
        <AddCameraModal onClose={() => setShowAddModal(false)} />
      )}
    </div>
  )
}

// Simple Add Camera Modal Component
function AddCameraModal({ onClose }: { onClose: () => void }) {
  const [name, setName] = useState('')
  const [source, setSource] = useState('0')
  const [sourceType, setSourceType] = useState<'webcam' | 'rtsp' | 'http' | 'file'>('webcam')
  const queryClient = useQueryClient()

  const createMutation = useMutation({
    mutationFn: cameraService.createCamera,
    onSuccess: () => {
      toast.success('Camera added successfully')
      queryClient.invalidateQueries({ queryKey: ['cameras'] })
      onClose()
    },
    onError: () => toast.error('Failed to add camera'),
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    createMutation.mutate({ name, source, source_type: sourceType })
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 max-w-md w-full">
        <h2 className="text-2xl font-bold mb-4">Add New Camera</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Camera Name</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="input mt-1"
              required
              placeholder="e.g., Front Door Camera"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Source Type</label>
            <select
              value={sourceType}
              onChange={(e) => setSourceType(e.target.value as any)}
              className="input mt-1"
            >
              <option value="webcam">Webcam</option>
              <option value="rtsp">RTSP Stream</option>
              <option value="http">HTTP Stream</option>
              <option value="file">File</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Source</label>
            <input
              type="text"
              value={source}
              onChange={(e) => setSource(e.target.value)}
              className="input mt-1"
              required
              placeholder={sourceType === 'webcam' ? '0' : 'rtsp://...'}
            />
            <p className="mt-1 text-xs text-gray-500">
              {sourceType === 'webcam' ? 'Enter device index (e.g., 0 for default webcam)' : 'Enter stream URL'}
            </p>
          </div>

          <div className="flex justify-end space-x-2 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="btn btn-secondary"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={createMutation.isPending}
              className="btn btn-primary"
            >
              {createMutation.isPending ? 'Adding...' : 'Add Camera'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
