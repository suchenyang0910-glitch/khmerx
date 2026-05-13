import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Login from '@/pages/Login'
import Dashboard from '@/pages/Dashboard'
import Rules from '@/pages/Rules'
import Cases from '@/pages/Cases'
import System from '@/pages/System'
import NotFound from '@/pages/NotFound'
import Forbidden from '@/pages/Forbidden'
import AppShell from '@/components/AppShell'
import RequireAuth from '@/components/RequireAuth'
import RequirePermission from '@/components/RequirePermission'

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/forbidden" element={<Forbidden />} />
        <Route element={<RequireAuth />}>
          <Route element={<AppShell />}>
            <Route path="/" element={<Dashboard />} />
            <Route element={<RequirePermission permKey="rules.read" />}>
              <Route path="/rules" element={<Rules />} />
            </Route>
            <Route element={<RequirePermission permKey="cases.read" />}>
              <Route path="/cases" element={<Cases />} />
            </Route>
            <Route element={<RequirePermission permKey="system.read" />}>
              <Route path="/system" element={<System />} />
            </Route>
          </Route>
        </Route>
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  )
}
