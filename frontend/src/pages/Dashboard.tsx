import { useQuery } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import api from '@/lib/api'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import Navigation from '@/components/Navigation'
import { TrendingUp, TrendingDown, Activity, Target, Zap, Calendar } from 'lucide-react'
import { Link } from 'react-router-dom'
import VitruvianMan from '@/components/VitruvianMan'
import { XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts'

export default function Dashboard() {
  const { data: dashboardData, isLoading } = useQuery({
    queryKey: ['dashboard'],
    queryFn: async () => {
      const response = await api.get('/dashboard')
      return response.data
    },
  })
  
  const { data: weightTrend } = useQuery({
    queryKey: ['weight-trend'],
    queryFn: async () => {
      const response = await api.get('/weight/trend?days=30')
      return response.data
    },
  })
  
  const { data: coaching } = useQuery({
    queryKey: ['coaching'],
    queryFn: async () => {
      const response = await api.get('/coaching/message')
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

  const nutrition = dashboardData?.nutrition || {}
  const workout = dashboardData?.workout || {}
  const soreness = dashboardData?.soreness || {}
  const metrics = dashboardData?.metrics || {}

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-indigo-50/50">
      <Navigation />
      
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        {/* Coaching Message */}
        {coaching?.message && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-6"
          >
            <Card className="bg-gradient-to-r from-blue-50 to-indigo-50 border-blue-200 shadow-lg">
              <CardContent className="pt-6">
                <p className="text-lg font-medium text-gray-800">{coaching.message}</p>
              </CardContent>
            </Card>
          </motion.div>
        )}

        {/* Top Metrics - Premium Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <motion.div
            initial={{ opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            transition={{ delay: 0.1, type: "spring", stiffness: 200 }}
            whileHover={{ y: -4, scale: 1.02 }}
          >
            <Card className="relative overflow-hidden border-0 shadow-premium bg-gradient-to-br from-white via-blue-50/50 to-blue-100/30 hover:shadow-premium-lg transition-all duration-300">
              <div className="absolute top-0 right-0 w-32 h-32 bg-blue-500/5 rounded-full -mr-16 -mt-16 blur-2xl" />
              <CardHeader className="pb-3 relative">
                <CardTitle className="text-base font-semibold flex items-center gap-2.5 text-gray-700">
                  <div className="p-2 rounded-lg bg-blue-100 text-blue-600">
                    <Target size={18} />
                  </div>
                  Current Weight
                </CardTitle>
              </CardHeader>
              <CardContent className="relative">
                <div className="text-4xl font-bold text-blue-600 mb-2">
                  {dashboardData?.user?.current_weight_lbs || '--'}
                  <span className="text-xl text-gray-500 font-normal ml-1">lbs</span>
                </div>
                {weightTrend?.change_lbs && (
                  <div className="flex items-center gap-2 mt-3">
                    {weightTrend.change_lbs > 0 ? (
                      <>
                        <div className="flex items-center gap-1 px-2 py-1 rounded-md bg-green-50 text-green-700">
                          <TrendingUp size={14} />
                          <span className="text-xs font-medium">+{weightTrend.change_lbs.toFixed(1)}</span>
                        </div>
                        <span className="text-xs text-gray-500">30 days</span>
                      </>
                    ) : (
                      <>
                        <div className="flex items-center gap-1 px-2 py-1 rounded-md bg-red-50 text-red-700">
                          <TrendingDown size={14} />
                          <span className="text-xs font-medium">{weightTrend.change_lbs.toFixed(1)}</span>
                        </div>
                        <span className="text-xs text-gray-500">30 days</span>
                      </>
                    )}
                  </div>
                )}
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
            whileHover={{ y: -4, scale: 1.02 }}
          >
            <Card className="relative overflow-hidden border-0 shadow-premium bg-gradient-to-br from-white via-green-50/50 to-emerald-100/30 hover:shadow-premium-lg transition-all duration-300">
              <div className="absolute top-0 right-0 w-32 h-32 bg-green-500/5 rounded-full -mr-16 -mt-16 blur-2xl" />
              <CardHeader className="pb-3 relative">
                <CardTitle className="text-base font-semibold flex items-center gap-2.5 text-gray-700">
                  <div className="p-2 rounded-lg bg-green-100 text-green-600">
                    <Zap size={18} />
                  </div>
                  Glutamine Score
                </CardTitle>
              </CardHeader>
              <CardContent className="relative">
                <div className="text-4xl font-bold text-green-600 mb-3">
                  {metrics.glutamine_competition_score?.toFixed(0) || '0'}
                  <span className="text-xl text-gray-500 font-normal"> / 100</span>
                </div>
                <div className="mt-3 w-full bg-gray-200/60 rounded-full h-2.5 overflow-hidden">
                  <motion.div
                    className="bg-gradient-to-r from-green-500 to-emerald-500 h-2.5 rounded-full shadow-sm"
                    initial={{ width: 0 }}
                    animate={{ width: `${metrics.glutamine_competition_score || 0}%` }}
                    transition={{ duration: 0.8, ease: "easeOut" }}
                  />
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            transition={{ delay: 0.3, type: "spring", stiffness: 200 }}
            whileHover={{ y: -4, scale: 1.02 }}
          >
            <Card className="relative overflow-hidden border-0 shadow-premium bg-gradient-to-br from-white via-purple-50/50 to-violet-100/30 hover:shadow-premium-lg transition-all duration-300">
              <div className="absolute top-0 right-0 w-32 h-32 bg-purple-500/5 rounded-full -mr-16 -mt-16 blur-2xl" />
              <CardHeader className="pb-3 relative">
                <CardTitle className="text-base font-semibold flex items-center gap-2.5 text-gray-700">
                  <div className="p-2 rounded-lg bg-purple-100 text-purple-600">
                    <Calendar size={18} />
                  </div>
                  Streak
                </CardTitle>
              </CardHeader>
              <CardContent className="relative">
                <div className="flex items-center gap-2 text-4xl font-bold text-purple-600 mb-2">
                  <span className="text-3xl">🔥</span>
                  <span>{metrics.current_streak || 0}</span>
                  <span className="text-xl text-gray-500 font-normal">days</span>
                </div>
                <div className="px-3 py-1.5 rounded-lg bg-purple-50/80 border border-purple-100 mt-3">
                  <p className="text-sm font-medium text-purple-700">
                    {metrics.is_perfect_day ? "✨ Perfect day today!" : "💪 Keep going!"}
                  </p>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            transition={{ delay: 0.4, type: "spring", stiffness: 200 }}
            whileHover={{ y: -4, scale: 1.02 }}
          >
            <Card className="relative overflow-hidden border-0 shadow-premium bg-gradient-to-br from-white via-amber-50/50 to-orange-100/30 hover:shadow-premium-lg transition-all duration-300">
              <div className="absolute top-0 right-0 w-32 h-32 bg-amber-500/5 rounded-full -mr-16 -mt-16 blur-2xl" />
              <CardHeader className="pb-3 relative">
                <CardTitle className="text-base font-semibold flex items-center gap-2.5 text-gray-700">
                  <div className="p-2 rounded-lg bg-amber-100 text-amber-600">
                    <Activity size={18} />
                  </div>
                  Adherence
                </CardTitle>
              </CardHeader>
              <CardContent className="relative">
                <div className="text-4xl font-bold text-amber-600 mb-3">
                  {metrics.combined_adherence?.toFixed(0) || 0}
                  <span className="text-xl text-gray-500 font-normal">%</span>
                </div>
                <div className="space-y-1.5 mt-3">
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-gray-600">Nutrition</span>
                    <span className="font-semibold text-gray-700">{nutrition.adherence_percentage?.toFixed(0) || 0}%</span>
                  </div>
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-gray-600">Workout</span>
                    <span className="font-semibold text-gray-700">{workout.adherence_percentage?.toFixed(0) || 0}%</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Nutrition Protocol */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.5 }}
          >
            <Card className="border-0 shadow-premium bg-white/90 backdrop-blur-sm h-full hover:shadow-premium-lg transition-all duration-300">
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span>Today's Nutrition Protocol</span>
                  <Link to="/protocol">
                    <Button variant="outline" size="sm">View Full</Button>
                  </Link>
                </CardTitle>
                <CardDescription>
                  {nutrition.today_protocol?.foods?.length || 0} foods • Target: {nutrition.today_protocol?.protein_target?.toFixed(1) || 0}g protein
                </CardDescription>
              </CardHeader>
              <CardContent>
                {nutrition.today_protocol ? (
                  <div className="space-y-2">
                    {nutrition.today_protocol.foods?.slice(0, 5).map((food: any, idx: number) => (
                      <div key={idx} className="flex items-center gap-2 text-sm">
                        <div className="w-2 h-2 rounded-full bg-green-500" />
                        <span className="font-medium">{food.name}</span>
                        <span className="text-muted-foreground">({food.amount_grams}g)</span>
                      </div>
                    ))}
                    {nutrition.today_protocol.foods?.length > 5 && (
                      <p className="text-sm text-muted-foreground mt-2">
                        +{nutrition.today_protocol.foods.length - 5} more foods
                      </p>
                    )}
                    <div className="mt-4 pt-4 border-t">
                      <p className="text-sm font-medium">Macros</p>
                      <div className="grid grid-cols-3 gap-2 mt-2 text-sm">
                        <div>Carbs: {nutrition.today_protocol.total_macros?.net_carbs?.toFixed(1) || 0}g</div>
                        <div>Protein: {nutrition.today_protocol.total_macros?.protein?.toFixed(1) || 0}g</div>
                        <div>Fat: {nutrition.today_protocol.total_macros?.fat?.toFixed(1) || 0}g</div>
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <p className="text-muted-foreground mb-4">No protocol generated yet</p>
                    <Link to="/protocol">
                      <Button>Generate Today's Protocol</Button>
                    </Link>
                  </div>
                )}
              </CardContent>
            </Card>
          </motion.div>

          {/* Workout */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.6 }}
          >
            <Card className="border-0 shadow-premium bg-white/90 backdrop-blur-sm h-full hover:shadow-premium-lg transition-all duration-300">
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span>Today's Workout</span>
                  <Link to="/workouts">
                    <Button variant="outline" size="sm">View Full</Button>
                  </Link>
                </CardTitle>
                <CardDescription>
                  {workout.today_workout?.workout_type || 'Not scheduled'} • 
                  {workout.today_workout?.estimated_duration_minutes || 0} min
                </CardDescription>
              </CardHeader>
              <CardContent>
                {workout.today_workout ? (
                  <div className="space-y-3">
                    {workout.completed ? (
                      <div className="flex items-center gap-2 text-green-600">
                        <div className="w-3 h-3 rounded-full bg-green-500" />
                        <span className="font-medium">Workout Completed!</span>
                      </div>
                    ) : (
                      <div className="flex items-center gap-2 text-amber-600">
                        <div className="w-3 h-3 rounded-full bg-amber-500" />
                        <span className="font-medium">Pending</span>
                      </div>
                    )}
                    <div>
                      <p className="text-sm font-medium mb-2">Target Muscle Groups:</p>
                      <div className="flex flex-wrap gap-2">
                        {workout.today_workout.target_muscle_groups?.map((group: string) => (
                          <span key={group} className="px-2 py-1 bg-blue-100 text-blue-700 rounded text-sm">
                            {group}
                          </span>
                        ))}
                      </div>
                    </div>
                    {workout.today_workout.coaching_message && (
                      <p className="text-sm text-muted-foreground italic">
                        "{workout.today_workout.coaching_message}"
                      </p>
                    )}
                    <Link to="/workouts">
                      <Button className="w-full mt-4">
                        {workout.completed ? 'View Details' : 'Start Workout'}
                      </Button>
                    </Link>
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <p className="text-muted-foreground mb-4">No workout planned yet</p>
                    <Link to="/workouts">
                      <Button>Generate Workout</Button>
                    </Link>
                  </div>
                )}
              </CardContent>
            </Card>
          </motion.div>
        </div>

        {/* Soreness Map */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
          className="mb-8"
        >
          <Card className="border-0 shadow-premium bg-white/90 backdrop-blur-sm hover:shadow-premium-lg transition-all duration-300">
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <span>Muscle Soreness Map</span>
                <Link to="/soreness">
                  <Button variant="outline" size="sm">Update Soreness</Button>
                </Link>
              </CardTitle>
              <CardDescription>
                Coverage: {soreness.coverage_percentage?.toFixed(0) || 0}% • 
                {soreness.sore_count || 0} groups sore
                {soreness.gap_warning && (
                  <span className="text-red-600 font-medium ml-2">⚠️ Gap Warning</span>
                )}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <VitruvianMan
                soreness={{
                  chest: soreness.current_state?.chest || 0,
                  back: soreness.current_state?.back || 0,
                  shoulders: soreness.current_state?.shoulders || 0,
                  legs: soreness.current_state?.legs || 0,
                  core: soreness.current_state?.core || 0,
                  arms: soreness.current_state?.arms || 0,
                }}
              />
            </CardContent>
          </Card>
        </motion.div>

        {/* Weight Trend Chart */}
        {weightTrend && weightTrend.dates?.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.8 }}
          >
            <Card className="border-0 shadow-premium bg-white/90 backdrop-blur-sm hover:shadow-premium-lg transition-all duration-300">
              <CardHeader>
                <CardTitle>Weight Trend (30 Days)</CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <AreaChart data={weightTrend.dates.map((date: string, idx: number) => ({
                    date: new Date(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
                    weight: weightTrend.weights[idx],
                  }))}>
                    <CartesianGrid strokeDasharray="3 3" opacity={0.2} />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Area type="monotone" dataKey="weight" stroke="#2563EB" fill="#2563EB" fillOpacity={0.3} />
                  </AreaChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </motion.div>
        )}
      </div>
    </div>
  )
}
