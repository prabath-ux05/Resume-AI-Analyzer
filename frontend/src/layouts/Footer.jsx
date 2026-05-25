import { Link } from 'react-router-dom'

export default function Footer() {
  return (
    <footer
      style={{
        borderTop: '1px solid var(--color-line)',
        padding: '32px 24px',
        marginTop: '96px',
      }}
    >
      <div
        style={{
          maxWidth: '1120px',
          margin: '0 auto',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '16px',
        }}
      >
        {/* Left — Logo + copyright */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="24" height="24" rx="6" fill="#18181B" stroke="#27272A" strokeWidth="1"/>
            <path d="M13.5 4L6.5 13.5H12.5L10.5 20L17.5 10.5H11.5L13.5 4Z" fill="var(--color-accent)"/>
          </svg>
          <span style={{ fontSize: '12px', color: 'var(--color-muted)' }}>
            © {new Date().getFullYear()} AscendAI. All rights reserved.
          </span>
        </div>

        {/* Right — Legal links */}
        <div style={{ display: 'flex', gap: '24px' }}>
          <Link
            to="/privacy"
            style={{ fontSize: '12px', color: 'var(--color-muted)', transition: 'color 0.15s' }}
            onMouseEnter={(e) => e.target.style.color = 'var(--color-text)'}
            onMouseLeave={(e) => e.target.style.color = 'var(--color-muted)'}
          >
            Privacy Policy
          </Link>
          <Link
            to="/terms"
            style={{ fontSize: '12px', color: 'var(--color-muted)', transition: 'color 0.15s' }}
            onMouseEnter={(e) => e.target.style.color = 'var(--color-text)'}
            onMouseLeave={(e) => e.target.style.color = 'var(--color-muted)'}
          >
            Terms & Conditions
          </Link>
        </div>
      </div>
    </footer>
  )
}
