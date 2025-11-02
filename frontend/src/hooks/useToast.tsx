import { useState, useCallback } from 'react'
import { Toast, ToastProps } from '@/components/ui/toast'
import { AnimatePresence } from 'framer-motion'

interface ToastState extends ToastProps {
  id: string
}

let toastId = 0

export function useToast() {
  const [toasts, setToasts] = useState<ToastState[]>([])

  const addToast = useCallback((props: ToastProps) => {
    const id = `toast-${toastId++}`
    const toast: ToastState = { ...props, id }
    
    setToasts((prev) => [...prev, toast])

    const duration = props.duration ?? 5000
    if (duration > 0) {
      setTimeout(() => {
        removeToast(id)
      }, duration)
    }

    return id
  }, [])

  const removeToast = useCallback((id: string) => {
    setToasts((prev) => prev.filter((toast) => toast.id !== id))
  }, [])

  const toast = useCallback((props: ToastProps) => {
    return addToast(props)
  }, [addToast])

  const ToastContainer = () => (
    <div className="fixed top-4 right-4 z-[100] flex flex-col gap-2 pointer-events-none">
      <AnimatePresence>
        {toasts.map((toastItem) => (
          <div key={toastItem.id} className="pointer-events-auto">
            <Toast
              {...toastItem}
              onClose={() => removeToast(toastItem.id)}
            />
          </div>
        ))}
      </AnimatePresence>
    </div>
  )

  return {
    toast,
    success: (title: string, description?: string) =>
      toast({ title, description, variant: 'success' }),
    error: (title: string, description?: string) =>
      toast({ title, description, variant: 'error' }),
    warning: (title: string, description?: string) =>
      toast({ title, description, variant: 'warning' }),
    info: (title: string, description?: string) =>
      toast({ title, description, variant: 'info' }),
    ToastContainer,
  }
}

