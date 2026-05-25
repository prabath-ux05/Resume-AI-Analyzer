import { motion } from 'framer-motion'

/**
 * Section wrapper with a heading and staggered children reveal.
 */
const container = {
  hidden: {},
  show: { transition: { staggerChildren: 0.06 } },
}

export default function SectionBlock({ title, children, className = '' }) {
  return (
    <motion.section
      variants={container}
      initial="hidden"
      animate="show"
      className={className}
    >
      {title && (
        <h3 className="text-lg font-semibold text-text-primary mb-4">{title}</h3>
      )}
      {children}
    </motion.section>
  )
}
