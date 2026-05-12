import { Outlet, useParams, useNavigate, useLocation } from 'react-router-dom';
import { useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import Header from './Header';
import Footer from './Footer';

const SUPPORTED_LANGS = ['km', 'en', 'zh'];

export default function Layout() {
  const { lang } = useParams<{ lang: string }>();
  const navigate = useNavigate();
  const location = useLocation();
  const { i18n } = useTranslation();

  useEffect(() => {
    if (!lang || !SUPPORTED_LANGS.includes(lang)) {
      navigate(`/km${location.pathname}`, { replace: true });
      return;
    }

    if (i18n.language !== lang) {
      i18n.changeLanguage(lang);
    }
  }, [lang, navigate, location, i18n]);

  if (!lang || !SUPPORTED_LANGS.includes(lang)) {
    return null;
  }

  return (
    <div className="min-h-screen bg-[#F5F7FA] text-slate-900 flex flex-col font-sans">
      <Header />
      <main className="flex-1">
        <Outlet />
      </main>
      <Footer />
    </div>
  );
}