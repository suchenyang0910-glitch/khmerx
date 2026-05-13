import { useTranslation } from 'react-i18next';
import { Helmet } from 'react-helmet-async';

export default function Terms() {
  const { t } = useTranslation();

  return (
    <>
      <Helmet>
        <title>{t('terms.title')}</title>
        <meta name="description" content={t('terms.desc')} />
        <meta name="keywords" content={t('terms.keywords')} />
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
        <div className="absolute inset-0 bg-[url('https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=Dark%20blue%20legal%20document%20contract%20rules%20shield%20technology%20background%20abstract%20modern%20clean%20business%20style&image_size=landscape_16_9')] bg-cover bg-center opacity-30 mix-blend-overlay"></div>
        <div className="relative mx-auto max-w-[1200px] px-5 py-20 md:py-28">
          <div className="grid gap-12 md:grid-cols-2 md:items-center">
            <div className="max-w-xl z-10">
              <div className="mb-6 inline-flex rounded-full bg-blue-500/20 px-4 py-2 text-sm font-bold text-blue-300 border border-blue-500/30">
                <svg className="w-4 h-4 inline mr-2 -mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>
                KhmerX Rules & Agreements
              </div>
              <h1 className="text-4xl font-extrabold leading-tight tracking-tight md:text-5xl lg:text-6xl mb-6">
                {t('terms.hero_title')}
              </h1>
              <p className="text-lg leading-relaxed text-slate-300 md:text-xl font-medium">
                {t('terms.hero_subtitle')}
              </p>
            </div>
            
            <div className="relative z-10 flex justify-center md:justify-end">
              <div className="relative w-48 h-48 sm:w-64 sm:h-64 animate-float">
                <div className="absolute inset-0 bg-blue-500 rounded-full blur-3xl opacity-40"></div>
                <svg className="relative w-full h-full text-blue-400 drop-shadow-2xl" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/*  内容区  */}
      <section className="mx-auto max-w-[800px] px-5 py-20 -mt-10 relative z-20">
        <div className="bg-white rounded-3xl p-8 md:p-12 shadow-xl border border-slate-100 prose prose-slate prose-blue max-w-none">
          
          <div className="bg-blue-50 border border-blue-100 rounded-2xl p-6 not-prose mb-10">
            <h2 className="text-xl font-bold text-blue-900 mb-4 flex items-center gap-2">
              <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
              {t('terms.sec1_title')}
            </h2>
            <p className="text-blue-800 text-sm mb-4 leading-relaxed">{t('terms.sec1_desc')}</p>
            <ul className="space-y-2 text-sm font-bold text-blue-900">
              <li className="flex items-center gap-2"><svg className="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>{t('terms.sec1_li1')}</li>
              <li className="flex items-center gap-2"><svg className="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>{t('terms.sec1_li2')}</li>
              <li className="flex items-center gap-2"><svg className="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>{t('terms.sec1_li3')}</li>
              <li className="flex items-center gap-2"><svg className="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>{t('terms.sec1_li4')}</li>
            </ul>
          </div>

          <h2 className="text-2xl font-bold text-slate-900 mt-12 mb-6">{t('terms.sec2_title')}</h2>
          <ul className="space-y-2">
            <li>{t('terms.sec2_li1')}</li>
            <li>{t('terms.sec2_li2')}</li>
            <li>{t('terms.sec2_li3')}</li>
            <li>{t('terms.sec2_li4')}</li>
          </ul>
          <p className="text-sm italic mt-4 text-slate-500">{t('terms.sec2_notice')}</p>

          <h2 className="text-2xl font-bold text-slate-900 mt-12 mb-6">{t('terms.sec3_title')}</h2>
          <p><strong>{t('terms.sec3_sub1')}</strong><br/>{t('terms.sec3_desc1')}</p>
          <p><strong>{t('terms.sec3_sub2')}</strong><br/>{t('terms.sec3_desc2')}</p>
          <p><strong>{t('terms.sec3_sub3')}</strong><br/>{t('terms.sec3_desc3')}</p>

          <h2 className="text-2xl font-bold text-slate-900 mt-12 mb-6">{t('terms.sec4_title')}</h2>
          <p><strong>{t('terms.sec4_sub1')}</strong><br/>{t('terms.sec4_desc1')}</p>
          <p><strong>{t('terms.sec4_sub2')}</strong><br/>{t('terms.sec4_desc2')}</p>
          <p><strong>{t('terms.sec4_sub3')}</strong><br/>{t('terms.sec4_desc3')}</p>

          <div className="bg-red-50 border border-red-100 rounded-2xl p-6 not-prose mb-10 mt-12">
            <h2 className="text-xl font-bold text-red-900 mb-4 flex items-center gap-2">
              <svg className="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
              {t('terms.sec5_title')}
            </h2>
            <p className="text-red-800 text-sm mb-4 leading-relaxed">{t('terms.sec5_desc')}</p>
            <ul className="space-y-2 text-sm text-red-800 list-disc list-inside">
              <li>{t('terms.sec5_li1')}</li>
              <li>{t('terms.sec5_li2')}</li>
              <li>{t('terms.sec5_li3')}</li>
              <li>{t('terms.sec5_li4')}</li>
            </ul>
          </div>

          <h2 className="text-2xl font-bold text-slate-900 mt-12 mb-6">{t('terms.sec6_title')}</h2>
          <ul className="space-y-2">
            <li>{t('terms.sec6_li1')}</li>
            <li>{t('terms.sec6_li2')}</li>
            <li>{t('terms.sec6_li3')}</li>
            <li>{t('terms.sec6_li4')}</li>
            <li>{t('terms.sec6_li5')}</li>
          </ul>
          <p className="text-sm font-medium mt-4 text-slate-700">{t('terms.sec6_notice')}</p>

          <h2 className="text-2xl font-bold text-slate-900 mt-12 mb-6">{t('terms.sec7_title')}</h2>
          <p>{t('terms.sec7_desc')}</p>
          <ul className="space-y-2 font-medium">
            <li>{t('terms.sec7_li1')}</li>
            <li>{t('terms.sec7_li2')}</li>
            <li>{t('terms.sec7_li3')}</li>
            <li>{t('terms.sec7_li4')}</li>
          </ul>

        </div>
      </section>

      {/*  联系方式  */}
      <section className="mx-auto max-w-[800px] px-5 pb-24">
        <div className="bg-blue-600 rounded-[2rem] p-10 text-center text-white shadow-xl relative overflow-hidden">
          <div className="absolute inset-0 bg-[url('https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=Blue%20technology%20abstract%20waves&image_size=landscape_16_9')] bg-cover bg-center opacity-20 mix-blend-overlay"></div>
          <div className="relative z-10">
            <h2 className="text-2xl md:text-3xl font-bold mb-4">{t('terms.contact_title')}</h2>
            <p className="text-blue-100 mb-8">{t('terms.contact_desc')}</p>
            <a className="inline-flex justify-center items-center rounded-xl bg-white px-8 py-4 text-lg font-bold text-blue-600 shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-300" href="https://t.me/KhmerXBot">
              <svg className="w-6 h-6 mr-2" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.74-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .38z"/></svg>
              {t('terms.contact_btn')}
            </a>
          </div>
        </div>
      </section>
      </div>
    </>
  );
}
