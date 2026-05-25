import { Link, useLocation, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useResumeContext } from '../context/ResumeContext'
import Button from '../components/Button'

const links = [
  { to: '/', label: 'Home' },
  { to: '/upload', label: 'Upload' },
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/match', label: 'Role Match' },
  { to: '/assistant', label: 'AI Assistant' },
]

export default function Navbar() {
  const { pathname } = useLocation()
  const navigate = useNavigate()
  const { hasAnalysis, resetAnalysis } = useResumeContext()

  const handleReset = () => {
    resetAnalysis()
    navigate('/upload')
  }

  return (
    <nav
      className="sticky top-0 z-50 backdrop-blur-xl"
      style={{
        backgroundColor: 'rgba(9, 9, 11, 0.82)',
        borderBottom: '1px solid var(--color-line)',
      }}
    >
      <div
        className="mx-auto flex items-center justify-between"
        style={{ maxWidth: '1100px', height: '56px', padding: '0 24px' }}
      >
        {/* Logo */}
        <Link to="/" className="flex items-center gap-2.5">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="24" height="24" rx="6" fill="#18181B" stroke="#27272A" strokeWidth="1"/>
            <path d="M13.5 4L6.5 13.5H12.5L10.5 20L17.5 10.5H11.5L13.5 4Z" fill="var(--color-accent)"/>
          </svg>
          <span className="text-sm font-semibold tracking-tight" style={{ color: 'var(--color-text)' }}>
            AscendAI
          </span>
        </Link>

        {/* Nav links */}
        <div className="flex items-center gap-0.5">
          {links.map(({ to, label }) => {
            const active = pathname === to
            return (
              <Link
                key={to}
                to={to}
                className="relative rounded-md transition-colors duration-150"
                style={{
                  padding: '6px 14px',
                  fontSize: '13px',
                  fontWeight: 500,
                  color: active ? 'var(--color-text)' : 'var(--color-dim)',
                }}
              >
                {label}
                {active && (
                  <motion.div
                    layoutId="nav-underline"
                    className="absolute rounded-full"
                    style={{
                      left: '14px',
                      right: '14px',
                      bottom: '-1px',
                      height: '2px',
                      backgroundColor: 'var(--color-accent)',
                    }}
                    transition={{ type: 'spring', stiffness: 400, damping: 32 }}
                  />
                )}
              </Link>
            )
          })}
        </div>

        {/* Reset */}
        <div style={{ width: '160px', display: 'flex', justifyContent: 'flex-end' }}>
          {hasAnalysis && (
            <Button onClick={handleReset} variant="ghost" style={{ padding: '5px 12px', fontSize: '12px' }}>
              Reset
            </Button>
          )}
        </div>
      </div>
    </nav>
  )
}
