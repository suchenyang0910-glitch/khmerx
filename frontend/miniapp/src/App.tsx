import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import AppShell from "@/components/AppShell";
import LangSelect from "@/pages/LangSelect";
import Onboarding from "@/pages/Onboarding";
import ProfileSetup from "@/pages/ProfileSetup";
import Home from "@/pages/Home";
import Orders from "@/pages/Orders";
import Credit from "@/pages/Credit";
import Borrow from "@/pages/Borrow";
import Lend from "@/pages/Lend";
import Trades from "@/pages/Trades";
import TradeDetail from "@/pages/TradeDetail";
import Me from "@/pages/Me";
import Notifications from "@/pages/Notifications";
import Services from "@/pages/Services";
import Catalog from "@/pages/Catalog";
import ProductDetail from "@/pages/ProductDetail";
import FinanceApply from "@/pages/FinanceApply";
import MyApplications from "@/pages/MyApplications";
import ApplicationDetail from "@/pages/ApplicationDetail";
import SalaryLoanApply from "@/pages/SalaryLoanApply";
import SalaryLoanOrderDetail from "@/pages/SalaryLoanOrderDetail";

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/lang" element={<LangSelect />} />
        <Route path="/onboarding" element={<Onboarding />} />
        <Route path="/setup" element={<ProfileSetup />} />

        <Route element={<AppShell />}>
          <Route path="/" element={<Home />} />
          <Route path="/services" element={<Services />} />
          <Route path="/orders" element={<Orders />} />
          <Route path="/credit" element={<Credit />} />
          <Route path="/catalog/:bizType" element={<Catalog />} />
          <Route path="/catalog/:bizType/:productId" element={<ProductDetail />} />
          <Route path="/apply/:bizType" element={<FinanceApply />} />
          <Route path="/applications" element={<MyApplications />} />
          <Route path="/applications/:applicationId" element={<ApplicationDetail />} />
          <Route path="/salary-loan/apply" element={<SalaryLoanApply />} />
          <Route path="/salary-loan/order/:orderId" element={<SalaryLoanOrderDetail />} />
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
