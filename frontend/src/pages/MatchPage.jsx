import { useState, useEffect, useRef } from 'react'
import { Navigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts'
import Card from '../components/Card'
import Button from '../components/Button'
import ScoreCircle from '../components/ScoreCircle'
import SkillTag from '../components/SkillTag'
import { autoRoleMatch } from '../services/api'
import { useResumeContext } from '../context/ResumeContext'

const fadeUp = (delay = 0) => ({
  initial: { opacity: 0, y: 16 },
  animate: { opacity: 1, y: 0 },
  transition: { delay, duration: 0.4, ease: 'easeOut' },
})

const ROLE_COLORS = [
  '#8B5CF6', '#06B6D4', '#F59E0B', '#EC4899', '#10B981', '#F97316', '#6366F1', '#14B8A6',
]

const ROLE_BG = [
  'rgba(139,92,246,0.07)', 'rgba(6,182,212,0.07)', 'rgba(245,158,11,0.07)',
  'rgba(236,72,153,0.07)', 'rgba(16,185,129,0.07)', 'rgba(249,115,22,0.07)',
  'rgba(99,102,241,0.07)', 'rgba(20,184,166,0.07)',
]

const ROLE_BORDER = [
  'rgba(139,92,246,0.22)', 'rgba(6,182,212,0.22)', 'rgba(245,158,11,0.22)',
  'rgba(236,72,153,0.22)', 'rgba(16,185,129,0.22)', 'rgba(249,115,22,0.22)',
  'rgba(99,102,241,0.22)', 'rgba(20,184,166,0.22)',
]

const RANK_ICONS = ['🥇', '🥈', '🥉', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣']

// ── Custom Recharts Tooltip
function CustomTooltip({ active, payload }) {
  if (!active || !payload?.length) return null
  const d = payload[0].payload
  return (
    <div style={{
      backgroundColor: 'var(--color-surface)', border: '1px solid var(--color-line)',
      borderRadius: '10px', padding: '12px 16px', boxShadow: '0 8px 32px rgba(0,0,0,0.35)',
      minWidth: '160px',
    }}>
      <p style={{ fontSize: '13px', fontWeight: 700, color: 'var(--color-text)', marginBottom: '4px' }}>{d.role}</p>
      <p style={{ fontSize: '24px', fontWeight: 800, color: d.fill || 'var(--color-accent)' }}>{d.score}<span style={{ fontSize: '12px', color: 'var(--color-dim)' }}>/100</span></p>
    </div>
  )
}

// ── Inline progress bar for score
function ScoreBar({ score, color, label }) {
  const barColor = color || (score >= 75 ? '#34D399' : score >= 50 ? '#E6B566' : '#F87171')
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '12px', width: '100%' }}>
      <span style={{ fontSize: '12px', fontWeight: 600, color: 'var(--color-muted)', minWidth: '110px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{label}</span>
      <div style={{ flex: 1, height: '8px', borderRadius: '4px', backgroundColor: 'var(--color-elevated)', overflow: 'hidden' }}>
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${score}%` }}
          transition={{ duration: 0.9, ease: [0.25, 0.46, 0.45, 0.94], delay: 0.1 }}
          style={{ height: '100%', borderRadius: '4px', backgroundColor: barColor }}
        />
      </div>
      <span style={{ fontSize: '13px', fontWeight: 700, color: barColor, minWidth: '32px', textAlign: 'right' }}>{score}</span>
    </div>
  )
}

// ── Expandable Role Card
function RoleCard({ match, index, isExpanded, onToggle }) {
  const color = ROLE_COLORS[index % ROLE_COLORS.length]
  const bg = ROLE_BG[index % ROLE_BG.length]
  const border = ROLE_BORDER[index % ROLE_BORDER.length]
  const scoreColor = match.score >= 75 ? '#34D399' : match.score >= 50 ? '#E6B566' : '#F87171'

  return (
    <motion.div {...fadeUp(0.04 * index)} layout onClick={onToggle} style={{ cursor: 'pointer' }}>
      <div style={{
        backgroundColor: 'var(--color-surface)',
        border: isExpanded ? `1.5px solid ${color}` : '1px solid var(--color-line)',
        borderRadius: '16px', padding: '20px 24px',
        transition: 'all 0.25s ease',
        boxShadow: isExpanded ? `0 0 24px ${bg}` : 'none',
      }}>
        {/* Header */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '14px', flex: 1, minWidth: 0 }}>
            <span style={{ fontSize: '24px', flexShrink: 0 }}>{RANK_ICONS[index]}</span>
            <div style={{ minWidth: 0, flex: 1 }}>
              <h3 style={{ fontSize: '15px', fontWeight: 700, color: 'var(--color-text)', margin: 0 }}>{match.role}</h3>
              <p style={{
                fontSize: '12px', color: 'var(--color-muted)', margin: '4px 0 0', lineHeight: 1.5,
                display: '-webkit-box', WebkitLineClamp: isExpanded ? 'unset' : 1, WebkitBoxOrient: 'vertical', overflow: 'hidden',
              }}>{match.reason}</p>
            </div>
          </div>
          {/* Score pill */}
          <div style={{
            display: 'flex', alignItems: 'center', gap: '8px', flexShrink: 0,
            padding: '8px 16px', borderRadius: '12px',
            background: bg, border: `1px solid ${border}`,
          }}>
            <span style={{ fontSize: '22px', fontWeight: 800, color: scoreColor }}>{match.score}</span>
            <span style={{ fontSize: '10px', color: 'var(--color-dim)', fontWeight: 600, letterSpacing: '0.06em' }}>/ 100</span>
          </div>
        </div>

        {/* Progress bar inline */}
        <div style={{ marginTop: '14px' }}>
          <ScoreBar score={match.score} color={color} label="Role Fit" />
        </div>

        {/* Expanded details */}
        <AnimatePresence>
          {isExpanded && (
            <motion.div
              key="details"
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              transition={{ duration: 0.3, ease: 'easeOut' }}
              style={{ overflow: 'hidden' }}
            >
              <div style={{ marginTop: '20px', paddingTop: '20px', borderTop: '1px solid var(--color-line)' }}>
                {/* Skills grid */}
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '20px' }}>
                  <div>
                    <h4 style={{
                      fontSize: '11px', fontWeight: 700, color: '#34D399', marginBottom: '10px',
                      textTransform: 'uppercase', letterSpacing: '0.08em',
                      display: 'flex', alignItems: 'center', gap: '5px',
                    }}><span>✓</span> Matching Skills</h4>
                    {match.matching_skills?.length > 0 ? (
                      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '5px' }}>
                        {match.matching_skills.map(s => <SkillTag key={s} label={s} variant="match" />)}
                      </div>
                    ) : (
                      <p style={{ fontSize: '12px', color: 'var(--color-dim)', fontStyle: 'italic' }}>No direct matches.</p>
                    )}
                  </div>
                  <div>
                    <h4 style={{
                      fontSize: '11px', fontWeight: 700, color: '#F87171', marginBottom: '10px',
                      textTransform: 'uppercase', letterSpacing: '0.08em',
                      display: 'flex', alignItems: 'center', gap: '5px',
                    }}><span>✗</span> Missing Skills</h4>
                    {match.missing_skills?.length > 0 ? (
                      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '5px' }}>
                        {match.missing_skills.map(s => <SkillTag key={s} label={s} variant="missing" />)}
                      </div>
                    ) : (
                      <p style={{ fontSize: '12px', color: 'var(--color-dim)', fontStyle: 'italic' }}>No gaps — great fit!</p>
                    )}
                  </div>
                </div>

                {/* Why this role fits */}
                <div style={{
                  padding: '14px 18px', borderRadius: '12px',
                  backgroundColor: bg, border: `1px solid ${border}`, marginBottom: '16px',
                }}>
                  <h4 style={{
                    fontSize: '11px', fontWeight: 700, color, marginBottom: '8px',
                    textTransform: 'uppercase', letterSpacing: '0.08em',
                  }}>✦ Why This Role Fits</h4>
                  <p style={{ fontSize: '13px', color: 'var(--color-text)', lineHeight: 1.7 }}>{match.reason}</p>
                </div>

                {/* Improvement suggestions */}
                {match.recommendations?.length > 0 && (
                  <div>
                    <h4 style={{
                      fontSize: '11px', fontWeight: 700, color: '#E6B566', marginBottom: '10px',
                      textTransform: 'uppercase', letterSpacing: '0.08em',
                      display: 'flex', alignItems: 'center', gap: '5px',
                    }}><span>💡</span> Improvement Suggestions</h4>
                    <ul style={{ listStyle: 'none', padding: 0, display: 'flex', flexDirection: 'column', gap: '8px' }}>
                      {match.recommendations.map((r, i) => (
                        <li key={i} style={{
                          display: 'flex', alignItems: 'flex-start', gap: '8px',
                          fontSize: '13px', color: 'var(--color-text)', lineHeight: 1.6,
                        }}>
                          <span style={{ color, flexShrink: 0, fontWeight: 700 }}>→</span>{r}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        <div style={{ marginTop: '10px', textAlign: 'center', fontSize: '10px', color: 'var(--color-dim)', letterSpacing: '0.04em' }}>
          {isExpanded ? '▲ Collapse' : '▼ View Details'}
        </div>
      </div>
    </motion.div>
  )
}

// ── Main Page
export default function MatchPage() {
  const { fileHash, hasAnalysis, roleMatchResult, setRoleMatchResult } = useResumeContext()
  const [loading, setLoading] = useState(false)
  const [matches, setMatches] = useState(roleMatchResult || null)
  const [error, setError] = useState('')
  const [expandedIdx, setExpandedIdx] = useState(roleMatchResult?.length > 0 ? 0 : null)
  const autoLoadAttempted = useRef(false)

  // Auto-load: on mount, if context has no matches, silently ask backend for cached results
  useEffect(() => {
    if (autoLoadAttempted.current) return
    if (!hasAnalysis || !fileHash) return
    if (matches && matches.length > 0) return // already have local data
    autoLoadAttempted.current = true

    // Check cache silently without triggering the main loading UI
    autoRoleMatch(fileHash, false, true)
      .then(res => {
        if (res.status === 'success' && res.matches?.length > 0) {
          setMatches(res.matches)
          setRoleMatchResult(res.matches)
          setExpandedIdx(0)
        }
      })
      .catch(() => {
        // Silently fail — user can still click Generate manually
      })
  }, [hasAnalysis, fileHash]) // eslint-disable-line react-hooks/exhaustive-deps

  if (!hasAnalysis || !fileHash) {
    return (
      <div style={{
        flex: 1,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '120px 24px',
        textAlign: 'center',
      }}>
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.4, ease: 'easeOut' }}
          style={{ maxWidth: '400px', display: 'flex', flexDirection: 'column', alignItems: 'center' }}
        >
          <div style={{
            width: '64px', height: '64px',
            borderRadius: '20px',
            background: 'linear-gradient(135deg, var(--color-accent) 0%, #FF4F87 100%)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: '28px',
            marginBottom: '24px',
            boxShadow: '0 0 32px rgba(255, 122, 89, 0.25)',
          }}>🎯</div>
          <h2 style={{ fontSize: '22px', fontWeight: 600, color: 'var(--color-text)', marginBottom: '12px' }}>
            Resume context required
          </h2>
          <p style={{ fontSize: '14px', color: 'var(--color-muted)', lineHeight: '1.7', marginBottom: '32px' }}>
            Upload and analyze a resume first to generate role matches.
          </p>
          <Button onClick={() => window.location.href = '/upload'}>
            Upload Resume
          </Button>
        </motion.div>
      </div>
    )
  }

  const handleGenerate = async (isRegenerate = false) => {
    setError('')
    setLoading(true)
    // Only clear matches if we are starting fresh. If regenerating, keep old ones on screen.
    if (!matches) {
      setExpandedIdx(null)
    }
    
    try {
      const res = await autoRoleMatch(fileHash, isRegenerate)
      setMatches(res.matches || [])
      setRoleMatchResult(res.matches || [])
      if (res.matches?.length > 0) setExpandedIdx(0)
    } catch (err) {
      setError(err?.response?.data?.detail || 'Role matching failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const avgScore = matches ? Math.round(matches.reduce((s, m) => s + m.score, 0) / matches.length) : 0
  const barData = matches ? matches.map((m, i) => ({ role: m.role.length > 18 ? m.role.slice(0, 16) + '…' : m.role, score: m.score, fill: ROLE_COLORS[i % ROLE_COLORS.length] })) : []

  // Build radar data from top match
  const radarData = matches && matches[0] ? [
    { axis: 'Matching', value: Math.min(100, (matches[0].matching_skills?.length || 0) * 14) },
    { axis: 'Score', value: matches[0].score },
    { axis: 'Fit', value: Math.max(30, matches[0].score + 5) },
    { axis: 'Skills Gap', value: Math.max(10, 100 - (matches[0].missing_skills?.length || 0) * 15) },
    { axis: 'Potential', value: Math.min(100, avgScore + 10) },
  ] : []

  return (
    <div style={{ maxWidth: '1100px', margin: '0 auto', padding: '48px 24px 96px' }}>
      {/* Header */}
      <motion.div {...fadeUp(0)} style={{ marginBottom: '36px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '6px' }}>
          <div style={{
            width: '38px', height: '38px', borderRadius: '11px',
            background: 'linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: '17px', boxShadow: '0 0 24px rgba(139,92,246,0.3)',
          }}>🎯</div>
          <h1 style={{ fontSize: '24px', fontWeight: 700, color: 'var(--color-text)' }}>AI Role Match</h1>
        </div>
        <p style={{ fontSize: '13px', color: 'var(--color-muted)', marginTop: '4px', maxWidth: '560px', lineHeight: 1.6 }}>
          Discover the roles that best fit your resume, skills, and project experience.
        </p>
      </motion.div>

      {/* ── Empty / Generate State */}
      {!matches && !loading && (
        <motion.div {...fadeUp(0.05)}>
          <Card style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '72px 24px', textAlign: 'center' }}>
            <div style={{
              width: '72px', height: '72px', borderRadius: '22px',
              background: 'linear-gradient(135deg, rgba(139,92,246,0.15), rgba(236,72,153,0.15))',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontSize: '30px', marginBottom: '28px',
              border: '1px solid rgba(139,92,246,0.2)',
              boxShadow: '0 0 40px rgba(139,92,246,0.12)',
            }}>✦</div>
            <h2 style={{ fontSize: '20px', fontWeight: 700, color: 'var(--color-text)', marginBottom: '8px' }}>
              {error ? 'Generation Failed' : 'Ready to discover your best-fit roles'}
            </h2>
            <p style={{ fontSize: '13px', color: 'var(--color-muted)', maxWidth: '400px', lineHeight: 1.7, marginBottom: '32px' }}>
              {error ? 'An error occurred while matching roles. Please try again.' : 'Our AI analyzes your skills, projects, and experience to rank the roles where you\'d be the strongest candidate — powered by hybrid semantic scoring.'}
            </p>
            {error && <p style={{ fontSize: '12px', color: 'var(--color-err)', marginBottom: '16px' }}>{error}</p>}
            
            <Button onClick={() => handleGenerate(false)} disabled={loading}>
              {error ? 'Retry Role Generation' : 'Generate Role Matches'}
            </Button>
          </Card>
        </motion.div>
      )}

      {/* ── Full Page Loading (Only if no matches exist yet) */}
      {!matches && loading && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '96px 24px', textAlign: 'center' }}>
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ repeat: Infinity, duration: 1.2, ease: 'linear' }}
            style={{ width: '52px', height: '52px', borderRadius: '50%', border: '3px solid var(--color-line)', borderTopColor: '#8B5CF6', marginBottom: '28px' }}
          />
          <p style={{ fontSize: '15px', fontWeight: 600, color: 'var(--color-text)', marginBottom: '6px' }}>Generating role matches...</p>
          <p style={{ fontSize: '12px', color: 'var(--color-muted)' }}>Evaluating skill overlap, project relevance, and domain fit</p>
        </motion.div>
      )}

      {/* ── Results Dashboard */}
      {matches && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px', opacity: loading ? 0.6 : 1, transition: 'opacity 0.3s ease' }}>

          {/* ── Top Summary Row */}
          <motion.div {...fadeUp(0)}>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '20px' }}>
              {/* Best Fit Score */}
              <Card style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '28px 16px' }}>
                <ScoreCircle score={matches[0]?.score || 0} label="Best Fit" size={120} />
                <p style={{ fontSize: '13px', fontWeight: 600, color: 'var(--color-text)', marginTop: '8px', textAlign: 'center' }}>{matches[0]?.role}</p>
              </Card>

              {/* Average & Stats */}
              <Card style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', padding: '28px 24px', gap: '16px' }}>
                <div>
                  <p style={{ fontSize: '10px', fontWeight: 700, color: 'var(--color-dim)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '4px' }}>Average Score</p>
                  <p style={{ fontSize: '32px', fontWeight: 800, color: 'var(--color-accent)', lineHeight: 1 }}>{avgScore}</p>
                </div>
                <div>
                  <p style={{ fontSize: '10px', fontWeight: 700, color: 'var(--color-dim)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '4px' }}>Roles Analyzed</p>
                  <p style={{ fontSize: '32px', fontWeight: 800, color: 'var(--color-text)', lineHeight: 1 }}>{matches.length}</p>
                </div>
                <div>
                  <p style={{ fontSize: '10px', fontWeight: 700, color: 'var(--color-dim)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '4px' }}>Top Match Skills</p>
                  <p style={{ fontSize: '32px', fontWeight: 800, color: '#34D399', lineHeight: 1 }}>{matches[0]?.matching_skills?.length || 0}</p>
                </div>
              </Card>

              {/* Radar Chart */}
              <Card style={{ padding: '16px 8px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <ResponsiveContainer width="100%" height={200}>
                  <RadarChart data={radarData} cx="50%" cy="50%" outerRadius="70%">
                    <PolarGrid stroke="var(--color-line)" />
                    <PolarAngleAxis dataKey="axis" tick={{ fill: 'var(--color-muted)', fontSize: 10, fontWeight: 600 }} />
                    <PolarRadiusAxis angle={90} domain={[0, 100]} tick={false} axisLine={false} />
                    <Radar name="Profile" dataKey="value" stroke="#8B5CF6" fill="rgba(139,92,246,0.2)" strokeWidth={2} />
                  </RadarChart>
                </ResponsiveContainer>
              </Card>
            </div>
          </motion.div>

          {/* ── Role Ranking Bar Chart */}
          <motion.div {...fadeUp(0.05)}>
            <Card style={{ padding: '24px' }}>
              <h3 style={{ fontSize: '13px', fontWeight: 700, color: 'var(--color-text)', marginBottom: '20px', textTransform: 'uppercase', letterSpacing: '0.06em' }}>
                Role Ranking Overview
              </h3>
              <ResponsiveContainer width="100%" height={260}>
                <BarChart data={barData} layout="vertical" margin={{ left: 8, right: 24, top: 4, bottom: 4 }} barCategoryGap="22%">
                  <CartesianGrid strokeDasharray="3 3" stroke="var(--color-line)" horizontal={false} />
                  <XAxis type="number" domain={[0, 100]} tick={{ fill: 'var(--color-dim)', fontSize: 11 }} axisLine={{ stroke: 'var(--color-line)' }} />
                  <YAxis type="category" dataKey="role" tick={{ fill: 'var(--color-muted)', fontSize: 12, fontWeight: 600 }} axisLine={false} tickLine={false} width={140} />
                  <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(255,255,255,0.03)' }} />
                  <Bar dataKey="score" radius={[0, 6, 6, 0]} barSize={18}>
                    {barData.map((entry, i) => (
                      <Cell key={`cell-${i}`} fill={entry.fill} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </Card>
          </motion.div>

          {/* ── All Scores Progress Bars */}
          <motion.div {...fadeUp(0.08)}>
            <Card style={{ padding: '24px' }}>
              <h3 style={{ fontSize: '13px', fontWeight: 700, color: 'var(--color-text)', marginBottom: '18px', textTransform: 'uppercase', letterSpacing: '0.06em' }}>
                Score Breakdown
              </h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
                {matches.map((m, i) => (
                  <ScoreBar key={m.role} score={m.score} color={ROLE_COLORS[i % ROLE_COLORS.length]} label={m.role} />
                ))}
              </div>
            </Card>
          </motion.div>

          {/* ── Individual Role Cards */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            <h3 style={{ fontSize: '13px', fontWeight: 700, color: 'var(--color-text)', textTransform: 'uppercase', letterSpacing: '0.06em', paddingLeft: '4px' }}>
              Detailed Role Analysis
            </h3>
            {matches.map((match, idx) => (
              <RoleCard
                key={match.role + idx}
                match={match}
                index={idx}
                isExpanded={expandedIdx === idx}
                onToggle={() => setExpandedIdx(expandedIdx === idx ? null : idx)}
              />
            ))}
          </div>

          {/* Re-generate */}
          <motion.div {...fadeUp(0.1)} style={{ display: 'flex', justifyContent: 'center', paddingTop: '8px' }}>
            <Button variant="secondary" onClick={() => handleGenerate(true)} disabled={loading}>
              {loading ? 'Regenerating...' : 'Regenerate Matches'}
            </Button>
          </motion.div>
        </div>
      )}
    </div>
  )
}
