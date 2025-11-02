import { Link, useLocation } from 'react-router-dom'
import { useAuth } from '@/contexts/AuthContext'
import { motion } from 'framer-motion'
import { Home, UtensilsCrossed, Dumbbell, Activity, TrendingUp, BookOpen, Settings, LogOut, Dna } from 'lucide-react'
import { Button } from './ui/button'

export default function Navigation() {
  const location = useLocation()
  const { logout } = useAuth()
  
  const navItems = [
    { path: '/dashboard', icon: Home, label: 'Dashboard' },
    { path: '/protocol', icon: UtensilsCrossed, label: 'Nutrition' },
    { path: '/workouts', icon: Dumbbell, label: 'Workouts' },
    { path: '/soreness', icon: Activity, label: 'Soreness' },
    { path: '/markers', icon: Dna, label: 'Markers' },
    { path: '/progress', icon: TrendingUp, label: 'Progress' },
    { path: '/research', icon: BookOpen, label: 'Research' },
    { path: '/settings', icon: Settings, label: 'Settings' },
  ]
  
  return (
    <nav className="sticky top-0 z-50 w-full border-b bg-white/80 backdrop-blur-xl supports-[backdrop-filter]:bg-white/60 shadow-sm">
      <div className="container mx-auto px-6 max-w-7xl">
        <div className="flex items-center justify-between h-16">
          {/* Logo Section - Premium */}
          <div className="flex items-center gap-3">
            <motion.div
              whileHover={{ scale: 1.05, rotate: 5 }}
              whileTap={{ scale: 0.95 }}
              className="relative"
            >
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-600 via-indigo-600 to-purple-600 flex items-center justify-center shadow-lg shadow-blue-500/20">
                <span className="text-white font-bold text-sm">NC</span>
              </div>
              <div className="absolute -inset-0.5 bg-gradient-to-br from-blue-600 to-purple-600 rounded-xl blur opacity-20 -z-10" />
            </motion.div>
            <h1 className="text-xl font-bold bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 bg-clip-text text-transparent tracking-tight">
              No Colon, Still Rollin'
            </h1>
          </div>
          
          {/* Navigation Items - Premium */}
          <div className="flex items-center gap-1 overflow-x-auto scrollbar-hide">
            {navItems.map((item, idx) => {
              const Icon = item.icon
              const isActive = location.pathname === item.path
              
              return (
                <Link key={item.path} to={item.path}>
                  <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: idx * 0.05 }}
                    whileHover={{ y: -2 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    <Button
                      variant={isActive ? "default" : "ghost"}
                      className={`flex items-center gap-2 whitespace-nowrap transition-all duration-200 ${
                        isActive 
                          ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-md shadow-blue-500/20' 
                          : 'hover:bg-gray-100/80 hover:text-blue-600'
                      }`}
                      size="sm"
                    >
                      <Icon size={18} className={isActive ? 'text-white' : ''} />
                      <span className="hidden lg:inline font-medium">{item.label}</span>
                    </Button>
                  </motion.div>
                </Link>
              )
            })}
            
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: navItems.length * 0.05 }}
              whileHover={{ y: -2 }}
              whileTap={{ scale: 0.95 }}
            >
              <Button
                variant="ghost"
                onClick={logout}
                className="flex items-center gap-2 text-red-600 hover:text-red-700 hover:bg-red-50 whitespace-nowrap transition-all duration-200"
                size="sm"
              >
                <LogOut size={18} />
                <span className="hidden lg:inline font-medium">Logout</span>
              </Button>
            </motion.div>
          </div>
        </div>
      </div>
    </nav>
  )
}

