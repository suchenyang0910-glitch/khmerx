import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';
import Borrow from './pages/Borrow';
import Fees from './pages/Fees';
import FAQ from './pages/FAQ';
import Contact from './pages/Contact';
import Risk from './pages/Risk';
import Privacy from './pages/Privacy';
import Terms from './pages/Terms';
import AppDownload from './pages/AppDownload';
import About from './pages/About';
import Blog from './pages/Blog';
import Article from './pages/Article';
import LandingPage from './pages/LandingPage';
import ApiDocs from './pages/ApiDocs';
import Apply from './pages/Apply';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/km" replace />} />
        
        <Route path="/:lang" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="borrow" element={<Borrow />} />
          <Route path="fees" element={<Fees />} />
          <Route path="faq" element={<FAQ />} />
          <Route path="contact" element={<Contact />} />
          <Route path="api" element={<ApiDocs />} />
          <Route path="apply" element={<Apply />} />
          <Route path="risk" element={<Risk />} />
          <Route path="privacy" element={<Privacy />} />
          <Route path="terms" element={<Terms />} />
          <Route path="app" element={<AppDownload />} />
          <Route path="about" element={<About />} />
          <Route path="blog" element={<Blog />} />
          <Route path="blog/:slug" element={<Article />} />
          <Route path="phnom-penh" element={<LandingPage slug="phnom-penh" />} />
          <Route path="aba-guide" element={<LandingPage slug="aba-guide" />} />
          <Route path="telegram-finance" element={<LandingPage slug="telegram-finance" />} />
          <Route path="cambodia-loan-guide" element={<LandingPage slug="cambodia-loan-guide" />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
