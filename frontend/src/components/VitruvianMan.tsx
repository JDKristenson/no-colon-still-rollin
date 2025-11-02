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
  const muscleAreas = {
    chest: { x: 40, y: 28, w: 20, h: 15 },
    back: { x: 38, y: 30, w: 24, h: 20 },
    shoulders: { x: 35, y: 22, w: 30, h: 12 },
    legs: { x: 38, y: 55, w: 24, h: 35 },
    core: { x: 42, y: 43, w: 16, h: 18 },
    arms: { x: 18, y: 25, w: 64, h: 45 },
  }

  const muscleGroups = [
    { name: 'chest', label: 'Chest', position: { x: 50, y: 35 } },
    { name: 'back', label: 'Back', position: { x: 50, y: 45 } },
    { name: 'shoulders', label: 'Shoulders', position: { x: 50, y: 25 } },
    { name: 'legs', label: 'Legs', position: { x: 50, y: 75 } },
    { name: 'core', label: 'Core', position: { x: 50, y: 50 } },
    { name: 'arms', label: 'Arms', position: { x: 50, y: 40 } },
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
          <circle id="vitruvianCircle" cx="50" cy="50" r="45" fill="none" stroke="#CBD5E1" strokeWidth="0.5" opacity="0.6" />
          
          {/* Vitruvian Square */}
          <rect id="vitruvianSquare" x="5" y="5" width="90" height="90" fill="none" stroke="#CBD5E1" strokeWidth="0.5" opacity="0.6" />
        </defs>

        {/* Background - Vitruvian Circle and Square */}
        <use href="#vitruvianCircle" />
        <use href="#vitruvianSquare" />

        {/* Actual Vitruvian Man - Leonardo da Vinci's Proportions */}
        <g id="vitruvianMan" opacity="0.95">
          {/* Head - proportional to body */}
          <ellipse cx="50" cy="16" rx="5" ry="6" fill="#F5E6D3" stroke="#2D3748" strokeWidth="0.4" />
          
          {/* Neck */}
          <rect x="48" y="22" width="4" height="3" rx="0.5" fill="#F5E6D3" stroke="#2D3748" strokeWidth="0.3" />
          
          {/* Torso - core of the figure */}
          <rect x="44" y="25" width="12" height="20" rx="1.5" fill="#F5E6D3" stroke="#2D3748" strokeWidth="0.4" />
          
          {/* Chest definition */}
          <path
            d="M 46 28 Q 50 26 54 28 Q 53 32 50 33 Q 47 32 46 28 Z"
            fill="none"
            stroke="#2D3748"
            strokeWidth="0.3"
            opacity="0.4"
          />
          
          {/* Arms - Extended Vitruvian pose */}
          {/* Left arm */}
          <path
            d="M 44 28 Q 30 30 18 38 Q 12 42 10 48 Q 8 54 12 58 Q 20 62 30 60 Q 40 58 44 50"
            fill="none"
            stroke="#2D3748"
            strokeWidth="0.6"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
          
          {/* Right arm */}
          <path
            d="M 56 28 Q 70 30 82 38 Q 88 42 90 48 Q 92 54 88 58 Q 80 62 70 60 Q 60 58 56 50"
            fill="none"
            stroke="#2D3748"
            strokeWidth="0.6"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
          
          {/* Hands */}
          <ellipse cx="12" cy="58" rx="2.5" ry="3.5" fill="#F5E6D3" stroke="#2D3748" strokeWidth="0.3" />
          <ellipse cx="88" cy="58" rx="2.5" ry="3.5" fill="#F5E6D3" stroke="#2D3748" strokeWidth="0.3" />
          
          {/* Legs - Standing position */}
          {/* Left leg */}
          <path
            d="M 48 45 L 42 72 L 38 88 L 44 88 L 46 72 Z"
            fill="#F5E6D3"
            stroke="#2D3748"
            strokeWidth="0.5"
            strokeLinejoin="round"
          />
          
          {/* Right leg */}
          <path
            d="M 52 45 L 58 72 L 62 88 L 56 88 L 54 72 Z"
            fill="#F5E6D3"
            stroke="#2D3748"
            strokeWidth="0.5"
            strokeLinejoin="round"
          />
          
          {/* Feet */}
          <ellipse cx="40" cy="88" rx="4" ry="2.5" fill="#F5E6D3" stroke="#2D3748" strokeWidth="0.3" />
          <ellipse cx="60" cy="88" rx="4" ry="2.5" fill="#F5E6D3" stroke="#2D3748" strokeWidth="0.3" />
          
          {/* Subtle anatomical details */}
          <ellipse cx="48" cy="16" rx="1" ry="1.5" fill="#2D3748" opacity="0.6" />
          <ellipse cx="52" cy="16" rx="1" ry="1.5" fill="#2D3748" opacity="0.6" />
          <path d="M 48 19 Q 50 20 52 19" stroke="#2D3748" strokeWidth="0.3" fill="none" opacity="0.4" />
        </g>

        {/* Muscle Overlays - Interactive soreness visualization */}
        {Object.entries(muscleAreas).map(([muscleName, area]) => {
          const intensity = soreness[muscleName] ?? 0
          const isHovered = hoveredMuscle === muscleName

          return (
            <motion.rect
              key={muscleName}
              x={`${area.x}%`}
              y={`${area.y}%`}
              width={`${area.w}%`}
              height={`${area.h}%`}
              fill={getSorenessColor(intensity)}
              opacity={intensity > 0 ? getSorenessOpacity(intensity) : 0}
              rx="3"
              stroke={isHovered ? '#1e40af' : intensity > 0 ? getSorenessColor(intensity) : 'none'}
              strokeWidth={isHovered ? 1.5 : 0.5}
              onMouseEnter={() => handleMuscleHover(muscleName)}
              onMouseLeave={handleMuscleLeave}
              onClick={() => handleMuscleClick(muscleName)}
              style={{ cursor: interactive ? 'pointer' : 'default' }}
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
                x={`${muscle.position.x - 10}%`}
                y={`${muscle.position.y - 4}%`}
                width="20%"
                height="6%"
                fill="rgba(30, 58, 138, 0.95)"
                rx="3"
              />
              <text
                x={`${muscle.position.x}%`}
                y={`${muscle.position.y}%`}
                textAnchor="middle"
                fill="white"
                fontSize="2.5"
                fontWeight="700"
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
