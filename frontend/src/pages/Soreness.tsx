import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import api from '@/lib/api'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Slider } from '@/components/ui/slider'
import Navigation from '@/components/Navigation'
import VitruvianMan from '@/components/VitruvianMan'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { AlertTriangle, CheckCircle, Zap } from 'lucide-react'
import { useState, useEffect } from 'react'

export default function Soreness() {
  const queryClient = useQueryClient()
  const [sorenessValues, setSorenessValues] = useState<Record<string, number>>({
    chest: 0,
    back: 0,
    shoulders: 0,
    legs: 0,
    core: 0,
    arms: 0,
  })
  
  const { data: currentSoreness, isLoading } = useQuery<{
    muscle_groups?: Record<string, number>;
    coverage_percentage?: number;
    detailed_state?: Array<{ name: string; status: string }>;
  }>({
    queryKey: ['soreness-current'],
    queryFn: async () => {
      const response = await api.get('/soreness/current')
      return response.data
    },
  })

  useEffect(() => {
    if (currentSoreness?.muscle_groups) {
      setSorenessValues(currentSoreness.muscle_groups)
    }
  }, [currentSoreness])
  
  const { data: coverageWarning } = useQuery({
    queryKey: ['soreness-coverage-warning'],
    queryFn: async () => {
      const response = await api.get('/soreness/coverage-warning')
      return response.data
    },
  })
  
  const { data: competitionScore } = useQuery({
    queryKey: ['soreness-competition-score'],
    queryFn: async () => {
      const response = await api.get('/soreness/competition-score')
      return response.data
    },
  })
  
  const logSoreness = useMutation({
    mutationFn: async (data: { muscle_group: string; intensity: number }) => {
      const response = await api.post('/soreness/log', data)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['soreness-current'] })
      queryClient.invalidateQueries({ queryKey: ['soreness-coverage-warning'] })
      queryClient.invalidateQueries({ queryKey: ['soreness-competition-score'] })
      queryClient.invalidateQueries({ queryKey: ['dashboard'] })
    },
  })
  
  const handleSorenessChange = (muscleGroup: string, value: number[]) => {
    const newValues = { ...sorenessValues, [muscleGroup]: value[0] }
    setSorenessValues(newValues)
    
    // Auto-save
    logSoreness.mutate({
      muscle_group: muscleGroup,
      intensity: value[0],
    })
  }
  
  const handleSaveAll = () => {
    Object.entries(sorenessValues).forEach(([group, intensity]) => {
      logSoreness.mutate({
        muscle_group: group,
        intensity,
      })
    })
  }

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

  const muscleGroups = ['chest', 'back', 'shoulders', 'legs', 'core', 'arms']
  const soreCount = Object.values(sorenessValues).filter(v => v >= 5).length

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
            Muscle Soreness Tracker
          </h1>
          <p className="text-muted-foreground mt-2">
            Track your muscle soreness to maintain continuous glutamine competition
          </p>
        </motion.div>

        {/* Coverage Warning */}
        {coverageWarning?.warning && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-6"
          >
            <Alert className={`${
              coverageWarning.severity === 'high' 
                ? 'border-red-500 bg-red-50' 
                : 'border-amber-500 bg-amber-50'
            }`}>
              <AlertTriangle className="h-4 w-4" />
              <AlertDescription>
                <div className="font-semibold mb-1">{coverageWarning.message}</div>
                <p className="text-sm">{coverageWarning.recommended_action}</p>
              </AlertDescription>
            </Alert>
          </motion.div>
        )}

        {/* Competition Score */}
        {competitionScore && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="mb-6"
          >
            <Card className="shadow-lg border-0 bg-gradient-to-r from-purple-50 to-indigo-50">
              <CardContent className="pt-6">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-lg font-semibold flex items-center gap-2">
                      <Zap className="text-purple-600" size={20} />
                      Glutamine Competition Score
                    </h3>
                    <p className="text-sm text-muted-foreground mt-1">
                      {competitionScore.sore_muscle_groups_count} of {competitionScore.total_muscle_groups} groups sore
                    </p>
                  </div>
                  <div className="text-right">
                    <div className="text-4xl font-bold text-purple-600">
                      {competitionScore.glutamine_competition_score?.toFixed(0) || 0}
                    </div>
                    <div className="text-sm text-muted-foreground">/ 100</div>
                  </div>
                </div>
                <div className="mt-4 w-full bg-gray-200 rounded-full h-3">
                  <motion.div
                    className="bg-purple-600 h-3 rounded-full"
                    initial={{ width: 0 }}
                    animate={{ width: `${competitionScore.glutamine_competition_score || 0}%` }}
                    transition={{ duration: 0.5 }}
                  />
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Vitruvian Man */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
          >
            <Card className="shadow-lg border-0">
              <CardHeader>
                <CardTitle>Visual Soreness Map</CardTitle>
                <CardDescription>
                  Interactive body diagram - click muscle groups to update
                </CardDescription>
              </CardHeader>
              <CardContent>
                <VitruvianMan
                  soreness={sorenessValues}
                  onMuscleClick={() => {
                    // Could open slider for that muscle group
                  }}
                />
              </CardContent>
            </Card>
          </motion.div>

          {/* Soreness Sliders */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
          >
            <Card className="shadow-lg border-0">
              <CardHeader>
                <CardTitle>Rate Your Soreness</CardTitle>
                <CardDescription>
                  Rate each muscle group on a scale of 0-10
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-6">
                  {muscleGroups.map((group, idx) => (
                    <motion.div
                      key={group}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: idx * 0.1 }}
                    >
                      <div className="flex items-center justify-between mb-3">
                        <div>
                          <span className="font-semibold capitalize">{group}</span>
                          <span className="ml-2 text-sm text-muted-foreground">
                            ({sorenessValues[group]}/10)
                          </span>
                        </div>
                        <div className="flex items-center gap-2">
                          {sorenessValues[group] === 0 && (
                            <span className="text-xs text-gray-400">No soreness</span>
                          )}
                          {sorenessValues[group] >= 1 && sorenessValues[group] <= 4 && (
                            <span className="text-xs text-blue-600">Mild</span>
                          )}
                          {sorenessValues[group] >= 5 && sorenessValues[group] <= 8 && (
                            <span className="text-xs text-purple-600">Moderate</span>
                          )}
                          {sorenessValues[group] >= 9 && (
                            <span className="text-xs text-red-600">Very Sore</span>
                          )}
                        </div>
                      </div>
                      <Slider
                        value={[sorenessValues[group]]}
                        onValueChange={(value) => handleSorenessChange(group, value)}
                        max={10}
                        min={0}
                        step={1}
                        className="mb-2"
                      />
                      <div className="flex justify-between text-xs text-muted-foreground">
                        <span>0</span>
                        <span>5</span>
                        <span>10</span>
                      </div>
                    </motion.div>
                  ))}
                </div>
                
                <div className="mt-6 pt-6 border-t">
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <p className="font-semibold">Coverage Summary</p>
                      <p className="text-sm text-muted-foreground">
                        {soreCount} muscle groups actively sore (≥5/10)
                      </p>
                    </div>
                    {soreCount >= 2 ? (
                      <CheckCircle className="text-green-600" size={24} />
                    ) : (
                      <AlertTriangle className="text-red-600" size={24} />
                    )}
                  </div>
                  
                  {currentSoreness?.coverage_percentage !== undefined && (
                    <div className="w-full bg-gray-200 rounded-full h-2 mb-2">
                      <motion.div
                        className={`h-2 rounded-full ${
                          currentSoreness.coverage_percentage >= 50 
                            ? 'bg-green-600' 
                            : currentSoreness.coverage_percentage > 0
                            ? 'bg-amber-600'
                            : 'bg-red-600'
                        }`}
                        initial={{ width: 0 }}
                        animate={{ width: `${currentSoreness.coverage_percentage}%` }}
                        transition={{ duration: 0.5 }}
                      />
                    </div>
                  )}
                  
                  <Button
                    onClick={handleSaveAll}
                    className="w-full mt-4"
                    size="lg"
                  >
                    Save All Changes
                  </Button>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </div>

        {/* Detailed State */}
        {currentSoreness?.detailed_state && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-6"
          >
            <Card className="shadow-lg border-0">
              <CardHeader>
                <CardTitle>Detailed Soreness State</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                  {currentSoreness.detailed_state.map((state: any) => (
                    <div
                      key={state.name}
                      className={`p-4 rounded-lg border-2 ${
                        state.status === 'active'
                          ? 'bg-green-50 border-green-200'
                          : state.status === 'fading'
                          ? 'bg-amber-50 border-amber-200'
                          : 'bg-gray-50 border-gray-200'
                      }`}
                    >
                      <div className="font-semibold capitalize mb-1">{state.name}</div>
                      <div className="text-2xl font-bold mb-1">{state.intensity}/10</div>
                      <div className="text-xs text-muted-foreground capitalize">{state.status}</div>
                      {state.days_sore > 0 && (
                        <div className="text-xs text-muted-foreground mt-1">
                          Day {state.days_sore} of soreness
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}
      </div>
    </div>
  )
}

