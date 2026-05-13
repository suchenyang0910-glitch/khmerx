import { Link, useParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

export default function Footer() {
  const { lang } = useParams();
  const { t } = useTranslation();

  const getPath = (path: string) => `/${lang}${path}`;

  return (
    <footer className="bg-slate-950 py-16 text-slate-300">
      <div className="mx-auto max-w-7xl px-5">
        <div className="grid gap-12 md:grid-cols-4 lg:grid-cols-5">
          <div className="lg:col-span-2">
            <Link to={`/${lang}`} className="flex items-center gap-3">
              <img src="/logo.jpg" alt="KhmerX" className="h-10 w-10 rounded-xl" />
              <div className="text-xl font-bold text-white">KhmerX</div>
            </Link>
            <p className="mt-4 max-w-xs text-sm leading-relaxed text-slate-400">
              {t('footer.desc', 'KhmerX is a Cambodia-focused micro lending information platform. We do not guarantee approval, returns, deposits, or repayment.')}
            </p>
            <div className="mt-6 flex gap-4">
              <a href="https://t.me/KhmerXBot" target="_blank" rel="noopener noreferrer" className="text-slate-400 hover:text-white transition-colors">
                <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24"><path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.892-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z"/></svg>
              </a>
              <a href="mailto:support@khmerx.org" className="text-slate-400 hover:text-white transition-colors">
                <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="2"><path strokeLinecap="round" strokeLinejoin="round" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
              </a>
            </div>
          </div>

          <div>
            <h3 className="font-semibold text-white">{t('footer.service', 'Services')}</h3>
            <ul className="mt-4 space-y-3 text-sm">
              <li><Link to={getPath('/borrow')} className="hover:text-white transition-colors">{t('nav.borrow', 'How to Borrow')}</Link></li>
              <li><Link to={getPath('/fees')} className="hover:text-white transition-colors">{t('nav.fees', 'Fees')}</Link></li>
              <li><Link to={getPath('/app')} className="hover:text-white transition-colors">{t('nav.app', 'Mini App')}</Link></li>
            </ul>
          </div>

          <div>
            <h3 className="font-semibold text-white">{t('footer.support', 'Support')}</h3>
            <ul className="mt-4 space-y-3 text-sm">
              <li><Link to={getPath('/faq')} className="hover:text-white transition-colors">{t('nav.faq', 'FAQ')}</Link></li>
              <li><Link to={getPath('/contact')} className="hover:text-white transition-colors">{t('nav.contact', 'Contact Us')}</Link></li>
              <li><Link to={getPath('/about')} className="hover:text-white transition-colors">{t('nav.about', 'About Us')}</Link></li>
              <li><Link to={getPath('/api')} className="hover:text-white transition-colors">{t('nav.api', 'API Docs')}</Link></li>
              <li><Link to={getPath('/apply')} className="hover:text-white transition-colors">{t('nav.apply', 'Apply')}</Link></li>
            </ul>
          </div>

          <div>
            <h3 className="font-semibold text-white">{t('footer.legal', 'Legal')}</h3>
            <ul className="mt-4 space-y-3 text-sm">
              <li><Link to={getPath('/terms')} className="hover:text-white transition-colors">{t('nav.terms', 'Terms of Service')}</Link></li>
              <li><Link to={getPath('/privacy')} className="hover:text-white transition-colors">{t('nav.privacy', 'Privacy Policy')}</Link></li>
              <li><Link to={getPath('/risk')} className="hover:text-white transition-colors text-red-400">{t('nav.risk', 'Risk Notice')}</Link></li>
            </ul>
          </div>
        </div>

        <div className="mt-16 flex flex-col items-center justify-between border-t border-slate-800 pt-8 sm:flex-row text-xs text-slate-500">
          <p>© {new Date().getFullYear()} KhmerX. All rights reserved.</p>
          <div className="mt-4 flex gap-4 sm:mt-0">
            <span>Cambodia</span>
            <span>·</span>
            <span>ABA</span>
            <span>·</span>
            <span>Telegram</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
