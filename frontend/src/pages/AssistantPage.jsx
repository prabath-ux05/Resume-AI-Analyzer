import { useState, useRef, useEffect, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Link } from 'react-router-dom'
import { useResumeContext } from '../context/ResumeContext'
import { sendStreamMessage, fetchChatHistory, clearChatHistory } from '../services/api'

// ── Suggestion chips shown on empty state
const SUGGESTIONS = [
  'What are my ATS weaknesses?',
  'Which skills should I improve?',
  'Generate interview questions from my projects.',
  'Which companies fit my profile?',
  'How can I improve my resume?',
]

// ── Animated cursor for streaming
function StreamCursor() {
  return (
    <motion.span
      animate={{ opacity: [1, 0] }}
      transition={{ repeat: Infinity, duration: 0.6, ease: 'linear' }}
      style={{
        display: 'inline-block',
        width: '2px',
        height: '14px',
        backgroundColor: 'var(--color-accent)',
        marginLeft: '2px',
        verticalAlign: 'text-bottom',
        borderRadius: '1px',
      }}
    />
  )
}

// ── Individual message renderer
function Message({ msg, isStreaming }) {
  const isUser = msg.role === 'user'

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.25, ease: 'easeOut' }}
      style={{
        display: 'flex',
        flexDirection: 'column',
        gap: '6px',
        alignItems: isUser ? 'flex-end' : 'flex-start',
        maxWidth: '100%',
      }}
    >
      {/* Label row */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: '6px',
        fontSize: '11px',
        fontWeight: 600,
        letterSpacing: '0.08em',
        textTransform: 'uppercase',
        color: isUser ? 'var(--color-dim)' : 'var(--color-accent)',
      }}>
        {!isUser && (
          <span style={{
            width: '16px', height: '16px',
            borderRadius: '4px',
            background: 'linear-gradient(135deg, var(--color-accent), #FF4F87)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: '9px',
          }}>✦</span>
        )}
        {isUser ? 'You' : 'Career Advisor'}
      </div>

      {/* Content */}
      <div style={{
        maxWidth: isUser ? '72%' : '100%',
        width: isUser ? 'auto' : '100%',
      }}>
        {isUser ? (
          // User bubble — minimal pill
          <div style={{
            padding: '10px 16px',
            borderRadius: '18px 18px 4px 18px',
            backgroundColor: 'var(--color-surface)',
            border: '1px solid var(--color-line)',
            fontSize: '14px',
            lineHeight: '1.65',
            color: 'var(--color-text)',
          }}>
            {msg.content}
          </div>
        ) : (
          // AI response — prose style, full-width
          <div style={{
            fontSize: '14.5px',
            lineHeight: '1.8',
            color: msg.isError ? 'var(--color-err)' : 'var(--color-text)',
            whiteSpace: 'pre-wrap',
            letterSpacing: '0.01em',
          }}>
            {msg.content || ''}
            {isStreaming && <StreamCursor />}
          </div>
        )}
      </div>
    </motion.div>
  )
}

// ── No-resume empty state
function NoResumeState() {
  return (
    <div style={{
      flex: 1,
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '60px 24px',
      textAlign: 'center',
    }}>
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.4, ease: 'easeOut' }}
        style={{ maxWidth: '400px' }}
      >
        <div style={{
          width: '56px', height: '56px',
          borderRadius: '16px',
          background: 'linear-gradient(135deg, var(--color-accent) 0%, #FF4F87 100%)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: '22px',
          margin: '0 auto 24px',
          boxShadow: '0 0 32px rgba(255, 122, 89, 0.25)',
        }}>✦</div>
        <h2 style={{ fontSize: '20px', fontWeight: 600, color: 'var(--color-text)', marginBottom: '10px' }}>
          Resume context required
        </h2>
        <p style={{ fontSize: '14px', color: 'var(--color-muted)', lineHeight: '1.7', marginBottom: '28px' }}>
          The Career Advisor reads your structured resume intelligence to give you
          highly personalized, actionable guidance — not generic advice.
        </p>
        <Link to="/upload" style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '8px',
          padding: '10px 20px',
          borderRadius: '8px',
          backgroundColor: 'var(--color-accent)',
          color: '#fff',
          fontSize: '13px',
          fontWeight: 600,
          textDecoration: 'none',
          transition: 'opacity 0.15s',
        }}
          onMouseEnter={e => e.currentTarget.style.opacity = '0.85'}
          onMouseLeave={e => e.currentTarget.style.opacity = '1'}
        >
          Upload Resume →
        </Link>
      </motion.div>
    </div>
  )
}

