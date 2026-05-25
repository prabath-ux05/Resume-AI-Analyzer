import { motion } from 'framer-motion'

const fadeUp = (delay = 0) => ({
  initial: { opacity: 0, y: 16 },
  animate: { opacity: 1, y: 0 },
  transition: { delay, duration: 0.45, ease: 'easeOut' },
})

const sections = [
  {
    title: '1. Introduction',
    body: `AscendAI ("we", "our", or "the Platform") is an AI-powered resume analysis service. This Privacy Policy explains how we collect, use, and protect your information when you use our platform. By using AscendAI, you agree to the practices described in this policy.`,
  },
  {
    title: '2. Information We Collect',
    body: `We collect the following types of information:
    
• Uploaded resume files (PDF or DOCX format)
• Text content extracted from uploaded resumes
• Technical skills, qualifications, and professional details parsed during analysis
• Basic usage analytics (pages visited, features used)

We do not collect personal account data, as no sign-up or login is required to use the platform.`,
  },
  {
    title: '3. Resume Data Usage',
    body: `Your uploaded resume is used solely for the purpose of providing analysis results, including ATS scoring, skill extraction, and job description matching. We do not sell, share, or distribute your resume data to any third party. Resume content is used only during your active session to generate analysis results.`,
  },
  {
    title: '4. File Processing',
    body: `Uploaded resume files are processed securely on our servers. Files are temporarily stored in memory during processing and are not permanently retained on our systems after your analysis is complete. We employ industry-standard encryption and secure transfer protocols to protect your data during upload and processing.`,
  },
  {
    title: '5. Data Security',
    body: `We implement reasonable technical and organizational measures to protect your information from unauthorized access, alteration, disclosure, or destruction. These measures include secure server infrastructure, encrypted data transmission, and access controls. However, no method of electronic transmission or storage is completely secure, and we cannot guarantee absolute security.`,
  },
  {
    title: '6. AI & NLP Processing',
    body: `Resume analysis is performed using automated AI and Natural Language Processing (NLP) systems, including transformer-based models for semantic analysis and rule-based engines for skill extraction and ATS scoring. These systems process your data algorithmically — no human reviews your resume content during analysis.`,
  },
  {
    title: '7. Third-Party Services',
    body: `We may use third-party infrastructure providers for hosting and processing. These providers are bound by their own privacy and security policies. We do not share identifiable resume content with third-party analytics or advertising services.`,
  },
  {
    title: '8. Your Rights',
    body: `You have the right to:

• Choose not to upload your resume at any time
• Request information about how your data was processed
• Contact us with any privacy-related concerns

Since we do not permanently store uploaded resumes, there is no retained data to delete after your session ends.`,
  },
  {
    title: '9. Changes to This Policy',
    body: `We may update this Privacy Policy from time to time to reflect changes in our practices or applicable regulations. We encourage you to review this page periodically. Continued use of the platform after any changes constitutes acceptance of the updated policy.`,
  },
  {
    title: '10. Contact Information',
    body: `If you have any questions or concerns about this Privacy Policy, please contact us at privacy@ascendai.com.`,
  },
]

export default function PrivacyPolicy() {
  return (
    <div style={{ maxWidth: '760px', margin: '0 auto', padding: '64px 24px 96px' }}>
      <motion.div {...fadeUp(0)} style={{ marginBottom: '48px' }}>
        <h1 style={{ fontSize: '32px', fontWeight: 700, color: 'var(--color-text)', marginBottom: '12px' }}>
          Privacy Policy
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
