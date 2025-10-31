import { Link, useLocation } from 'react-router-dom'
import { useAuth } from '@/contexts/AuthContext'
import { motion } from 'framer-motion'
import { Home, UtensilsCrossed, Dumbbell, Activity, TrendingUp, BookOpen, Settings, LogOut } from 'lucide-react'
import { Button } from './ui/button'

export default function Navigation() {
  const location = useLocation()
  const { logout } = useAuth()
  
  const navItems = [
    { path: '/dashboard', icon: Home, label: 'Dashboard' },
    { path: '/protocol', icon: UtensilsCrossed, label: 'Nutrition' },
    { path: '/workouts', icon: Dumbbell, label: 'Workouts' },
    { path: '/soreness', icon: Activity, label: 'Soreness' },
    { path: '/progress', icon: TrendingUp, label: 'Progress' },
    { path: '/research', icon: BookOpen, label: 'Research' },
    { path: '/settings', icon: Settings, label: 'Settings' },
  ]
  
  return (
    <nav className="bg-white/80 backdrop-blur-lg border-b border-gray-200 sticky top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center gap-2">
            <h1 className="text-xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
              No Colon, Still Rollin'
            </h1>
          </div>
          
          <div className="flex items-center gap-1">
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
                      className="flex items-center gap-2"
                    >
                      <Icon size={18} />
                      <span className="hidden md:inline">{item.label}</span>
                    </Button>
                  </motion.div>
                </Link>
              )
            })}
            
            <Button
              variant="ghost"
              onClick={logout}
              className="flex items-center gap-2 text-red-600 hover:text-red-700"
            >
              <LogOut size={18} />
              <span className="hidden md:inline">Logout</span>
            </Button>
          </div>
        </div>
      </div>
    </nav>
  )
}

