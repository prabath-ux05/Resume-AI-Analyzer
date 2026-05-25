import { Navigate, Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import Card from '../components/Card'
import ScoreCircle from '../components/ScoreCircle'
import SkillTag from '../components/SkillTag'
import Button from '../components/Button'
import { useResumeContext } from '../context/ResumeContext'

/* ── Animation helpers ── */
const fadeUp = (delay = 0) => ({
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  transition: { delay, duration: 0.5, ease: [0.25, 0.46, 0.45, 0.94] },
})

const stagger = {
  animate: { transition: { staggerChildren: 0.06 } },
}
const staggerChild = {
  initial: { opacity: 0, y: 10 },
  animate: { opacity: 1, y: 0, transition: { duration: 0.3, ease: [0.25, 0.46, 0.45, 0.94] } },
}

/* ── Config ── */
const SKILL_LABELS = {
  languages: 'Programming Languages',
  frameworks: 'Frameworks & Libraries',
  cloud_devops: 'Cloud & DevOps',
  databases: 'Databases',
  ai_ml: 'AI / ML',
  tools_platforms: 'Tools & Platforms',
}

const BREAKDOWN_CONFIG = [
  { key: 'resume_structure',  label: 'Structure',   max: 20, color: '#FF7A59' },
  { key: 'skills',            label: 'Skills',      max: 25, color: '#E6B566' },
  { key: 'projects',          label: 'Projects',    max: 25, color: '#34D399' },
  { key: 'experience',        label: 'Experience',  max: 15, color: '#60A5FA' },
  { key: 'ats_keywords',      label: 'Keywords',    max: 10, color: '#A78BFA' },
  { key: 'education',         label: 'Education',   max: 5,  color: '#F472B6' },
]

const CONFIDENCE_CONFIG = {
  High:   { color: '#34D399', bg: 'rgba(52,211,153,0.06)',  border: 'rgba(52,211,153,0.15)',  label: 'Strong Candidate' },
  Medium: { color: '#E6B566', bg: 'rgba(230,181,102,0.06)', border: 'rgba(230,181,102,0.15)', label: 'Competitive Profile' },
  Low:    { color: '#F87171', bg: 'rgba(248,113,113,0.06)', border: 'rgba(248,113,113,0.15)', label: 'Needs Improvement' },
}

/* ── Section Header ── */
function SectionHeader({ title, subtitle, accentColor = 'var(--color-accent)', delay = 0 }) {
  return (
    <motion.div {...fadeUp(delay)} style={{ marginBottom: '24px' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: subtitle ? '6px' : '0' }}>
        <div style={{ width: '3px', height: '20px', borderRadius: '2px', backgroundColor: accentColor, flexShrink: 0 }} />
        <h2 style={{ fontSize: '18px', fontWeight: 600, color: 'var(--color-text)', letterSpacing: '-0.02em' }}>
          {title}
        </h2>
      </div>
      {subtitle && (
        <p style={{ fontSize: '13px', color: 'var(--color-dim)', marginLeft: '15px' }}>{subtitle}</p>
      )}
    </motion.div>
  )
}

/* ── Section Divider ── */
function SectionDivider() {
  return <div style={{ borderTop: '1px solid var(--color-line)', margin: '48px 0' }} />
}

/* ── Insight List Component ── */
function InsightList({ items, dotColor, emptyText }) {
  if (!items || items.length === 0) {
    return <p style={{ fontSize: '13px', color: 'var(--color-dim)', fontStyle: 'italic' }}>{emptyText}</p>
  }
  return (
    <motion.ul variants={stagger} initial="initial" animate="animate"
      style={{ listStyle: 'none', padding: 0, display: 'flex', flexDirection: 'column', gap: '10px' }}
    >
      {items.map((s, i) => (
        <motion.li key={i} variants={staggerChild}
          style={{ display: 'flex', alignItems: 'flex-start', gap: '10px', fontSize: '13px', color: 'var(--color-text)', lineHeight: 1.7 }}
        >
          <span style={{ color: dotColor, fontSize: '6px', marginTop: '8px', flexShrink: 0 }}>●</span>
          {s}
        </motion.li>
      ))}
    </motion.ul>
  )
}

/* ── Category Progress Bar ── */
function CategoryProgress({ label, score, max, color, delay }) {
  const pct = max > 0 ? Math.round((score / max) * 100) : 0
  return (
    <motion.div {...fadeUp(delay)} style={{ marginBottom: '14px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '7px' }}>
        <span style={{ fontSize: '13px', fontWeight: 500, color: 'var(--color-text)' }}>
          {label}
        </span>
        <span style={{ fontSize: '13px', fontWeight: 600, color: 'var(--color-text)', fontVariantNumeric: 'tabular-nums' }}>
          {score}<span style={{ fontSize: '11px', fontWeight: 400, color: 'var(--color-dim)', marginLeft: '1px' }}>/{max}</span>
        </span>
      </div>
      <div style={{ height: '5px', borderRadius: '3px', backgroundColor: 'var(--color-elevated)', overflow: 'hidden' }}>
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${pct}%` }}
          transition={{ duration: 1, delay: delay + 0.15, ease: [0.25, 0.46, 0.45, 0.94] }}
          style={{ height: '100%', borderRadius: '3px', backgroundColor: color }}
        />
      </div>
    </motion.div>
  )
}

/* ── Stat Card ── */
function StatCard({ label, value, color, bg, border, subtitle, delay = 0 }) {
  return (
    <motion.div {...fadeUp(delay)} style={{
      backgroundColor: bg || 'var(--color-surface)',
      border: `1px solid ${border || 'var(--color-line)'}`,
      borderRadius: '14px',
      padding: '24px',
    }}>
      <p style={{ fontSize: '11px', fontWeight: 600, color: 'var(--color-dim)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '10px' }}>
        {label}
      </p>
      <p style={{ fontSize: '26px', fontWeight: 700, color: color || 'var(--color-text)', letterSpacing: '-0.02em', lineHeight: 1.1 }}>
        {value}
      </p>
      {subtitle && <p style={{ fontSize: '12px', color: 'var(--color-dim)', marginTop: '6px' }}>{subtitle}</p>}
    </motion.div>
  )
}

/* ── Company Match Card ── */
function CompanyCard({ company, delay }) {
  return (
    <motion.div {...fadeUp(delay)}
      style={{
        backgroundColor: 'var(--color-surface)',
        border: '1px solid var(--color-line)',
        borderRadius: '14px',
        padding: '24px',
        transition: 'border-color 0.25s ease, box-shadow 0.25s ease',
      }}
      whileHover={{ borderColor: 'var(--color-line-hover)', boxShadow: '0 4px 16px rgba(0,0,0,0.15)' }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
        <h4 style={{ fontSize: '15px', fontWeight: 600, color: 'var(--color-text)' }}>{company.company_type}</h4>
        <span style={{
          fontSize: '12px', fontWeight: 700, color: '#34D399',
          backgroundColor: 'rgba(52,211,153,0.08)', padding: '4px 10px', borderRadius: '6px',
          fontVariantNumeric: 'tabular-nums',
        }}>
          {company.match_score}%
        </span>
      </div>
      <p style={{ fontSize: '13px', color: 'var(--color-muted)', lineHeight: 1.65 }}>
        {company.match_reason}
      </p>
    </motion.div>
  )
}

/* ═══════════════════════════════════════════ */
/*            MAIN DASHBOARD PAGE             */
/* ═══════════════════════════════════════════ */
export default function DashboardPage() {
  const { hasAnalysis, ats, skills, filename, resumeText } = useResumeContext()

  if (!hasAnalysis || !ats) return <Navigate to="/upload" replace />
  const bd = ats.score_breakdown || {}

  const confidenceLevel = ats.hiring_confidence_level || ats.recruiter_confidence || 'Medium'
  const conf = CONFIDENCE_CONFIG[confidenceLevel] || CONFIDENCE_CONFIG.Medium

  return (
    <div style={{ maxWidth: '1100px', margin: '0 auto', padding: '40px 24px 120px' }}>

      {/* ─────────── HEADER ─────────── */}
      <motion.div {...fadeUp(0)}
        style={{ display: 'flex', flexWrap: 'wrap', alignItems: 'flex-end', justifyContent: 'space-between', gap: '16px', marginBottom: '48px' }}
      >
        <div>
          <h1 style={{ fontSize: '26px', fontWeight: 700, color: 'var(--color-text)', letterSpacing: '-0.03em', marginBottom: '4px' }}>Resume Analysis</h1>
          <p style={{ fontSize: '14px', color: 'var(--color-dim)' }}>
            Results for <span style={{ color: 'var(--color-muted)', fontWeight: 500 }}>{filename || 'your resume'}</span>
          </p>
        </div>
        <div style={{ display: 'flex', gap: '10px' }}>
          <Link to="/match" state={{ resumeText }}><Button variant="secondary">Match Job →</Button></Link>
          <Link to="/upload"><Button variant="ghost">Upload New</Button></Link>
        </div>
      </motion.div>

      {/* ═══════════ 1. PROFESSIONAL OVERVIEW ═══════════ */}
      <motion.div {...fadeUp(0.04)} style={{ marginBottom: '0' }}>
        <Card style={{ padding: '32px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '20px' }}>
            <p style={{ fontSize: '11px', fontWeight: 600, color: 'var(--color-dim)', textTransform: 'uppercase', letterSpacing: '0.08em' }}>
              Professional Overview
            </p>
            {ats.domain_specialization && ats.domain_specialization !== "Not provided" && (
              <span style={{
                fontSize: '11px', fontWeight: 600, color: 'var(--color-accent)',
                backgroundColor: 'rgba(226, 104, 73, 0.08)', padding: '5px 12px',
                borderRadius: '6px', border: '1px solid rgba(226, 104, 73, 0.15)'
              }}>
                {ats.domain_specialization}
              </span>
            )}
          </div>

          <p style={{ fontSize: '17px', color: 'var(--color-text)', lineHeight: 1.65, fontWeight: 500, marginBottom: '28px' }}>
            {ats.semantic_profile_summary || 'No overview available.'}
          </p>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '24px', borderTop: '1px solid var(--color-line)', paddingTop: '24px' }}>
            <div>
              <h3 style={{ fontSize: '11px', fontWeight: 600, color: 'var(--color-dim)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '10px' }}>
                Candidate Summary
              </h3>
              <p style={{ fontSize: '14px', color: 'var(--color-muted)', lineHeight: 1.65 }}>
                {ats.candidate_summary || 'Not provided.'}
              </p>
            </div>
            <div>
              <h3 style={{ fontSize: '11px', fontWeight: 600, color: 'var(--color-dim)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '10px' }}>
                Recruiter Interpretation
              </h3>
              <p style={{ fontSize: '14px', color: 'var(--color-muted)', lineHeight: 1.65, fontStyle: 'italic' }}>
                "{ats.recruiter_interpretation || 'Not provided.'}"
              </p>
            </div>
          </div>
        </Card>
      </motion.div>

      <SectionDivider />

      {/* ═══════════ 2. ATS EVALUATION SYSTEM ═══════════ */}
      <SectionHeader title="ATS Evaluation System" subtitle="Weighted category breakdown" delay={0.06} />
      <div style={{ display: 'grid', gridTemplateColumns: 'minmax(280px, 320px) 1fr', gap: '24px', marginBottom: '0' }}>
        {/* Left column */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <motion.div {...fadeUp(0.08)}>
            <Card style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '36px 24px' }}>
              <ScoreCircle score={ats.ats_score} label="ATS Score" size={190} />
            </Card>
          </motion.div>

          <motion.div {...fadeUp(0.1)}>
            <Card style={{ padding: '20px' }}>
              <h3 style={{ fontSize: '11px', fontWeight: 600, color: 'var(--color-dim)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '10px' }}>
                Scoring Method
              </h3>
              <p style={{ fontSize: '13px', color: 'var(--color-muted)', lineHeight: 1.65 }}>
                Weighted algorithm: <strong style={{ color: 'var(--color-text)' }}>Skills 25%</strong> · <strong style={{ color: 'var(--color-text)' }}>Projects 25%</strong> · <strong style={{ color: 'var(--color-text)' }}>Structure 20%</strong> · <strong style={{ color: 'var(--color-text)' }}>Experience 15%</strong> · <strong style={{ color: 'var(--color-text)' }}>Keywords 10%</strong> · <strong style={{ color: 'var(--color-text)' }}>Education 5%</strong>
              </p>
            </Card>
          </motion.div>
        </div>

        {/* Right column */}
        <motion.div {...fadeUp(0.12)}>
          <Card style={{ height: '100%', padding: '28px 28px 16px' }}>
            <h3 style={{ fontSize: '11px', fontWeight: 600, color: 'var(--color-dim)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '24px' }}>
              Category Breakdown
            </h3>
            <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between', height: 'calc(100% - 48px)' }}>
              {BREAKDOWN_CONFIG.map((c, i) => (
                <CategoryProgress key={c.key} label={c.label} score={bd[c.key] ?? 0} max={c.max} color={c.color} delay={0.14 + i * 0.04} />
              ))}
            </div>
          </Card>
        </motion.div>
      </div>

      <SectionDivider />

      {/* ═══════════ 3. AI RECRUITER INTELLIGENCE ═══════════ */}
      <SectionHeader title="AI Recruiter Intelligence" subtitle="Hiring signals and risk assessment" accentColor="#60A5FA" delay={0.18} />

      {/* Stat cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '20px', marginBottom: '20px' }}>
        <StatCard label="Hiring Confidence" value={confidenceLevel} color={conf.color} bg={conf.bg} border={conf.border} subtitle={conf.label} delay={0.2} />
        <StatCard label="Profile Competitiveness" value={ats.profile_competitiveness || 'Average'} color="#60A5FA" subtitle="Estimated applicant ranking" delay={0.22} />
      </div>

      {/* Recruiter Impression */}
      <motion.div {...fadeUp(0.24)}>
        <Card style={{ marginBottom: '20px', padding: '24px' }}>
          <h3 style={{ fontSize: '11px', fontWeight: 600, color: 'var(--color-dim)', marginBottom: '12px', textTransform: 'uppercase', letterSpacing: '0.06em' }}>
            Recruiter Impression
          </h3>
          <p style={{ fontSize: '15px', color: 'var(--color-text)', lineHeight: 1.7, fontStyle: 'italic' }}>
            "{ats.recruiter_impression || 'No impression available.'}"
          </p>
        </Card>
      </motion.div>

      {/* Insights Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px', marginBottom: '20px' }}>
        <Card>
          <h3 style={{ fontSize: '12px', fontWeight: 600, color: '#34D399', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ width: '6px', height: '6px', borderRadius: '50%', backgroundColor: '#34D399' }} /> Key Strengths
          </h3>
          <InsightList items={ats.strengths} dotColor="#34D399" emptyText="No significant strengths identified." />
        </Card>

        <Card>
          <h3 style={{ fontSize: '12px', fontWeight: 600, color: '#E6B566', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ width: '6px', height: '6px', borderRadius: '50%', backgroundColor: '#E6B566' }} /> Areas for Growth
          </h3>
          <InsightList items={ats.weaknesses} dotColor="#E6B566" emptyText="No significant weaknesses identified." />
        </Card>

        <Card>
          <h3 style={{ fontSize: '12px', fontWeight: 600, color: '#F87171', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ width: '6px', height: '6px', borderRadius: '50%', backgroundColor: '#F87171' }} /> Hiring Risks
          </h3>
          <InsightList items={ats.hiring_risks} dotColor="#F87171" emptyText="No hiring risks detected." />
        </Card>
      </div>

      {/* Missing Keywords */}
      <Card>
        <h3 style={{ fontSize: '12px', fontWeight: 600, color: '#E6B566', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span style={{ width: '6px', height: '6px', borderRadius: '50%', backgroundColor: '#E6B566' }} /> Missing Industry Keywords
        </h3>
        {ats.missing_keywords && ats.missing_keywords.length > 0 ? (
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
            {ats.missing_keywords.map((kw, i) => (
              <span key={i} style={{
                fontSize: '12px', color: '#E6B566', backgroundColor: 'rgba(230,181,102,0.08)',
                padding: '4px 10px', borderRadius: '4px', border: '1px solid rgba(230,181,102,0.15)',
                fontWeight: 500,
              }}>
                {kw}
              </span>
            ))}
          </div>
        ) : (
          <p style={{ fontSize: '13px', color: 'var(--color-dim)', fontStyle: 'italic' }}>None missing.</p>
        )}
      </Card>

      <SectionDivider />

      {/* ═══════════ 4. PROJECT PORTFOLIO INTELLIGENCE ═══════════ */}
      <SectionHeader title="Project Portfolio Intelligence" subtitle="Deep evaluation of individual projects" accentColor="#A78BFA" delay={0.28} />
      {ats.project_portfolio ? (
        <>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '20px', marginBottom: '24px' }}>
            <Card style={{ padding: '24px' }}>
              <h3 style={{ fontSize: '11px', fontWeight: 600, color: 'var(--color-dim)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '12px' }}>AI Impact Evaluation</h3>
              <p style={{ fontSize: '14px', color: 'var(--color-muted)', lineHeight: 1.65 }}>{ats.project_portfolio.ai_impact_evaluation || 'Not evaluated.'}</p>
            </Card>
            <Card style={{ padding: '24px' }}>
              <h3 style={{ fontSize: '11px', fontWeight: 600, color: 'var(--color-dim)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '12px' }}>Recruiter Interpretation</h3>
              <p style={{ fontSize: '14px', color: 'var(--color-muted)', lineHeight: 1.65, fontStyle: 'italic' }}>"{ats.project_portfolio.recruiter_interpretation || 'Not evaluated.'}"</p>
            </Card>
          </div>
          {ats.project_portfolio.projects && ats.project_portfolio.projects.length > 0 && (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: '20px' }}>
              {ats.project_portfolio.projects.map((proj, i) => (
                <Card key={i} style={{ padding: '24px' }}>
                  <h4 style={{ fontSize: '15px', fontWeight: 600, color: 'var(--color-text)', marginBottom: '14px' }}>{proj.project_name}</h4>
                  <div style={{ display: 'flex', gap: '8px', marginBottom: '20px' }}>
                    <span style={{ fontSize: '11px', fontWeight: 600, backgroundColor: 'var(--color-elevated)', padding: '4px 10px', borderRadius: '4px', color: 'var(--color-muted)' }}>{proj.complexity_level}</span>
                    <span style={{ fontSize: '11px', fontWeight: 600, backgroundColor: 'rgba(52,211,153,0.08)', padding: '4px 10px', borderRadius: '4px', color: '#34D399' }}>{proj.production_readiness}</span>
                  </div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                    <CategoryProgress label="Technical Depth" score={proj.technical_depth_score || 0} max={10} color="#60A5FA" delay={0} />
                    <CategoryProgress label="Quality Rating" score={proj.project_quality_rating || 0} max={10} color="#E6B566" delay={0} />
                    <CategoryProgress label="Innovation" score={proj.innovation_score || 0} max={10} color="#A78BFA" delay={0} />
                  </div>
                </Card>
              ))}
            </div>
          )}
        </>
      ) : (
        <Card style={{ padding: '32px', textAlign: 'center' }}>
          <p style={{ fontSize: '14px', color: 'var(--color-dim)' }}>Upload a new resume to unlock project intelligence.</p>
        </Card>
      )}

      <SectionDivider />

      {/* ═══════════ 5. CAREER & COMPANY MATCHING ═══════════ */}
      <SectionHeader title="Career & Company Matching" subtitle="Role alignment and intelligent company fit" accentColor="#34D399" delay={0.3} />
      {ats.role_alignment_intelligence ? (
        <>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '20px', marginBottom: '20px' }}>
            <StatCard label="Career Alignment" value={`${ats.role_alignment_intelligence.career_alignment_score || 0}%`} color="#60A5FA" bg="rgba(96,165,250,0.06)" border="rgba(96,165,250,0.15)" delay={0.32} />
            <StatCard label="Strongest Domain" value={ats.role_alignment_intelligence.strongest_domain || 'Unknown'} delay={0.34} />
          </div>

          <motion.div {...fadeUp(0.36)}>
            <Card style={{ padding: '24px', marginBottom: '20px' }}>
              <h3 style={{ fontSize: '11px', fontWeight: 600, color: 'var(--color-dim)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '12px' }}>Industry Fit Analysis</h3>
              <p style={{ fontSize: '14px', color: 'var(--color-muted)', lineHeight: 1.65 }}>{ats.role_alignment_intelligence.industry_fit_analysis || 'Not evaluated.'}</p>
            </Card>
          </motion.div>

          {ats.role_alignment_intelligence.best_fit_roles && ats.role_alignment_intelligence.best_fit_roles.length > 0 && (
            <motion.div {...fadeUp(0.38)}>
              <Card style={{ padding: '24px', marginBottom: '20px' }}>
                <h3 style={{ fontSize: '11px', fontWeight: 600, color: 'var(--color-dim)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '14px' }}>Best Fit Roles</h3>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                  {ats.role_alignment_intelligence.best_fit_roles.map((r, i) => (
                    <span key={i} style={{ fontSize: '13px', fontWeight: 500, color: 'var(--color-text)', backgroundColor: 'var(--color-elevated)', padding: '6px 14px', borderRadius: '6px', border: '1px solid var(--color-line)' }}>
                      {r}
                    </span>
                  ))}
                </div>
              </Card>
            </motion.div>
          )}

          {ats.role_alignment_intelligence.company_matches && ats.role_alignment_intelligence.company_matches.length > 0 && (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px' }}>
              {ats.role_alignment_intelligence.company_matches.map((c, i) => (
                <CompanyCard key={i} company={c} delay={0.4 + i * 0.04} />
              ))}
            </div>
          )}
        </>
      ) : (
        <Card style={{ padding: '32px', textAlign: 'center' }}>
          <p style={{ fontSize: '14px', color: 'var(--color-dim)' }}>Upload a new resume to unlock career mapping.</p>
        </Card>
      )}

      <SectionDivider />

      {/* ═══════════ 6. EXTRACTED SKILLS ═══════════ */}
      <SectionHeader title="Skills Intelligence" subtitle="Semantically grouped technical skills" accentColor="#E6B566" delay={0.42} />
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '20px' }}>
        {Object.entries(SKILL_LABELS).map(([key, label]) => {
          const list = skills?.[key] || []
          if (list.length === 0) return null
          return (
            <Card key={key}>
              <h4 style={{ fontSize: '11px', fontWeight: 600, color: 'var(--color-dim)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '14px' }}>
                {label}
              </h4>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                {list.map(s => <SkillTag key={s} label={s} />)}
              </div>
            </Card>
          )
        })}
      </div>

      <SectionDivider />

      {/* ═══════════ 7. IMPROVEMENT ROADMAP ═══════════ */}
      <SectionHeader title="Resume Improvement Roadmap" subtitle="Actionable steps to strengthen your profile" accentColor="#F472B6" delay={0.46} />
      {ats.improvement_roadmap ? (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px' }}>
          <Card>
            <h3 style={{ fontSize: '12px', fontWeight: 600, color: 'var(--color-accent)', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span style={{ width: '6px', height: '6px', borderRadius: '50%', backgroundColor: 'var(--color-accent)' }} /> Prioritized Suggestions
            </h3>
            <InsightList items={ats.improvement_roadmap.prioritized_suggestions} dotColor="var(--color-accent)" emptyText="No suggestions." />
          </Card>
          <Card>
            <h3 style={{ fontSize: '12px', fontWeight: 600, color: '#34D399', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span style={{ width: '6px', height: '6px', borderRadius: '50%', backgroundColor: '#34D399' }} /> Missing Skills
            </h3>
            <InsightList items={ats.improvement_roadmap.missing_skills} dotColor="#34D399" emptyText="No missing skills detected." />
          </Card>
          <Card>
            <h3 style={{ fontSize: '12px', fontWeight: 600, color: '#A78BFA', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span style={{ width: '6px', height: '6px', borderRadius: '50%', backgroundColor: '#A78BFA' }} /> Keyword Gaps
            </h3>
            <InsightList items={ats.improvement_roadmap.recruiter_keyword_gaps} dotColor="#A78BFA" emptyText="No gaps detected." />
          </Card>
          <Card>
            <h3 style={{ fontSize: '12px', fontWeight: 600, color: '#F472B6', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span style={{ width: '6px', height: '6px', borderRadius: '50%', backgroundColor: '#F472B6' }} /> Learning Roadmap
            </h3>
            <InsightList items={ats.improvement_roadmap.learning_roadmap} dotColor="#F472B6" emptyText="No learning steps identified." />
          </Card>
          <Card style={{ gridColumn: '1 / -1' }}>
            <h3 style={{ fontSize: '12px', fontWeight: 600, color: '#60A5FA', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span style={{ width: '6px', height: '6px', borderRadius: '50%', backgroundColor: '#60A5FA' }} /> Next Career Steps
            </h3>
            <InsightList items={ats.improvement_roadmap.next_career_steps} dotColor="#60A5FA" emptyText="No next steps identified." />
          </Card>
        </div>
      ) : (
        <Card style={{ padding: '32px', textAlign: 'center' }}>
          <p style={{ fontSize: '14px', color: 'var(--color-dim)' }}>Upload a new resume to unlock the improvement roadmap.</p>
        </Card>
      )}
    </div>
  )
}
