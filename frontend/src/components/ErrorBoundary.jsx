import React from 'react'

export class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }

  componentDidCatch(error, errorInfo) {
    console.error("ErrorBoundary caught an error:", error, errorInfo)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{
          minHeight: '100vh',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          backgroundColor: 'var(--color-bg)',
          color: 'var(--color-text)',
          padding: '24px'
        }}>
          <div style={{
            maxWidth: '400px',
            width: '100%',
            backgroundColor: 'var(--color-surface)',
            border: '1px solid var(--color-line)',
            borderRadius: '16px',
            padding: '32px',
            textAlign: 'center'
          }}>
            <div style={{
              width: '48px', height: '48px',
              borderRadius: '12px',
              backgroundColor: 'rgba(248, 113, 113, 0.1)',
              color: 'var(--color-err)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontSize: '24px',
              margin: '0 auto 20px'
            }}>
              ⚠️
            </div>
            <h2 style={{ fontSize: '20px', fontWeight: 600, marginBottom: '8px' }}>Something went wrong</h2>
            <p style={{ fontSize: '14px', color: 'var(--color-muted)', lineHeight: '1.6', marginBottom: '24px' }}>
              We encountered an unexpected error while rendering this page.
            </p>
            <button
              onClick={() => window.location.reload()}
              style={{
                width: '100%',
                padding: '10px 16px',
                borderRadius: '8px',
                backgroundColor: 'var(--color-text)',
                color: 'var(--color-bg)',
                border: 'none',
                fontWeight: 600,
                fontSize: '14px',
                cursor: 'pointer',
                transition: 'opacity 0.2s'
              }}
              onMouseEnter={e => e.currentTarget.style.opacity = '0.9'}
              onMouseLeave={e => e.currentTarget.style.opacity = '1'}
            >
              Refresh Page
            </button>
          </div>
        </div>
      )
    }

    return this.props.children
  }
}
