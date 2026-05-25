import { createContext, useContext, useState, useEffect } from 'react'

const ResumeContext = createContext()

const STORAGE_KEY = 'resume_analysis_state'

export function ResumeProvider({ children }) {
  // Initialize state from localStorage if it exists
  const [analysisState, setAnalysisState] = useState(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY)
      if (saved) {
        return JSON.parse(saved)
      }
    } catch (e) {
      console.error('Failed to parse resume state from localStorage', e)
    }
    // Default empty state
    return {
      filename: null,
      resumeText: null,
      fileHash: null,
      skills: null,
      ats: null,
      jobMatchResult: null,
      jobDescriptionText: '',
      roleMatchResult: null,
    }
  })

  // Whenever analysisState changes, sync it to localStorage
  useEffect(() => {
    try {
      if (analysisState.filename) {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(analysisState))
      } else {
        localStorage.removeItem(STORAGE_KEY)
      }
    } catch (e) {
      console.error('Failed to save resume state to localStorage', e)
    }
  }, [analysisState])

  // Helpers to update specific parts of the state
  const setAnalysisData = (filename, resumeText, fileHash, skills, ats) => {
    setAnalysisState(prev => ({
      ...prev,
      filename,
      resumeText,
      fileHash,
      skills,
      ats,
      roleMatchResult: null, // Clear old matches on new upload
    }))
  }

  const setJobMatchResult = (jobMatchResult, jobDescriptionText = null) => {
    setAnalysisState(prev => ({ 
      ...prev, 
      jobMatchResult, 
      ...(jobDescriptionText !== null && { jobDescriptionText }) 
    }))
  }

  const setRoleMatchResult = (roleMatchResult) => {
    setAnalysisState(prev => ({ ...prev, roleMatchResult }))
  }

  const resetAnalysis = () => {
    setAnalysisState({
      filename: null,
      resumeText: null,
      fileHash: null,
      skills: null,
      ats: null,
      jobMatchResult: null,
      jobDescriptionText: '',
      roleMatchResult: null,
    })
    localStorage.removeItem(STORAGE_KEY)
  }

  return (
    <ResumeContext.Provider value={{
      ...analysisState,
      hasAnalysis: !!analysisState.ats,
      setAnalysisData,
      setJobMatchResult,
      setJobDescriptionText: (text) => setAnalysisState(prev => ({ ...prev, jobDescriptionText: text })),
      setRoleMatchResult,
      resetAnalysis
    }}>
      {children}
    </ResumeContext.Provider>
  )
}

export const useResumeContext = () => {
  const context = useContext(ResumeContext)
  if (!context) {
    throw new Error('useResumeContext must be used within a ResumeProvider')
  }
  return context
}
