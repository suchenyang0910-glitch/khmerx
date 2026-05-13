import { useTranslation } from 'react-i18next';
import { Helmet } from 'react-helmet-async';

export default function AppDownload() {
  const { t } = useTranslation();

  return (
    <>
      <Helmet>
        <title>{t('appdownload.title')}</title>
        <meta name="description" content={t('appdownload.desc')} />
        <meta name="keywords" content={t('appdownload.keywords')} />
        <script type="application/ld+json">{`{
        "@context": "https://schema.org",
        "@type": "MobileApplication",
        "name": "KhmerX Telegram Mini App",
        "operatingSystem": "Android, iOS",
        "applicationCategory": "FinanceApplication",
        "url": "https://t.me/KhmerXBot/app",
        "description": "${t('appdownload.desc')}"
      }`}</script>
        <script type="application/ld+json">{`{
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "KhmerX",
        "url": "https://khmerx.org",
        "logo": "https://khmerx.org/logo.jpg",
        "sameAs": [
          "https://t.me/KhmerXBot"
        ]
      }`}</script>
      </Helmet>

      <div className="flex-1">
        {/*  Hero 区  */}
      <section className="relative bg-slate-900 overflow-hidden text-white flex-1 flex flex-col justify-center">
        <div className="absolute inset-0 bg-[url('https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=Dark%20blue%20telegram%20mini%20app%20interface%20technology%20background%20abstract%20modern%20clean%20business%20style&image_size=landscape_16_9')] bg-cover bg-center opacity-30 mix-blend-overlay"></div>
        <div className="absolute inset-0 bg-gradient-to-b from-transparent to-slate-900/90"></div>
        
        <div className="relative mx-auto max-w-[1200px] px-5 py-16 md:py-24 flex-1 w-full">
          <div className="grid gap-12 md:grid-cols-2 md:items-center h-full">
            <div className="max-w-xl z-10 flex flex-col justify-center">
              <div className="mb-6 inline-flex rounded-full bg-blue-500/20 px-4 py-2 text-sm font-bold text-blue-300 border border-blue-500/30 w-max">
                Telegram · ABA · Cambodia
              </div>
              <h1 className="text-4xl font-extrabold leading-tight tracking-tight md:text-5xl lg:text-6xl mb-6">
                {t('appdownload.hero_title')}
              </h1>
              <p className="text-lg leading-relaxed text-slate-300 md:text-xl font-medium mb-10">
                {t('appdownload.hero_subtitle')}
              </p>
              
              {/*  CTA 区  */}
              <div id="mobile-cta" className="flex flex-col sm:flex-row gap-4">
                <a href="https://t.me/KhmerXBot/app" className="inline-flex justify-center items-center rounded-2xl bg-gradient-to-r from-[#0A5BFF] to-[#00AEEF] px-8 py-4 text-lg font-bold text-white shadow-[0_8px_30px_rgb(10,91,255,0.4)] hover:shadow-[0_8px_40px_rgb(10,91,255,0.6)] hover:scale-105 transition-all duration-300 h-[56px]">
                  <svg className="w-6 h-6 mr-3" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.74-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .38z"/></svg>
                  {t('appdownload.cta_open')}
                </a>
                <a id="dl-telegram-btn" href="https://telegram.org/" style={{display: "none"}} className="inline-flex justify-center items-center rounded-2xl bg-slate-800 border border-slate-700 px-8 py-4 text-lg font-bold text-white shadow-lg hover:bg-slate-700 hover:scale-105 transition-all duration-300 h-[56px]">
                  <svg className="w-6 h-6 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
                  {t('appdownload.cta_dl')}
                </a>
              </div>
              
              {/*  QR 区 (PC)  */}
              <div id="qr-section" className="hidden flex-col items-start gap-4">
                <div className="bg-white p-4 rounded-3xl shadow-xl flex gap-6 items-center border border-slate-200">
                  <img className="w-32 h-32 rounded-xl" alt="KhmerX Mini App QR" src="https://api.qrserver.com/v1/create-qr-code/?size=240x240&data=https%3A%2F%2Ft.me%2FKhmerXBot%2Fapp" />
                  <div className="pr-4">
                    <h4 className="font-bold text-slate-900 text-lg mb-1">{t('appdownload.qr_title')}</h4>
                    <p className="text-slate-500 text-sm">{t('appdownload.qr_desc')}</p>
                  </div>
                </div>
              </div>

            </div>
            
            <div className="relative z-10 hidden md:flex justify-center md:justify-end items-center h-[500px]">
              {/*  Mockups  */}
              <div className="relative w-full max-w-md h-full">
                {/*  Phone 1  */}
                <div className="absolute right-0 top-10 w-48 h-auto rounded-[2rem] border-4 border-slate-800 bg-slate-900 shadow-2xl overflow-hidden animate-float z-10 rotate-6">
                  <img src="https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=Telegram%20Mini%20App%20UI%20Mockup%20Finance%20Dashboard%20Clean%20Modern%20Mobile%20Interface%20Blue%20Tones&image_size=portrait_16_9" alt="App Preview 1" className="w-full h-full object-cover" />
                </div>
                {/*  Phone 2  */}
                <div className="absolute left-10 top-20 w-48 h-auto rounded-[2rem] border-4 border-slate-800 bg-slate-900 shadow-2xl overflow-hidden animate-float-delay z-20 -rotate-3">
                  <img src="https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=Telegram%20Mini%20App%20UI%20Mockup%20Loan%20Application%20Form%20Clean%20Modern%20Mobile%20Interface%20Blue%20Tones&image_size=portrait_16_9" alt="App Preview 2" className="w-full h-full object-cover" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/*  Telegram 打开方式  */}
      <section className="mx-auto max-w-[1200px] px-5 py-20 bg-white rounded-t-[3rem] -mt-10 relative z-20 w-full shadow-lg border-t border-slate-100">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-slate-900">{t('appdownload.steps_title')}</h2>
        </div>
        <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
          <div className="bg-slate-50 rounded-3xl p-8 text-center border border-slate-100 relative">
            <div className="w-12 h-12 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center font-bold text-xl mx-auto mb-4">1</div>
            <h4 className="font-bold text-slate-900 text-lg mb-2">{t('appdownload.step1_title')}</h4>
            <p className="text-slate-500 text-sm">{t('appdownload.step1_desc')}</p>
          </div>
          <div className="bg-slate-50 rounded-3xl p-8 text-center border border-slate-100 relative">
            <div className="w-12 h-12 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center font-bold text-xl mx-auto mb-4">2</div>
            <h4 className="font-bold text-slate-900 text-lg mb-2">{t('appdownload.step2_title')}</h4>
            <p className="text-slate-500 text-sm">{t('appdownload.step2_desc')}</p>
          </div>
          <div className="bg-blue-50 rounded-3xl p-8 text-center border border-blue-100 relative">
            <div className="w-12 h-12 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold text-xl mx-auto mb-4">3</div>
            <h4 className="font-bold text-blue-900 text-lg mb-2">{t('appdownload.step3_title')}</h4>
            <p className="text-blue-700 text-sm">{t('appdownload.step3_desc')}</p>
          </div>
        </div>
      </section>

      {/*  FAQ & 风险说明  */}
      <section className="bg-[#F5F7FA] py-20 border-t border-slate-200 flex-1">
        <div className="mx-auto max-w-[800px] px-5">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-slate-900">FAQ</h2>
          </div>
          <div className="space-y-4 mb-16">
            <details className="group rounded-3xl border border-slate-200 bg-white [&_summary::-webkit-details-marker]:hidden">
              <summary className="flex cursor-pointer items-center justify-between p-6 font-bold text-lg text-slate-900">
                {t('appdownload.faq1_q')}
                <span className="transition group-open:rotate-180">
                  <svg fill="none" height="24" shape-rendering="geometricPrecision" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" viewBox="0 0 24 24" width="24"><path d="M6 9l6 6 6-6"></path></svg>
                </span>
              </summary>
              <div className="px-6 pb-6 text-slate-600"><p>{t('appdownload.faq1_a')}</p></div>
            </details>
            <details className="group rounded-3xl border border-slate-200 bg-white [&_summary::-webkit-details-marker]:hidden">
              <summary className="flex cursor-pointer items-center justify-between p-6 font-bold text-lg text-slate-900">
                {t('appdownload.faq2_q')}
                <span className="transition group-open:rotate-180">
                  <svg fill="none" height="24" shape-rendering="geometricPrecision" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" viewBox="0 0 24 24" width="24"><path d="M6 9l6 6 6-6"></path></svg>
                </span>
              </summary>
              <div className="px-6 pb-6 text-slate-600"><p>{t('appdownload.faq2_a')}</p></div>
            </details>
            <details className="group rounded-3xl border border-slate-200 bg-white [&_summary::-webkit-details-marker]:hidden">
              <summary className="flex cursor-pointer items-center justify-between p-6 font-bold text-lg text-slate-900">
                {t('appdownload.faq3_q')}
                <span className="transition group-open:rotate-180">
                  <svg fill="none" height="24" shape-rendering="geometricPrecision" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" viewBox="0 0 24 24" width="24"><path d="M6 9l6 6 6-6"></path></svg>
                </span>
              </summary>
              <div className="px-6 pb-6 text-slate-600"><p>{t('appdownload.faq3_a')}</p></div>
            </details>
            <details className="group rounded-3xl border border-slate-200 bg-white [&_summary::-webkit-details-marker]:hidden">
              <summary className="flex cursor-pointer items-center justify-between p-6 font-bold text-lg text-slate-900">
                {t('appdownload.faq4_q')}
                <span className="transition group-open:rotate-180">
                  <svg fill="none" height="24" shape-rendering="geometricPrecision" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" viewBox="0 0 24 24" width="24"><path d="M6 9l6 6 6-6"></path></svg>
                </span>
              </summary>
              <div className="px-6 pb-6 text-slate-600"><p>{t('appdownload.faq4_a')}</p></div>
            </details>
          </div>

          {/*  风险说明  */}
          <div className="bg-yellow-50 border border-yellow-200 rounded-3xl p-8 flex gap-4">
            <svg className="w-8 h-8 text-yellow-600 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
            <div>
              <h4 className="font-bold text-yellow-900 text-lg mb-2">{t('appdownload.risk_title')}</h4>
              <p className="text-yellow-800 text-sm mb-2">{t('appdownload.risk_desc1')}</p>
              <p className="text-yellow-900 text-sm font-bold">{t('appdownload.risk_desc2')}</p>
            </div>
          </div>
        </div>
      </section>
      </div>
    </>
  );
}
