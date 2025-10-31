import { useQuery } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import api from '@/lib/api'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { useAuth } from '@/contexts/AuthContext'

export default function Dashboard() {
  const { user } = useAuth()
  
  const { data: dashboardData, isLoading } = useQuery({
    queryKey: ['dashboard'],
    queryFn: async () => {
      const response = await api.get('/dashboard')
      return response.data
    },
  })

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      <div className="container mx-auto px-4 py-8">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
            Welcome back, {user?.name}
          </h1>
          <p className="text-muted-foreground mt-2">
            Your integrated cancer protocol & workout dashboard
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.1 }}
          >
            <Card className="shadow-lg border-0 bg-gradient-to-br from-white to-blue-50">
              <CardHeader>
                <CardTitle className="text-lg font-semibold">Current Weight</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold text-blue-600">
                  {dashboardData?.user?.current_weight_lbs || '--'} lbs
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2 }}
          >
            <Card className="shadow-lg border-0 bg-gradient-to-br from-white to-green-50">
              <CardHeader>
                <CardTitle className="text-lg font-semibold">Glutamine Score</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold text-green-600">
                  {dashboardData?.metrics?.glutamine_competition_score?.toFixed(0) || '0'} / 100
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.3 }}
          >
            <Card className="shadow-lg border-0 bg-gradient-to-br from-white to-purple-50">
              <CardHeader>
                <CardTitle className="text-lg font-semibold">Streak</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold text-purple-600">
                  🔥 {dashboardData?.metrics?.current_streak || 0} days
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.4 }}
          >
            <Card className="shadow-lg border-0 bg-gradient-to-br from-white to-amber-50">
              <CardHeader>
                <CardTitle className="text-lg font-semibold">Adherence</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold text-amber-600">
                  {dashboardData?.metrics?.combined_adherence?.toFixed(0) || 0}%
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.5 }}
          >
            <Card className="shadow-lg border-0">
              <CardHeader>
                <CardTitle>Today's Nutrition Protocol</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">Protocol generation coming soon...</p>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.6 }}
          >
            <Card className="shadow-lg border-0">
              <CardHeader>
                <CardTitle>Today's Workout</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">Workout generation coming soon...</p>
              </CardContent>
            </Card>
          </motion.div>
        </div>
      </div>
    </div>
  )
}

