import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import api from '@/lib/api'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import Navigation from '@/components/Navigation'
import GroceryList from '@/components/GroceryList'
import { Check, RefreshCw, UtensilsCrossed, ShoppingCart } from 'lucide-react'
import { useState, useEffect } from 'react'

export default function Protocol() {
  const queryClient = useQueryClient()
  const [checkedFoods, setCheckedFoods] = useState<string[]>([])
  
  const { data: protocol, isLoading } = useQuery({
    queryKey: ['protocol-today'],
    queryFn: async () => {
      const response = await api.get('/protocol/today')
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
  
  const generateProtocol = useMutation({
    mutationFn: async () => {
      try {
        const response = await api.post('/protocol/generate')
        return response.data
      } catch (err: any) {
        const errorMsg = err?.response?.data?.detail || err?.message || 'Failed to generate protocol'
        throw new Error(errorMsg)
      }
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['protocol-today'] })
      queryClient.invalidateQueries({ queryKey: ['grocery-list'] })
    },
    onError: (error: Error) => {
      console.error('Protocol generation error:', error)
    },
  })
  
  const logCompliance = useMutation({
    mutationFn: async (foods: string[]) => {
      const response = await api.post('/compliance/nutrition', {
        foods_consumed: foods,
      })
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['compliance-stats'] })
      queryClient.invalidateQueries({ queryKey: ['dashboard'] })
    },
  })
  
  const handleFoodToggle = (foodName: string) => {
    const newChecked = checkedFoods.includes(foodName)
      ? checkedFoods.filter(f => f !== foodName)
      : [...checkedFoods, foodName]
    setCheckedFoods(newChecked)
    
    // Auto-save compliance
    logCompliance.mutate(newChecked)
  }
  
  const handleCheckAll = () => {
    if (protocol?.foods) {
      const allFoods = protocol.foods.map((f: any) => f.name)
      if (checkedFoods.length === allFoods.length) {
        setCheckedFoods([])
        logCompliance.mutate([])
      } else {
        setCheckedFoods(allFoods)
        logCompliance.mutate(allFoods)
      }
    }
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

  const foods = protocol?.foods || []
  const completionPercentage = foods.length > 0 ? (checkedFoods.length / foods.length) * 100 : 0

  // Sync checkedFoods with protocol when it loads
  useEffect(() => {
    if (protocol?.foods && checkedFoods.length === 0) {
      // Optionally check foods that were already marked as consumed today
      // This would require a separate API call to get compliance data
    }
  }, [protocol])

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-indigo-50/50">
      <Navigation />
      
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 bg-clip-text text-transparent tracking-tight">
                Nutrition Protocol
              </h1>
              <p className="text-muted-foreground mt-2 text-lg">
                Your daily anti-cancer food protocol
              </p>
              {protocol?.active_markers && protocol.active_markers.length > 0 && (
                <div className="mt-3 flex items-center gap-2">
                  <span className="px-3 py-1 bg-red-100 text-red-700 rounded-full text-sm font-medium">
                    {protocol.active_markers.length} Active Mutation{protocol.active_markers.length > 1 ? 's' : ''} Targeted
                  </span>
                </div>
              )}
            </div>
            <Button
              onClick={() => generateProtocol.mutate()}
              disabled={generateProtocol.isPending}
              className="flex items-center gap-2 shadow-lg hover:shadow-xl transition-all"
              size="lg"
            >
              <RefreshCw className={generateProtocol.isPending ? 'animate-spin' : ''} size={18} />
              {generateProtocol.isPending ? 'Generating...' : 'Generate Protocol'}
            </Button>
          </div>
        </motion.div>

        {!protocol && (
          <Card className="shadow-lg border-0">
            <CardContent className="py-12 text-center">
              <UtensilsCrossed className="mx-auto text-muted-foreground mb-4" size={48} />
              <p className="text-lg font-medium mb-2">No protocol generated yet</p>
              <p className="text-muted-foreground mb-6">
                Generate your personalized daily nutrition protocol to get started
              </p>
              <Button onClick={() => generateProtocol.mutate()} size="lg">
                Generate Today's Protocol
              </Button>
            </CardContent>
          </Card>
        )}

        {protocol && (
          <>
            {/* Progress Card */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="mb-6"
            >
              <Card className="shadow-premium-lg border-0 bg-gradient-to-r from-green-50 via-emerald-50 to-teal-50">
                <CardContent className="pt-6">
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <h3 className="text-lg font-semibold">Today's Progress</h3>
                      <p className="text-sm text-muted-foreground">
                        {checkedFoods.length} of {foods.length} foods consumed
                      </p>
                    </div>
                    <div className="text-3xl font-bold text-green-600">
                      {completionPercentage.toFixed(0)}%
                    </div>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <motion.div
                      className="bg-green-600 h-3 rounded-full"
                      initial={{ width: 0 }}
                      animate={{ width: `${completionPercentage}%` }}
                      transition={{ duration: 0.5 }}
                    />
                  </div>
                  <div className="flex items-center justify-between mt-4">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={handleCheckAll}
                    >
                      {checkedFoods.length === foods.length ? 'Uncheck All' : 'Check All'}
                    </Button>
                    <span className="text-sm text-muted-foreground">
                      7-day avg: {compliance?.['7_day_nutrition_avg']?.toFixed(0) || 0}%
                    </span>
                  </div>
                </CardContent>
              </Card>
            </motion.div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Foods Checklist */}
              <div className="lg:col-span-2">
                <Card className="shadow-premium border-0">
                  <CardHeader>
                    <CardTitle className="text-2xl">Protocol Foods</CardTitle>
                    <CardDescription className="text-base">
                      Check off foods as you consume them throughout the day
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {foods.map((food: any, idx: number) => {
                        const isChecked = checkedFoods.includes(food.name)
                        
                        return (
                          <motion.div
                            key={idx}
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: idx * 0.05 }}
                          >
                            <Card
                              className={`cursor-pointer transition-all duration-300 hover:shadow-premium hover:scale-[1.02] ${
                                isChecked ? 'bg-gradient-to-r from-green-50 to-emerald-50 border-green-300 shadow-md' : 'hover:bg-blue-50/50'
                              }`}
                              onClick={() => handleFoodToggle(food.name)}
                            >
                              <CardContent className="pt-4">
                                <div className="flex items-start gap-4">
                                  <div className={`flex-shrink-0 w-6 h-6 rounded-full border-2 flex items-center justify-center ${
                                    isChecked 
                                      ? 'bg-green-600 border-green-600' 
                                      : 'border-gray-300'
                                  }`}>
                                    {isChecked && <Check className="text-white" size={16} />}
                                  </div>
                                  <div className="flex-1">
                                    <div className="flex items-center justify-between mb-2">
                                      <h4 className="font-semibold text-lg">{food.name}</h4>
                                      <span className="text-sm font-medium text-blue-600">
                                        {food.amount_grams}g
                                      </span>
                                    </div>
                                    <p className="text-sm text-muted-foreground mb-2">
                                      {food.reason}
                                    </p>
                                    <div className="flex flex-wrap gap-2">
                                      {food.mechanisms?.map((mech: string, i: number) => (
                                        <span
                                          key={i}
                                          className="px-2 py-0.5 bg-blue-100 text-blue-700 rounded text-xs"
                                        >
                                          {mech}
                                        </span>
                                      ))}
                                    </div>
                                    {food.safety_notes && (
                                      <p className="text-xs text-amber-600 mt-2">
                                        ⚠️ {food.safety_notes}
                                      </p>
                                    )}
                                  </div>
                                </div>
                              </CardContent>
                            </Card>
                          </motion.div>
                        )
                      })}
                    </div>
                  </CardContent>
                </Card>
              </div>

              {/* Sidebar */}
              <div className="space-y-6">
                {/* Macros Card */}
                <Card className="shadow-lg border-0">
                  <CardHeader>
                    <CardTitle>Macros</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div>
                        <div className="flex justify-between mb-1">
                          <span className="text-sm">Net Carbs</span>
                          <span className="text-sm font-semibold">
                            {protocol.total_macros?.net_carbs?.toFixed(1) || 0}g
                          </span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div
                            className="bg-blue-600 h-2 rounded-full"
                            style={{ width: `${Math.min(100, (protocol.total_macros?.net_carbs || 0) / 50 * 100)}%` }}
                          />
                        </div>
                        <p className="text-xs text-muted-foreground mt-1">
                          Target: &lt;50g (Keto)
                        </p>
                      </div>
                      
                      <div>
                        <div className="flex justify-between mb-1">
                          <span className="text-sm">Protein</span>
                          <span className="text-sm font-semibold">
                            {protocol.total_macros?.protein?.toFixed(1) || 0}g
                          </span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div
                            className="bg-green-600 h-2 rounded-full"
                            style={{ width: `${Math.min(100, (protocol.total_macros?.protein || 0) / (protocol.protein_target || 1) * 100)}%` }}
                          />
                        </div>
                        <p className="text-xs text-muted-foreground mt-1">
                          Target: {protocol.protein_target?.toFixed(1) || 0}g
                        </p>
                        {protocol.protein_reasoning && (
                          <p className="text-xs text-blue-600 mt-1 italic">
                            {protocol.protein_reasoning}
                          </p>
                        )}
                      </div>
                      
                      <div>
                        <div className="flex justify-between mb-1">
                          <span className="text-sm">Fat</span>
                          <span className="text-sm font-semibold">
                            {protocol.total_macros?.fat?.toFixed(1) || 0}g
                          </span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div
                            className="bg-purple-600 h-2 rounded-full"
                            style={{ width: `${Math.min(100, (protocol.total_macros?.fat || 0) / 150 * 100)}%` }}
                          />
                        </div>
                      </div>
                      
                      <div>
                        <div className="flex justify-between">
                          <span className="text-sm font-medium">Calories</span>
                          <span className="text-sm font-bold">
                            {protocol.total_macros?.calories?.toFixed(0) || 0}
                          </span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="mt-4 pt-4 border-t">
                      <div className="flex items-center justify-between">
                        <span className="text-sm font-medium">Keto Score</span>
                        <span className={`text-lg font-bold ${
                          protocol.keto_compatible ? 'text-green-600' : 'text-red-600'
                        }`}>
                          {protocol.keto_score?.toFixed(0) || 0}/100
                        </span>
                      </div>
                      {protocol.keto_compatible ? (
                        <p className="text-xs text-green-600 mt-1">✓ Keto compatible</p>
                      ) : (
                        <p className="text-xs text-red-600 mt-1">⚠️ Exceeds keto limits</p>
                      )}
                    </div>
                  </CardContent>
                </Card>

                {/* Glutamine Score */}
                <Card className="shadow-lg border-0 bg-gradient-to-br from-purple-50 to-indigo-50">
                  <CardHeader>
                    <CardTitle>Glutamine Competition</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-center">
                      <div className="text-4xl font-bold text-purple-600 mb-2">
                        {protocol.estimated_glutamine_competition_score?.toFixed(0) || 0}
                      </div>
                      <p className="text-sm text-muted-foreground">
                        Competition Score / 100
                      </p>
                      <div className="mt-4 w-full bg-gray-200 rounded-full h-2">
                        <motion.div
                          className="bg-purple-600 h-2 rounded-full"
                          initial={{ width: 0 }}
                          animate={{ width: `${protocol.estimated_glutamine_competition_score || 0}%` }}
                          transition={{ duration: 0.5 }}
                        />
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Shopping List */}
                <Card className="border-0 shadow-premium">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <ShoppingCart size={20} />
                      Shopping List
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <GroceryList protocol={protocol} />
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

