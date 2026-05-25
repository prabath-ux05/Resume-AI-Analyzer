import { motion } from 'framer-motion'

export default function ScoreCircle({ score = 0, label = 'ATS Score', size = 170 }) {
  const radius = 62
  const circumference = 2 * Math.PI * radius
  const offset = circumference - (score / 100) * circumference

  const color =
    score >= 75 ? '#34D399' :
    score >= 50 ? '#E6B566' :
    '#F87171'

  const glowColor =
    score >= 75 ? 'rgba(52,211,153,0.15)' :
    score >= 50 ? 'rgba(230,181,102,0.15)' :
    'rgba(248,113,113,0.15)'

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '14px', padding: '8px 0' }}>
      <svg width={size} height={size} viewBox="0 0 140 140">
        {/* Subtle glow behind the ring */}
        <circle cx="70" cy="70" r={radius - 4} fill="none" stroke={glowColor} strokeWidth="18" opacity="0.5" />
        {/* Background track */}
        <circle cx="70" cy="70" r={radius} fill="none" stroke="var(--color-elevated)" strokeWidth="7" />
        {/* Score arc */}
        <motion.circle
          cx="70" cy="70" r={radius}
          fill="none"
          stroke={color}
          strokeWidth="7"
          strokeLinecap="round"
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset: offset }}
          transition={{ duration: 1.4, ease: [0.25, 0.46, 0.45, 0.94] }}
          transform="rotate(-90 70 70)"
        />
        <text x="70" y="62" textAnchor="middle" dominantBaseline="middle"
          fill="var(--color-text)" fontSize="36" fontWeight="700" fontFamily="Inter, sans-serif">
          {score}
        </text>
        <text x="70" y="88" textAnchor="middle" dominantBaseline="middle"
          fill="var(--color-dim)" fontSize="11" fontWeight="500" fontFamily="Inter, sans-serif">
          / 100
        </text>
      </svg>
      <span style={{ fontSize: '12px', fontWeight: 600, color: 'var(--color-muted)', textTransform: 'uppercase', letterSpacing: '0.06em' }}>{label}</span>
    </div>
  )
}
