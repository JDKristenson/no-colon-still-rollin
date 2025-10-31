import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { AuthProvider } from './contexts/AuthContext'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Protocol from './pages/Protocol'
import Workouts from './pages/Workouts'
import Soreness from './pages/Soreness'
import Progress from './pages/Progress'
import Exercises from './pages/Exercises'
import Research from './pages/Research'
import Settings from './pages/Settings'
import ProtectedRoute from './components/ProtectedRoute'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
})

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route
              path="/*"
              element={
                <ProtectedRoute>
                  <Routes>
                    <Route path="/dashboard" element={<Dashboard />} />
                    <Route path="/protocol" element={<Protocol />} />
                    <Route path="/workouts" element={<Workouts />} />
                    <Route path="/soreness" element={<Soreness />} />
                    <Route path="/progress" element={<Progress />} />
                    <Route path="/exercises" element={<Exercises />} />
                    <Route path="/research" element={<Research />} />
                    <Route path="/settings" element={<Settings />} />
                    <Route path="/" element={<Navigate to="/dashboard" replace />} />
                  </Routes>
                </ProtectedRoute>
              }
            />
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </QueryClientProvider>
  )
}

export default App

