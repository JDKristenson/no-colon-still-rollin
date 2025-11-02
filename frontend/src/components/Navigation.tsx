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
    <nav className="glass border-b border-gray-200/50 sticky top-0 z-50 shadow-sm">
      <div className="container mx-auto px-4 max-w-7xl">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-600 to-indigo-600 flex items-center justify-center">
              <span className="text-white font-bold text-sm">NC</span>
            </div>
            <h1 className="text-xl font-bold bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 bg-clip-text text-transparent tracking-tight">
              No Colon, Still Rollin'
            </h1>
          </div>
          
          <div className="flex items-center gap-1 overflow-x-auto">
            {navItems.map((item) => {
              const Icon = item.icon
              const isActive = location.pathname === item.path
              
              return (
                <Link key={item.path} to={item.path}>
                  <motion.div
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    <Button
                      variant={isActive ? "default" : "ghost"}
                      className="flex items-center gap-2 whitespace-nowrap"
                      size="sm"
                    >
                      <Icon size={18} />
                      <span className="hidden lg:inline">{item.label}</span>
                    </Button>
                  </motion.div>
                </Link>
              )
            })}
            
            <Button
              variant="ghost"
              onClick={logout}
              className="flex items-center gap-2 text-red-600 hover:text-red-700 whitespace-nowrap"
              size="sm"
            >
              <LogOut size={18} />
              <span className="hidden lg:inline">Logout</span>
            </Button>
          </div>
        </div>
      </div>
    </nav>
  )
}

