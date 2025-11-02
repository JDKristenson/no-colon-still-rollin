import axios from 'axios'

// Use environment variable for API URL, fallback to relative path
// If VITE_API_URL is set to full Railway URL, ensure it includes /api suffix
let API_URL = import.meta.env.VITE_API_URL || '/api'

// If API_URL is a full URL (starts with http) and doesn't end with /api, add it
if (API_URL.startsWith('http') && !API_URL.endsWith('/api') && !API_URL.endsWith('/api/')) {
  // Ensure there's a trailing slash before appending /api
  API_URL = API_URL.replace(/\/$/, '') + '/api'
}

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

