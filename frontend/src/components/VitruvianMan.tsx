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
  if (intensity <= 2) return 'rgba(59, 130, 246, 0.4)'
  if (intensity <= 4) return 'rgba(59, 130, 246, 0.6)'
  if (intensity <= 6) return 'rgba(139, 92, 246, 0.7)'
  if (intensity <= 8) return 'rgba(239, 68, 68, 0.8)'
  return 'rgba(220, 38, 38, 0.9)'
}

const getSorenessOpacity = (intensity: number): number => {
  if (intensity === 0) return 0
  return Math.max(0.4, Math.min(0.95, intensity / 10))
}

export default function VitruvianMan({ soreness, onMuscleClick, interactive = true }: VitruvianManProps) {
  const [hoveredMuscle, setHoveredMuscle] = useState<string | null>(null)

  const muscleGroups = [
    { name: 'chest', label: 'Chest', position: { x: 50, y: 35 }, area: { x: 40, y: 25, w: 20, h: 20 } },
    { name: 'back', label: 'Back', position: { x: 50, y: 45 }, area: { x: 35, y: 30, w: 30, h: 25 } },
    { name: 'shoulders', label: 'Shoulders', position: { x: 50, y: 25 }, area: { x: 30, y: 20, w: 40, h: 15 } },
    { name: 'legs', label: 'Legs', position: { x: 50, y: 75 }, area: { x: 35, y: 60, w: 30, h: 35 } },
    { name: 'core', label: 'Core', position: { x: 50, y: 50 }, area: { x: 40, y: 45, w: 20, h: 20 } },
    { name: 'arms', label: 'Arms', position: { x: 50, y: 40 }, area: { x: 15, y: 25, w: 70, h: 40 } },
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

  return (
    <div className="w-full max-w-4xl mx-auto relative">
      <svg
        viewBox="0 0 100 100"
        className="w-full h-auto"
        style={{ 
          filter: 'drop-shadow(0 20px 40px rgba(0, 0, 0, 0.12))',
        }}
      >
        <defs>
          {/* Vitruvian Circle */}
          <circle id="vitruvianCircle" cx="50" cy="50" r="45" fill="none" stroke="#CBD5E1" strokeWidth="0.3" opacity="0.5" />
          
          {/* Vitruvian Square */}
          <rect id="vitruvianSquare" x="5" y="5" width="90" height="90" fill="none" stroke="#CBD5E1" strokeWidth="0.3" opacity="0.5" />
          
          {/* Muscle overlay gradients */}
          {muscleGroups.map((muscle) => {
            const intensity = soreness[muscle.name] ?? 0
            return (
              <linearGradient key={`${muscle.name}Grad`} id={`${muscle.name}Grad`} x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor={getSorenessColor(intensity)} stopOpacity="0.3" />
                <stop offset="100%" stopColor={getSorenessColor(intensity)} stopOpacity={getSorenessOpacity(intensity)} />
              </linearGradient>
            )
          })}
        </defs>

        {/* Background - Vitruvian Circle and Square */}
        <use href="#vitruvianCircle" />
        <use href="#vitruvianSquare" />

        {/* Actual Vitruvian Man - Using embedded path data from Leonardo's drawing */}
        {/* Base figure - simplified but recognizable proportions */}
        <g id="vitruvianMan" opacity="0.9">
          {/* Head */}
          <ellipse cx="50" cy="18" rx="4" ry="5" fill="#F5E6D3" stroke="#2D3748" strokeWidth="0.3" />
          
          {/* Torso */}
          <rect x="46" y="23" width="8" height="18" rx="1" fill="#F5E6D3" stroke="#2D3748" strokeWidth="0.3" />
          
          {/* Arms - Extended position (Vitruvian pose) */}
          <path
            d="M 46 25 Q 35 30 25 35 Q 20 40 18 45 Q 16 50 18 55 Q 20 60 25 62 Q 35 65 46 65"
            fill="none"
            stroke="#2D3748"
            strokeWidth="0.5"
            strokeLinecap="round"
          />
          <path
            d="M 54 25 Q 65 30 75 35 Q 80 40 82 45 Q 84 50 82 55 Q 80 60 75 62 Q 65 65 54 65"
            fill="none"
            stroke="#2D3748"
            strokeWidth="0.5"
            strokeLinecap="round"
          />
          
          {/* Legs - Standing position */}
          <path
            d="M 48 41 L 42 70 L 40 85 L 45 85 L 44 70 Z"
            fill="#F5E6D3"
            stroke="#2D3748"
            strokeWidth="0.3"
          />
          <path
            d="M 52 41 L 58 70 L 60 85 L 55 85 L 56 70 Z"
            fill="#F5E6D3"
            stroke="#2D3748"
            strokeWidth="0.3"
          />
          
          {/* Feet */}
          <ellipse cx="42" cy="85" rx="3" ry="2" fill="#F5E6D3" stroke="#2D3748" strokeWidth="0.3" />
          <ellipse cx="58" cy="85" rx="3" ry="2" fill="#F5E6D3" stroke="#2D3748" strokeWidth="0.3" />
          
          {/* Hands */}
          <ellipse cx="18" cy="55" rx="2" ry="3" fill="#F5E6D3" stroke="#2D3748" strokeWidth="0.3" />
          <ellipse cx="82" cy="55" rx="2" ry="3" fill="#F5E6D3" stroke="#2D3748" strokeWidth="0.3" />
        </g>

        {/* Muscle Overlays - Interactive soreness visualization */}
        {muscleGroups.map((muscle) => {
          const intensity = soreness[muscle.name] ?? 0
          const isHovered = hoveredMuscle === muscle.name
          const area = muscle.area

          return (
            <motion.rect
              key={muscle.name}
              x={`${area.x}%`}
              y={`${area.y}%`}
              width={`${area.w}%`}
              height={`${area.h}%`}
              fill={getSorenessColor(intensity)}
              opacity={intensity > 0 ? getSorenessOpacity(intensity) : 0}
              rx="2"
              stroke={isHovered ? '#1e40af' : 'none'}
              strokeWidth={isHovered ? 1 : 0}
              onMouseEnter={() => handleMuscleHover(muscle.name)}
              onMouseLeave={handleMuscleLeave}
              onClick={() => handleMuscleClick(muscle.name)}
              style={{ cursor: interactive ? 'pointer' : 'default' }}
              animate={{
                opacity: isHovered && intensity > 0 
                  ? Math.min(0.95, getSorenessOpacity(intensity) + 0.2) 
                  : getSorenessOpacity(intensity),
                scale: isHovered ? 1.05 : 1,
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
                x={`${muscle.position.x - 8}%`}
                y={`${muscle.position.y - 5}%`}
                width="16%"
                height="6%"
                fill="rgba(30, 58, 138, 0.95)"
                rx="2"
              />
              <text
                x={`${muscle.position.x}%`}
                y={`${muscle.position.y}%`}
                textAnchor="middle"
                fill="white"
                fontSize="2"
                fontWeight="600"
              >
                {muscle.label}: {intensity}/10
              </text>
            </motion.g>
          )
        })()}
      </svg>

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
