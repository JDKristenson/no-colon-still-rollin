import { useQuery } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import api from '@/lib/api'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import Navigation from '@/components/Navigation'
import { Search, ExternalLink, BookOpen } from 'lucide-react'
import { useState } from 'react'

export default function Research() {
  const [searchQuery, setSearchQuery] = useState('')
  const [activeTab, setActiveTab] = useState<'nutrition' | 'glutamine' | 'exercise'>('nutrition')
  
  const { data: studies, isLoading } = useQuery({
    queryKey: ['research', activeTab],
    queryFn: async () => {
      const endpoint = activeTab === 'nutrition' ? '/research/nutrition' :
                      activeTab === 'glutamine' ? '/research/glutamine' :
                      '/research/exercise-cancer'
      const response = await api.get(endpoint)
      return response.data
    },
  })
  
  const { data: searchResults } = useQuery({
    queryKey: ['research-search', searchQuery],
    queryFn: async () => {
      if (!searchQuery) return []
      const response = await api.get('/research/search', {
        params: { query: searchQuery },
      })
      return response.data
    },
    enabled: searchQuery.length > 0,
  })

  const displayedStudies = searchQuery ? (searchResults || []) : (studies || [])

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
            Research Library
          </h1>
          <p className="text-muted-foreground mt-2">
            Evidence-based research supporting the protocol
          </p>
        </motion.div>

        {/* Search and Tabs */}
        <div className="mb-6 space-y-4">
          <Card className="shadow-lg border-0">
            <CardContent className="pt-6">
              <div className="relative mb-4">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground" size={18} />
                <Input
                  placeholder="Search research studies..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10"
                />
              </div>
              
              <div className="flex gap-2">
                <Button
                  variant={activeTab === 'nutrition' ? 'default' : 'outline'}
                  onClick={() => {
                    setActiveTab('nutrition')
                    setSearchQuery('')
                  }}
                >
                  Nutrition
                </Button>
                <Button
                  variant={activeTab === 'glutamine' ? 'default' : 'outline'}
                  onClick={() => {
                    setActiveTab('glutamine')
                    setSearchQuery('')
                  }}
                >
                  Glutamine
                </Button>
                <Button
                  variant={activeTab === 'exercise' ? 'default' : 'outline'}
                  onClick={() => {
                    setActiveTab('exercise')
                    setSearchQuery('')
                  }}
                >
                  Exercise & Cancer
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Studies Grid */}
        {isLoading ? (
          <div className="flex items-center justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
          </div>
        ) : displayedStudies.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {displayedStudies.map((study: any, idx: number) => (
              <motion.div
                key={study.id || idx}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: idx * 0.05 }}
              >
                <Card className="shadow-lg border-0 h-full hover:shadow-xl transition-shadow">
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <CardTitle className="text-lg line-clamp-2">{study.title}</CardTitle>
                      {study.url && (
                        <a
                          href={study.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-blue-600 hover:text-blue-700"
                        >
                          <ExternalLink size={18} />
                        </a>
                      )}
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      {study.authors && (
                        <p className="text-sm text-muted-foreground">
                          {study.authors}
                        </p>
                      )}
                      {study.journal && study.year && (
                        <p className="text-sm font-medium">
                          {study.journal} ({study.year})
                        </p>
                      )}
                      {study.summary && (
                        <p className="text-sm mt-3 line-clamp-3">
                          {study.summary}
                        </p>
                      )}
                      {study.pubmed_id && (
                        <p className="text-xs text-muted-foreground mt-2">
                          PubMed ID: {study.pubmed_id}
                        </p>
                      )}
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        ) : (
          <Card className="shadow-lg border-0">
            <CardContent className="py-12 text-center">
              <BookOpen className="mx-auto text-muted-foreground mb-4" size={48} />
              <p className="text-muted-foreground">
                {searchQuery ? 'No studies found matching your search' : 'No studies available yet'}
              </p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}

