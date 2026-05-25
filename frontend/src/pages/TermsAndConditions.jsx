import { motion } from 'framer-motion'

const fadeUp = (delay = 0) => ({
  initial: { opacity: 0, y: 16 },
  animate: { opacity: 1, y: 0 },
  transition: { delay, duration: 0.45, ease: 'easeOut' },
})

const sections = [
  {
    title: '1. Acceptance of Terms',
    body: `By accessing or using the AscendAI platform ("the Platform"), you agree to be bound by these Terms & Conditions. If you do not agree to these terms, please do not use the Platform. We reserve the right to modify these terms at any time, and your continued use of the Platform constitutes acceptance of any changes.`,
  },
  {
    title: '2. Platform Usage',
    body: `AscendAI provides AI-powered resume analysis tools, including ATS scoring, technical skill extraction, and semantic job description matching. The Platform is provided "as-is" and is intended for personal, non-commercial use to assist individuals in improving their resumes. You agree to use the Platform only for lawful purposes and in accordance with these terms.`,
  },
  {
    title: '3. User Responsibilities',
    body: `As a user of the Platform, you are responsible for:

• Ensuring that the resumes you upload are your own or that you have authorization to upload them
• Providing accurate and truthful information in uploaded documents
• Not uploading malicious files, scripts, or content designed to exploit or damage the Platform
• Not attempting to reverse-engineer, decompile, or interfere with the Platform's AI systems`,
  },
  {
    title: '4. AI Analysis Disclaimer',
    body: `The ATS scores, skill extractions, job match scores, and recommendations provided by the Platform are estimation-based and generated using automated AI and NLP algorithms. These results are intended as guidance only and should not be interpreted as guaranteed outcomes.

Analysis results may not fully reflect actual recruiter decisions, applicant tracking system behavior, or hiring outcomes. Different companies use different ATS software with varying criteria. We recommend using our analysis as one of several tools in your job search process.`,
  },
  {
    title: '5. Intellectual Property',
    body: `All content, design, code, algorithms, and branding associated with the Platform are the intellectual property of AscendAI. You may not reproduce, distribute, or create derivative works from any part of the Platform without prior written consent. The resume content you upload remains your own intellectual property.`,
  },
  {
    title: '6. Data Handling',
    body: `Uploaded resumes are processed in real-time and are not permanently stored on our servers. We do not claim ownership over any content you upload. For full details on how we handle your data, please refer to our Privacy Policy.`,
  },
  {
    title: '7. Limitation of Liability',
    body: `To the maximum extent permitted by applicable law, AscendAI and its operators shall not be liable for any indirect, incidental, special, consequential, or punitive damages arising from your use of the Platform. This includes, but is not limited to, damages resulting from reliance on analysis results, loss of employment opportunities, or inaccuracies in the AI-generated output.

The Platform is provided without warranties of any kind, whether express or implied, including but not limited to warranties of merchantability, fitness for a particular purpose, or non-infringement.`,
  },
  {
    title: '8. Service Availability',
    body: `We strive to maintain continuous availability of the Platform but do not guarantee uninterrupted access. The Platform may be temporarily unavailable due to maintenance, updates, or circumstances beyond our control. We reserve the right to modify, suspend, or discontinue any aspect of the Platform at any time.`,
  },
  {
    title: '9. Changes to Terms',
    body: `We may revise these Terms & Conditions at any time by updating this page. Changes become effective immediately upon posting. It is your responsibility to review these terms periodically. Your continued use of the Platform after any changes constitutes acceptance of the revised terms.`,
  },
  {
    title: '10. Contact Information',
    body: `If you have any questions about these Terms & Conditions, please contact us at legal@ascendai.com.`,
  },
]

export default function TermsAndConditions() {
  return (
    <div style={{ maxWidth: '760px', margin: '0 auto', padding: '64px 24px 96px' }}>
      <motion.div {...fadeUp(0)} style={{ marginBottom: '48px' }}>
        <h1 style={{ fontSize: '32px', fontWeight: 700, color: 'var(--color-text)', marginBottom: '12px' }}>
          Terms & Conditions
        </h1>
        <p style={{ fontSize: '13px', color: 'var(--color-muted)' }}>
          Last updated: May 2026
        </p>
      </motion.div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '36px' }}>
        {sections.map((s, i) => (
          <motion.div key={i} {...fadeUp(0.03 * i)}>
            <h2 style={{
              fontSize: '16px', fontWeight: 600, color: 'var(--color-text)',
              marginBottom: '12px',
            }}>
              {s.title}
            </h2>
            <p style={{
              fontSize: '14px', color: 'var(--color-muted)', lineHeight: 1.8,
              whiteSpace: 'pre-line',
            }}>
              {s.body}
            </p>
          </motion.div>
        ))}
      </div>
    </div>
  )
}
