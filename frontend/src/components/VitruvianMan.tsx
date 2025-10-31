import { motion } from 'framer-motion'
import { useState } from 'react'

interface MuscleSoreness {
  chest: number
  back: number
  shoulders: number
  legs: number
  core: number
  arms: number
}

interface VitruvianManProps {
  soreness: MuscleSoreness
  onMuscleClick?: (muscle: string) => void
  interactive?: boolean
}

// Color mapping: 0 (no soreness) = white/gray, 10 (very sore) = deep red/purple
const getSorenessColor = (intensity: number): string => {
  if (intensity === 0) return '#E5E7EB' // gray
  if (intensity <= 2) return '#DBEAFE' // light blue
  if (intensity <= 4) return '#93C5FD' // blue
  if (intensity <= 6) return '#60A5FA' // medium blue
  if (intensity <= 8) return '#8B5CF6' // purple
  return '#EF4444' // red (very sore)
}

const getSorenessOpacity = (intensity: number): number => {
  if (intensity === 0) return 0.1
  return Math.max(0.3, intensity / 10)
}

export default function VitruvianMan({ soreness, onMuscleClick, interactive = true }: VitruvianManProps) {
  const [hoveredMuscle, setHoveredMuscle] = useState<string | null>(null)

  const muscleGroups = [
    { name: 'chest', label: 'Chest', position: { x: 50, y: 35 } },
    { name: 'back', label: 'Back', position: { x: 50, y: 35 } },
    { name: 'shoulders', label: 'Shoulders', position: { x: 50, y: 28 } },
    { name: 'legs', label: 'Legs', position: { x: 50, y: 70 } },
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
    <div className="w-full max-w-2xl mx-auto relative">
      <svg
        viewBox="0 0 400 600"
        className="w-full h-auto"
        style={{ filter: 'drop-shadow(0 4px 6px rgba(0, 0, 0, 0.1))' }}
      >
        {/* Background circle - Vitruvian Man style */}
        <circle
          cx="200"
          cy="300"
          r="280"
          fill="none"
          stroke="#E5E7EB"
          strokeWidth="2"
          opacity="0.3"
        />
        
        {/* Square frame - Vitruvian Man style */}
        <rect
          x="50"
          y="50"
          width="300"
          height="500"
          fill="none"
          stroke="#E5E7EB"
          strokeWidth="2"
          opacity="0.3"
        />

        {/* Body outline - Simplified Vitruvian Man figure */}
        {/* Head */}
        <ellipse
          cx="200"
          cy="80"
          rx="25"
          ry="25"
          fill="#F9FAFB"
          stroke="#1F2937"
          strokeWidth="2"
        />

        {/* Neck */}
        <rect x="190" y="105" width="20" height="15" fill="#F9FAFB" stroke="#1F2937" strokeWidth="2" />

        {/* Torso */}
        <rect
          x="160"
          y="120"
          width="80"
          height="120"
          fill="#F9FAFB"
          stroke="#1F2937"
          strokeWidth="2"
          rx="5"
        />

        {/* Arms - Left */}
        <motion.line
          x1="160"
          y1="150"
          x2="120"
          y2="220"
          stroke="#1F2937"
          strokeWidth="8"
          strokeLinecap="round"
          fill="none"
          animate={{
            stroke: hoveredMuscle === 'arms' || hoveredMuscle === 'shoulders' 
              ? getSorenessColor(soreness.arms) 
              : '#1F2937',
            strokeWidth: hoveredMuscle === 'arms' || hoveredMuscle === 'shoulders' ? 12 : 8,
          }}
          transition={{ duration: 0.2 }}
          onMouseEnter={() => handleMuscleHover('arms')}
          onMouseLeave={handleMuscleLeave}
          onClick={() => handleMuscleClick('arms')}
          style={{ cursor: interactive ? 'pointer' : 'default' }}
        />
        {/* Arms - Right */}
        <motion.line
          x1="240"
          y1="150"
          x2="280"
          y2="220"
          stroke="#1F2937"
          strokeWidth="8"
          strokeLinecap="round"
          fill="none"
          animate={{
            stroke: hoveredMuscle === 'arms' || hoveredMuscle === 'shoulders'
              ? getSorenessColor(soreness.arms)
              : '#1F2937',
            strokeWidth: hoveredMuscle === 'arms' || hoveredMuscle === 'shoulders' ? 12 : 8,
          }}
          transition={{ duration: 0.2 }}
          onMouseEnter={() => handleMuscleHover('arms')}
          onMouseLeave={handleMuscleLeave}
          onClick={() => handleMuscleClick('arms')}
          style={{ cursor: interactive ? 'pointer' : 'default' }}
        />

        {/* Legs - Left */}
        <motion.line
          x1="180"
          y1="240"
          x2="150"
          y2="380"
          stroke="#1F2937"
          strokeWidth="10"
          strokeLinecap="round"
          fill="none"
          animate={{
            stroke: hoveredMuscle === 'legs' ? getSorenessColor(soreness.legs) : '#1F2937',
            strokeWidth: hoveredMuscle === 'legs' ? 14 : 10,
          }}
          transition={{ duration: 0.2 }}
          onMouseEnter={() => handleMuscleHover('legs')}
          onMouseLeave={handleMuscleLeave}
          onClick={() => handleMuscleClick('legs')}
          style={{ cursor: interactive ? 'pointer' : 'default' }}
        />
        {/* Legs - Right */}
        <motion.line
          x1="220"
          y1="240"
          x2="250"
          y2="380"
          stroke="#1F2937"
          strokeWidth="10"
          strokeLinecap="round"
          fill="none"
          animate={{
            stroke: hoveredMuscle === 'legs' ? getSorenessColor(soreness.legs) : '#1F2937',
            strokeWidth: hoveredMuscle === 'legs' ? 14 : 10,
          }}
          transition={{ duration: 0.2 }}
          onMouseEnter={() => handleMuscleHover('legs')}
          onMouseLeave={handleMuscleLeave}
          onClick={() => handleMuscleClick('legs')}
          style={{ cursor: interactive ? 'pointer' : 'default' }}
        />

        {/* Chest overlay */}
        <motion.rect
          x="160"
          y="120"
          width="80"
          height="60"
          fill={getSorenessColor(soreness.chest)}
          opacity={getSorenessOpacity(soreness.chest)}
          rx="5"
          animate={{
            opacity: hoveredMuscle === 'chest' 
              ? Math.min(1, getSorenessOpacity(soreness.chest) + 0.3)
              : getSorenessOpacity(soreness.chest),
            scale: hoveredMuscle === 'chest' ? 1.05 : 1,
          }}
          transition={{ duration: 0.2 }}
          onMouseEnter={() => handleMuscleHover('chest')}
          onMouseLeave={handleMuscleLeave}
          onClick={() => handleMuscleClick('chest')}
          style={{ cursor: interactive ? 'pointer' : 'default' }}
        />

        {/* Back overlay (same area, different visual) */}
        <motion.rect
          x="160"
          y="120"
          width="80"
          height="120"
          fill={getSorenessColor(soreness.back)}
          opacity={getSorenessOpacity(soreness.back) * 0.7}
          rx="5"
          stroke={soreness.back > 0 ? getSorenessColor(soreness.back) : 'none'}
          strokeWidth="2"
          strokeDasharray="5,5"
          animate={{
            opacity: hoveredMuscle === 'back'
              ? Math.min(1, getSorenessOpacity(soreness.back) * 0.7 + 0.3)
              : getSorenessOpacity(soreness.back) * 0.7,
            scale: hoveredMuscle === 'back' ? 1.05 : 1,
          }}
          transition={{ duration: 0.2 }}
          onMouseEnter={() => handleMuscleHover('back')}
          onMouseLeave={handleMuscleLeave}
          onClick={() => handleMuscleClick('back')}
          style={{ cursor: interactive ? 'pointer' : 'default' }}
        />

        {/* Shoulders overlay */}
        <motion.ellipse
          cx="200"
          cy="145"
          rx="50"
          ry="25"
          fill={getSorenessColor(soreness.shoulders)}
          opacity={getSorenessOpacity(soreness.shoulders)}
          animate={{
            opacity: hoveredMuscle === 'shoulders'
              ? Math.min(1, getSorenessOpacity(soreness.shoulders) + 0.3)
              : getSorenessOpacity(soreness.shoulders),
            scale: hoveredMuscle === 'shoulders' ? 1.1 : 1,
          }}
          transition={{ duration: 0.2 }}
          onMouseEnter={() => handleMuscleHover('shoulders')}
          onMouseLeave={handleMuscleLeave}
          onClick={() => handleMuscleClick('shoulders')}
          style={{ cursor: interactive ? 'pointer' : 'default' }}
        />

        {/* Core overlay */}
        <motion.rect
          x="170"
          y="180"
          width="60"
          height="60"
          fill={getSorenessColor(soreness.core)}
          opacity={getSorenessOpacity(soreness.core)}
          rx="30"
          animate={{
            opacity: hoveredMuscle === 'core'
              ? Math.min(1, getSorenessOpacity(soreness.core) + 0.3)
              : getSorenessOpacity(soreness.core),
            scale: hoveredMuscle === 'core' ? 1.1 : 1,
          }}
          transition={{ duration: 0.2 }}
          onMouseEnter={() => handleMuscleHover('core')}
          onMouseLeave={handleMuscleLeave}
          onClick={() => handleMuscleClick('core')}
          style={{ cursor: interactive ? 'pointer' : 'default' }}
        />

        {/* Tooltips on hover */}
        {hoveredMuscle && (
          <motion.g
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.2 }}
          >
            <rect
              x={(muscleGroups.find(m => m.name === hoveredMuscle)?.position.x || 200) - 40}
              y={(muscleGroups.find(m => m.name === hoveredMuscle)?.position.y || 200) - 40}
              width="80"
              height="30"
              fill="#1F2937"
              opacity="0.9"
              rx="4"
            />
            <text
              x={muscleGroups.find(m => m.name === hoveredMuscle)?.position.x || 200}
              y={(muscleGroups.find(m => m.name === hoveredMuscle)?.position.y || 200) - 20}
              textAnchor="middle"
              fill="white"
              fontSize="12"
              fontWeight="600"
            >
              {muscleGroups.find(m => m.name === hoveredMuscle)?.label}: {soreness[hoveredMuscle as keyof MuscleSoreness]}/10
            </text>
          </motion.g>
        )}
      </svg>

      {/* Legend */}
      <div className="mt-4 flex flex-wrap gap-4 justify-center">
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded" style={{ backgroundColor: '#E5E7EB' }}></div>
          <span className="text-sm text-muted-foreground">No Soreness (0)</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded" style={{ backgroundColor: '#93C5FD' }}></div>
          <span className="text-sm text-muted-foreground">Mild (1-4)</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded" style={{ backgroundColor: '#8B5CF6' }}></div>
          <span className="text-sm text-muted-foreground">Moderate (5-8)</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded" style={{ backgroundColor: '#EF4444' }}></div>
          <span className="text-sm text-muted-foreground">Very Sore (9-10)</span>
        </div>
      </div>
    </div>
  )
}
