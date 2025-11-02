import { motion } from 'framer-motion'
import { useState } from 'react'

interface VitruvianManProps {
  soreness: Record<string, number>
  onMuscleClick?: (muscle: string) => void
  interactive?: boolean
}

// Premium color mapping with smooth gradients
const getSorenessColor = (intensity: number): string => {
  if (intensity === 0) return 'rgba(229, 231, 235, 0.1)' // transparent gray
  if (intensity <= 2) return 'rgba(59, 130, 246, 0.3)' // light blue
  if (intensity <= 4) return 'rgba(59, 130, 246, 0.5)' // blue
  if (intensity <= 6) return 'rgba(139, 92, 246, 0.6)' // purple
  if (intensity <= 8) return 'rgba(239, 68, 68, 0.7)' // red
  return 'rgba(220, 38, 38, 0.85)' // deep red
}

const getSorenessOpacity = (intensity: number): number => {
  if (intensity === 0) return 0
  return Math.max(0.3, Math.min(0.9, intensity / 12))
}

export default function VitruvianMan({ soreness, onMuscleClick, interactive = true }: VitruvianManProps) {
  const [hoveredMuscle, setHoveredMuscle] = useState<string | null>(null)

  const muscleGroups = [
    { name: 'chest', label: 'Chest', position: { x: 250, y: 200 } },
    { name: 'back', label: 'Back', position: { x: 250, y: 240 } },
    { name: 'shoulders', label: 'Shoulders', position: { x: 250, y: 150 } },
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

  return (
    <div className="w-full max-w-4xl mx-auto relative">
      <svg
        viewBox="0 0 500 500"
        className="w-full h-auto"
        style={{ 
          filter: 'drop-shadow(0 20px 40px rgba(0, 0, 0, 0.12))',
        }}
      >
        <defs>
          {/* Premium gradients */}
          <linearGradient id="skinGradient" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#FEFBF7" stopOpacity="1" />
            <stop offset="50%" stopColor="#FAF6F1" stopOpacity="1" />
            <stop offset="100%" stopColor="#F5EFE8" stopOpacity="1" />
          </linearGradient>
          
          <linearGradient id="circleGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#E0E7FF" stopOpacity="0.3" />
            <stop offset="100%" stopColor="#C7D2FE" stopOpacity="0.2" />
          </linearGradient>
          
          <linearGradient id="squareGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#DBEAFE" stopOpacity="0.3" />
            <stop offset="100%" stopColor="#BFDBFE" stopOpacity="0.2" />
          </linearGradient>

          {/* Muscle overlay gradients */}
          {muscleGroups.map((muscle) => {
            const intensity = soreness[muscle.name] ?? 0
            return (
              <linearGradient key={`${muscle.name}Grad`} id={`${muscle.name}Grad`} x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor={getSorenessColor(intensity)} stopOpacity="0.4" />
                <stop offset="100%" stopColor={getSorenessColor(intensity)} stopOpacity={getSorenessOpacity(intensity)} />
              </linearGradient>
            )
          })}

          {/* Subtle glow effect */}
          <filter id="glow">
            <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
            <feMerge>
              <feMergeNode in="coloredBlur"/>
              <feMergeNode in="SourceGraphic"/>
            </feMerge>
          </filter>
        </defs>

        {/* Vitruvian Circle - elegant and subtle */}
        <circle
          cx="250"
          cy="250"
          r="200"
          fill="url(#circleGradient)"
          stroke="#94A3B8"
          strokeWidth="1.5"
          opacity="0.5"
          style={{ filter: 'blur(0.5px)' }}
        />
        
        {/* Vitruvian Square - elegant and subtle */}
        <rect
          x="50"
          y="50"
          width="400"
          height="400"
          fill="url(#squareGradient)"
          stroke="#94A3B8"
          strokeWidth="1.5"
          opacity="0.5"
          style={{ filter: 'blur(0.5px)' }}
        />

        {/* Actual Vitruvian Man figure - Leonardo's proportions */}
        {/* Head */}
        <circle
          cx="250"
          cy="100"
          r="32"
          fill="url(#skinGradient)"
          stroke="#2D3748"
          strokeWidth="2.5"
          style={{ filter: 'drop-shadow(0 2px 4px rgba(0,0,0,0.1))' }}
        />
        {/* Face details - subtle */}
        <circle cx="242" cy="95" r="2" fill="#2D3748" opacity="0.6" />
        <circle cx="258" cy="95" r="2" fill="#2D3748" opacity="0.6" />
        <path d="M 242 105 Q 250 110 258 105" stroke="#2D3748" strokeWidth="1.5" fill="none" opacity="0.4" />

        {/* Neck */}
        <rect x="238" y="132" width="24" height="28" fill="url(#skinGradient)" stroke="#2D3748" strokeWidth="2" rx="3" />

        {/* Torso - properly proportioned */}
        <rect
          x="200"
          y="160"
          width="100"
          height="150"
          fill="url(#skinGradient)"
          stroke="#2D3748"
          strokeWidth="2.5"
          rx="8"
          style={{ filter: 'drop-shadow(0 2px 6px rgba(0,0,0,0.08))' }}
        />

        {/* Chest definition - subtle */}
        <path
          d="M 220 180 Q 250 170 280 180 Q 275 210 250 215 Q 225 210 220 180 Z"
          fill="none"
          stroke="#2D3748"
          strokeWidth="1.5"
          opacity="0.3"
        />

        {/* Shoulders - elegant curves */}
        <path
          d="M 200 160 Q 250 140 300 160 Q 310 175 305 185 L 295 190 Q 250 180 205 190 L 195 185 Q 190 170 200 160 Z"
          fill="url(#skinGradient)"
          stroke="#2D3748"
          strokeWidth="2.5"
        />

        {/* Arms - Left (extended Vitruvian pose) */}
        <path
          d="M 195 185 Q 150 210 125 260 Q 115 285 125 295 Q 140 290 150 275 Q 160 245 185 210 Z"
          fill={hoveredMuscle === 'arms' ? getSorenessColor(soreness.arms ?? 0) : 'url(#skinGradient)'}
          stroke={hoveredMuscle === 'arms' ? '#1e40af' : '#2D3748'}
          strokeWidth={hoveredMuscle === 'arms' ? 3 : 2.5}
          opacity={hoveredMuscle === 'arms' ? 1 : 1}
          onMouseEnter={() => handleMuscleHover('arms')}
          onMouseLeave={handleMuscleLeave}
          onClick={() => handleMuscleClick('arms')}
          style={{ cursor: interactive ? 'pointer' : 'default', transition: 'all 0.2s' }}
        />
        {/* Hand - Left */}
        <ellipse cx="125" cy="295" rx="10" ry="14" fill="url(#skinGradient)" stroke="#2D3748" strokeWidth="2" />

        {/* Arms - Right (extended Vitruvian pose) */}
        <path
          d="M 305 185 Q 350 210 375 260 Q 385 285 375 295 Q 360 290 350 275 Q 340 245 315 210 Z"
          fill={hoveredMuscle === 'arms' ? getSorenessColor(soreness.arms ?? 0) : 'url(#skinGradient)'}
          stroke={hoveredMuscle === 'arms' ? '#1e40af' : '#2D3748'}
          strokeWidth={hoveredMuscle === 'arms' ? 3 : 2.5}
          opacity={hoveredMuscle === 'arms' ? 1 : 1}
          onMouseEnter={() => handleMuscleHover('arms')}
          onMouseLeave={handleMuscleLeave}
          onClick={() => handleMuscleClick('arms')}
          style={{ cursor: interactive ? 'pointer' : 'default', transition: 'all 0.2s' }}
        />
        {/* Hand - Right */}
        <ellipse cx="375" cy="295" rx="10" ry="14" fill="url(#skinGradient)" stroke="#2D3748" strokeWidth="2" />

        {/* Legs - Left (standing) */}
        <path
          d="M 230 310 L 210 420 L 205 455 L 230 450 L 225 420 Z"
          fill={hoveredMuscle === 'legs' ? getSorenessColor(soreness.legs ?? 0) : 'url(#skinGradient)'}
          stroke={hoveredMuscle === 'legs' ? '#1e40af' : '#2D3748'}
          strokeWidth={hoveredMuscle === 'legs' ? 3 : 2.5}
          opacity={hoveredMuscle === 'legs' ? 1 : 1}
          onMouseEnter={() => handleMuscleHover('legs')}
          onMouseLeave={handleMuscleLeave}
          onClick={() => handleMuscleClick('legs')}
          style={{ cursor: interactive ? 'pointer' : 'default', transition: 'all 0.2s' }}
        />
        {/* Foot - Left */}
        <ellipse cx="217" cy="455" rx="22" ry="10" fill="url(#skinGradient)" stroke="#2D3748" strokeWidth="2" />

        {/* Legs - Right (standing) */}
        <path
          d="M 270 310 L 290 420 L 295 455 L 270 450 L 275 420 Z"
          fill={hoveredMuscle === 'legs' ? getSorenessColor(soreness.legs ?? 0) : 'url(#skinGradient)'}
          stroke={hoveredMuscle === 'legs' ? '#1e40af' : '#2D3748'}
          strokeWidth={hoveredMuscle === 'legs' ? 3 : 2.5}
          opacity={hoveredMuscle === 'legs' ? 1 : 1}
          onMouseEnter={() => handleMuscleHover('legs')}
          onMouseLeave={handleMuscleLeave}
          onClick={() => handleMuscleClick('legs')}
          style={{ cursor: interactive ? 'pointer' : 'default', transition: 'all 0.2s' }}
        />
        {/* Foot - Right */}
        <ellipse cx="283" cy="455" rx="22" ry="10" fill="url(#skinGradient)" stroke="#2D3748" strokeWidth="2" />

        {/* Muscle overlays for soreness visualization */}
        {/* Chest */}
        <motion.path
          d="M 220 180 Q 250 170 280 180 Q 275 210 250 215 Q 225 210 220 180 Z"
          fill={getSorenessColor(soreness.chest ?? 0)}
          opacity={getSorenessOpacity(soreness.chest ?? 0)}
          stroke={(soreness.chest ?? 0) > 0 ? getSorenessColor(soreness.chest ?? 0) : 'none'}
          strokeWidth={hoveredMuscle === 'chest' ? 2.5 : 0}
          onMouseEnter={() => handleMuscleHover('chest')}
          onMouseLeave={handleMuscleLeave}
          onClick={() => handleMuscleClick('chest')}
          style={{ cursor: interactive ? 'pointer' : 'default' }}
          animate={{
            opacity: hoveredMuscle === 'chest' ? Math.min(1, getSorenessOpacity(soreness.chest ?? 0) + 0.2) : getSorenessOpacity(soreness.chest ?? 0),
            scale: hoveredMuscle === 'chest' ? 1.02 : 1,
          }}
          transition={{ duration: 0.2 }}
        />

        {/* Shoulders */}
        <motion.path
          d="M 200 160 Q 250 140 300 160 Q 310 175 305 185 L 295 190 Q 250 180 205 190 L 195 185 Q 190 170 200 160 Z"
          fill={getSorenessColor(soreness.shoulders ?? 0)}
          opacity={getSorenessOpacity(soreness.shoulders ?? 0)}
          stroke={(soreness.shoulders ?? 0) > 0 ? getSorenessColor(soreness.shoulders ?? 0) : 'none'}
          strokeWidth={hoveredMuscle === 'shoulders' ? 2.5 : 0}
          onMouseEnter={() => handleMuscleHover('shoulders')}
          onMouseLeave={handleMuscleLeave}
          onClick={() => handleMuscleClick('shoulders')}
          style={{ cursor: interactive ? 'pointer' : 'default' }}
          animate={{
            opacity: hoveredMuscle === 'shoulders' ? Math.min(1, getSorenessOpacity(soreness.shoulders ?? 0) + 0.2) : getSorenessOpacity(soreness.shoulders ?? 0),
            scale: hoveredMuscle === 'shoulders' ? 1.02 : 1,
          }}
          transition={{ duration: 0.2 }}
        />

        {/* Core */}
        <motion.path
          d="M 225 230 Q 250 260 275 230 Q 270 280 250 285 Q 230 280 225 230 Z"
          fill={getSorenessColor(soreness.core ?? 0)}
          opacity={getSorenessOpacity(soreness.core ?? 0)}
          stroke={(soreness.core ?? 0) > 0 ? getSorenessColor(soreness.core ?? 0) : 'none'}
          strokeWidth={hoveredMuscle === 'core' ? 2.5 : 0}
          onMouseEnter={() => handleMuscleHover('core')}
          onMouseLeave={handleMuscleLeave}
          onClick={() => handleMuscleClick('core')}
          style={{ cursor: interactive ? 'pointer' : 'default' }}
          animate={{
            opacity: hoveredMuscle === 'core' ? Math.min(1, getSorenessOpacity(soreness.core ?? 0) + 0.2) : getSorenessOpacity(soreness.core ?? 0),
            scale: hoveredMuscle === 'core' ? 1.02 : 1,
          }}
          transition={{ duration: 0.2 }}
        />

        {/* Back - subtle overlay */}
        <motion.path
          d="M 200 160 L 300 160 L 295 310 L 205 310 Z"
          fill={getSorenessColor(soreness.back ?? 0)}
          opacity={getSorenessOpacity(soreness.back ?? 0) * 0.7}
          stroke={(soreness.back ?? 0) > 0 ? getSorenessColor(soreness.back ?? 0) : 'none'}
          strokeWidth={hoveredMuscle === 'back' ? 2 : 0}
          strokeDasharray="8,4"
          onMouseEnter={() => handleMuscleHover('back')}
          onMouseLeave={handleMuscleLeave}
          onClick={() => handleMuscleClick('back')}
          style={{ cursor: interactive ? 'pointer' : 'default' }}
          animate={{
            opacity: hoveredMuscle === 'back' ? Math.min(1, getSorenessOpacity(soreness.back ?? 0) * 0.7 + 0.2) : getSorenessOpacity(soreness.back ?? 0) * 0.7,
          }}
          transition={{ duration: 0.2 }}
        />

        {/* Premium labels */}
        {muscleGroups.map((group) => {
          const intensity = soreness[group.name] ?? 0
          const isHovered = hoveredMuscle === group.name
          const isSore = intensity > 0

          return (
            <motion.g key={group.name} pointerEvents="none">
              {(isSore || isHovered) && (
                <motion.rect
                  x={group.position.x - 50}
                  y={group.position.y - 18}
                  width="100"
                  height="28"
                  rx="14"
                  fill={isSore ? getSorenessColor(intensity) : 'rgba(30, 58, 138, 0.9)'}
                  opacity={0.95}
                  animate={{
                    scale: isHovered ? 1.1 : 1,
                  }}
                />
              )}
              <motion.text
                x={group.position.x}
                y={group.position.y}
                fontSize="13"
                fontWeight="600"
                textAnchor="middle"
                fill={isSore || isHovered ? '#FFFFFF' : '#6B7280'}
                opacity={isSore || isHovered ? 1 : 0.7}
                animate={{
                  y: isHovered ? group.position.y - 2 : group.position.y,
                }}
                transition={{ duration: 0.2 }}
              >
                {group.label} {isSore ? `${intensity}` : ''}
              </motion.text>
            </motion.g>
          )
        })}
      </svg>

      {/* Premium legend */}
      <div className="mt-6 flex flex-wrap gap-4 justify-center">
        {[
          { color: 'rgba(229, 231, 235, 0.3)', label: 'No Soreness', range: '0' },
          { color: 'rgba(59, 130, 246, 0.5)', label: 'Mild', range: '1-4' },
          { color: 'rgba(139, 92, 246, 0.6)', label: 'Moderate', range: '5-6' },
          { color: 'rgba(239, 68, 68, 0.7)', label: 'Sore', range: '7-8' },
          { color: 'rgba(220, 38, 38, 0.85)', label: 'Very Sore', range: '9-10' },
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
