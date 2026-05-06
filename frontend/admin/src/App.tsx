import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import type { ReactNode } from "react";
import Dashboard from "@/pages/Dashboard";
import Login from "@/pages/Login";
import Users from "@/pages/Users";
import Offers from "@/pages/Offers";
import Trades from "@/pages/Trades";
import Reports from "@/pages/Reports";
import RiskEvents from "@/pages/RiskEvents";
import RiskRules from "@/pages/RiskRules";
import Disputes from "@/pages/Disputes";
import Notifications from "@/pages/Notifications";
import Announcements from "@/pages/Announcements";
import Config from "@/pages/Config";
import InterestRates from "@/pages/InterestRates";
import { AdminLayout } from "@/components/layout/AdminLayout";
import { useAdminAuthStore } from "@/stores/adminAuthStore";


function RequireAuth({ children }: { children: ReactNode }) {
  const token = useAdminAuthStore((s) => s.token)
  if (!token) return <Navigate to="/login" replace />
  return <>{children}</>
}

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route
          path="/"
          element={
            <RequireAuth>
              <AdminLayout />
            </RequireAuth>
          }
        >
          <Route index element={<Dashboard />} />
          <Route path="reports" element={<Reports />} />
          <Route path="users" element={<Users />} />
          <Route path="offers" element={<Offers />} />
          <Route path="trades" element={<Trades />} />
          <Route path="risk/events" element={<RiskEvents />} />
          <Route path="risk/rules" element={<RiskRules />} />
          <Route path="disputes" element={<Disputes />} />
          <Route path="notifications" element={<Notifications />} />
          <Route path="announcements" element={<Announcements />} />
          <Route path="config" element={<Config />} />
          <Route path="interest-rates" element={<InterestRates />} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}
