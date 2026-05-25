import { motion } from 'framer-motion'

export default function Card({ children, className = '', hover = false, style = {} }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 14 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, ease: [0.25, 0.46, 0.45, 0.94] }}
      whileHover={hover ? { y: -2, transition: { duration: 0.2 } } : {}}
      className={className}
      style={{
        backgroundColor: 'var(--color-surface)',
        border: '1px solid var(--color-line)',
        borderRadius: '14px',
        padding: '24px',
        boxShadow: '0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.08)',
        transition: 'border-color 0.25s ease, box-shadow 0.25s ease',
        ...style,
      }}
    >
      {children}
    </motion.div>
  )
}
