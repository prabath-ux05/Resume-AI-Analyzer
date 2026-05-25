import { RouterProvider } from 'react-router-dom'
import router from './routes/index'
import { ResumeProvider } from './context/ResumeContext'
import { ErrorBoundary } from './components/ErrorBoundary'

export default function App() {
  return (
    <ErrorBoundary>
      <ResumeProvider>
        <RouterProvider router={router} />
      </ResumeProvider>
    </ErrorBoundary>
  )
}
