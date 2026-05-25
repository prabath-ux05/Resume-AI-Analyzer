import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
})

/**
 * Upload a resume file (PDF/DOCX) and get comprehensive AI analysis.
 */
export async function analyzeResume(file) {
  const formData = new FormData()
  formData.append('file', file)
  const res = await api.post('/v1/analyze-resume', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return res.data
}

/**
 * Match resume text against a job description.
 */
export async function matchJob(resumeText, jobDescription, fileHash) {
  const res = await api.post('/v1/job-match', {
    resume_text: resumeText,
    job_description: jobDescription,
    file_hash: fileHash,
  })
  return res.data
}

/**
 * Auto-generate AI role matches from analyzed resume intelligence.
 */
export async function autoRoleMatch(fileHash, forceRegenerate = false, onlyCache = false) {
  console.log(`[Frontend API] Request started: POST /v1/job-match/auto for fileHash: ${fileHash} (forceRegenerate: ${forceRegenerate}, onlyCache: ${onlyCache})`)
  const startTime = Date.now()
  try {
    const res = await api.post('/v1/job-match/auto', {
      file_hash: fileHash,
      force_regenerate: forceRegenerate,
      only_cache: onlyCache,
    }, {
      timeout: 90000 // 90 seconds timeout
    })
    console.log(`[Frontend API] Request completed in ${(Date.now() - startTime) / 1000}s`)
    return res.data
  } catch (error) {
    console.error(`[Frontend API] Request failed after ${(Date.now() - startTime) / 1000}s`, error)
    throw error
  }
}

/**
 * Send a message to the AI Assistant and get a streaming response.
 */
export async function sendStreamMessage(message, fileHash, sessionId, isInterview = false) {
  const endpoint = isInterview ? '/v1/chat/interview' : '/v1/chat/message'
  const res = await fetch(`/api${endpoint}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message,
      file_hash: fileHash,
      session_id: sessionId
    })
  })
  
  if (!res.ok) throw new Error('Failed to send message')
  return res.body.getReader()
}

/**
 * Fetch chat history
 */
export async function fetchChatHistory(sessionId) {
  const res = await api.get(`/v1/chat/history?session_id=${sessionId}`)
  return res.data
}

/**
 * Clear chat history
 */
export async function clearChatHistory(sessionId) {
  const res = await api.delete(`/v1/chat/history?session_id=${sessionId}`)
  return res.data
}
