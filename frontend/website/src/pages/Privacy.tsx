import { useTranslation } from 'react-i18next';
import { Helmet } from 'react-helmet-async';
import { useParams } from 'react-router-dom';

export default function Privacy() {
  const { t } = useTranslation();
  const { lang } = useParams();

  return (
    <>
      <Helmet>
        <title>{t('privacy.title')}</title>
        <meta name="description" content={t('privacy.desc')} />
        <meta name="keywords" content={t('privacy.keywords')} />
        <script type="application/ld+json">{`{
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "KhmerX",
        "url": "https://khmerx.org",
        "logo": "https://khmerx.org/logo.jpg",
        "contactPoint": {
          "@type": "ContactPoint",
          "contactType": "customer support",
          "email": "support@khmerx.org",
          "availableLanguage": ["Khmer", "English", "Chinese"]
        },
        "sameAs": [
          "https://t.me/KhmerXBot"
        ]
      }`}</script>
      </Helmet>

      <div className="flex-1">
        {/*  Hero 区  */}
      <section className="relative bg-slate-900 border-b border-slate-800 overflow-hidden text-white">
        <div className="absolute inset-0 bg-[url('https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=Dark%20blue%20data%20security%20privacy%20lock%20shield%20technology%20background%20abstract%20modern%20clean%20business%20style&image_size=landscape_16_9')] bg-cover bg-center opacity-30 mix-blend-overlay"></div>
        <div className="relative mx-auto max-w-[1200px] px-5 py-20 md:py-28">
          <div className="grid gap-12 md:grid-cols-2 md:items-center">
            <div className="max-w-xl z-10">
              <div className="mb-6 inline-flex rounded-full bg-blue-500/20 px-4 py-2 text-sm font-bold text-blue-300 border border-blue-500/30">
                <svg className="w-4 h-4 inline mr-2 -mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path></svg>
                KhmerX Privacy & Data
              </div>
              <h1 className="text-4xl font-extrabold leading-tight tracking-tight md:text-5xl lg:text-6xl mb-6">
                {t('privacy.hero_title')}
              </h1>
              <p className="text-lg leading-relaxed text-slate-300 md:text-xl font-medium">
                {t('privacy.hero_subtitle')}
              </p>
            </div>
            
            <div className="relative z-10 flex justify-center md:justify-end">
              <div className="relative w-48 h-48 sm:w-64 sm:h-64 animate-float">
                <div className="absolute inset-0 bg-blue-500 rounded-full blur-3xl opacity-40"></div>
                <svg className="relative w-full h-full text-blue-400 drop-shadow-2xl" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
                </svg>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/*  内容区  */}
      <section className="mx-auto max-w-[800px] px-5 py-20 -mt-10 relative z-20">
        <div className="bg-white rounded-3xl p-8 md:p-12 shadow-xl border border-slate-100 prose prose-slate prose-blue max-w-none">
          
          <h2 className="text-2xl font-bold text-slate-900 mb-6">{t('privacy.sec1_title')}</h2>
          <div className="grid sm:grid-cols-2 gap-6 not-prose mb-10">
            <div className="bg-slate-50 rounded-2xl p-6 border border-slate-100">
              <h4 className="font-bold text-slate-900 mb-4 flex items-center gap-2">
                <svg className="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207"></path></svg>
                {t('privacy.sec1_box1_title')}
              </h4>
              <ul className="space-y-2 text-sm text-slate-600">
                <li className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-blue-400"></div>Telegram ID</li>
                <li className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-blue-400"></div>{t('privacy.sec1_box1_item1')}</li>
                <li className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-blue-400"></div>{t('privacy.sec1_box1_item2')}</li>
              </ul>
            </div>
            <div className="bg-slate-50 rounded-2xl p-6 border border-slate-100">
              <h4 className="font-bold text-slate-900 mb-4 flex items-center gap-2">
                <svg className="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"></path></svg>
                {t('privacy.sec1_box2_title')}
              </h4>
              <ul className="space-y-2 text-sm text-slate-600">
                <li className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-blue-400"></div>{t('privacy.sec1_box2_item1')}</li>
                <li className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-blue-400"></div>{t('privacy.sec1_box2_item2')}</li>
                <li className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-blue-400"></div>{t('privacy.sec1_box2_item3')}</li>
              </ul>
            </div>
          </div>

          <h2 className="text-2xl font-bold text-slate-900 mt-12 mb-6">{t('privacy.sec2_title')}</h2>
          <ul className="not-prose grid sm:grid-cols-2 gap-4 mb-10">
            <li className="flex items-center gap-3 bg-blue-50/50 px-4 py-3 rounded-xl text-slate-700">
              <svg className="w-5 h-5 text-blue-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
              {t('privacy.sec2_item1')}
            </li>
            <li className="flex items-center gap-3 bg-blue-50/50 px-4 py-3 rounded-xl text-slate-700">
              <svg className="w-5 h-5 text-blue-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
              {t('privacy.sec2_item2')}
            </li>
            <li className="flex items-center gap-3 bg-blue-50/50 px-4 py-3 rounded-xl text-slate-700">
              <svg className="w-5 h-5 text-blue-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
              {t('privacy.sec2_item3')}
            </li>
            <li className="flex items-center gap-3 bg-blue-50/50 px-4 py-3 rounded-xl text-slate-700">
              <svg className="w-5 h-5 text-blue-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
              {t('privacy.sec2_item4')}
            </li>
          </ul>

          <h2 className="text-2xl font-bold text-slate-900 mt-12 mb-6">{t('privacy.sec3_title')}</h2>
          <div className="bg-yellow-50 border border-yellow-200 rounded-2xl p-6 not-prose mb-10">
            <h4 className="font-bold text-yellow-900 mb-2">{t('privacy.sec3_sub1')}</h4>
            <p className="text-yellow-800 text-sm mb-4">{t('privacy.sec3_desc1')}</p>
            <h4 className="font-bold text-yellow-900 mb-2">{t('privacy.sec3_sub2')}</h4>
            <p className="text-yellow-800 text-sm mb-4">{t('privacy.sec3_desc2')}</p>
            <div className="bg-white/60 px-4 py-3 rounded-lg border border-yellow-200 text-sm font-medium text-yellow-900">
              ⚠️ {t('privacy.sec3_notice')}
            </div>
          </div>

          <h2 className="text-2xl font-bold text-slate-900 mt-12 mb-6">{t('privacy.sec4_title')}</h2>
          <div className="space-y-4 text-slate-600 mb-10">
            <p>{t('privacy.sec4_desc')}</p>
            <div className="flex flex-wrap gap-3 not-prose">
              <span className="bg-slate-100 text-slate-700 px-3 py-1 rounded-full text-sm font-medium">HTTPS</span>
              <span className="bg-slate-100 text-slate-700 px-3 py-1 rounded-full text-sm font-medium">Database Access Control</span>
              <span className="bg-slate-100 text-slate-700 px-3 py-1 rounded-full text-sm font-medium">Risk Monitoring</span>
            </div>
            <p className="text-sm text-slate-500 italic">{t('privacy.sec4_notice')}</p>
          </div>

          <h2 className="text-2xl font-bold text-slate-900 mt-12 mb-6">{t('privacy.sec5_title')}</h2>
          <p className="text-slate-600 mb-6">{t('privacy.sec5_desc')}</p>

        </div>
      </section>

      {/*  联系方式  */}
      <section className="mx-auto max-w-[800px] px-5 pb-24">
        <div className="bg-blue-600 rounded-[2rem] p-10 text-center text-white shadow-xl relative overflow-hidden">
          <div className="absolute inset-0 bg-[url('https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=Blue%20technology%20abstract%20waves&image_size=landscape_16_9')] bg-cover bg-center opacity-20 mix-blend-overlay"></div>
          <div className="relative z-10">
            <h2 className="text-2xl md:text-3xl font-bold mb-4">{t('privacy.contact_title')}</h2>
            <p className="text-blue-100 mb-8">{t('privacy.contact_desc')}</p>
            <a className="inline-flex justify-center items-center rounded-xl bg-white px-8 py-4 text-lg font-bold text-blue-600 shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-300" href="https://t.me/KhmerXBot">
              <svg className="w-6 h-6 mr-2" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.74-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .38z"/></svg>
              {t('privacy.contact_btn')}
            </a>
          </div>
        </div>
      </section>
      </div>
    </>
  );
}
