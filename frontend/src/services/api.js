import axios from 'axios'
const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://resume-ai-analyzer-9.onrender.com'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' },
})

export async function analyzeResume(file) {
  const formData = new FormData()
  formData.append('file', file)

  const res = await api.post('/api/v1/analyze-resume', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })

  return res.data
}

export async function matchJob(resumeText, jobDescription, fileHash) {
  const res = await api.post('/api/v1/job-match', {
    resume_text: resumeText,
    job_description: jobDescription,
    file_hash: fileHash,
  })

  return res.data
}

export async function autoRoleMatch(fileHash, forceRegenerate = false, onlyCache = false) {
  const res = await api.post('/api/v1/job-match/auto', {
    file_hash: fileHash,
    force_regenerate: forceRegenerate,
    only_cache: onlyCache,
  }, {
    timeout: 90000
  })

  return res.data
}

export async function sendStreamMessage(message, fileHash, sessionId, isInterview = false) {
  const endpoint = isInterview ? '/api/v1/chat/interview' : '/api/v1/chat/message'

  const res = await fetch(`${API_BASE_URL}${endpoint}`, {
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

export async function fetchChatHistory(sessionId) {
  const res = await api.get(`/api/v1/chat/history?session_id=${sessionId}`)
  return res.data
}

export async function clearChatHistory(sessionId) {
  const res = await api.delete(`/api/v1/chat/history?session_id=${sessionId}`)
  return res.data
}