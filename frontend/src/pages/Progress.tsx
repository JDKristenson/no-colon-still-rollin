import { useQuery } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import api from '@/lib/api'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import Navigation from '@/components/Navigation'
import { LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts'
import { TrendingUp, Weight, Target, Activity } from 'lucide-react'

export default function Progress() {
  const { data: weightTrend } = useQuery({
    queryKey: ['weight-trend'],
    queryFn: async () => {
      const response = await api.get('/weight/trend?days=90')
      return response.data
    },
  })
  
  const { data: compliance } = useQuery({
    queryKey: ['compliance-stats'],
    queryFn: async () => {
      const response = await api.get('/compliance/stats')
      return response.data
    },
  })
  
  const { data: weightHistory } = useQuery({
    queryKey: ['weight-history'],
    queryFn: async () => {
      const response = await api.get('/weight/history?limit=90')
      return response.data
    },
  })

  // Prepare chart data
  const chartData = weightTrend?.dates?.map((date: string, idx: number) => ({
    date: new Date(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
    weight: weightTrend.weights[idx],
  })) || []

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
            Progress & Analytics
          </h1>
          <p className="text-muted-foreground mt-2">
            Track your progress over time
          </p>
        </motion.div>

        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="shadow-lg border-0">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">Weight Change</p>
                  <p className="text-2xl font-bold">
                    {weightTrend?.change_lbs ? (
                      <span className={weightTrend.change_lbs > 0 ? 'text-green-600' : 'text-red-600'}>
                        {weightTrend.change_lbs > 0 ? '+' : ''}{weightTrend.change_lbs.toFixed(1)} lbs
                      </span>
                    ) : (
                      '--'
                    )}
                  </p>
                  <p className="text-xs text-muted-foreground mt-1">30 days</p>
                </div>
                <Weight className="text-blue-600" size={32} />
              </div>
            </CardContent>
          </Card>

          <Card className="shadow-lg border-0">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">Current Streak</p>
                  <p className="text-2xl font-bold text-purple-600">
                    {compliance?.current_streak || 0} days
                  </p>
                  <p className="text-xs text-muted-foreground mt-1">Perfect days</p>
                </div>
                <Target className="text-purple-600" size={32} />
              </div>
            </CardContent>
          </Card>

          <Card className="shadow-lg border-0">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">7-Day Avg</p>
                  <p className="text-2xl font-bold text-green-600">
                    {compliance?.['7_day_combined_avg']?.toFixed(0) || 0}%
                  </p>
                  <p className="text-xs text-muted-foreground mt-1">Combined adherence</p>
                </div>
                <TrendingUp className="text-green-600" size={32} />
              </div>
            </CardContent>
          </Card>

          <Card className="shadow-lg border-0">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">Nutrition</p>
                  <p className="text-2xl font-bold text-blue-600">
                    {compliance?.['7_day_nutrition_avg']?.toFixed(0) || 0}%
                  </p>
                  <p className="text-xs text-muted-foreground mt-1">7-day average</p>
                </div>
                <Activity className="text-blue-600" size={32} />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Weight Trend Chart */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-6"
        >
          <Card className="shadow-lg border-0">
            <CardHeader>
              <CardTitle>Weight Trend (90 Days)</CardTitle>
            </CardHeader>
            <CardContent>
              {chartData.length > 0 ? (
                <ResponsiveContainer width="100%" height={400}>
                  <AreaChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" opacity={0.2} />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Area
                      type="monotone"
                      dataKey="weight"
                      stroke="#2563EB"
                      fill="#2563EB"
                      fillOpacity={0.3}
                    />
                    {weightTrend?.first_weight && weightTrend?.last_weight && (
                      <Line
                        type="linear"
                        dataKey={() => weightTrend.first_weight}
                        stroke="#10B981"
                        strokeDasharray="5 5"
                        dot={false}
                      />
                    )}
                  </AreaChart>
                </ResponsiveContainer>
              ) : (
                <div className="text-center py-12 text-muted-foreground">
                  No weight data available yet
                </div>
              )}
            </CardContent>
          </Card>
        </motion.div>

        {/* Health Metrics */}
        {weightHistory && weightHistory.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-6"
          >
            <Card className="shadow-lg border-0">
              <CardHeader>
                <CardTitle>Health Metrics</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                  {['energy_level', 'sleep_quality', 'digestion_quality', 'overall_feeling'].map((metric) => {
                    const metricData = weightHistory
                      .filter((r: any) => r[metric])
                      .map((r: any) => ({
                        date: new Date(r.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
                        value: r[metric],
                      }))
                    
                    if (metricData.length === 0) return null
                    
                    return (
                      <div key={metric}>
                        <p className="text-sm font-medium mb-2 capitalize">
                          {metric.replace('_', ' ')}
                        </p>
                        <ResponsiveContainer width="100%" height={150}>
                          <LineChart data={metricData}>
                            <Line
                              type="monotone"
                              dataKey="value"
                              stroke="#8B5CF6"
                              strokeWidth={2}
                              dot={false}
                            />
                          </LineChart>
                        </ResponsiveContainer>
                      </div>
                    )
                  })}
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}

        {/* Weight History Table */}
        {weightHistory && weightHistory.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <Card className="shadow-lg border-0">
              <CardHeader>
                <CardTitle>Weight History</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b">
                        <th className="text-left p-2">Date</th>
                        <th className="text-left p-2">Weight (lbs)</th>
                        <th className="text-left p-2">Energy</th>
                        <th className="text-left p-2">Sleep</th>
                        <th className="text-left p-2">Notes</th>
                      </tr>
                    </thead>
                    <tbody>
                      {weightHistory.slice(0, 30).map((record: any) => (
                        <tr key={record.id} className="border-b">
                          <td className="p-2">
                            {new Date(record.date).toLocaleDateString()}
                          </td>
                          <td className="p-2 font-medium">{record.weight_lbs}</td>
                          <td className="p-2">
                            {record.energy_level ? `${record.energy_level}/10` : '--'}
                          </td>
                          <td className="p-2">
                            {record.sleep_quality ? `${record.sleep_quality}/10` : '--'}
                          </td>
                          <td className="p-2 text-sm text-muted-foreground">
                            {record.notes?.slice(0, 50) || '--'}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}
      </div>
    </div>
  )
}

