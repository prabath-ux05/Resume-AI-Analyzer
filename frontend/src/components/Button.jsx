export default function Button({
  children,
  variant = 'primary',
  disabled = false,
  className = '',
  style = {},
  ...rest
}) {
  const base = {
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '6px',
    borderRadius: '10px',
    padding: '9px 18px',
    fontSize: '13px',
    fontWeight: 600,
    fontFamily: 'inherit',
    cursor: disabled ? 'not-allowed' : 'pointer',
    opacity: disabled ? 0.4 : 1,
    border: 'none',
    transition: 'all 0.2s ease',
    letterSpacing: '-0.01em',
  }

  const styles = {
    primary: {
      ...base,
      backgroundColor: 'var(--color-accent)',
      color: '#ffffff',
    },
    secondary: {
      ...base,
      backgroundColor: 'var(--color-elevated)',
      color: 'var(--color-text)',
      border: '1px solid var(--color-line)',
    },
    ghost: {
      ...base,
      backgroundColor: 'transparent',
      color: 'var(--color-dim)',
    },
  }

  return (
    <button
      disabled={disabled}
      className={className}
      style={{ ...styles[variant], ...style }}
      onMouseEnter={(e) => {
        if (disabled) return
        if (variant === 'primary') e.target.style.backgroundColor = 'var(--color-accent-hover)'
        if (variant === 'secondary') e.target.style.borderColor = 'var(--color-line-hover)'
        if (variant === 'ghost') e.target.style.color = 'var(--color-muted)'
      }}
      onMouseLeave={(e) => {
        if (variant === 'primary') e.target.style.backgroundColor = 'var(--color-accent)'
        if (variant === 'secondary') e.target.style.borderColor = 'var(--color-line)'
        if (variant === 'ghost') e.target.style.color = 'var(--color-dim)'
      }}
      {...rest}
    >
      {children}
    </button>
  )
}
