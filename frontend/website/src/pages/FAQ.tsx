import { useTranslation } from 'react-i18next';
import { Helmet } from 'react-helmet-async';
import { useParams } from 'react-router-dom';

export default function FAQ() {
  const { t } = useTranslation();
  const { lang } = useParams();

  return (
    <>
      <Helmet>
        <title>{t('faq.title')}</title>
        <meta name="description" content={t('faq.desc')} />
        <meta name="keywords" content={t('faq.keywords')} />
        <script type="application/ld+json">{`{
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
          {
            "@type": "Question",
            "name": "${t('faq.q1_q')}",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "${t('faq.q1_a')}"
            }
          },
          {
            "@type": "Question",
            "name": "${t('faq.q2_q')}",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "${t('faq.q2_a')}"
            }
          },
          {
            "@type": "Question",
            "name": "${t('faq.q3_q')}",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "${t('faq.q3_a')}"
            }
          },
          {
            "@type": "Question",
            "name": "${t('faq.q4_q')}",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "${t('faq.q4_a')}"
            }
          },
          {
            "@type": "Question",
            "name": "${t('faq.q5_q')}",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "${t('faq.q5_a')}"
            }
          },
          {
            "@type": "Question",
            "name": "${t('faq.q6_q')}",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "${t('faq.q6_a')}"
            }
          },
          {
            "@type": "Question",
            "name": "${t('faq.q7_q')}",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "${t('faq.q7_a')}"
            }
          },
          {
            "@type": "Question",
            "name": "${t('faq.q8_q')}",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "${t('faq.q8_a')}"
            }
          },
          {
            "@type": "Question",
            "name": "${t('faq.q9_q')}",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "${t('faq.q9_a')}"
            }
          },
          {
            "@type": "Question",
            "name": "${t('faq.q10_q')}",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "${t('faq.q10_a')}"
            }
          },
          {
            "@type": "Question",
            "name": "${t('faq.q11_q')}",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "${t('faq.q11_a')}"
            }
          }
        ]
      }`}</script>
      </Helmet>

      <div className="flex-1">
        {/*  Hero 区  */}
      <section className="relative bg-gradient-to-b from-blue-50 to-[#F5F7FA] pt-20 pb-12">
        <div className="mx-auto max-w-[800px] px-5 text-center">
          <h1 className="text-4xl md:text-5xl font-extrabold text-slate-900 mb-6">{t('faq.hero_title')}</h1>
          <p className="text-lg text-slate-600 mb-10">{t('faq.hero_subtitle')}</p>
          
          {/*  搜索框  */}
          <div className="relative max-w-2xl mx-auto">
            <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <svg className="w-6 h-6 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
            </div>
            <input type="text" id="faq-search" className="w-full pl-12 pr-4 py-4 rounded-[18px] border-2 border-slate-200 focus:border-blue-500 focus:ring-0 text-lg shadow-sm transition-colors outline-none" placeholder="{t('faq.search_placeholder')}" />
          </div>
        </div>
      </section>

      {/*  FAQ 分类导航  */}
      <section className="mx-auto max-w-[1000px] px-5 mb-12">
        <div className="flex flex-wrap justify-center gap-3">
          <a href="#cat-borrow" className="flex items-center gap-2 bg-white px-5 py-3 rounded-2xl shadow-sm border border-slate-200 hover:border-blue-500 hover:text-blue-600 transition-colors font-medium">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            {t('faq.cat_borrow')}
          </a>
          <a href="#cat-fees" className="flex items-center gap-2 bg-white px-5 py-3 rounded-2xl shadow-sm border border-slate-200 hover:border-blue-500 hover:text-blue-600 transition-colors font-medium">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
            {t('faq.cat_fees')}
          </a>
          <a href="#cat-repay" className="flex items-center gap-2 bg-white px-5 py-3 rounded-2xl shadow-sm border border-slate-200 hover:border-blue-500 hover:text-blue-600 transition-colors font-medium">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"></path></svg>
            {t('faq.cat_repay')}
          </a>
          <a href="#cat-credit" className="flex items-center gap-2 bg-white px-5 py-3 rounded-2xl shadow-sm border border-slate-200 hover:border-blue-500 hover:text-blue-600 transition-colors font-medium">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>
            {t('faq.cat_credit')}
          </a>
          <a href="#cat-tg" className="flex items-center gap-2 bg-white px-5 py-3 rounded-2xl shadow-sm border border-slate-200 hover:border-blue-500 hover:text-blue-600 transition-colors font-medium">
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.74-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .38z"/></svg>
            Telegram
          </a>
        </div>
      </section>

      {/*  FAQ 列表  */}
      <section className="mx-auto max-w-[800px] px-5 pb-20" id="faq-list">
        
        <div className="mb-12 faq-category" id="cat-borrow">
          <h2 className="text-2xl font-bold text-slate-900 mb-6 flex items-center gap-3">
            <svg className="w-6 h-6 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            {t('faq.cat_borrow')}
          </h2>
          <div className="space-y-4">
            <details className="faq-item group bg-white rounded-2xl border border-slate-200 overflow-hidden hover:border-blue-300 transition-colors">
              <summary className="flex items-center justify-between p-6 cursor-pointer font-bold text-lg text-slate-800 hover:bg-blue-50/50">
                <span className="faq-q">{t('faq.q1_q')}</span>
                <span className="text-blue-500 group-open:rotate-180 transition-transform"><svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <div className="px-6 pb-6 text-slate-600 leading-relaxed border-t border-slate-100 pt-4 faq-a">{t('faq.q1_a')}</div>
            </details>
            <details className="faq-item group bg-white rounded-2xl border border-slate-200 overflow-hidden hover:border-blue-300 transition-colors">
              <summary className="flex items-center justify-between p-6 cursor-pointer font-bold text-lg text-slate-800 hover:bg-blue-50/50">
                <span className="faq-q">{t('faq.q2_q')}</span>
                <span className="text-blue-500 group-open:rotate-180 transition-transform"><svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <div className="px-6 pb-6 text-slate-600 leading-relaxed border-t border-slate-100 pt-4 faq-a">{t('faq.q2_a')}</div>
            </details>
            <details className="faq-item group bg-white rounded-2xl border border-slate-200 overflow-hidden hover:border-blue-300 transition-colors">
              <summary className="flex items-center justify-between p-6 cursor-pointer font-bold text-lg text-slate-800 hover:bg-blue-50/50">
                <span className="faq-q">{t('faq.q3_q')}</span>
                <span className="text-blue-500 group-open:rotate-180 transition-transform"><svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <div className="px-6 pb-6 text-slate-600 leading-relaxed border-t border-slate-100 pt-4 faq-a">{t('faq.q3_a')}</div>
            </details>
          </div>
        </div>

        <div className="mb-12 faq-category" id="cat-fees">
          <h2 className="text-2xl font-bold text-slate-900 mb-6 flex items-center gap-3">
            <svg className="w-6 h-6 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
            {t('faq.cat_fees')}
          </h2>
          <div className="space-y-4">
            <details className="faq-item group bg-white rounded-2xl border border-slate-200 overflow-hidden hover:border-blue-300 transition-colors">
              <summary className="flex items-center justify-between p-6 cursor-pointer font-bold text-lg text-slate-800 hover:bg-blue-50/50">
                <span className="faq-q">{t('faq.q4_q')}</span>
                <span className="text-blue-500 group-open:rotate-180 transition-transform"><svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <div className="px-6 pb-6 text-slate-600 leading-relaxed border-t border-slate-100 pt-4 faq-a">{t('faq.q4_a')}</div>
            </details>
            <details className="faq-item group bg-white rounded-2xl border border-slate-200 overflow-hidden hover:border-blue-300 transition-colors">
              <summary className="flex items-center justify-between p-6 cursor-pointer font-bold text-lg text-slate-800 hover:bg-blue-50/50">
                <span className="faq-q">{t('faq.q5_q')}</span>
                <span className="text-blue-500 group-open:rotate-180 transition-transform"><svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <div className="px-6 pb-6 text-slate-600 leading-relaxed border-t border-slate-100 pt-4 faq-a">{t('faq.q5_a')}</div>
            </details>
          </div>
        </div>

        <div className="mb-12 faq-category" id="cat-repay">
          <h2 className="text-2xl font-bold text-slate-900 mb-6 flex items-center gap-3">
            <svg className="w-6 h-6 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"></path></svg>
            {t('faq.cat_repay')}
          </h2>
          <div className="space-y-4">
            <details className="faq-item group bg-white rounded-2xl border border-slate-200 overflow-hidden hover:border-blue-300 transition-colors">
              <summary className="flex items-center justify-between p-6 cursor-pointer font-bold text-lg text-slate-800 hover:bg-blue-50/50">
                <span className="faq-q">{t('faq.q6_q')}</span>
                <span className="text-blue-500 group-open:rotate-180 transition-transform"><svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <div className="px-6 pb-6 text-slate-600 leading-relaxed border-t border-slate-100 pt-4 faq-a">{t('faq.q6_a')}</div>
            </details>
            <details className="faq-item group bg-white rounded-2xl border border-slate-200 overflow-hidden hover:border-blue-300 transition-colors">
              <summary className="flex items-center justify-between p-6 cursor-pointer font-bold text-lg text-slate-800 hover:bg-blue-50/50">
                <span className="faq-q">{t('faq.q7_q')}</span>
                <span className="text-blue-500 group-open:rotate-180 transition-transform"><svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <div className="px-6 pb-6 text-slate-600 leading-relaxed border-t border-slate-100 pt-4 faq-a">{t('faq.q7_a')}</div>
            </details>
          </div>
        </div>

        <div className="mb-12 faq-category" id="cat-credit">
          <h2 className="text-2xl font-bold text-slate-900 mb-6 flex items-center gap-3">
            <svg className="w-6 h-6 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>
            {t('faq.cat_credit')}
          </h2>
          <div className="space-y-4">
            <details className="faq-item group bg-white rounded-2xl border border-slate-200 overflow-hidden hover:border-blue-300 transition-colors">
              <summary className="flex items-center justify-between p-6 cursor-pointer font-bold text-lg text-slate-800 hover:bg-blue-50/50">
                <span className="faq-q">{t('faq.q8_q')}</span>
                <span className="text-blue-500 group-open:rotate-180 transition-transform"><svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <div className="px-6 pb-6 text-slate-600 leading-relaxed border-t border-slate-100 pt-4 faq-a">{t('faq.q8_a')}</div>
            </details>
            <details className="faq-item group bg-white rounded-2xl border border-slate-200 overflow-hidden hover:border-blue-300 transition-colors">
              <summary className="flex items-center justify-between p-6 cursor-pointer font-bold text-lg text-slate-800 hover:bg-blue-50/50">
                <span className="faq-q">{t('faq.q9_q')}</span>
                <span className="text-blue-500 group-open:rotate-180 transition-transform"><svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <div className="px-6 pb-6 text-slate-600 leading-relaxed border-t border-slate-100 pt-4 faq-a">{t('faq.q9_a')}</div>
            </details>
          </div>
        </div>

        <div className="mb-12 faq-category" id="cat-tg">
          <h2 className="text-2xl font-bold text-slate-900 mb-6 flex items-center gap-3">
            <svg className="w-6 h-6 text-blue-500" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.74-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .38z"/></svg>
            Telegram
          </h2>
          <div className="space-y-4">
            <details className="faq-item group bg-white rounded-2xl border border-slate-200 overflow-hidden hover:border-blue-300 transition-colors">
              <summary className="flex items-center justify-between p-6 cursor-pointer font-bold text-lg text-slate-800 hover:bg-blue-50/50">
                <span className="faq-q">{t('faq.q10_q')}</span>
                <span className="text-blue-500 group-open:rotate-180 transition-transform"><svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <div className="px-6 pb-6 text-slate-600 leading-relaxed border-t border-slate-100 pt-4 faq-a">{t('faq.q10_a')}</div>
            </details>
            <details className="faq-item group bg-white rounded-2xl border border-slate-200 overflow-hidden hover:border-blue-300 transition-colors">
              <summary className="flex items-center justify-between p-6 cursor-pointer font-bold text-lg text-slate-800 hover:bg-blue-50/50">
                <span className="faq-q">{t('faq.q11_q')}</span>
                <span className="text-blue-500 group-open:rotate-180 transition-transform"><svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <div className="px-6 pb-6 text-slate-600 leading-relaxed border-t border-slate-100 pt-4 faq-a">{t('faq.q11_a')}</div>
            </details>
          </div>
        </div>

        <div id="faq-empty" className="hidden text-center py-12">
          <svg className="w-16 h-16 text-slate-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
          <h3 className="text-xl font-bold text-slate-700 mb-2">{t('faq.empty_title')}</h3>
          <p className="text-slate-500">{t('faq.empty_desc')}</p>
        </div>
      </section>

      {/*  风险与规则说明  */}
      <section className="mx-auto max-w-[800px] px-5 pb-12">
        <div className="bg-[#FFFBEB] border-2 border-[#FDE68A] rounded-2xl p-6 md:p-8 flex gap-4 items-start">
          <svg className="w-8 h-8 text-[#F59E0B] shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
          <div>
            <h4 className="font-bold text-[#92400E] text-lg mb-2">{t('faq.risk_title')}</h4>
            <p className="text-[#B45309] mb-4">{t('faq.risk_desc')}</p>
            <ul className="list-disc list-inside text-[#B45309] font-medium space-y-1">
              <li>{t('faq.risk_1')}</li>
              <li>{t('faq.risk_2')}</li>
              <li>{t('faq.risk_3')}</li>
            </ul>
          </div>
        </div>
      </section>

      {/*  联系客服  */}
      <section className="mx-auto max-w-[800px] px-5 pb-20">
        <div className="bg-white rounded-3xl p-8 border border-slate-200 text-center shadow-sm">
          <h3 className="text-2xl font-bold text-slate-900 mb-3">{t('faq.contact_title')}</h3>
          <p className="text-slate-500 mb-6">{t('faq.contact_desc')}</p>
          <a className="inline-flex items-center justify-center rounded-xl border-2 border-blue-600 bg-white px-8 py-3 text-lg font-bold text-blue-600 hover:bg-blue-50 transition-colors" href="https://t.me/KhmerXBot">
            <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.74-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .38z"/></svg>
            {t('faq.contact_btn')}
          </a>
        </div>
      </section>

      {/*  CTA  */}
      <section className="mx-auto max-w-[1200px] px-5 pb-24">
        <div className="bg-gradient-to-br from-[#0A5BFF] to-[#00AEEF] rounded-[3rem] p-10 md:p-16 text-center text-white shadow-2xl relative overflow-hidden">
          <div className="absolute top-0 right-0 -mt-20 -mr-20 w-64 h-64 bg-white opacity-10 rounded-full blur-3xl"></div>
          <div className="absolute bottom-0 left-0 -mb-20 -ml-20 w-64 h-64 bg-white opacity-10 rounded-full blur-3xl"></div>
          
          <div className="relative z-10 max-w-2xl mx-auto">
            <h2 className="text-3xl md:text-5xl font-bold mb-8">{t('faq.cta_title')}</h2>
            <div className="flex flex-col items-center justify-center gap-8">
              <div className="bg-white p-4 rounded-3xl shadow-lg inline-block">
                <img className="w-48 h-48 rounded-2xl" alt="KhmerX Mini App QR" src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https%3A%2F%2Ft.me%2FKhmerXBot%2Fapp" />
                <div className="text-slate-500 text-sm font-medium mt-3">Scan with Camera</div>
              </div>
              <a className="inline-flex justify-center items-center rounded-2xl bg-white px-10 py-5 text-xl font-bold text-blue-600 shadow-xl hover:shadow-2xl hover:scale-105 transition-all duration-300" href="https://t.me/KhmerXBot/app">
                <svg className="w-6 h-6 mr-3" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.74-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .38z"/></svg>
                {t('faq.cta_btn')}
              </a>
            </div>
          </div>
        </div>
      </section>
      </div>
    </>
  );
}
