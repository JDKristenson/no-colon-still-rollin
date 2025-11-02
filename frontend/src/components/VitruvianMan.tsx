import { motion } from 'framer-motion'
import { useState } from 'react'

interface VitruvianManProps {
  soreness: Record<string, number>
  onMuscleClick?: (muscle: string) => void
  interactive?: boolean
}

// Color mapping: 0 (no soreness) = light gray, 10 (very sore) = deep red
const getSorenessColor = (intensity: number): string => {
  if (intensity === 0) return '#E5E7EB' // light gray
  if (intensity <= 2) return '#DBEAFE' // light blue
  if (intensity <= 4) return '#93C5FD' // blue
  if (intensity <= 6) return '#60A5FA' // medium blue
  if (intensity <= 8) return '#8B5CF6' // purple
  return '#EF4444' // red (very sore)
}

const getSorenessOpacity = (intensity: number): number => {
  if (intensity === 0) return 0.1
  return Math.max(0.4, intensity / 10)
}

export default function VitruvianMan({ soreness, onMuscleClick, interactive = true }: VitruvianManProps) {
  const [hoveredMuscle, setHoveredMuscle] = useState<string | null>(null)

  const muscleGroups = [
    { name: 'chest', label: 'Chest', position: { x: 250, y: 180 } },
    { name: 'back', label: 'Back', position: { x: 250, y: 180 } },
    { name: 'shoulders', label: 'Shoulders', position: { x: 250, y: 140 } },
    { name: 'legs', label: 'Legs', position: { x: 250, y: 380 } },
    { name: 'core', label: 'Core', position: { x: 250, y: 280 } },
    { name: 'arms', label: 'Arms', position: { x: 250, y: 220 } },
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

  // Get muscle regions for Vitruvian Man based on Leonardo's proportions
  const getMusclePaths = (muscle: string) => {
    const baseOpacity = getSorenessOpacity(soreness[muscle] ?? 0)
    const color = getSorenessColor(soreness[muscle] ?? 0)
    const isHovered = hoveredMuscle === muscle
    
    switch (muscle) {
      case 'chest':
        return {
          d: 'M 220 180 Q 250 160 280 180 L 275 230 Q 250 240 225 230 Z',
          fill: color,
          opacity: isHovered ? Math.min(1, baseOpacity + 0.2) : baseOpacity,
          stroke: isHovered ? '#1e40af' : '#334155',
          strokeWidth: isHovered ? 2 : 1,
        }
      case 'back':
        return {
          d: 'M 220 180 Q 250 160 280 180 L 275 230 Q 250 240 225 230 Z',
          fill: color,
          opacity: baseOpacity * 0.8,
          stroke: 'none',
          strokeWidth: 0,
        }
      case 'shoulders':
        return {
          d: 'M 200 140 Q 250 120 300 140 Q 310 150 305 170 L 295 180 Q 250 175 205 180 L 195 170 Q 190 150 200 140 Z',
          fill: color,
          opacity: isHovered ? Math.min(1, baseOpacity + 0.2) : baseOpacity,
          stroke: isHovered ? '#1e40af' : '#334155',
          strokeWidth: isHovered ? 2 : 1,
        }
      case 'legs':
        return {
          d: 'M 230 320 L 210 420 L 215 450 L 235 445 L 230 415 Z M 270 320 L 290 420 L 285 450 L 265 445 L 270 415 Z',
          fill: color,
          opacity: isHovered ? Math.min(1, baseOpacity + 0.2) : baseOpacity,
          stroke: isHovered ? '#1e40af' : '#334155',
          strokeWidth: isHovered ? 2 : 1,
        }
      case 'core':
        return {
          d: 'M 225 230 Q 250 260 275 230 Q 270 280 250 285 Q 230 280 225 230 Z',
          fill: color,
          opacity: isHovered ? Math.min(1, baseOpacity + 0.2) : baseOpacity,
          stroke: isHovered ? '#1e40af' : '#334155',
          strokeWidth: isHovered ? 2 : 1,
        }
      case 'arms':
        return {
          paths: [
            { d: 'M 195 170 Q 150 200 130 250 Q 125 270 135 275 Q 150 270 155 255 Q 160 230 185 200 Z', fill: color, opacity: isHovered ? Math.min(1, baseOpacity + 0.2) : baseOpacity },
            { d: 'M 305 170 Q 350 200 370 250 Q 375 270 365 275 Q 350 270 345 255 Q 340 230 315 200 Z', fill: color, opacity: isHovered ? Math.min(1, baseOpacity + 0.2) : baseOpacity },
          ],
          stroke: isHovered ? '#1e40af' : '#334155',
          strokeWidth: isHovered ? 2 : 1,
        }
      default:
        return null
    }
  }

  return (
    <div className="w-full max-w-3xl mx-auto relative">
      <svg
        viewBox="0 0 500 500"
        className="w-full h-auto"
        style={{ filter: 'drop-shadow(0 10px 25px rgba(0, 0, 0, 0.1))' }}
      >
        <defs>
          <linearGradient id="skinGradient" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#FAF9F6" stopOpacity="1" />
            <stop offset="100%" stopColor="#F5F3F0" stopOpacity="1" />
          </linearGradient>
        </defs>

        {/* Circle (Vitruvian proportion) */}
        <circle
          cx="250"
          cy="250"
          r="200"
          fill="none"
          stroke="#CBD5E1"
          strokeWidth="1.5"
          opacity="0.4"
        />
        
        {/* Square (Vitruvian proportion) */}
        <rect
          x="50"
          y="50"
          width="400"
          height="400"
          fill="none"
          stroke="#CBD5E1"
          strokeWidth="1.5"
          opacity="0.4"
        />

        {/* Back (subtle overlay) */}
        {soreness.back !== undefined && soreness.back > 0 && (
          <motion.path
            {...getMusclePaths('back')}
            onMouseEnter={() => handleMuscleHover('back')}
            onMouseLeave={handleMuscleLeave}
            onClick={() => handleMuscleClick('back')}
            style={{ cursor: interactive ? 'pointer' : 'default' }}
          />
        )}

        {/* Head (proportional circle based on Vitruvian Man) */}
        <circle
          cx="250"
          cy="100"
          r="35"
          fill="url(#skinGradient)"
          stroke="#2D3748"
          strokeWidth="2"
        />

        {/* Neck */}
        <rect x="240" y="135" width="20" height="25" fill="url(#skinGradient)" stroke="#2D3748" strokeWidth="2" rx="2" />

        {/* Torso (proportional rectangle) */}
        <rect
          x="200"
          y="160"
          width="100"
          height="140"
          fill="url(#skinGradient)"
          stroke="#2D3748"
          strokeWidth="2"
          rx="5"
        />

        {/* Chest overlay */}
        <motion.path
          {...getMusclePaths('chest')}
          onMouseEnter={() => handleMuscleHover('chest')}
          onMouseLeave={handleMuscleLeave}
          onClick={() => handleMuscleClick('chest')}
          style={{ cursor: interactive ? 'pointer' : 'default' }}
          transition={{ duration: 0.2 }}
        />

        {/* Shoulders overlay */}
        <motion.path
          {...getMusclePaths('shoulders')}
          onMouseEnter={() => handleMuscleHover('shoulders')}
          onMouseLeave={handleMuscleLeave}
          onClick={() => handleMuscleClick('shoulders')}
          style={{ cursor: interactive ? 'pointer' : 'default' }}
          transition={{ duration: 0.2 }}
        />

        {/* Arms - Left (extended) */}
        <motion.path
          d="M 195 170 Q 150 200 130 250 Q 125 270 135 275 Q 150 270 155 255 Q 160 230 185 200 Z"
          fill={hoveredMuscle === 'arms' ? getSorenessColor(soreness.arms ?? 0) : 'url(#skinGradient)'}
          stroke={hoveredMuscle === 'arms' ? '#1e40af' : '#2D3748'}
          strokeWidth={hoveredMuscle === 'arms' ? 2.5 : 2}
          opacity={hoveredMuscle === 'arms' ? getSorenessOpacity(soreness.arms ?? 0) : 1}
          onMouseEnter={() => handleMuscleHover('arms')}
          onMouseLeave={handleMuscleLeave}
          onClick={() => handleMuscleClick('arms')}
          style={{ cursor: interactive ? 'pointer' : 'default' }}
          transition={{ duration: 0.2 }}
        />
        {/* Hand - Left */}
        <ellipse cx="135" cy="275" rx="8" ry="12" fill="url(#skinGradient)" stroke="#2D3748" strokeWidth="1.5" />

        {/* Arms - Right (extended) */}
        <motion.path
          d="M 305 170 Q 350 200 370 250 Q 375 270 365 275 Q 350 270 345 255 Q 340 230 315 200 Z"
          fill={hoveredMuscle === 'arms' ? getSorenessColor(soreness.arms ?? 0) : 'url(#skinGradient)'}
          stroke={hoveredMuscle === 'arms' ? '#1e40af' : '#2D3748'}
          strokeWidth={hoveredMuscle === 'arms' ? 2.5 : 2}
          opacity={hoveredMuscle === 'arms' ? getSorenessOpacity(soreness.arms ?? 0) : 1}
          onMouseEnter={() => handleMuscleHover('arms')}
          onMouseLeave={handleMuscleLeave}
          onClick={() => handleMuscleClick('arms')}
          style={{ cursor: interactive ? 'pointer' : 'default' }}
          transition={{ duration: 0.2 }}
        />
        {/* Hand - Right */}
        <ellipse cx="365" cy="275" rx="8" ry="12" fill="url(#skinGradient)" stroke="#2D3748" strokeWidth="1.5" />

        {/* Core overlay */}
        <motion.path
          {...getMusclePaths('core')}
          onMouseEnter={() => handleMuscleHover('core')}
          onMouseLeave={handleMuscleLeave}
          onClick={() => handleMuscleClick('core')}
          style={{ cursor: interactive ? 'pointer' : 'default' }}
          transition={{ duration: 0.2 }}
        />

        {/* Legs - Left (standing) */}
        <motion.path
          d="M 230 300 L 210 420 L 215 450 L 235 445 L 230 415 Z"
          fill={hoveredMuscle === 'legs' ? getSorenessColor(soreness.legs ?? 0) : 'url(#skinGradient)'}
          stroke={hoveredMuscle === 'legs' ? '#1e40af' : '#2D3748'}
          strokeWidth={hoveredMuscle === 'legs' ? 2.5 : 2}
          opacity={hoveredMuscle === 'legs' ? getSorenessOpacity(soreness.legs ?? 0) : 1}
          onMouseEnter={() => handleMuscleHover('legs')}
          onMouseLeave={handleMuscleLeave}
          onClick={() => handleMuscleClick('legs')}
          style={{ cursor: interactive ? 'pointer' : 'default' }}
          transition={{ duration: 0.2 }}
        />
        {/* Foot - Left */}
        <ellipse cx="225" cy="450" rx="20" ry="8" fill="url(#skinGradient)" stroke="#2D3748" strokeWidth="1.5" />

        {/* Legs - Right (standing) */}
        <motion.path
          d="M 270 300 L 290 420 L 285 450 L 265 445 L 270 415 Z"
          fill={hoveredMuscle === 'legs' ? getSorenessColor(soreness.legs ?? 0) : 'url(#skinGradient)'}
          stroke={hoveredMuscle === 'legs' ? '#1e40af' : '#2D3748'}
          strokeWidth={hoveredMuscle === 'legs' ? 2.5 : 2}
          opacity={hoveredMuscle === 'legs' ? getSorenessOpacity(soreness.legs ?? 0) : 1}
          onMouseEnter={() => handleMuscleHover('legs')}
          onMouseLeave={handleMuscleLeave}
          onClick={() => handleMuscleClick('legs')}
          style={{ cursor: interactive ? 'pointer' : 'default' }}
          transition={{ duration: 0.2 }}
        />
        {/* Foot - Right */}
        <ellipse cx="275" cy="450" rx="20" ry="8" fill="url(#skinGradient)" stroke="#2D3748" strokeWidth="1.5" />

        {/* Labels for muscle groups */}
        {muscleGroups.map((group) => {
          const intensity = soreness[group.name] ?? 0
          const isHovered = hoveredMuscle === group.name
          const isSore = intensity > 0

          return (
            <motion.text
              key={group.name}
              x={group.position.x}
              y={group.position.y}
              fontSize="14"
              fontWeight="bold"
              textAnchor="middle"
              fill={isSore ? getSorenessColor(intensity) : '#6B7280'}
              opacity={isSore || isHovered ? 1 : 0.6}
              pointerEvents="none"
              animate={{
                scale: isHovered ? 1.15 : 1,
                y: isHovered ? group.position.y - 3 : group.position.y,
              }}
              transition={{ duration: 0.2 }}
            >
              {group.label} {isSore ? `(${intensity})` : ''}
            </motion.text>
          )
        })}
      </svg>
    </div>
  )
}
