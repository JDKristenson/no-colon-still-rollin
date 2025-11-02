import { useQuery, useQueryClient } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import api from '@/lib/api'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import Navigation from '@/components/Navigation'
import { Upload, Circle, AlertCircle, Calendar, FileText, Dna } from 'lucide-react'
import { useState } from 'react'
import MarkerUpload from '@/components/MarkerUpload'

export default function Markers() {
  const queryClient = useQueryClient()
  const [showUpload, setShowUpload] = useState(false)
  
  const { data: markersData, isLoading } = useQuery({
    queryKey: ['genetic-markers'],
    queryFn: async () => {
      const response = await api.get('/genetics/markers')
      return response.data
    },
  })
  
  const { data: activeMarkers } = useQuery({
    queryKey: ['active-markers'],
    queryFn: async () => {
      const response = await api.get('/genetics/markers/active')
      return response.data
    },
  })
  
  const { data: testsData } = useQuery({
    queryKey: ['genetic-tests'],
    queryFn: async () => {
      const response = await api.get('/genetics/tests')
      return response.data
    },
  })

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
        <Navigation />
        <div className="flex items-center justify-center min-h-[80vh]">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
        </div>
      </div>
    )
  }

  const markers = markersData?.markers || []
  const activeMarkerIds = new Set((activeMarkers?.markers || []).map((m: any) => m.id))
  const tests = testsData?.tests || []

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      <Navigation />
      
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent mb-2">
                Genetic Markers
              </h1>
              <p className="text-muted-foreground">
                Track your Signatera ctDNA test results and monitor detected mutations
              </p>
            </div>
            <Button onClick={() => setShowUpload(!showUpload)} size="lg" className="gap-2">
              <Upload size={20} />
              Upload Test Result
            </Button>
          </div>
        </motion.div>

        {/* Upload Section */}
        {showUpload && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="mb-8"
          >
            <MarkerUpload onSuccess={() => {
              setShowUpload(false)
              queryClient.invalidateQueries({ queryKey: ['genetic-markers'] })
              queryClient.invalidateQueries({ queryKey: ['active-markers'] })
              queryClient.invalidateQueries({ queryKey: ['genetic-tests'] })
            }} />
          </motion.div>
        )}

        {/* Active Markers Alert */}
        {activeMarkerIds.size > 0 && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-6"
          >
            <Card className="bg-gradient-to-r from-red-50 to-orange-50 border-red-200 shadow-lg">
              <CardContent className="pt-6">
                <div className="flex items-center gap-3">
                  <AlertCircle className="text-red-600" size={24} />
                  <div>
                    <h3 className="font-semibold text-red-900">
                      {activeMarkerIds.size} Active Mutation{activeMarkerIds.size !== 1 ? 's' : ''} Detected
                    </h3>
                    <p className="text-sm text-red-700 mt-1">
                      Your protocol is being prioritized to target these mutations
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card className="shadow-lg border-0 bg-gradient-to-br from-white to-blue-50">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground mb-1">Baseline Markers</p>
                  <p className="text-3xl font-bold text-blue-600">{markers.length}</p>
                </div>
                <Dna className="text-blue-600" size={32} />
              </div>
            </CardContent>
          </Card>

          <Card className="shadow-lg border-0 bg-gradient-to-br from-white to-red-50">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground mb-1">Active Mutations</p>
                  <p className="text-3xl font-bold text-red-600">{activeMarkerIds.size}</p>
                </div>
                <AlertCircle className="text-red-600" size={32} />
              </div>
            </CardContent>
          </Card>

          <Card className="shadow-lg border-0 bg-gradient-to-br from-white to-purple-50">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground mb-1">Test Results</p>
                  <p className="text-3xl font-bold text-purple-600">{tests.length}</p>
                </div>
                <FileText className="text-purple-600" size={32} />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Markers Table */}
        <Card className="shadow-lg border-0 mb-8">
          <CardHeader>
            <CardTitle>All Baseline Markers</CardTitle>
            <CardDescription>
              All 16 markers monitored by Signatera ctDNA testing
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b">
                    <th className="text-left p-3 font-semibold">Target ID</th>
                    <th className="text-left p-3 font-semibold">Chromosome</th>
                    <th className="text-left p-3 font-semibold">Position</th>
                    <th className="text-left p-3 font-semibold">Variant</th>
                    <th className="text-left p-3 font-semibold">Type</th>
                    <th className="text-left p-3 font-semibold">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {markers.map((marker: any) => {
                    const isActive = activeMarkerIds.has(marker.id)
                    return (
                      <motion.tr
                        key={marker.id}
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className={`border-b hover:bg-gray-50 ${isActive ? 'bg-red-50' : ''}`}
                      >
                        <td className="p-3 font-mono text-sm">{marker.target_id}</td>
                        <td className="p-3">{marker.chromosome}</td>
                        <td className="p-3 font-mono text-sm">{marker.position.toLocaleString()}</td>
                        <td className="p-3">
                          <span className="font-mono">
                            {marker.ref_base} → {marker.mut_base}
                          </span>
                        </td>
                        <td className="p-3">
                          <span className="px-2 py-1 bg-gray-100 rounded text-xs">
                            {marker.variant_type}
                          </span>
                        </td>
                        <td className="p-3">
                          {isActive ? (
                            <div className="flex items-center gap-2 text-red-600">
                              <div className="w-3 h-3 rounded-full bg-red-500 animate-pulse" />
                              <span className="font-medium">Active</span>
                            </div>
                          ) : (
                            <div className="flex items-center gap-2 text-gray-400">
                              <Circle size={16} />
                              <span>Baseline</span>
                            </div>
                          )}
                        </td>
                      </motion.tr>
                    )
                  })}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>

        {/* Test History */}
        {tests.length > 0 && (
          <Card className="shadow-lg border-0">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Calendar size={20} />
                Test History
              </CardTitle>
              <CardDescription>
                Chronological record of all ctDNA test results
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {tests.map((test: any) => (
                  <motion.div
                    key={test.id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    className="p-4 border rounded-lg hover:bg-gray-50 transition-colors"
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="font-semibold">
                          {new Date(test.test_date).toLocaleDateString('en-US', {
                            year: 'numeric',
                            month: 'long',
                            day: 'numeric'
                          })}
                        </p>
                        <p className="text-sm text-muted-foreground mt-1">
                          {test.test_lab} • {test.detected_count} marker(s) detected
                          {test.result_file_name && ` • ${test.result_file_name}`}
                        </p>
                      </div>
                      {test.detected_count > 0 && (
                        <div className="flex items-center gap-2 text-red-600">
                          <AlertCircle size={20} />
                          <span className="font-medium">{test.detected_count} Active</span>
                        </div>
                      )}
                    </div>
                  </motion.div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}

