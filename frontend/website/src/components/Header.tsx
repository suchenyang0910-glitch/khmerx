import { Link, useParams, useLocation } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { Menu, X } from 'lucide-react';
import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { track } from '@/utils/analytics';

export default function Header() {
  const { lang } = useParams();
  const { t } = useTranslation();
  const location = useLocation();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const getLocalizedPath = (path: string) => {
    return `/${lang}${path}`;
  };

  const changeLanguagePath = (newLang: string) => {
    const currentPath = location.pathname;
    return currentPath.replace(`/${lang}`, `/${newLang}`);
  };

  const navLinks = [
    { name: t('nav.borrow', 'How to Borrow'), path: '/borrow' },
    { name: t('nav.fees', 'Fees'), path: '/fees' },
    { name: t('nav.faq', 'FAQ'), path: '/faq' },
    { name: t('nav.contact', 'Contact'), path: '/contact' },
    { name: t('nav.api', 'API Docs'), path: '/api' },
    { name: t('nav.apply', 'Apply'), path: '/apply' },
  ];

  return (
    <header className="sticky top-0 z-50 border-b border-slate-200 bg-white/80 backdrop-blur-md">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-5 py-4">
        <Link to={`/${lang}`} className="group flex items-center gap-3">
          <motion.img 
            whileHover={{ scale: 1.05 }}
            src="/logo.jpg" 
            alt="KhmerX Logo" 
            className="h-10 w-10 rounded-xl object-cover shadow-sm" 
          />
          <div>
            <div className="font-bold text-slate-900 group-hover:text-blue-600 transition-colors">KhmerX</div>
            <div className="text-[10px] font-medium text-slate-500 uppercase tracking-wider">ABA · Telegram · Cambodia</div>
          </div>
        </Link>

        {/* Desktop Nav */}
        <nav className="hidden items-center gap-8 md:flex">
          {navLinks.map((link) => (
            <Link
              key={link.path}
              to={getLocalizedPath(link.path)}
              className="text-sm font-medium text-slate-600 transition-colors hover:text-blue-600"
            >
              {link.name}
            </Link>
          ))}
        </nav>

        {/* Right Actions */}
        <div className="hidden items-center gap-4 md:flex">
          <div className="flex items-center gap-1 rounded-lg bg-slate-100 p-1 text-sm">
            <Link
              to={changeLanguagePath('km')}
              onClick={() => track('language_switch', { from_locale: lang, to_locale: 'km', from_path: location.pathname })}
              className={`rounded-md px-3 py-1 font-medium transition-colors ${lang === 'km' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-500 hover:text-slate-900'}`}
            >
              ខ្មែរ
            </Link>
            <Link
              to={changeLanguagePath('en')}
              onClick={() => track('language_switch', { from_locale: lang, to_locale: 'en', from_path: location.pathname })}
              className={`rounded-md px-3 py-1 font-medium transition-colors ${lang === 'en' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-500 hover:text-slate-900'}`}
            >
              EN
            </Link>
            <Link
              to={changeLanguagePath('zh')}
              onClick={() => track('language_switch', { from_locale: lang, to_locale: 'zh', from_path: location.pathname })}
              className={`rounded-md px-3 py-1 font-medium transition-colors ${lang === 'zh' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-500 hover:text-slate-900'}`}
            >
              中文
            </Link>
          </div>
          <a
            href="https://t.me/KhmerXBot/app"
            target="_blank"
            rel="noopener noreferrer"
            className="rounded-xl bg-[#0A5BFF] px-5 py-2.5 text-sm font-semibold text-white shadow-md shadow-blue-500/20 transition-all hover:bg-blue-700 hover:shadow-lg hover:shadow-blue-500/30 active:scale-95"
          >
            {t('nav.cta', 'Open Mini App')}
          </a>
        </div>

        {/* Mobile Menu Toggle */}
        <button
          className="rounded-lg p-2 text-slate-600 hover:bg-slate-100 md:hidden"
          onClick={() => setIsMenuOpen(!isMenuOpen)}
        >
          {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>

      {/* Mobile Menu */}
      <AnimatePresence>
        {isMenuOpen && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="overflow-hidden border-t border-slate-200 bg-white md:hidden"
          >
            <nav className="flex flex-col px-5 py-4">
              {navLinks.map((link) => (
                <Link
                  key={link.path}
                  to={getLocalizedPath(link.path)}
                  className="py-3 text-base font-medium text-slate-700 border-b border-slate-100 last:border-0"
                  onClick={() => setIsMenuOpen(false)}
                >
                  {link.name}
                </Link>
              ))}
              
              <div className="mt-4 flex gap-2">
                <Link
                  to={changeLanguagePath('km')}
                  onClick={() => {
                    track('language_switch', { from_locale: lang, to_locale: 'km', from_path: location.pathname })
                    setIsMenuOpen(false)
                  }}
                  className={`flex-1 rounded-lg py-2 text-center text-sm font-medium ${lang === 'km' ? 'bg-blue-50 text-blue-600' : 'bg-slate-100 text-slate-600'}`}
                >
                  ខ្មែរ
                </Link>
                <Link
                  to={changeLanguagePath('en')}
                  onClick={() => {
                    track('language_switch', { from_locale: lang, to_locale: 'en', from_path: location.pathname })
                    setIsMenuOpen(false)
                  }}
                  className={`flex-1 rounded-lg py-2 text-center text-sm font-medium ${lang === 'en' ? 'bg-blue-50 text-blue-600' : 'bg-slate-100 text-slate-600'}`}
                >
                  EN
                </Link>
                <Link
                  to={changeLanguagePath('zh')}
                  onClick={() => {
                    track('language_switch', { from_locale: lang, to_locale: 'zh', from_path: location.pathname })
                    setIsMenuOpen(false)
                  }}
                  className={`flex-1 rounded-lg py-2 text-center text-sm font-medium ${lang === 'zh' ? 'bg-blue-50 text-blue-600' : 'bg-slate-100 text-slate-600'}`}
                >
                  中文
                </Link>
              </div>

              <a
                href="https://t.me/KhmerXBot/app"
                target="_blank"
                rel="noopener noreferrer"
                className="mt-4 block w-full rounded-xl bg-[#0A5BFF] py-3 text-center font-semibold text-white shadow-md"
              >
                {t('nav.cta', 'Open Mini App')}
              </a>
            </nav>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  );
}
