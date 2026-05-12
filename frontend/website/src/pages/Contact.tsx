import { useTranslation } from 'react-i18next';
import { Helmet } from 'react-helmet-async';
import { useParams } from 'react-router-dom';

export default function Contact() {
  const { t } = useTranslation();
  const { lang } = useParams();

  return (
    <>
      <Helmet>
        <title>{t('contact.title')}</title>
        <meta name="description" content={t('contact.desc')} />
        <meta name="keywords" content={t('contact.keywords')} />
        <script type="application/ld+json">{`{
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "KhmerX",
        "url": "https://khmerx.org",
        "logo": "https://khmerx.org/logo.jpg",
        "sameAs": [
          "https://t.me/KhmerXBot"
        ],
        "contactPoint": {
          "@type": "ContactPoint",
          "contactType": "customer support",
          "email": "support@khmerx.org"
        }
      }`}</script>
      </Helmet>

      <div className="flex-1">
        {/*  Hero 区  */}
      <section className="relative bg-white border-b border-slate-100 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-blue-50/50 to-white"></div>
        <div className="relative mx-auto max-w-[1200px] px-5 py-16 md:py-24">
          <div className="grid gap-12 md:grid-cols-2 md:items-center">
            <div className="max-w-xl z-10">
              <h1 className="text-4xl font-extrabold leading-tight tracking-tight text-slate-900 md:text-5xl lg:text-6xl mb-6">
                {t('contact.hero_title')}
              </h1>
              <p className="text-lg leading-relaxed text-slate-600 md:text-xl mb-10">
                {t('contact.hero_subtitle')}
              </p>
            </div>
            
            <div className="relative z-10 flex justify-center md:justify-end">
              <div className="relative w-[300px] sm:w-[340px] animate-float">
                <div className="absolute inset-0 bg-blue-500 rounded-[3rem] blur-3xl opacity-20 transform translate-y-10"></div>
                <img src="https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=Telegram%20customer%20support%20chat%20UI%20mockup%20blue%20white%20gradient%20background%20modern%20clean%20business%20style&image_size=portrait_9_16" alt="KhmerX Telegram Support" className="relative rounded-[2.5rem] shadow-2xl border-[6px] border-slate-800 object-cover w-full h-[500px] bg-slate-100" />
                
                <div className="absolute -bottom-6 -left-8 bg-white p-4 rounded-2xl shadow-xl border border-slate-100 flex items-center gap-3 animate-float" style={{ animationDelay: '1.5s' }}>
                  <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center text-blue-600">
                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.74-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .38z"/></svg>
                  </div>
                  <div>
                    <div className="text-xs text-slate-500">Official Support</div>
                    <div className="font-bold text-slate-800">Online Now</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/*  联系方式卡片  */}
      <section className="mx-auto max-w-[1200px] px-5 py-20 -mt-10 relative z-20">
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {/*  Card 1  */}
          <div className="bg-white rounded-3xl p-8 shadow-lg border border-slate-100 flex flex-col items-center text-center hover:-translate-y-2 transition-transform">
            <div className="w-16 h-16 bg-[#0088cc]/10 text-[#0088cc] rounded-2xl flex items-center justify-center mb-6">
              <svg className="w-8 h-8" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.74-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .38z"/></svg>
            </div>
            <h3 className="text-xl font-bold text-slate-900 mb-2">Telegram Mini App</h3>
            <p className="text-slate-500 mb-8 flex-1">{t('contact.card_1_desc')}</p>
            <a href="https://t.me/KhmerXBot/app" className="w-full inline-flex justify-center items-center rounded-xl bg-blue-600 px-6 py-3 font-bold text-white hover:bg-blue-700 transition-colors">
              {t('contact.card_1_btn')}
            </a>
          </div>
          
          {/*  Card 2  */}
          <div className="bg-white rounded-3xl p-8 shadow-lg border border-blue-200 ring-2 ring-blue-500/20 flex flex-col items-center text-center hover:-translate-y-2 transition-transform">
            <div className="absolute top-0 right-0 -mt-3 -mr-3 flex h-6 w-6">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-6 w-6 bg-blue-500"></span>
            </div>
            <div className="w-16 h-16 bg-blue-100 text-blue-600 rounded-2xl flex items-center justify-center mb-6">
              <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"></path></svg>
            </div>
            <h3 className="text-xl font-bold text-slate-900 mb-2">{t('contact.card_2_title')}</h3>
            <p className="text-slate-500 mb-8 flex-1">{t('contact.card_2_desc')}</p>
            <a href="https://t.me/KhmerXBot" className="w-full inline-flex justify-center items-center rounded-xl bg-gradient-to-r from-blue-600 to-[#00AEEF] px-6 py-3 font-bold text-white shadow-md hover:shadow-lg transition-all">
              {t('contact.card_2_btn')}
            </a>
          </div>
          
          {/*  Card 3  */}
          <div className="bg-white rounded-3xl p-8 shadow-lg border border-slate-100 flex flex-col items-center text-center hover:-translate-y-2 transition-transform md:col-span-2 lg:col-span-1">
            <div className="w-16 h-16 bg-slate-100 text-slate-600 rounded-2xl flex items-center justify-center mb-6">
              <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>
            </div>
            <h3 className="text-xl font-bold text-slate-900 mb-2">Email</h3>
            <p className="text-slate-500 mb-8 flex-1">{t('contact.card_3_desc')}</p>
            <a href="mailto:support@khmerx.org" className="w-full inline-flex justify-center items-center rounded-xl border-2 border-slate-200 px-6 py-3 font-bold text-slate-700 hover:border-slate-300 hover:bg-slate-50 transition-colors">
              support@khmerx.org
            </a>
          </div>
        </div>
      </section>

      {/*  客服支持与工作时间  */}
      <section className="mx-auto max-w-[1200px] px-5 pb-20">
        <div className="grid gap-8 md:grid-cols-2">
          {/*  支持范围  */}
          <div className="bg-white rounded-3xl p-8 border border-slate-200">
            <h3 className="text-2xl font-bold text-slate-900 mb-6">{t('contact.support_title')}</h3>
            <ul className="space-y-4 mb-8">
              <li className="flex items-center gap-3 text-slate-600">
                <svg className="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                {t('contact.support_1')}
              </li>
              <li className="flex items-center gap-3 text-slate-600">
                <svg className="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                {t('contact.support_2')}
              </li>
              <li className="flex items-center gap-3 text-slate-600">
                <svg className="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                {t('contact.support_3')}
              </li>
              <li className="flex items-center gap-3 text-slate-600">
                <svg className="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                {t('contact.support_4')}
              </li>
            </ul>
            <div className="text-sm text-slate-500 bg-slate-50 p-4 rounded-xl border border-slate-100">
              {t('contact.support_tip')}
            </div>
          </div>
          
          {/*  工作时间  */}
          <div className="bg-slate-900 text-white rounded-3xl p-8 relative overflow-hidden">
            <div className="absolute top-0 right-0 w-32 h-32 bg-blue-500 rounded-full blur-3xl opacity-20 -mr-10 -mt-10"></div>
            <h3 className="text-2xl font-bold mb-8 relative z-10">{t('contact.time_title')}</h3>
            
            <div className="flex items-start gap-4 mb-8 relative z-10">
              <div className="w-12 h-12 rounded-full bg-blue-500/20 flex items-center justify-center text-blue-400 shrink-0">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
              </div>
              <div>
                <div className="text-lg font-bold">{t('contact.time_days')}</div>
                <div className="text-3xl font-extrabold text-blue-400 mt-1">09:00 - 21:00</div>
                <div className="text-slate-400 mt-1">(Cambodia Time)</div>
              </div>
            </div>
            
            <div className="bg-slate-800/50 p-4 rounded-xl border border-slate-700 text-sm text-slate-300 relative z-10">
              {t('contact.time_tip')}
            </div>
          </div>
        </div>
      </section>

      {/*  安全与风险提醒（重点）  */}
      <section className="mx-auto max-w-[1200px] px-5 pb-20">
        <div className="bg-[#FFFBEB] border-2 border-[#FDE68A] rounded-[2rem] p-8 md:p-12 shadow-sm">
          <div className="flex flex-col md:flex-row gap-6 items-start">
            <div className="w-16 h-16 bg-[#F59E0B] rounded-2xl flex items-center justify-center text-white shrink-0 shadow-lg">
              <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
            </div>
            <div>
              <h2 className="text-2xl font-bold text-[#92400E] mb-4">{t('contact.risk_title')}</h2>
              <div className="space-y-4 text-[#B45309] font-medium text-lg">
                <p>{t('contact.risk_1')}</p>
                <p>{t('contact.risk_2')}</p>
                <div className="bg-[#FEF3C7] px-4 py-3 rounded-xl border border-[#FDE68A] inline-block mt-2">
                  <span className="font-bold text-[#92400E]">{t('contact.risk_3')}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/*  FAQ 快捷入口  */}
      <section className="mx-auto max-w-[800px] px-5 pb-20 text-center">
        <h3 className="text-2xl font-bold text-slate-900 mb-8">{t('contact.faq_title')}</h3>
        <div className="grid sm:grid-cols-2 gap-4 mb-8 text-left">
          <a href="/{lang}/faq" className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm hover:border-blue-400 hover:shadow-md transition-all flex items-center justify-between group">
            <span className="font-medium text-slate-700 group-hover:text-blue-600 transition-colors">{t('contact.faq_1')}</span>
            <svg className="w-5 h-5 text-slate-400 group-hover:text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
          </a>
          <a href="/{lang}/faq" className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm hover:border-blue-400 hover:shadow-md transition-all flex items-center justify-between group">
            <span className="font-medium text-slate-700 group-hover:text-blue-600 transition-colors">{t('contact.faq_2')}</span>
            <svg className="w-5 h-5 text-slate-400 group-hover:text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
          </a>
          <a href="/{lang}/faq" className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm hover:border-blue-400 hover:shadow-md transition-all flex items-center justify-between group">
            <span className="font-medium text-slate-700 group-hover:text-blue-600 transition-colors">{t('contact.faq_3')}</span>
            <svg className="w-5 h-5 text-slate-400 group-hover:text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
          </a>
          <a href="/{lang}/faq" className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm hover:border-blue-400 hover:shadow-md transition-all flex items-center justify-between group">
            <span className="font-medium text-slate-700 group-hover:text-blue-600 transition-colors">{t('contact.faq_4')}</span>
            <svg className="w-5 h-5 text-slate-400 group-hover:text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
          </a>
        </div>
        <a href="/{lang}/faq" className="inline-flex items-center text-blue-600 font-bold hover:text-blue-800 transition-colors">
          {t('contact.faq_btn')}
          <svg className="w-5 h-5 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path></svg>
        </a>
      </section>

      {/*  CTA 引导  */}
      <section className="mx-auto max-w-[1200px] px-5 pb-24">
        <div className="bg-gradient-to-br from-[#0A5BFF] to-[#00AEEF] rounded-[3rem] p-10 md:p-16 text-center text-white shadow-2xl relative overflow-hidden">
          <div className="absolute top-0 right-0 -mt-20 -mr-20 w-64 h-64 bg-white opacity-10 rounded-full blur-3xl"></div>
          <div className="absolute bottom-0 left-0 -mb-20 -ml-20 w-64 h-64 bg-white opacity-10 rounded-full blur-3xl"></div>
          
          <div className="relative z-10 max-w-2xl mx-auto">
            <h2 className="text-3xl md:text-5xl font-bold mb-8">{t('contact.cta_title')}</h2>
            <div className="flex flex-col items-center justify-center gap-8">
              <div className="bg-white p-4 rounded-3xl shadow-lg inline-block">
                <img className="w-48 h-48 rounded-2xl" alt="KhmerX Mini App QR" src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https%3A%2F%2Ft.me%2FKhmerXBot%2Fapp" />
                <div className="text-slate-500 text-sm font-medium mt-3">Scan with Camera</div>
              </div>
              <a className="inline-flex justify-center items-center rounded-2xl bg-white px-10 py-5 text-xl font-bold text-blue-600 shadow-xl hover:shadow-2xl hover:scale-105 transition-all duration-300" href="https://t.me/KhmerXBot/app">
                <svg className="w-6 h-6 mr-3" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.74-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .38z"/></svg>
                {t('contact.cta_btn')}
              </a>
            </div>
          </div>
        </div>
      </section>
      </div>
    </>
  );
}