// ── Main component
export default function AssistantPage() {
  const { fileHash, hasAnalysis, filename } = useResumeContext()
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [isInterviewMode, setIsInterviewMode] = useState(false)
  const [streamingIdx, setStreamingIdx] = useState(null)
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)
  const [sessionId] = useState(() => `sess_${Date.now()}_${Math.random().toString(36).slice(2, 7)}`)

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [])

  useEffect(() => { scrollToBottom() }, [messages, scrollToBottom])

  // Load history from Redis on mount
  useEffect(() => {
    if (!fileHash) return
    fetchChatHistory(sessionId)
      .then(data => {
        if (data.messages?.length > 0) {
          setMessages(data.messages.map(m => ({ role: m.role, content: m.parts[0] })))
        }
      })
      .catch(() => {}) // silently fail — fresh start
  }, [fileHash, sessionId])

  const handleSend = useCallback(async (messageOverride = null) => {
    const userMessage = (messageOverride ?? input).trim()
    if (!userMessage || isLoading) return

    setInput('')
    const userMsg = { role: 'user', content: userMessage }
    const aiMsg = { role: 'model', content: '' }

    setMessages(prev => [...prev, userMsg, aiMsg])
    const newIdx = messages.length + 1
    setStreamingIdx(newIdx)
    setIsLoading(true)

    try {
      const reader = await sendStreamMessage(userMessage, fileHash, sessionId, isInterviewMode)
      const decoder = new TextDecoder()
      let fullText = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        fullText += decoder.decode(value, { stream: true })
        
        const isErrorStream = fullText.includes('⚠️')
        
        setMessages(prev => {
          const next = [...prev]
          next[next.length - 1] = { 
            role: 'model', 
            content: fullText,
            isError: isErrorStream
          }
          return next
        })
      }
    } catch {
      setMessages(prev => {
        const next = [...prev]
        next[next.length - 1] = {
          role: 'model',
          content: 'Something went wrong. Please try again.',
          isError: true
        }
        return next
      })
    } finally {
      setIsLoading(false)
      setStreamingIdx(null)
      setTimeout(() => inputRef.current?.focus(), 100)
    }
  }, [input, isLoading, fileHash, sessionId, isInterviewMode, messages.length])

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const handleClear = async () => {
    await clearChatHistory(sessionId)
    setMessages([])
  }

  const isEmpty = messages.length === 0

  if (!hasAnalysis || !fileHash) return <NoResumeState />

  return (
    <div style={{
      height: 'calc(100vh - 64px)',
      display: 'flex',
      flexDirection: 'column',
      maxWidth: '760px',
      margin: '0 auto',
      padding: '0 24px',
    }}>

      {/* ── Top bar */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '20px 0 16px',
        borderBottom: '1px solid var(--color-line)',
        flexShrink: 0,
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div style={{
            width: '28px', height: '28px',
            borderRadius: '8px',
            background: 'linear-gradient(135deg, var(--color-accent) 0%, #FF4F87 100%)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: '12px',
            flexShrink: 0,
          }}>✦</div>
          <div>
            <div style={{ fontSize: '14px', fontWeight: 600, color: 'var(--color-text)' }}>Career Advisor</div>
            <div style={{ fontSize: '11px', color: 'var(--color-muted)' }}>
              Context: <span style={{ color: 'var(--color-accent)', fontWeight: 500 }}>{filename}</span>
            </div>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          {/* Interview mode pill */}
          <button
            onClick={() => setIsInterviewMode(v => !v)}
            title="Toggle Interview Mode"
            style={{
              display: 'flex', alignItems: 'center', gap: '5px',
              padding: '5px 10px',
              borderRadius: '20px',
              border: '1px solid',
              borderColor: isInterviewMode ? 'var(--color-accent)' : 'var(--color-line)',
              backgroundColor: isInterviewMode ? 'rgba(255,122,89,0.12)' : 'transparent',
              color: isInterviewMode ? 'var(--color-accent)' : 'var(--color-muted)',
              fontSize: '11px',
              fontWeight: 600,
              cursor: 'pointer',
              transition: 'all 0.2s',
              letterSpacing: '0.04em',
            }}
          >
            <span style={{ width: '6px', height: '6px', borderRadius: '50%', backgroundColor: isInterviewMode ? 'var(--color-accent)' : 'var(--color-dim)', display: 'inline-block' }} />
            {isInterviewMode ? 'Interview On' : 'Interview Off'}
          </button>

          {/* Clear button */}
          {messages.length > 0 && (
            <button
              onClick={handleClear}
              title="Clear chat"
              style={{
                padding: '5px 10px',
                borderRadius: '6px',
                border: '1px solid var(--color-line)',
                backgroundColor: 'transparent',
                color: 'var(--color-dim)',
                fontSize: '11px',
                cursor: 'pointer',
                transition: 'color 0.15s',
              }}
              onMouseEnter={e => e.currentTarget.style.color = 'var(--color-err)'}
              onMouseLeave={e => e.currentTarget.style.color = 'var(--color-dim)'}
            >
              Clear
            </button>
          )}
        </div>
      </div>

      {/* ── Messages area */}
      <div style={{
        flex: 1,
        overflowY: 'auto',
        padding: '32px 0 16px',
        display: 'flex',
        flexDirection: 'column',
        gap: '32px',
      }}>
        {/* Empty state — suggestion chips */}
        <AnimatePresence>
          {isEmpty && (
            <motion.div
              key="empty"
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.3 }}
              style={{ display: 'flex', flexDirection: 'column', gap: '28px', paddingTop: '20px' }}
            >
              <div>
                <div style={{
                  width: '40px', height: '40px',
                  borderRadius: '12px',
                  background: 'linear-gradient(135deg, var(--color-accent) 0%, #FF4F87 100%)',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  fontSize: '16px',
                  marginBottom: '16px',
                  boxShadow: '0 0 24px rgba(255,122,89,0.2)',
                }}>✦</div>
                <h2 style={{ fontSize: '18px', fontWeight: 600, color: 'var(--color-text)', marginBottom: '6px' }}>
                  What would you like to work on?
                </h2>
                <p style={{ fontSize: '13px', color: 'var(--color-muted)', lineHeight: 1.6 }}>
                  I've analyzed <span style={{ color: 'var(--color-text)', fontWeight: 500 }}>{filename}</span> and I'm ready to give you brutally honest, strategic career advice.
                </p>
              </div>

              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                {SUGGESTIONS.map((s, i) => (
                  <motion.button
                    key={s}
                    initial={{ opacity: 0, y: 6 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: i * 0.06 }}
                    onClick={() => handleSend(s)}
                    style={{
                      padding: '7px 13px',
                      borderRadius: '20px',
                      border: '1px solid var(--color-line)',
                      backgroundColor: 'var(--color-surface)',
                      color: 'var(--color-text)',
                      fontSize: '12.5px',
                      cursor: 'pointer',
                      transition: 'border-color 0.15s, background-color 0.15s',
                      textAlign: 'left',
                    }}
                    onMouseEnter={e => {
                      e.currentTarget.style.borderColor = 'var(--color-accent)'
                      e.currentTarget.style.backgroundColor = 'var(--color-elevated)'
                    }}
                    onMouseLeave={e => {
                      e.currentTarget.style.borderColor = 'var(--color-line)'
                      e.currentTarget.style.backgroundColor = 'var(--color-surface)'
                    }}
                  >
                    {s}
                  </motion.button>
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Message list */}
        <AnimatePresence initial={false}>
          {messages.map((msg, idx) => (
            <Message
              key={idx}
              msg={msg}
              isStreaming={idx === streamingIdx && isLoading}
            />
          ))}
        </AnimatePresence>

        <div ref={messagesEndRef} />
      </div>

      {/* ── Input area */}
      <div style={{
        flexShrink: 0,
        padding: '12px 0 20px',
        borderTop: '1px solid var(--color-line)',
      }}>
        <div style={{
          display: 'flex',
          alignItems: 'flex-end',
          gap: '8px',
          backgroundColor: 'var(--color-surface)',
          border: '1px solid var(--color-line)',
          borderRadius: '12px',
          padding: '8px 8px 8px 16px',
          transition: 'border-color 0.2s',
        }}
          onFocusCapture={e => e.currentTarget.style.borderColor = 'var(--color-line-hover)'}
          onBlurCapture={e => e.currentTarget.style.borderColor = 'var(--color-line)'}
        >
          <textarea
            ref={inputRef}
            value={input}
            onChange={e => {
              setInput(e.target.value)
              // Auto-resize
              e.target.style.height = 'auto'
              e.target.style.height = Math.min(e.target.scrollHeight, 160) + 'px'
            }}
            onKeyDown={handleKeyDown}
            placeholder={isInterviewMode ? 'Interview mode active — ask for questions...' : 'Ask anything about your career, resume, or interview prep...'}
            rows={1}
            style={{
              flex: 1,
              resize: 'none',
              border: 'none',
              outline: 'none',
              backgroundColor: 'transparent',
              color: 'var(--color-text)',
              fontSize: '14px',
              lineHeight: '1.6',
              fontFamily: 'inherit',
              minHeight: '24px',
              maxHeight: '160px',
              overflowY: 'auto',
            }}
          />
          <button
            onClick={() => handleSend()}
            disabled={!input.trim() || isLoading}
            style={{
              flexShrink: 0,
              width: '32px', height: '32px',
              borderRadius: '8px',
              border: 'none',
              backgroundColor: (!input.trim() || isLoading) ? 'var(--color-elevated)' : 'var(--color-accent)',
              color: (!input.trim() || isLoading) ? 'var(--color-dim)' : '#fff',
              cursor: (!input.trim() || isLoading) ? 'default' : 'pointer',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontSize: '14px',
              transition: 'background-color 0.15s, color 0.15s',
              flexDirection: 'column',
            }}
          >
            {isLoading ? (
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ repeat: Infinity, duration: 1, ease: 'linear' }}
                style={{
                  width: '12px', height: '12px',
                  border: '2px solid var(--color-dim)',
                  borderTopColor: 'var(--color-accent)',
                  borderRadius: '50%',
                }}
              />
            ) : '↑'}
          </button>
        </div>

        <div style={{ marginTop: '8px', fontSize: '11px', color: 'var(--color-dim)', textAlign: 'center' }}>
          Press <kbd style={{ padding: '1px 5px', borderRadius: '3px', border: '1px solid var(--color-line)', backgroundColor: 'var(--color-elevated)', fontSize: '10px' }}>Enter</kbd> to send · <kbd style={{ padding: '1px 5px', borderRadius: '3px', border: '1px solid var(--color-line)', backgroundColor: 'var(--color-elevated)', fontSize: '10px' }}>Shift+Enter</kbd> for newline
        </div>
      </div>
    </div>
  )
}
