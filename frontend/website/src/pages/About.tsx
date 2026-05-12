import { useTranslation } from 'react-i18next';
import { Helmet } from 'react-helmet-async';
import { useParams } from 'react-router-dom';

export default function About() {
  const { t } = useTranslation();
  const { lang } = useParams();

  return (
    <>
      <Helmet>
        <title>{t('about.title')}</title>
        <meta name="description" content={t('about.desc')} />
        <meta name="keywords" content={t('about.keywords')} />
        <script type="application/ld+json">{`{
        "@context": "https://schema.org",
        "@type": "AboutPage",
        "name": "${t('about.title')}",
        "description": "${t('about.desc')}",
        "url": "https://khmerx.org/${lang}/about",
        "mainEntity": {
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
        }
      }`}</script>
      </Helmet>

      <div className="flex-1">
        {/*  Hero 区  */}
      <section className="relative bg-slate-900 border-b border-slate-800 overflow-hidden text-white">
        <div className="absolute inset-0 bg-[url('https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=Cambodia%20Phnom%20Penh%20city%20modern%20finance%20technology%20blue%20tones%20abstract%20clean%20business%20style&image_size=landscape_16_9')] bg-cover bg-center opacity-30 mix-blend-overlay"></div>
        <div className="relative mx-auto max-w-[1200px] px-5 py-20 md:py-28">
          <div className="grid gap-12 md:grid-cols-2 md:items-center">
            <div className="max-w-xl z-10">
              <div className="mb-6 inline-flex rounded-full bg-blue-500/20 px-4 py-2 text-sm font-bold text-blue-300 border border-blue-500/30">
                <svg className="w-4 h-4 inline mr-2 -mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                KhmerX Story
              </div>
              <h1 className="text-4xl font-extrabold leading-tight tracking-tight md:text-5xl lg:text-6xl mb-6">
                {t('about.hero_title')}
              </h1>
              <p className="text-lg leading-relaxed text-slate-300 md:text-xl font-medium">
                {t('about.hero_subtitle')}
              </p>
            </div>
            
            <div className="relative z-10 flex justify-center md:justify-end">
              <div className="relative w-64 h-64 sm:w-80 sm:h-80 animate-float">
                <img src="https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=Telegram%20Mini%20App%20on%20Mobile%20Phone%20with%20ABA%20bank%20elements%20blue%20tones%20clean%20modern%20business&image_size=square" alt="KhmerX App" className="w-full h-full object-contain drop-shadow-2xl" />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/*  KhmerX 是什么  */}
      <section className="mx-auto max-w-[1200px] px-5 py-20 -mt-10 relative z-20">
        <div className="bg-white rounded-3xl p-8 md:p-12 shadow-xl border border-slate-100 flex flex-col md:flex-row gap-10 items-center">
          <div className="flex-1">
            <h2 className="text-3xl font-bold text-slate-900 mb-6">{t('about.sec1_title')}</h2>
            <p className="text-slate-600 text-lg mb-8 leading-relaxed">{t('about.sec1_desc')}</p>
            
            <div className="flex flex-wrap gap-3 mb-8">
              <span className="bg-blue-50 text-blue-700 px-4 py-2 rounded-full font-bold text-sm">Telegram</span>
              <span className="bg-blue-50 text-blue-700 px-4 py-2 rounded-full font-bold text-sm">ABA</span>
              <span className="bg-blue-50 text-blue-700 px-4 py-2 rounded-full font-bold text-sm">Cambodia</span>
              <span className="bg-blue-50 text-blue-700 px-4 py-2 rounded-full font-bold text-sm">{t('about.sec1_tag4')}</span>
              <span className="bg-blue-50 text-blue-700 px-4 py-2 rounded-full font-bold text-sm">{t('about.sec1_tag5')}</span>
            </div>

            <div className="bg-slate-900 text-white p-6 rounded-2xl border border-slate-800">
              <h4 className="font-bold text-blue-400 mb-4">{t('about.sec1_platform_title')}</h4>
              <ul className="space-y-3">
                <li className="flex items-center gap-3">
                  <svg className="w-5 h-5 text-blue-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                  {t('about.sec1_li1')}
                </li>
                <li className="flex items-center gap-3">
                  <svg className="w-5 h-5 text-blue-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                  {t('about.sec1_li2')}
                </li>
                <li className="flex items-center gap-3">
                  <svg className="w-5 h-5 text-blue-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                  {t('about.sec1_li3')}
                </li>
              </ul>
            </div>
          </div>
          
          <div className="w-full md:w-1/3 flex flex-col gap-6">
            {/*  为什么做 KhmerX  */}
            <div className="bg-blue-600 text-white p-8 rounded-3xl shadow-lg relative overflow-hidden">
              <div className="absolute top-0 right-0 -mt-10 -mr-10 w-32 h-32 bg-white opacity-10 rounded-full blur-2xl"></div>
              <h3 className="text-2xl font-bold mb-4 relative z-10">{t('about.sec2_title')}</h3>
              <p className="text-blue-100 mb-4 relative z-10">{t('about.sec2_desc1')}</p>
              <p className="font-bold relative z-10">{t('about.sec2_desc2')}</p>
            </div>
          </div>
        </div>
      </section>

      {/*  KhmerX 如何工作  */}
      <section className="bg-white py-20 border-y border-slate-100">
        <div className="mx-auto max-w-[1200px] px-5">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-slate-900">{t('about.sec3_title')}</h2>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4 relative">
            <div className="hidden md:block absolute top-1/2 left-10 right-10 h-0.5 bg-slate-100 -z-10 -translate-y-1/2"></div>
            
            <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm text-center relative z-10 group hover:-translate-y-2 transition-transform">
              <div className="w-12 h-12 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center font-bold text-xl mx-auto mb-4 group-hover:bg-blue-600 group-hover:text-white transition-colors">1</div>
              <h4 className="font-bold text-slate-900">{t('about.step1')}</h4>
            </div>
            
            <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm text-center relative z-10 group hover:-translate-y-2 transition-transform">
              <div className="w-12 h-12 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center font-bold text-xl mx-auto mb-4 group-hover:bg-blue-600 group-hover:text-white transition-colors">2</div>
              <h4 className="font-bold text-slate-900">{t('about.step2')}</h4>
            </div>
            
            <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm text-center relative z-10 group hover:-translate-y-2 transition-transform">
              <div className="w-12 h-12 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center font-bold text-xl mx-auto mb-4 group-hover:bg-blue-600 group-hover:text-white transition-colors">3</div>
              <h4 className="font-bold text-slate-900">{t('about.step3')}</h4>
            </div>
            
            <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm text-center relative z-10 group hover:-translate-y-2 transition-transform">
              <div className="w-12 h-12 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center font-bold text-xl mx-auto mb-4 group-hover:bg-blue-600 group-hover:text-white transition-colors">4</div>
              <h4 className="font-bold text-slate-900">{t('about.step4')}</h4>
            </div>
            
            <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm text-center relative z-10 group hover:-translate-y-2 transition-transform">
              <div className="w-12 h-12 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center font-bold text-xl mx-auto mb-4 group-hover:bg-blue-600 group-hover:text-white transition-colors">5</div>
              <h4 className="font-bold text-slate-900">{t('about.step5')}</h4>
            </div>
          </div>
        </div>
      </section>

      {/*  本地化与 Telegram & 安全与风控  */}
      <section className="mx-auto max-w-[1200px] px-5 py-20">
        <div className="grid md:grid-cols-2 gap-8">
          
          <div className="bg-white rounded-[2rem] p-8 md:p-12 border border-slate-200 shadow-sm">
            <div className="w-12 h-12 bg-blue-100 text-blue-600 rounded-xl flex items-center justify-center mb-6">
              <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.74-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .38z"/></svg>
            </div>
            <h3 className="text-2xl font-bold text-slate-900 mb-6">{t('about.sec4_title')}</h3>
            <ul className="space-y-4">
              <li className="flex gap-4 items-start">
                <svg className="w-6 h-6 text-blue-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                <div>
                  <h4 className="font-bold text-slate-900">Telegram</h4>
                  <p className="text-slate-600 text-sm">{t('about.sec4_li1')}</p>
                </div>
              </li>
              <li className="flex gap-4 items-start">
                <svg className="w-6 h-6 text-blue-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                <div>
                  <h4 className="font-bold text-slate-900">{t('about.sec4_li2_t')}</h4>
                  <p className="text-slate-600 text-sm">{t('about.sec4_li2')}</p>
                </div>
              </li>
              <li className="flex gap-4 items-start">
                <svg className="w-6 h-6 text-blue-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                <div>
                  <h4 className="font-bold text-slate-900">ABA</h4>
                  <p className="text-slate-600 text-sm">{t('about.sec4_li3')}</p>
                </div>
              </li>
            </ul>
          </div>
          
          <div className="bg-white rounded-[2rem] p-8 md:p-12 border border-slate-200 shadow-sm">
            <div className="w-12 h-12 bg-indigo-100 text-indigo-600 rounded-xl flex items-center justify-center mb-6">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>
            </div>
            <h3 className="text-2xl font-bold text-slate-900 mb-6">{t('about.sec5_title')}</h3>
            <div className="grid grid-cols-2 gap-4 mb-6">
              <div className="bg-slate-50 p-4 rounded-xl border border-slate-100 font-bold text-slate-700 text-sm text-center">{t('about.sec5_tag1')}</div>
              <div className="bg-slate-50 p-4 rounded-xl border border-slate-100 font-bold text-slate-700 text-sm text-center">{t('about.sec5_tag2')}</div>
              <div className="bg-slate-50 p-4 rounded-xl border border-slate-100 font-bold text-slate-700 text-sm text-center">{t('about.sec5_tag3')}</div>
              <div className="bg-slate-50 p-4 rounded-xl border border-slate-100 font-bold text-slate-700 text-sm text-center">{t('about.sec5_tag4')}</div>
            </div>
            <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-4 text-sm text-yellow-800">
              ⚠️ <strong>{t('about.sec5_notice_title')}</strong>: {t('about.sec5_notice')}
            </div>
          </div>

        </div>
      </section>

      {/*  平台原则  */}
      <section className="bg-slate-900 py-20 text-white">
        <div className="mx-auto max-w-[1200px] px-5">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold">{t('about.sec6_title')}</h2>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="bg-slate-800 p-8 rounded-3xl border border-slate-700 text-center hover:bg-slate-750 transition-colors">
              <h4 className="font-bold text-xl text-blue-400 mb-2">{t('about.sec6_1')}</h4>
            </div>
            <div className="bg-slate-800 p-8 rounded-3xl border border-slate-700 text-center hover:bg-slate-750 transition-colors">
              <h4 className="font-bold text-xl text-blue-400 mb-2">{t('about.sec6_2')}</h4>
            </div>
            <div className="bg-slate-800 p-8 rounded-3xl border border-slate-700 text-center hover:bg-slate-750 transition-colors">
              <h4 className="font-bold text-xl text-blue-400 mb-2">{t('about.sec6_3')}</h4>
            </div>
            <div className="bg-slate-800 p-8 rounded-3xl border border-slate-700 text-center hover:bg-slate-750 transition-colors">
              <h4 className="font-bold text-xl text-blue-400 mb-2">{t('about.sec6_4')}</h4>
            </div>
          </div>
        </div>
      </section>

      {/*  CTA  */}
      <section className="mx-auto max-w-[1200px] px-5 py-24">
        <div className="bg-gradient-to-br from-[#0A5BFF] to-[#00AEEF] rounded-[3rem] p-10 md:p-16 text-center text-white shadow-2xl relative overflow-hidden">
          <div className="absolute top-0 right-0 -mt-20 -mr-20 w-64 h-64 bg-white opacity-10 rounded-full blur-3xl"></div>
          <div className="absolute bottom-0 left-0 -mb-20 -ml-20 w-64 h-64 bg-white opacity-10 rounded-full blur-3xl"></div>
          
          <div className="relative z-10 max-w-2xl mx-auto">
            <h2 className="text-3xl md:text-4xl font-bold mb-8">{t('about.cta_title')}</h2>
            <div className="flex flex-col items-center justify-center gap-8">
              <div className="bg-white p-4 rounded-3xl shadow-lg inline-block">
                <img className="w-48 h-48 rounded-2xl" alt="KhmerX Mini App QR" src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https%3A%2F%2Ft.me%2FKhmerXBot%2Fapp" />
                <div className="text-slate-500 text-sm font-medium mt-3">Scan with Camera</div>
              </div>
              <a className="inline-flex justify-center items-center rounded-2xl bg-white px-10 py-5 text-xl font-bold text-blue-600 shadow-xl hover:shadow-2xl hover:scale-105 transition-all duration-300" href="https://t.me/KhmerXBot/app">
                <svg className="w-6 h-6 mr-3" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.74-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .38z"/></svg>
                {t('about.cta_btn')}
              </a>
              <p className="mt-4 opacity-80 text-sm max-w-md mx-auto">{t('about.contact_desc')} <a href="https://t.me/KhmerXBot" className="underline font-bold">Contact Telegram</a></p>
            </div>
          </div>
        </div>
      </section>
      </div>
    </>
  );
}
