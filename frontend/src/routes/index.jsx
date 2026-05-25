import { createBrowserRouter } from 'react-router-dom'
import AppShell from '../layouts/AppShell'
import LandingPage from '../pages/LandingPage'
import UploadPage from '../pages/UploadPage'
import DashboardPage from '../pages/DashboardPage'
import MatchPage from '../pages/MatchPage'
import AssistantPage from '../pages/AssistantPage'
import PrivacyPolicy from '../pages/PrivacyPolicy'
import TermsAndConditions from '../pages/TermsAndConditions'
import DemoPage from '../pages/DemoPage'

const router = createBrowserRouter([
  {
    element: <AppShell />,
    children: [
      { path: '/', element: <LandingPage /> },
      { path: '/demo', element: <DemoPage /> },
      { path: '/upload', element: <UploadPage /> },
      { path: '/dashboard', element: <DashboardPage /> },
      { path: '/match', element: <MatchPage /> },
      { path: '/assistant', element: <AssistantPage /> },
      { path: '/privacy', element: <PrivacyPolicy /> },
      { path: '/terms', element: <TermsAndConditions /> },
    ],
  },
])

export default router
