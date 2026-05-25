import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import Button from '../components/Button'
import Card from '../components/Card'

const fadeUp = (delay = 0) => ({
  initial: { opacity: 0, y: 28 },
  animate: { opacity: 1, y: 0 },
  transition: { delay, duration: 0.55, ease: 'easeOut' },
})

const features = [
  { icon: '⚡', title: 'Instant ATS Score', desc: 'Get a realistic score breakdown across five key categories in seconds.' },
  { icon: '🔍', title: 'Skill Extraction', desc: 'AI identifies and categorizes every technical skill on your resume.' },
  { icon: '🎯', title: 'AI Role Match', desc: 'Discover the exact job roles that best fit your skills and experience.' },
  { icon: '📝', title: 'Smart Suggestions', desc: 'Actionable recommendations to improve your resume and land more interviews.' },
]

const metrics = [
  { label: 'Resumes Analyzed', value: '10K+' },
  { label: 'Skills Tracked', value: '120+' },
  { label: 'Accuracy Rate', value: '94%' },
  { label: 'Avg. Score Boost', value: '+18pts' },
]

export default function LandingPage() {
  return (
    <div style={{ maxWidth: '1120px', margin: '0 auto', padding: '0 24px' }}>

      {/* ─── Hero ─── */}
      <section style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center', paddingTop: '100px', paddingBottom: '80px' }}>
        <motion.div {...fadeUp(0)}
          style={{
            display: 'inline-flex', alignItems: 'center', gap: '8px',
            borderRadius: '999px', border: '1px solid var(--color-line)',
            backgroundColor: 'var(--color-surface)', padding: '6px 16px',
            fontSize: '12px', fontWeight: 500, color: 'var(--color-muted)', marginBottom: '24px',
          }}
        >
          <span style={{ width: '6px', height: '6px', borderRadius: '50%', backgroundColor: 'var(--color-accent)' }} />
          AI-Powered Resume Intelligence
        </motion.div>

        <motion.h1 {...fadeUp(0.1)}
          style={{
            maxWidth: '640px', fontSize: 'clamp(32px, 5vw, 52px)',
            fontWeight: 700, lineHeight: 1.15, letterSpacing: '-0.02em',
            color: 'var(--color-text)',
          }}
        >
          Analyze your resume.{' '}
          <span style={{ color: 'var(--color-accent)' }}>Land interviews.</span>
        </motion.h1>

        <motion.p {...fadeUp(0.2)}
          style={{
            marginTop: '20px', maxWidth: '480px',
            fontSize: '16px', lineHeight: 1.7, color: 'var(--color-muted)',
          }}
        >
          Upload your resume and get an instant ATS score, extracted skills,
          and AI-powered job matching — all in one place.
        </motion.p>

        <motion.div {...fadeUp(0.3)} style={{ marginTop: '36px', display: 'flex', gap: '12px' }}>
          <Link to="/upload"><Button>Upload Resume →</Button></Link>
          <Link to="/demo"><Button variant="secondary">View Demo</Button></Link>
        </motion.div>
      </section>

      {/* ─── Metrics Bar ─── */}
      <motion.section {...fadeUp(0.15)}
        style={{
          display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1px',
          backgroundColor: 'var(--color-line)', borderRadius: '16px', overflow: 'hidden',
          marginBottom: '80px',
        }}
      >
        {metrics.map((m) => (
          <div key={m.label} style={{
            backgroundColor: 'var(--color-surface)',
            padding: '28px 24px', textAlign: 'center',
          }}>
            <div style={{ fontSize: '28px', fontWeight: 700, color: 'var(--color-text)', marginBottom: '4px' }}>
              {m.value}
            </div>
            <div style={{ fontSize: '12px', color: 'var(--color-muted)', fontWeight: 500 }}>
              {m.label}
            </div>
          </div>
        ))}
      </motion.section>

      {/* ─── Features Grid ─── */}
      <section style={{ paddingBottom: '80px' }}>
        <div style={{ textAlign: 'center', marginBottom: '48px' }}>
          <h2 style={{ fontSize: '28px', fontWeight: 700, color: 'var(--color-text)', marginBottom: '8px' }}>
            Everything you need to optimize your resume
          </h2>
          <p style={{ fontSize: '14px', color: 'var(--color-muted)', maxWidth: '480px', margin: '0 auto' }}>
            Our AI engine evaluates your resume the same way top ATS systems do.
          </p>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '16px' }}>
          {features.map((f, i) => (
            <motion.div key={f.title} {...fadeUp(0.05 * i)}>
              <Card hover style={{ height: '100%' }}>
                <span style={{ fontSize: '28px', display: 'block', marginBottom: '16px' }}>{f.icon}</span>
                <h3 style={{ fontSize: '15px', fontWeight: 600, color: 'var(--color-text)', marginBottom: '8px' }}>
                  {f.title}
                </h3>
                <p style={{ fontSize: '13px', color: 'var(--color-muted)', lineHeight: 1.6 }}>{f.desc}</p>
              </Card>
            </motion.div>
          ))}
        </div>
      </section>

      {/* ─── ATS Preview ─── */}
      <section style={{ paddingBottom: '80px' }}>
        <motion.div {...fadeUp(0)}
          style={{
            borderRadius: '20px', border: '1px solid var(--color-line)',
            backgroundColor: 'var(--color-surface)',
            padding: 'clamp(32px, 5vw, 56px)',
          }}
        >
          <div style={{ display: 'flex', flexWrap: 'wrap', alignItems: 'center', gap: '48px' }}>
            {/* Left */}
            <div style={{ flex: '1 1 320px' }}>
              <h2 style={{ fontSize: '24px', fontWeight: 700, color: 'var(--color-text)', marginBottom: '12px' }}>
                Real ATS scoring, not guesswork.
              </h2>
              <p style={{ fontSize: '14px', color: 'var(--color-muted)', lineHeight: 1.7, marginBottom: '28px' }}>
                Our engine evaluates your resume across five dimensions: section structure,
                skill density, technical depth, project impact, and readability — just like a real ATS.
              </p>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
                {[
                  { label: 'Section Structure', pct: 90, color: '#FF7A59' },
                  { label: 'Skill Density', pct: 75, color: '#E6B566' },
                  { label: 'Technical Depth', pct: 85, color: '#34D399' },
                  { label: 'Project Impact', pct: 70, color: '#60A5FA' },
                  { label: 'Readability', pct: 95, color: '#A78BFA' },
                ].map((bar) => (
                  <div key={bar.label} style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
                    <span style={{ fontSize: '12px', color: 'var(--color-muted)', width: '120px', flexShrink: 0 }}>
                      {bar.label}
                    </span>
                    <div style={{ flex: 1, height: '6px', borderRadius: '3px', backgroundColor: 'var(--color-elevated)', overflow: 'hidden' }}>
                      <motion.div
                        initial={{ width: 0 }}
                        whileInView={{ width: `${bar.pct}%` }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.8, ease: 'easeOut' }}
                        style={{ height: '100%', borderRadius: '3px', backgroundColor: bar.color }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Right — Score ring */}
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px' }}>
              <div style={{
                width: '140px', height: '140px', borderRadius: '50%',
                border: '4px solid rgba(255, 122, 89, 0.25)',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
              }}>
                <span style={{ fontSize: '40px', fontWeight: 700, color: 'var(--color-accent)' }}>85</span>
              </div>
              <span style={{ fontSize: '12px', color: 'var(--color-muted)' }}>Sample ATS Score</span>
            </div>
          </div>
        </motion.div>
      </section>

      {/* ─── CTA ─── */}
      <section style={{ textAlign: 'center', paddingBottom: '80px' }}>
        <motion.div {...fadeUp(0)}>
          <h2 style={{ fontSize: '28px', fontWeight: 700, color: 'var(--color-text)', marginBottom: '12px' }}>
            Ready to optimize your resume?
          </h2>
          <p style={{ fontSize: '14px', color: 'var(--color-muted)', marginBottom: '28px' }}>
            It takes less than 30 seconds. No sign-up required.
          </p>
          <Link to="/upload"><Button>Get Started Free →</Button></Link>
        </motion.div>
      </section>
    </div>
  )
}
