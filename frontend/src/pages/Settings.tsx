import { useMutation } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import api from '@/lib/api'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import Navigation from '@/components/Navigation'
import { Download, FileText } from 'lucide-react'

export default function Settings() {
  const exportData = useMutation({
    mutationFn: async (format: 'json' | 'csv') => {
      const response = await api.get(`/export/data?format=${format}&days=90`, {
        responseType: format === 'csv' ? 'blob' : 'json',
      })
      
      if (format === 'csv') {
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `nocolon_export_${new Date().toISOString().split('T')[0]}.csv`)
        document.body.appendChild(link)
        link.click()
        link.remove()
        window.URL.revokeObjectURL(url)
      } else {
        const dataStr = JSON.stringify(response.data, null, 2)
        const dataBlob = new Blob([dataStr], { type: 'application/json' })
        const url = window.URL.createObjectURL(dataBlob)
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `nocolon_export_${new Date().toISOString().split('T')[0]}.json`)
        document.body.appendChild(link)
        link.click()
        link.remove()
        window.URL.revokeObjectURL(url)
      }
    },
  })
  
  const exportReport = useMutation({
    mutationFn: async () => {
      const response = await api.get('/export/complete-report')
      const dataStr = JSON.stringify(response.data, null, 2)
      const dataBlob = new Blob([dataStr], { type: 'application/json' })
      const url = window.URL.createObjectURL(dataBlob)
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `nocolon_report_${new Date().toISOString().split('T')[0]}.json`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
    },
  })

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      <Navigation />
      
      <div className="container mx-auto px-4 py-8">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
            Settings & Export
          </h1>
          <p className="text-muted-foreground mt-2">
            Manage your account and export your data
          </p>
        </motion.div>

        {/* Export Data */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-6"
        >
          <Card className="shadow-lg border-0">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Download size={20} />
                Export Your Data
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-sm text-muted-foreground">
                Download your complete health data for analysis or sharing with healthcare providers.
              </p>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Button
                  variant="outline"
                  onClick={() => exportData.mutate('json')}
                  disabled={exportData.isPending}
                  className="flex items-center gap-2"
                >
                  <FileText size={18} />
                  Export JSON
                </Button>
                
                <Button
                  variant="outline"
                  onClick={() => exportData.mutate('csv')}
                  disabled={exportData.isPending}
                  className="flex items-center gap-2"
                >
                  <FileText size={18} />
                  Export CSV
                </Button>
                
                <Button
                  onClick={() => exportReport.mutate()}
                  disabled={exportReport.isPending}
                  className="flex items-center gap-2"
                >
                  <FileText size={18} />
                  Complete Report
                </Button>
              </div>
              
              {exportData.isSuccess && (
                <p className="text-sm text-green-600">
                  ✓ Export downloaded successfully
                </p>
              )}
            </CardContent>
          </Card>
        </motion.div>

        {/* Account Settings */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <Card className="shadow-lg border-0">
            <CardHeader>
              <CardTitle>Account Settings</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">
                Account management features coming soon...
              </p>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </div>
  )
}

