import { AxiosError } from 'axios'

export function getErrorMessage(error: unknown): string {
  if (error instanceof AxiosError) {
    return error.response?.data?.detail || error.message || 'An error occurred'
  }
  
  if (error instanceof Error) {
    return error.message
  }
  
  return 'An unexpected error occurred'
}

export function handleApiError(error: unknown): void {
  const message = getErrorMessage(error)
  console.error('API Error:', message)
  // Could integrate with error tracking service here (e.g., Sentry)
}

