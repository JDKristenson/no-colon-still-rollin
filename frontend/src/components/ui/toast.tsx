import * as React from "react"
import { cn } from "@/lib/utils"
import { X, CheckCircle2, AlertCircle, Info, AlertTriangle } from "lucide-react"
import { motion, AnimatePresence } from "framer-motion"

export interface ToastProps {
  id?: string
  title?: string
  description?: string
  variant?: "default" | "success" | "error" | "warning" | "info"
  duration?: number
  onClose?: () => void
}

const Toast = React.forwardRef<HTMLDivElement, ToastProps>(
  ({ title, description, variant = "default", onClose, ...props }, ref) => {
    const icons = {
      default: Info,
      success: CheckCircle2,
      error: AlertCircle,
      warning: AlertTriangle,
      info: Info,
    }

    const styles = {
      default: "bg-white border-gray-200",
      success: "bg-green-50 border-green-200 text-green-900",
      error: "bg-red-50 border-red-200 text-red-900",
      warning: "bg-amber-50 border-amber-200 text-amber-900",
      info: "bg-blue-50 border-blue-200 text-blue-900",
    }

    const Icon = icons[variant]

    return (
      <motion.div
        ref={ref}
        initial={{ opacity: 0, y: -20, scale: 0.95 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        exit={{ opacity: 0, scale: 0.95, transition: { duration: 0.2 } }}
        className={cn(
          "rounded-lg border shadow-premium-lg p-4 pr-8 min-w-[300px] max-w-md",
          styles[variant]
        )}
        {...props}
      >
        <div className="flex items-start gap-3">
          <Icon
            className={cn(
              "flex-shrink-0 mt-0.5",
              variant === "success" && "text-green-600",
              variant === "error" && "text-red-600",
              variant === "warning" && "text-amber-600",
              variant === "info" && "text-blue-600"
            )}
            size={20}
          />
          <div className="flex-1">
            {title && (
              <div className="font-semibold text-sm mb-1">{title}</div>
            )}
            {description && (
              <div className="text-sm opacity-90">{description}</div>
            )}
          </div>
          {onClose && (
            <button
              onClick={onClose}
              className="absolute top-2 right-2 rounded-md p-1 hover:bg-black/5 transition-colors"
            >
              <X size={14} />
            </button>
          )}
        </div>
      </motion.div>
    )
  }
)
Toast.displayName = "Toast"

export { Toast }

