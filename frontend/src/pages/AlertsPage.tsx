import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { alertService } from '../services/alertService'
import { format } from 'date-fns'
import { CheckCircle, XCircle } from 'lucide-react'
import toast from 'react-hot-toast'

export default function AlertsPage() {
  const queryClient = useQueryClient()

  const { data: alerts, isLoading } = useQuery({
    queryKey: ['alerts'],
    queryFn: () => alertService.getAlerts(),
  })

  const acknowledgeMutation = useMutation({
    mutationFn: alertService.acknowledgeAlert,
    onSuccess: () => {
      toast.success('Alert acknowledged')
      queryClient.invalidateQueries({ queryKey: ['alerts'] })
    },
  })

  const resolveMutation = useMutation({
    mutationFn: alertService.resolveAlert,
    onSuccess: () => {
      toast.success('Alert resolved')
      queryClient.invalidateQueries({ queryKey: ['alerts'] })
    },
  })

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'bg-red-100 text-red-800 border-red-200'
      case 'high':
        return 'bg-orange-100 text-orange-800 border-orange-200'
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200'
      case 'low':
        return 'bg-blue-100 text-blue-800 border-blue-200'
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200'
    }
  }

  return (
    <div className="px-4 py-6 sm:px-0">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Alerts</h1>
        <p className="mt-2 text-sm text-gray-600">
          Manage and respond to security alerts
        </p>
      </div>

      {isLoading ? (
        <div className="text-center py-12">
          <p className="text-gray-500">Loading alerts...</p>
        </div>
      ) : alerts && alerts.length > 0 ? (
        <div className="space-y-4">
          {alerts.map((alert) => (
            <div
              key={alert.id}
              className={`card border-l-4 ${
                alert.severity === 'critical' || alert.severity === 'high'
                  ? 'border-red-500'
                  : alert.severity === 'medium'
                  ? 'border-yellow-500'
                  : 'border-blue-500'
              }`}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-2">
                    <span
                      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium uppercase ${getSeverityColor(
                        alert.severity
                      )}`}
                    >
                      {alert.severity}
                    </span>
                    <span
                      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        alert.status === 'pending'
                          ? 'bg-yellow-100 text-yellow-800'
                          : alert.status === 'acknowledged'
                          ? 'bg-blue-100 text-blue-800'
                          : alert.status === 'resolved'
                          ? 'bg-green-100 text-green-800'
                          : 'bg-gray-100 text-gray-800'
                      }`}
                    >
                      {alert.status}
                    </span>
                  </div>

                  <h3 className="text-lg font-semibold text-gray-900 mb-1">
                    {alert.title}
                  </h3>
                  <p className="text-sm text-gray-600 mb-3">{alert.message}</p>

                  <div className="flex items-center space-x-4 text-xs text-gray-500">
                    <span>
                      Created: {format(new Date(alert.created_at), 'MMM d, yyyy HH:mm')}
                    </span>
                    {alert.acknowledged_at && (
                      <span>
                        Acknowledged:{' '}
                        {format(new Date(alert.acknowledged_at), 'MMM d, yyyy HH:mm')}
                      </span>
                    )}
                    {alert.resolved_at && (
                      <span>
                        Resolved: {format(new Date(alert.resolved_at), 'MMM d, yyyy HH:mm')}
                      </span>
                    )}
                  </div>
                </div>

                <div className="flex space-x-2 ml-4">
                  {alert.status === 'pending' && (
                    <button
                      onClick={() => acknowledgeMutation.mutate(alert.id)}
                      disabled={acknowledgeMutation.isPending}
                      className="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none disabled:opacity-50"
                      title="Acknowledge"
                    >
                      <CheckCircle className="h-4 w-4 mr-1" />
                      Acknowledge
                    </button>
                  )}

                  {(alert.status === 'pending' || alert.status === 'acknowledged') && (
                    <button
                      onClick={() => resolveMutation.mutate(alert.id)}
                      disabled={resolveMutation.isPending}
                      className="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none disabled:opacity-50"
                      title="Resolve"
                    >
                      <XCircle className="h-4 w-4 mr-1" />
                      Resolve
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-12 card">
          <p className="text-gray-500">No alerts found</p>
        </div>
      )}
    </div>
  )
}
