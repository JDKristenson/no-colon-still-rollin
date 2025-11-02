import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import api from '@/lib/api'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Slider } from '@/components/ui/slider'
import Navigation from '@/components/Navigation'
import { Check, Clock, Dumbbell, Target, Info } from 'lucide-react'
import { useState } from 'react'

export default function Workouts() {
  const queryClient = useQueryClient()
  const [completedExercises, setCompletedExercises] = useState<Record<string, boolean>>({})
  const [rpe, setRpe] = useState([5])
  const [expectedSoreness, setExpectedSoreness] = useState<Record<string, number>>({})
  
  const { data: workout, isLoading } = useQuery({
    queryKey: ['workout-today'],
    queryFn: async () => {
      const response = await api.get('/workouts/today')
      return response.data
    },
  })
  
  const logWorkout = useMutation({
    mutationFn: async (data: any) => {
      const response = await api.post('/workouts/log', data)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['workout-today'] })
      queryClient.invalidateQueries({ queryKey: ['dashboard'] })
      queryClient.invalidateQueries({ queryKey: ['compliance-stats'] })
    },
  })
  
  const logWorkoutCompliance = useMutation({
    mutationFn: async (completed: boolean) => {
      const response = await api.post('/compliance/workout', {
        completed,
        duration_minutes: workout?.estimated_duration_minutes || 0,
      })
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['compliance-stats'] })
    },
  })
  
  const handleCompleteWorkout = () => {
    const exercisesCompleted = workout?.exercises?.map((ex: any) => ({
      exercise_id: ex.id,
      sets_completed: completedExercises[ex.name] ? 3 : 0,
      completed: completedExercises[ex.name] || false,
    })) || []
    
    const postWorkoutSoreness = Object.entries(expectedSoreness).map(([group, intensity]) => ({
      muscle_group: group,
      expected_intensity: intensity,
    }))
    
    logWorkout.mutate({
      workout_plan_id: workout?.id,
      completed: true,
      actual_duration_minutes: workout?.estimated_duration_minutes || 0,
      exercises_completed: exercisesCompleted,
      perceived_exertion: rpe[0],
      post_workout_soreness_prediction: postWorkoutSoreness,
    })
    
    logWorkoutCompliance.mutate(true)
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

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-indigo-50/50">
      <Navigation />
      
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 bg-clip-text text-transparent tracking-tight">
            Workout Plan
          </h1>
          <p className="text-muted-foreground mt-2 text-lg">
            Maintain continuous muscle soreness for glutamine competition
          </p>
        </motion.div>
        {!workout && (
          <Card className="shadow-lg border-0">
            <CardContent className="py-12 text-center">
              <Dumbbell className="mx-auto text-muted-foreground mb-4" size={48} />
              <p className="text-lg font-medium mb-2">No workout planned yet</p>
              <p className="text-muted-foreground mb-6">
                Generate your workout plan to maintain continuous muscle soreness
              </p>
              <Button 
                onClick={() => {
                  queryClient.invalidateQueries({ queryKey: ['workout-today'] })
                }} 
                size="lg"
                className="shadow-lg hover:shadow-xl transition-all"
              >
                Generate Workout
              </Button>
            </CardContent>
          </Card>
        )}

        {workout && (
          <>
            {/* Workout Header */}
            <motion.div
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              className="mb-6"
            >
              <Card className="shadow-premium-lg border-0 bg-gradient-to-r from-blue-50 via-indigo-50 to-purple-50">
                <CardContent className="pt-6">
                  <div className="flex items-start justify-between">
                    <div>
                      <h1 className="text-3xl font-bold mb-2">
                        {workout.workout_type?.toUpperCase()} Workout
                      </h1>
                      <div className="flex items-center gap-4 text-sm text-muted-foreground">
                        <div className="flex items-center gap-2">
                          <Clock size={16} />
                          {workout.estimated_duration_minutes} minutes
                        </div>
                        <div className="flex items-center gap-2">
                          <Target size={16} />
                          {workout.target_muscle_groups?.join(', ')}
                        </div>
                      </div>
                      {workout.coaching_message && (
                        <p className="mt-4 text-base text-gray-700 italic">
                          "{workout.coaching_message}"
                        </p>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>

            {/* Exercises */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2">
                <Card className="shadow-premium border-0 mb-6">
                  <CardHeader>
                    <CardTitle className="text-2xl">Exercises</CardTitle>
                    <CardDescription className="text-base">
                      Complete each exercise as prescribed
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {workout.exercises?.map((exercise: any, idx: number) => (
                        <motion.div
                          key={idx}
                          initial={{ opacity: 0, x: -20 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: idx * 0.1 }}
                        >
                          <Card className={`transition-all duration-300 hover:shadow-premium hover:scale-[1.01] ${
                            completedExercises[exercise.name] 
                              ? 'bg-gradient-to-r from-green-50 to-emerald-50 border-green-300 shadow-md' 
                              : ''
                          }`}>
                            <CardContent className="pt-4">
                              <div className="flex items-start justify-between mb-4">
                                <div className="flex-1">
                                  <div className="flex items-center gap-2 mb-2">
                                    <h4 className="font-semibold text-lg">{exercise.name}</h4>
                                    {completedExercises[exercise.name] && (
                                      <Check className="text-green-600" size={20} />
                                    )}
                                  </div>
                                  <p className="text-sm text-muted-foreground mb-3">
                                    {exercise.description}
                                  </p>
                                  <div className="flex flex-wrap gap-4 text-sm mb-3">
                                    {exercise.sets && (
                                      <span className="font-medium">
                                        Sets: {exercise.sets}
                                      </span>
                                    )}
                                    {exercise.reps && (
                                      <span className="font-medium">
                                        Reps: {exercise.reps}
                                      </span>
                                    )}
                                    {exercise.weight_lbs && (
                                      <span className="font-medium">
                                        Weight: {exercise.weight_lbs} lbs
                                      </span>
                                    )}
                                    {exercise.duration_seconds && (
                                      <span className="font-medium">
                                        Duration: {exercise.duration_seconds}s
                                      </span>
                                    )}
                                  </div>
                                  {exercise.form_cues && exercise.form_cues.length > 0 && (
                                    <div className="bg-blue-50 p-3 rounded-lg mb-3">
                                      <div className="flex items-start gap-2 mb-2">
                                        <Info className="text-blue-600 mt-0.5" size={16} />
                                        <span className="text-sm font-medium text-blue-900">
                                          Form Cues:
                                        </span>
                                      </div>
                                      <ul className="list-disc list-inside text-sm text-blue-800 space-y-1">
                                        {exercise.form_cues.map((cue: string, i: number) => (
                                          <li key={i}>{cue}</li>
                                        ))}
                                      </ul>
                                    </div>
                                  )}
                                </div>
                                <Button
                                  variant={completedExercises[exercise.name] ? "default" : "outline"}
                                  onClick={() => {
                                    setCompletedExercises(prev => ({
                                      ...prev,
                                      [exercise.name]: !prev[exercise.name],
                                    }))
                                  }}
                                >
                                  {completedExercises[exercise.name] ? 'Completed' : 'Mark Complete'}
                                </Button>
                              </div>
                            </CardContent>
                          </Card>
                        </motion.div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </div>

              {/* Sidebar */}
              <div className="space-y-6">
                {/* Post-Workout */}
                <Card className="shadow-lg border-0">
                  <CardHeader>
                    <CardTitle>Post-Workout</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    {/* RPE */}
                    <div>
                      <label className="text-sm font-medium mb-2 block">
                        Rate of Perceived Exertion (RPE)
                      </label>
                      <Slider
                        value={rpe}
                        onValueChange={setRpe}
                        max={10}
                        min={1}
                        step={1}
                        className="mb-2"
                      />
                      <div className="flex justify-between text-sm text-muted-foreground">
                        <span>1 - Easy</span>
                        <span className="font-semibold text-lg">{rpe[0]}/10</span>
                        <span>10 - Maximum</span>
                      </div>
                    </div>

                    {/* Expected Soreness */}
                    <div>
                      <label className="text-sm font-medium mb-4 block">
                        Expected Soreness Tomorrow
                      </label>
                      <div className="space-y-4">
                        {workout.target_muscle_groups?.map((group: string) => (
                          <div key={group}>
                            <div className="flex justify-between mb-2">
                              <span className="text-sm capitalize">{group}</span>
                              <span className="text-sm font-semibold">
                                {expectedSoreness[group] || 0}/10
                              </span>
                            </div>
                            <Slider
                              value={[expectedSoreness[group] || 0]}
                              onValueChange={(val) => {
                                setExpectedSoreness(prev => ({
                                  ...prev,
                                  [group]: val[0],
                                }))
                              }}
                              max={10}
                              min={0}
                              step={1}
                            />
                          </div>
                        ))}
                      </div>
                    </div>

                    <Button
                      onClick={handleCompleteWorkout}
                      className="w-full"
                      size="lg"
                    >
                      <Check className="mr-2" size={18} />
                      Complete Workout
                    </Button>
                  </CardContent>
                </Card>

                {/* Target Info */}
                <Card className="shadow-lg border-0 bg-gradient-to-br from-purple-50 to-indigo-50">
                  <CardHeader>
                    <CardTitle>Target Goals</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {workout.soreness_maintenance_goals?.map((goal: any, idx: number) => (
                        <div key={idx} className="text-sm">
                          <div className="flex justify-between mb-1">
                            <span className="font-medium capitalize">{goal.muscle_group}</span>
                            <span className="text-muted-foreground">
                              {goal.current_soreness}/10 → {goal.target_soreness}/10
                            </span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div
                              className="bg-purple-600 h-2 rounded-full"
                              style={{ width: `${(goal.current_soreness / 10) * 100}%` }}
                            />
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  )
}

