import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { AuthProvider } from './contexts/AuthContext'
import { ErrorBoundary } from './components/ErrorBoundary'
import { useToast } from './hooks/useToast'
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
import Markers from './pages/Markers'
import ProtectedRoute from './components/ProtectedRoute'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
})

function AppContent() {
  const { ToastContainer } = useToast()
  
  return (
    <>
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
                      <Route path="/markers" element={<Markers />} />
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
      <ToastContainer />
    </>
  )
}

function App() {
  return (
    <ErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <AuthProvider>
          <AppContent />
        </AuthProvider>
      </QueryClientProvider>
    </ErrorBoundary>
  )
}

export default App

