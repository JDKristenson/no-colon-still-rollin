import { useQuery } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import api from '@/lib/api'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import Navigation from '@/components/Navigation'
import { Search, Filter, Play, Info } from 'lucide-react'
import { useState } from 'react'
import { Input } from '@/components/ui/input'

export default function Exercises() {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedMuscleGroup, setSelectedMuscleGroup] = useState<string | null>(null)
  const [showBaseballOnly, setShowBaseballOnly] = useState(false)
  const [selectedExercise, setSelectedExercise] = useState<any>(null)
  
  const { data: exercises, isLoading } = useQuery({
    queryKey: ['exercises', selectedMuscleGroup, showBaseballOnly],
    queryFn: async () => {
      const response = await api.get('/workouts/exercises', {
        params: {
          muscle_group: selectedMuscleGroup || undefined,
          is_baseball_specific: showBaseballOnly || undefined,
        },
      })
      return response.data
    },
  })
  
  const filteredExercises = exercises?.filter((ex: any) => {
    if (!searchQuery) return true
    return ex.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
           ex.description?.toLowerCase().includes(searchQuery.toLowerCase())
  }) || []

  const muscleGroups = ['chest', 'back', 'shoulders', 'legs', 'core', 'arms']

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
            Exercise Library
          </h1>
          <p className="text-muted-foreground mt-2">
            Browse exercises for your workouts
          </p>
        </motion.div>

        {/* Filters */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-6"
        >
          <Card className="shadow-lg border-0">
            <CardContent className="pt-6">
              <div className="flex flex-col md:flex-row gap-4">
                <div className="flex-1">
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground" size={18} />
                    <Input
                      placeholder="Search exercises..."
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      className="pl-10"
                    />
                  </div>
                </div>
                
                <div className="flex gap-2 flex-wrap">
                  {muscleGroups.map((group) => (
                    <Button
                      key={group}
                      variant={selectedMuscleGroup === group ? 'default' : 'outline'}
                      onClick={() => setSelectedMuscleGroup(
                        selectedMuscleGroup === group ? null : group
                      )}
                      size="sm"
                    >
                      {group}
                    </Button>
                  ))}
                </div>
                
                <Button
                  variant={showBaseballOnly ? 'default' : 'outline'}
                  onClick={() => setShowBaseballOnly(!showBaseballOnly)}
                  size="sm"
                >
                  <Filter size={16} className="mr-2" />
                  Baseball Only
                </Button>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Exercise Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredExercises.map((exercise: any, idx: number) => (
            <motion.div
              key={exercise.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.05 }}
            >
              <Card
                className="shadow-lg border-0 cursor-pointer hover:shadow-xl transition-shadow h-full"
                onClick={() => setSelectedExercise(exercise)}
              >
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <CardTitle className="text-lg">{exercise.name}</CardTitle>
                    {exercise.is_baseball_specific && (
                      <span className="px-2 py-1 bg-amber-100 text-amber-700 rounded text-xs font-medium">
                        Baseball
                      </span>
                    )}
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground mb-4 line-clamp-2">
                    {exercise.description}
                  </p>
                  
                  <div className="flex flex-wrap gap-2 mb-4">
                    <span className="px-2 py-1 bg-blue-100 text-blue-700 rounded text-xs capitalize">
                      {exercise.muscle_group_primary}
                    </span>
                    {exercise.equipment_required?.length > 0 && (
                      <span className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs">
                        {exercise.equipment_required.join(', ')}
                      </span>
                    )}
                    <span className="px-2 py-1 bg-purple-100 text-purple-700 rounded text-xs">
                      Level {exercise.difficulty_level}
                    </span>
                  </div>
                  
                  <Button
                    variant="outline"
                    className="w-full"
                    onClick={(e) => {
                      e.stopPropagation()
                      setSelectedExercise(exercise)
                    }}
                  >
                    <Info className="mr-2" size={16} />
                    View Details
                  </Button>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>

        {filteredExercises.length === 0 && (
          <Card className="shadow-lg border-0">
            <CardContent className="py-12 text-center">
              <p className="text-muted-foreground">No exercises found</p>
            </CardContent>
          </Card>
        )}

        {/* Exercise Detail Modal */}
        {selectedExercise && (
          <div
            className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
            onClick={() => setSelectedExercise(null)}
          >
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              onClick={(e) => e.stopPropagation()}
              className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto"
            >
              <Card className="border-0 shadow-none">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div>
                      <CardTitle className="text-2xl">{selectedExercise.name}</CardTitle>
                      <p className="text-muted-foreground mt-2">
                        {selectedExercise.description}
                      </p>
                    </div>
                    <Button
                      variant="ghost"
                      onClick={() => setSelectedExercise(null)}
                    >
                      ×
                    </Button>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <h4 className="font-semibold mb-2">Primary Muscle Group</h4>
                    <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded capitalize">
                      {selectedExercise.muscle_group_primary}
                    </span>
                  </div>
                  
                  {selectedExercise.muscle_groups_secondary?.length > 0 && (
                    <div>
                      <h4 className="font-semibold mb-2">Secondary Muscle Groups</h4>
                      <div className="flex flex-wrap gap-2">
                        {selectedExercise.muscle_groups_secondary.map((group: string) => (
                          <span key={group} className="px-3 py-1 bg-gray-100 text-gray-700 rounded capitalize">
                            {group}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                  
                  {selectedExercise.form_cues && selectedExercise.form_cues.length > 0 && (
                    <div>
                      <h4 className="font-semibold mb-2 flex items-center gap-2">
                        <Info size={18} />
                        Form Cues
                      </h4>
                      <ul className="list-disc list-inside space-y-1 text-sm">
                        {selectedExercise.form_cues.map((cue: string, i: number) => (
                          <li key={i}>{cue}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                  
                  <div className="grid grid-cols-2 gap-4">
                    {selectedExercise.default_sets && (
                      <div>
                        <h4 className="font-semibold text-sm text-muted-foreground">Sets</h4>
                        <p className="text-lg font-medium">{selectedExercise.default_sets}</p>
                      </div>
                    )}
                    {selectedExercise.default_reps && (
                      <div>
                        <h4 className="font-semibold text-sm text-muted-foreground">Reps</h4>
                        <p className="text-lg font-medium">{selectedExercise.default_reps}</p>
                      </div>
                    )}
                    {selectedExercise.default_weight_lbs && (
                      <div>
                        <h4 className="font-semibold text-sm text-muted-foreground">Weight</h4>
                        <p className="text-lg font-medium">{selectedExercise.default_weight_lbs} lbs</p>
                      </div>
                    )}
                    {selectedExercise.default_duration_seconds && (
                      <div>
                        <h4 className="font-semibold text-sm text-muted-foreground">Duration</h4>
                        <p className="text-lg font-medium">{selectedExercise.default_duration_seconds}s</p>
                      </div>
                    )}
                  </div>
                  
                  {selectedExercise.equipment_required?.length > 0 && (
                    <div>
                      <h4 className="font-semibold mb-2">Equipment Required</h4>
                      <div className="flex flex-wrap gap-2">
                        {selectedExercise.equipment_required.map((eq: string) => (
                          <span key={eq} className="px-3 py-1 bg-gray-100 text-gray-700 rounded">
                            {eq}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>
            </motion.div>
          </div>
        )}
      </div>
    </div>
  )
}

