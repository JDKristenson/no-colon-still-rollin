import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import api from '@/lib/api'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Upload, X, CheckCircle2, AlertCircle, FileText } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'

interface MarkerUploadProps {
  onSuccess?: () => void
}

export default function MarkerUpload({ onSuccess }: MarkerUploadProps) {
  const [file, setFile] = useState<File | null>(null)
  const [dragActive, setDragActive] = useState(false)

  const uploadMutation = useMutation({
    mutationFn: async (file: File) => {
      const formData = new FormData()
      formData.append('file', file)
      const response = await api.post('/genetics/upload-test', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      return response.data
    },
    onSuccess: (data) => {
      setFile(null)
      if (onSuccess) onSuccess()
    },
  })

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const droppedFile = e.dataTransfer.files[0]
      if (droppedFile.name.endsWith('.xlsx') || droppedFile.name.endsWith('.xls')) {
        setFile(droppedFile)
      }
    }
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
    }
  }

  const handleUpload = () => {
    if (file) {
      uploadMutation.mutate(file)
    }
  }

  return (
    <Card className="border-2 border-dashed border-blue-300 bg-gradient-to-br from-blue-50 to-indigo-50">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Upload size={20} />
          Upload Signatera Test Result
        </CardTitle>
      </CardHeader>
      <CardContent>
        <AnimatePresence mode="wait">
          {!file && !uploadMutation.isSuccess && (
            <motion.div
              key="upload-area"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
              className={`border-2 border-dashed rounded-lg p-12 text-center transition-colors ${
                dragActive
                  ? 'border-blue-500 bg-blue-100'
                  : 'border-gray-300 bg-white'
              }`}
            >
              <Upload size={48} className="mx-auto text-gray-400 mb-4" />
              <p className="text-lg font-medium mb-2">
                Drag and drop your Excel file here
              </p>
              <p className="text-sm text-muted-foreground mb-4">
                or click to browse (Signatera .xlsx format)
              </p>
              <input
                type="file"
                id="file-upload"
                accept=".xlsx,.xls"
                onChange={handleFileChange}
                className="hidden"
              />
              <label htmlFor="file-upload">
                <Button as="span" variant="outline">
                  Select File
                </Button>
              </label>
            </motion.div>
          )}

          {file && !uploadMutation.isSuccess && (
            <motion.div
              key="file-selected"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="space-y-4"
            >
              <div className="flex items-center justify-between p-4 bg-white rounded-lg border">
                <div className="flex items-center gap-3">
                  <FileText className="text-blue-600" size={24} />
                  <div>
                    <p className="font-medium">{file.name}</p>
                    <p className="text-sm text-muted-foreground">
                      {(file.size / 1024).toFixed(1)} KB
                    </p>
                  </div>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setFile(null)}
                  disabled={uploadMutation.isPending}
                >
                  <X size={20} />
                </Button>
              </div>

              {uploadMutation.isError && (
                <div className="flex items-center gap-2 p-3 bg-red-50 text-red-700 rounded-lg">
                  <AlertCircle size={20} />
                  <span className="text-sm">
                    {uploadMutation.error instanceof Error
                      ? uploadMutation.error.message
                      : 'Upload failed'}
                  </span>
                </div>
              )}

              <Button
                onClick={handleUpload}
                disabled={uploadMutation.isPending}
                className="w-full"
                size="lg"
              >
                {uploadMutation.isPending ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2" />
                    Uploading...
                  </>
                ) : (
                  <>
                    <Upload size={20} className="mr-2" />
                    Upload Test Result
                  </>
                )}
              </Button>
            </motion.div>
          )}

          {uploadMutation.isSuccess && (
            <motion.div
              key="success"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              className="text-center py-8"
            >
              <CheckCircle2 className="mx-auto text-green-600 mb-4" size={48} />
              <h3 className="text-lg font-semibold mb-2">Upload Successful!</h3>
              <p className="text-sm text-muted-foreground mb-4">
                Processed {uploadMutation.data.markers_processed} markers
                {uploadMutation.data.markers_detected > 0 && (
                  <span className="text-red-600 font-medium ml-2">
                    • {uploadMutation.data.markers_detected} detected
                  </span>
                )}
              </p>
            </motion.div>
          )}
        </AnimatePresence>
      </CardContent>
    </Card>
  )
}

