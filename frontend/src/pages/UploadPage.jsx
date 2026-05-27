import { useState, useCallback } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import Card from '../components/Card'
import Button from '../components/Button'
import { analyzeResume, autoRoleMatch } from '../services/api'
import { useResumeContext } from '../context/ResumeContext'

const ALLOWED = [
  'application/pdf',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
]

export default function UploadPage() {
  const navigate = useNavigate()
  const { hasAnalysis, filename: existingFilename, setAnalysisData, resetAnalysis } = useResumeContext()
  
  const [file, setFile] = useState(null)
  const [dragging, setDragging] = useState(false)
  const [status, setStatus] = useState('idle') // idle | uploading | processing | done | error
  const [error, setError] = useState('')
  const [progress, setProgress] = useState(0)

  const validate = (f) => {
    if (!f) return 'No file selected.'
    if (!ALLOWED.includes(f.type)) return 'Only PDF and DOCX files are accepted.'
    if (f.size > 10 * 1024 * 1024) return 'File must be under 10 MB.'
    return null
  }

  const selectFile = (f) => {
    const err = validate(f)
    if (err) { setError(err); return }
    setError('')
    setFile(f)
    setStatus('idle')
  }

  const onDrop = useCallback((e) => {
    e.preventDefault()
    setDragging(false)
    const f = e.dataTransfer?.files?.[0]
    if (f) selectFile(f)
  }, [])

  const handleUpload = async () => {
    if (!file) return
    try {
      setStatus('uploading')
      setError('')
      setProgress(15)

      const uploadRes = await analyzeResume(file)
      console.log('UPLOAD SUCCESS PAYLOAD:', uploadRes)
      
      if (uploadRes?.status === 'error' || (uploadRes?.status && uploadRes?.status !== 'success')) {
        throw new Error(uploadRes?.message || uploadRes?.detail || 'Analysis failed on server.')
      }
      
      setProgress(60)
      setStatus('processing')

      setProgress(100)
      setStatus('done')

      // Set global state
      const { filename, data } = uploadRes
      const fileHash = data?.file_hash || ''
      setAnalysisData(
        filename || file.name, 
        "Extracted text not available in V2 API", 
        fileHash, 
        data?.skills || [], 
        data || {}
      )

      setStatus('done')

      // Trigger auto role match in the background
      if (fileHash) {
        console.log(`Triggering /job-match/auto for file_hash: ${fileHash}`)
        try {
          await autoRoleMatch(fileHash, false, false)
          console.log('Role match triggered successfully.')
        } catch (roleErr) {
          console.error('Role Match Error after upload:', roleErr)
          // We don't want to block the user from seeing their analysis.
          // The MatchPage will show the error when they navigate there.
          console.warn('Resume uploaded successfully, but role matching failed.')
        }
      } else {
        console.warn('Skipping /job-match/auto: No valid file_hash found in response.')
      }

      setTimeout(() => {
        navigate('/dashboard')
      }, 1200)
    } catch (err) {
      console.error('Upload error:', err)
      setStatus('error')
      
      const isNetworkError = err?.message === 'Network Error' || err?.name === 'AxiosError'
      
      setError(
        isNetworkError 
          ? 'Network Error during upload. The server might have succeeded but CORS blocked the response.' 
          : (err?.response?.data?.detail || err?.response?.data?.message || err?.message || 'Upload failed. Please try again.')
      )
    }
  }

  const statusLabel = {
    uploading: 'Uploading resume…',
    processing: 'Running AI analysis…',
    done: 'Analysis complete — redirecting…',
  }

  const formatSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B'
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
  }

  // EARLY RETURN FOR EXISTING ANALYSIS MUST BE AFTER ALL HOOKS
  if (hasAnalysis && status === 'idle' && !file) {
    return (
      <div style={{ maxWidth: '600px', margin: '0 auto', padding: '80px 24px 96px', textAlign: 'center' }}>
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          <span style={{ fontSize: '48px', display: 'block', marginBottom: '16px' }}>✨</span>
          <h1 style={{ fontSize: '28px', fontWeight: 700, color: 'var(--color-text)', marginBottom: '8px' }}>
            Resume Already Analyzed
          </h1>
          <p style={{ fontSize: '14px', color: 'var(--color-muted)', marginBottom: '40px' }}>
            You currently have <strong>{existingFilename}</strong> loaded in your session.
          </p>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', alignItems: 'center' }}>
            <Link to="/dashboard" style={{ width: '100%', maxWidth: '300px' }}>
              <Button style={{ width: '100%' }}>View Dashboard</Button>
            </Link>
            
            <div style={{ display: 'flex', alignItems: 'center', gap: '16px', width: '100%', maxWidth: '300px' }}>
              <div style={{ height: '1px', flex: 1, backgroundColor: 'var(--color-line)' }} />
              <span style={{ fontSize: '12px', color: 'var(--color-dim)' }}>OR</span>
              <div style={{ height: '1px', flex: 1, backgroundColor: 'var(--color-line)' }} />
            </div>

            <Button 
              variant="secondary" 
              style={{ width: '100%', maxWidth: '300px' }}
              onClick={() => {
                resetAnalysis()
                setFile(null)
              }}
            >
              Upload New Resume
            </Button>
          </div>
        </motion.div>
      </div>
    )
  }

  return (
    <div style={{ maxWidth: '600px', margin: '0 auto', padding: '80px 24px 96px' }}>
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
        <h1 style={{ fontSize: '28px', fontWeight: 700, color: 'var(--color-text)', marginBottom: '8px' }}>
          Upload Resume
        </h1>
        <p style={{ fontSize: '14px', color: 'var(--color-muted)', marginBottom: '40px' }}>
          Drop your PDF or DOCX file below to start the AI analysis.
        </p>
      </motion.div>

      <Card>
        {/* Drop zone */}
        <div
          onDragOver={(e) => { e.preventDefault(); setDragging(true) }}
          onDragLeave={() => setDragging(false)}
          onDrop={onDrop}
          onClick={() => document.getElementById('file-input')?.click()}
          style={{
            display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
            borderRadius: '14px', border: `2px dashed ${dragging ? 'var(--color-accent)' : 'var(--color-line)'}`,
            backgroundColor: dragging ? 'rgba(255,122,89,0.04)' : 'transparent',
            padding: '48px 24px', textAlign: 'center', cursor: 'pointer',
            transition: 'all 0.2s ease',
          }}
        >
          <input
            id="file-input" type="file" accept=".pdf,.docx"
            style={{ display: 'none' }}
            onChange={(e) => selectFile(e.target.files?.[0])}
          />
          <span style={{ fontSize: '40px', marginBottom: '16px', display: 'block' }}>
            {file ? '📄' : '☁️'}
          </span>
          {file ? (
            <div>
              <p style={{ fontSize: '14px', fontWeight: 600, color: 'var(--color-text)', marginBottom: '4px' }}>
                {file.name}
              </p>
              <p style={{ fontSize: '12px', color: 'var(--color-muted)' }}>
                {formatSize(file.size)} · Click to change
              </p>
            </div>
          ) : (
            <div>
              <p style={{ fontSize: '14px', fontWeight: 600, color: 'var(--color-text)', marginBottom: '4px' }}>
                Drag & drop your resume here
              </p>
              <p style={{ fontSize: '12px', color: 'var(--color-muted)' }}>
                or click to browse · PDF, DOCX · Max 10 MB
              </p>
            </div>
          )}
        </div>

        {/* Error */}
        <AnimatePresence>
          {error && (
            <motion.p
              initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }} exit={{ opacity: 0, height: 0 }}
              style={{ marginTop: '16px', fontSize: '13px', color: 'var(--color-err)' }}
            >
              {error}
            </motion.p>
          )}
        </AnimatePresence>

        {/* Progress */}
        <AnimatePresence>
          {status !== 'idle' && status !== 'error' && (
            <motion.div
              initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
              style={{ marginTop: '24px' }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                <span style={{ fontSize: '12px', color: 'var(--color-muted)' }}>{statusLabel[status] || ''}</span>
                <span style={{ fontSize: '12px', fontWeight: 600, color: 'var(--color-accent)' }}>{progress}%</span>
              </div>
              <div style={{
                height: '6px', width: '100%', borderRadius: '3px',
                backgroundColor: 'var(--color-elevated)', overflow: 'hidden',
              }}>
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${progress}%` }}
                  transition={{ duration: 0.4, ease: 'easeOut' }}
                  style={{ height: '100%', borderRadius: '3px', backgroundColor: 'var(--color-accent)' }}
                />
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Upload button */}
        <div style={{ marginTop: '24px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <Link to="/demo" style={{ fontSize: '14px', color: 'var(--color-muted)', textDecoration: 'underline' }} className="hover:text-white transition-colors">
            See how it works first →
          </Link>
          <Button
            onClick={handleUpload}
            disabled={!file || status === 'uploading' || status === 'processing'}
          >
            {status === 'uploading' || status === 'processing' ? 'Analyzing…' : 'Analyze Resume'}
          </Button>
        </div>
      </Card>
    </div>
  )
}
