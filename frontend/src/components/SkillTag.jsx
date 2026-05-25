import { motion } from 'framer-motion'

export default function SkillTag({ label, variant = 'default' }) {
  const styles = {
    default: {
      backgroundColor: 'var(--color-elevated)',
      color: 'var(--color-text)',
      border: '1px solid var(--color-line)',
    },
    match: {
      backgroundColor: 'rgba(52, 211, 153, 0.08)',
      color: '#34D399',
      border: '1px solid rgba(52, 211, 153, 0.2)',
    },
    missing: {
      backgroundColor: 'rgba(248, 113, 113, 0.08)',
      color: '#F87171',
      border: '1px solid rgba(248, 113, 113, 0.2)',
    },
  }

  return (
    <motion.span
      initial={{ opacity: 0, scale: 0.92 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.25, ease: [0.25, 0.46, 0.45, 0.94] }}
      whileHover={{ scale: 1.04, transition: { duration: 0.15 } }}
      style={{
        display: 'inline-block',
        borderRadius: '6px',
        padding: '4px 10px',
        fontSize: '12px',
        fontWeight: 500,
        letterSpacing: '0.01em',
        cursor: 'default',
        transition: 'border-color 0.2s ease',
        ...styles[variant],
      }}
    >
      {label}
    </motion.span>
  )
}
