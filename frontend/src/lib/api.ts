import axios from 'axios'

// Use environment variable for API URL, fallback to relative path
const API_URL = import.meta.env.VITE_API_URL || '/api'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    // Log error for debugging
    if (error.response?.status >= 500) {
      console.error('Server error:', error.response?.data)
    }
    // Log network errors (connection issues)
    if (error.code === 'ERR_NETWORK' || error.message?.includes('Network Error')) {
      console.error('Network error - cannot reach backend:', {
        baseURL: API_URL,
        error: error.message
      })
    }
    return Promise.reject(error)
  }
)

export default api

