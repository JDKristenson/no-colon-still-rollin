import { motion } from 'framer-motion'
import { useState } from 'react'

interface VitruvianManProps {
  soreness: Record<string, number>
  onMuscleClick?: (muscle: string) => void
  interactive?: boolean
}

// Premium color mapping with smooth gradients
const getSorenessColor = (intensity: number): string => {
  if (intensity === 0) return 'rgba(229, 231, 235, 0.1)'
  if (intensity <= 2) return 'rgba(59, 130, 246, 0.5)'
  if (intensity <= 4) return 'rgba(59, 130, 246, 0.6)'
  if (intensity <= 6) return 'rgba(139, 92, 246, 0.7)'
  if (intensity <= 8) return 'rgba(239, 68, 68, 0.8)'
  return 'rgba(220, 38, 38, 0.9)'
}

const getSorenessOpacity = (intensity: number): number => {
  if (intensity === 0) return 0
  return Math.max(0.5, Math.min(0.95, intensity / 10))
}

export default function VitruvianMan({ soreness, onMuscleClick, interactive = true }: VitruvianManProps) {
  const [hoveredMuscle, setHoveredMuscle] = useState<string | null>(null)

  // Muscle group overlay areas (percentage-based for responsiveness)
  // These coordinates are positioned to overlay on the actual Vitruvian Man image
  const muscleAreas = {
    chest: { x: 42, y: 30, w: 16, h: 12 },
    back: { x: 38, y: 32, w: 24, h: 18 },
    shoulders: { x: 38, y: 24, w: 24, h: 10 },
    legs: { x: 40, y: 58, w: 20, h: 32 },
    core: { x: 44, y: 45, w: 12, h: 15 },
    arms: { x: 25, y: 26, w: 50, h: 42 },
  }

  const muscleGroups = [
    { name: 'chest', label: 'Chest', position: { x: 50, y: 36 } },
    { name: 'back', label: 'Back', position: { x: 50, y: 44 } },
    { name: 'shoulders', label: 'Shoulders', position: { x: 50, y: 28 } },
    { name: 'legs', label: 'Legs', position: { x: 50, y: 75 } },
    { name: 'core', label: 'Core', position: { x: 50, y: 52 } },
    { name: 'arms', label: 'Arms', position: { x: 50, y: 42 } },
  ]

  const handleMuscleHover = (muscle: string) => {
    if (interactive) setHoveredMuscle(muscle)
  }

  const handleMuscleLeave = () => {
    setHoveredMuscle(null)
  }

  const handleMuscleClick = (muscle: string) => {
    if (interactive && onMuscleClick) {
      onMuscleClick(muscle)
    }
  }

  // Try to load the actual image from public folder, fallback to CDN if needed
  const vitruvianImageUrl = '/vitruvian-man.jpg'

  return (
    <div className="w-full max-w-4xl mx-auto relative">
      <div className="relative" style={{ aspectRatio: '1/1', maxWidth: '600px', margin: '0 auto' }}>
        {/* Actual Vitruvian Man Image */}
        <img
          src={vitruvianImageUrl}
          alt="Vitruvian Man by Leonardo da Vinci"
          className="w-full h-full object-contain"
          style={{ 
            filter: 'drop-shadow(0 10px 30px rgba(0, 0, 0, 0.15))',
          }}
          onError={(e) => {
            // Fallback to high-quality Wikimedia image
            const target = e.target as HTMLImageElement
            console.log('Local image failed, using Wikimedia fallback')
            target.src = 'https://upload.wikimedia.org/wikipedia/commons/1/14/Vitruvian_Man_by_Leonardo_da_Vinci.jpg'
          }}
        />
        
        {/* Overlay SVG for interactive muscle mapping */}
        <svg
          className="absolute inset-0 w-full h-full pointer-events-none"
          style={{ mixBlendMode: 'multiply' }}
          viewBox="0 0 100 100"
          preserveAspectRatio="xMidYMid meet"
        >
          {/* Muscle Overlays - Interactive soreness visualization */}
          {Object.entries(muscleAreas).map(([muscleName, area]) => {
            const intensity = soreness[muscleName] ?? 0
            const isHovered = hoveredMuscle === muscleName

            if (intensity === 0 && !isHovered) return null

            return (
              <motion.rect
                key={muscleName}
                x={`${area.x}%`}
                y={`${area.y}%`}
                width={`${area.w}%`}
                height={`${area.h}%`}
                fill={getSorenessColor(intensity)}
                opacity={getSorenessOpacity(intensity)}
                rx="2"
                stroke={isHovered ? '#1e40af' : intensity > 0 ? getSorenessColor(intensity) : 'none'}
                strokeWidth={isHovered ? 2 : 1}
                onMouseEnter={() => handleMuscleHover(muscleName)}
                onMouseLeave={handleMuscleLeave}
                onClick={() => handleMuscleClick(muscleName)}
                style={{ cursor: interactive ? 'pointer' : 'default', pointerEvents: 'all' }}
                animate={{
                  opacity: isHovered && intensity > 0 
                    ? Math.min(0.95, getSorenessOpacity(intensity) + 0.15) 
                    : getSorenessOpacity(intensity),
                  scale: isHovered ? 1.02 : 1,
                }}
                transition={{ duration: 0.2 }}
              />
            )
          })}

          {/* Labels on hover */}
          {hoveredMuscle && (() => {
            const muscle = muscleGroups.find(m => m.name === hoveredMuscle)
            const intensity = soreness[hoveredMuscle!] ?? 0
            if (!muscle) return null

            return (
              <motion.g
                initial={{ opacity: 0, y: -5 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.2 }}
              >
                <rect
                  x={`${muscle.position.x - 12}%`}
                  y={`${muscle.position.y - 4}%`}
                  width="24%"
                  height="6%"
                  fill="rgba(30, 58, 138, 0.95)"
                  rx="3"
                />
                <text
                  x={`${muscle.position.x}%`}
                  y={`${muscle.position.y}%`}
                  textAnchor="middle"
                  fill="white"
                  fontSize="3"
                  fontWeight="700"
                  dominantBaseline="middle"
                >
                  {muscle.label}: {intensity}/10
                </text>
              </motion.g>
            )
          })()}
        </svg>
      </div>

      {/* Premium legend */}
      <div className="mt-6 flex flex-wrap gap-4 justify-center">
        {[
          { color: 'rgba(229, 231, 235, 0.3)', label: 'No Soreness', range: '0' },
          { color: 'rgba(59, 130, 246, 0.6)', label: 'Mild', range: '1-4' },
          { color: 'rgba(139, 92, 246, 0.7)', label: 'Moderate', range: '5-6' },
          { color: 'rgba(239, 68, 68, 0.8)', label: 'Sore', range: '7-8' },
          { color: 'rgba(220, 38, 38, 0.9)', label: 'Very Sore', range: '9-10' },
        ].map((item, idx) => (
          <motion.div
            key={idx}
            className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-white/80 backdrop-blur-sm border border-gray-200/50 shadow-sm"
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: idx * 0.1 }}
          >
            <div 
              className="w-3 h-3 rounded-full" 
              style={{ backgroundColor: item.color }}
            />
            <span className="text-xs font-medium text-gray-700">{item.label}</span>
            <span className="text-xs text-gray-500">({item.range})</span>
          </motion.div>
        ))}
      </div>
    </div>
  )
}
