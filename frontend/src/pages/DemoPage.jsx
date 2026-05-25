import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import Button from '../components/Button'

const steps = [
  {
    id: 'upload',
    title: 'Instant Resume Parsing',
    description: 'Drop your PDF or DOCX file. Our engine parses the structure, extracts text, and prepares it for deep analysis in milliseconds.',
    icon: '📄',
    color: '#34D399',
  },
  {
    id: 'ats',
    title: 'ATS Scoring Breakdown',
    description: 'Get a realistic score across five key categories: Section Structure, Skill Density, Technical Depth, Project Impact, and Readability.',
    icon: '🎯',
    color: '#FF7A59',
  },
  {
    id: 'match',
    title: 'AI Role Match',
    description: 'Compare your resume directly against any Job Description. Uncover missing keywords and see your exact fit percentage.',
    icon: '🔍',
    color: '#60A5FA',
  },
  {
    id: 'assistant',
    title: 'AI Career Assistant',
    description: 'Chat with an AI that knows your resume inside and out. Ask for actionable feedback, summary rewrites, or career advice.',
    icon: '🤖',
    color: '#A78BFA',
  },
  {
    id: 'interview',
    title: 'Interview Intelligence',
    description: 'Coming soon. Practice mock interviews based on your specific projects and experience to ace the behavioral rounds.',
    icon: '🎙️',
    color: '#E6B566',
  },
]

const variants = {
  enter: (direction) => ({ x: direction > 0 ? 50 : -50, opacity: 0 }),
  center: { zIndex: 1, x: 0, opacity: 1 },
  exit: (direction) => ({ zIndex: 0, x: direction < 0 ? 50 : -50, opacity: 0 })
}

export default function DemoPage() {
  const navigate = useNavigate()
  const [stepIndex, setStepIndex] = useState(0)
  const [direction, setDirection] = useState(0)

  const paginate = (newDirection) => {
    setDirection(newDirection)
    if (stepIndex + newDirection >= 0 && stepIndex + newDirection < steps.length) {
      setStepIndex(stepIndex + newDirection)
    } else if (stepIndex + newDirection === steps.length) {
      // Finished tour
      navigate('/upload')
    }
  }

  const currentStep = steps[stepIndex]

  return (
    <div style={{
      position: 'fixed', inset: 0, zIndex: 9999,
      backgroundColor: 'var(--color-bg)', display: 'flex',
      alignItems: 'center', justifyContent: 'center', padding: '24px'
    }}>
      {/* Abstract Background Blur */}
      <div style={{
        position: 'absolute', width: '60vw', height: '60vw',
        borderRadius: '50%', background: 'radial-gradient(circle, rgba(255,122,89,0.05) 0%, rgba(17,19,21,0) 70%)',
        top: '50%', left: '50%', transform: 'translate(-50%, -50%)', pointerEvents: 'none',
      }} />

      <div style={{
        position: 'relative', width: '100%', maxWidth: '900px',
        backgroundColor: 'var(--color-surface)', border: '1px solid var(--color-line)',
        borderRadius: '24px', overflow: 'hidden', boxShadow: '0 24px 64px rgba(0,0,0,0.4)',
        display: 'flex', flexDirection: 'column', height: '600px'
      }}>
        {/* Top Header */}
        <div style={{
          display: 'flex', alignItems: 'center', justifyContent: 'space-between',
          padding: '24px 32px', borderBottom: '1px solid var(--color-line)'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ color: 'var(--color-accent)', fontWeight: 700 }}>◆</span>
            <span style={{ fontSize: '14px', fontWeight: 600, color: 'var(--color-text)' }}>Product Tour</span>
          </div>
          <button
            onClick={() => navigate('/')}
            style={{ fontSize: '14px', color: 'var(--color-muted)', fontWeight: 500 }}
            className="hover:text-white transition-colors"
          >
            Exit Tour ✕
          </button>
        </div>

        {/* Main Content Area */}
        <div style={{ flex: 1, display: 'flex', position: 'relative' }}>
          
          {/* Left Text Content */}
          <div style={{ flex: 1, padding: '48px 48px', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
            <AnimatePresence mode="wait" custom={direction}>
              <motion.div
                key={stepIndex}
                custom={direction}
                variants={variants}
                initial="enter"
                animate="center"
                exit="exit"
                transition={{ x: { type: 'spring', stiffness: 300, damping: 30 }, opacity: { duration: 0.2 } }}
              >
                <div style={{ 
                  display: 'inline-flex', alignItems: 'center', gap: '8px',
                  backgroundColor: 'var(--color-line)', padding: '6px 12px',
                  borderRadius: '99px', fontSize: '12px', fontWeight: 600,
                  color: currentStep.color, marginBottom: '24px'
                }}>
                  Step {stepIndex + 1} of {steps.length}
                </div>
                
                <h2 style={{ fontSize: '32px', fontWeight: 700, color: 'var(--color-text)', marginBottom: '16px', lineHeight: 1.2 }}>
                  {currentStep.title}
                </h2>
                
                <p style={{ fontSize: '16px', color: 'var(--color-muted)', lineHeight: 1.6, maxWidth: '380px' }}>
                  {currentStep.description}
                </p>
              </motion.div>
            </AnimatePresence>
          </div>

          {/* Right Visual Area */}
          <div style={{
            flex: 1, backgroundColor: 'var(--color-elevated)', borderLeft: '1px solid var(--color-line)',
            display: 'flex', alignItems: 'center', justifyContent: 'center', position: 'relative', overflow: 'hidden'
          }}>
            <AnimatePresence mode="wait">
              <motion.div
                key={stepIndex}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 1.1 }}
                transition={{ duration: 0.4 }}
                style={{
                  width: '180px', height: '180px', borderRadius: '40px',
                  backgroundColor: 'var(--color-surface)', border: '1px solid var(--color-line)',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  boxShadow: '0 12px 32px rgba(0,0,0,0.2)',
                  color: currentStep.color
                }}
              >
                <span style={{ fontSize: '72px', filter: 'drop-shadow(0px 4px 8px rgba(0,0,0,0.2))' }}>
                  {currentStep.icon}
                </span>
              </motion.div>
            </AnimatePresence>
          </div>
        </div>

        {/* Bottom Footer Navigation */}
        <div style={{
          display: 'flex', alignItems: 'center', justifyContent: 'space-between',
          padding: '24px 32px', borderTop: '1px solid var(--color-line)', backgroundColor: 'var(--color-surface)'
        }}>
          {/* Progress Dots */}
          <div style={{ display: 'flex', gap: '8px' }}>
            {steps.map((_, i) => (
              <div
                key={i}
                style={{
                  width: i === stepIndex ? '24px' : '8px',
                  height: '8px',
                  borderRadius: '4px',
                  backgroundColor: i === stepIndex ? 'var(--color-accent)' : 'var(--color-line)',
                  transition: 'all 0.3s ease'
                }}
              />
            ))}
          </div>

          <div style={{ display: 'flex', gap: '12px' }}>
            <Button
              variant="secondary"
              onClick={() => paginate(-1)}
              disabled={stepIndex === 0}
            >
              Previous
            </Button>
            <Button onClick={() => paginate(1)}>
              {stepIndex === steps.length - 1 ? 'Start Uploading →' : 'Next'}
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}
