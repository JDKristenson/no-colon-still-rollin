import { useQuery } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import api from '@/lib/api'
import { Button } from './ui/button'
import { Download, Check } from 'lucide-react'
import { useState } from 'react'

interface GroceryListProps {
  protocol: any
}

interface GroceryListItem {
  name: string
  amount: string
  category: string
  notes: string
}

interface GroceryListData {
  date: string
  items: GroceryListItem[]
  grouped: Record<string, GroceryListItem[]>
  total_items: number
}

export default function GroceryList({ protocol }: GroceryListProps) {
  const [downloaded, setDownloaded] = useState(false)
  
  const { data: groceryList, isLoading, error: queryError } = useQuery<GroceryListData>({
    queryKey: ['grocery-list', protocol?.id],
    queryFn: async () => {
      const response = await api.get('/protocol/grocery-list')
      return response.data as GroceryListData
    },
    enabled: !!protocol,
    retry: 1,
  })

  // Extract error message safely
  const errorMessage = queryError 
    ? ((queryError as any)?.response?.data?.detail || (queryError as any)?.message || 'Failed to load grocery list')
    : null

  const handleDownload = () => {
    if (!groceryList) return
    
    // Create text content
    let content = "No Colon, Still Rollin' - Grocery List\n"
    content += "=".repeat(40) + "\n\n"
    content += `Date: ${new Date(groceryList.date).toLocaleDateString()}\n\n`
    
    if (groceryList.grouped) {
      Object.entries(groceryList.grouped).forEach(([category, items]: [string, any]) => {
        content += `${category}:\n`
        items.forEach((item: any) => {
          content += `  • ${item.name} - ${item.amount}`
          if (item.notes) {
            content += ` (${item.notes.substring(0, 50)})`
          }
          content += "\n"
        })
        content += "\n"
      })
    }
    
    // Create blob and download
    const blob = new Blob([content], { type: 'text/plain' })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `grocery-list-${new Date().toISOString().split('T')[0]}.txt`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    
    setDownloaded(true)
    setTimeout(() => setDownloaded(false), 2000)
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    )
  }

  if (errorMessage) {
    return (
      <div className="text-center py-4">
        <p className="text-sm text-red-600 mb-2">
          {errorMessage}
        </p>
        <p className="text-xs text-muted-foreground">
          Generate a protocol first to create your shopping list
        </p>
      </div>
    )
  }

  if (!groceryList || !groceryList.items || groceryList.items.length === 0) {
    return (
      <div className="text-center py-4">
        <p className="text-sm text-muted-foreground">
          Generate a protocol to create your shopping list
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-gray-700">
          {groceryList.total_items} items
        </span>
        <Button
          variant="outline"
          size="sm"
          onClick={handleDownload}
          className="flex items-center gap-2"
        >
          {downloaded ? (
            <>
              <Check size={16} />
              Downloaded!
            </>
          ) : (
            <>
              <Download size={16} />
              Download
            </>
          )}
        </Button>
      </div>
      
      <div className="space-y-4 max-h-96 overflow-y-auto">
        {groceryList.grouped && Object.entries(groceryList.grouped).map(([category, items]: [string, any], idx) => (
          <motion.div
            key={category}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.1 }}
          >
            <div className="border-b border-gray-200 pb-2 mb-2">
              <h4 className="font-semibold text-gray-800">{category}</h4>
            </div>
            <div className="space-y-2">
              {items.map((item: any, itemIdx: number) => (
                <motion.div
                  key={itemIdx}
                  className="flex items-start justify-between p-2 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <div className="w-1.5 h-1.5 rounded-full bg-blue-600" />
                      <span className="font-medium text-sm">{item.name}</span>
                    </div>
                    <div className="ml-4 mt-1">
                      <span className="text-xs text-blue-600 font-medium">{item.amount}</span>
                      {item.notes && (
                        <p className="text-xs text-gray-500 mt-1">{item.notes.substring(0, 60)}</p>
                      )}
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  )
}

