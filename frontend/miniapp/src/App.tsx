import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import AppShell from "@/components/AppShell";
import Onboarding from "@/pages/Onboarding";
import ProfileSetup from "@/pages/ProfileSetup";
import Home from "@/pages/Home";
import Borrow from "@/pages/Borrow";
import Lend from "@/pages/Lend";
import Trades from "@/pages/Trades";
import TradeDetail from "@/pages/TradeDetail";
import Me from "@/pages/Me";
import Notifications from "@/pages/Notifications";

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/onboarding" element={<Onboarding />} />
        <Route path="/setup" element={<ProfileSetup />} />

        <Route element={<AppShell />}>
          <Route path="/" element={<Home />} />
          <Route path="/borrow" element={<Borrow />} />
          <Route path="/lend" element={<Lend />} />
          <Route path="/trades" element={<Trades />} />
          <Route path="/trade/:tradeId" element={<TradeDetail />} />
          <Route path="/me" element={<Me />} />
          <Route path="/notifications" element={<Notifications />} />
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}
