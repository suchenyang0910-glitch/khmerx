import { useTranslation } from 'react-i18next';
import { Helmet } from 'react-helmet-async';
import { useParams } from 'react-router-dom';

export default function Risk() {
  const { t } = useTranslation();
  const { lang } = useParams();

  return (
    <>
      <Helmet>
        <title>{t('risk.title')}</title>
        <meta name="description" content={t('risk.desc')} />
        <meta name="keywords" content={t('risk.keywords')} />
        <script type="application/ld+json">{`{
        "@context": "https://schema.org",
        "@type": "FinancialService",
        "name": "KhmerX",
        "description": "${t('risk.desc')}",
        "url": "https://khmerx.org/${lang}",
        "telephone": "",
        "email": "support@khmerx.org",
        "areaServed": "Cambodia",
        "knowsAbout": ["Micro Lending", "Peer-to-Peer Lending", "Risk Management"]
      }`}</script>
      </Helmet>

      <div className="flex-1">
        {/*  Hero 区  */}
      <section className="relative bg-slate-900 border-b border-slate-800 overflow-hidden text-white">
        <div className="absolute inset-0 bg-[url('https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=Dark%20blue%20financial%20security%20shield%20network%20technology%20background%20abstract%20modern%20clean%20business%20style&image_size=landscape_16_9')] bg-cover bg-center opacity-30 mix-blend-overlay"></div>
        <div className="relative mx-auto max-w-[1200px] px-5 py-20 md:py-28">
          <div className="grid gap-12 md:grid-cols-2 md:items-center">
            <div className="max-w-xl z-10">
              <div className="mb-6 inline-flex rounded-full bg-blue-500/20 px-4 py-2 text-sm font-bold text-blue-300 border border-blue-500/30">
                <svg className="w-4 h-4 inline mr-2 -mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path></svg>
                KhmerX Safety & Rules
              </div>
              <h1 className="text-4xl font-extrabold leading-tight tracking-tight md:text-5xl lg:text-6xl mb-6">
                {t('risk.hero_title')}
              </h1>
              <p className="text-lg leading-relaxed text-slate-300 md:text-xl font-medium">
                {t('risk.hero_subtitle')}
              </p>
            </div>
            
            <div className="relative z-10 flex justify-center md:justify-end">
              <div className="relative w-48 h-48 sm:w-64 sm:h-64 animate-float">
                <div className="absolute inset-0 bg-blue-500 rounded-full blur-3xl opacity-40"></div>
                <svg className="relative w-full h-full text-blue-400 drop-shadow-2xl" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
                </svg>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/*  KhmerX 服务说明（官方定位）  */}
      <section className="mx-auto max-w-[1200px] px-5 py-20 -mt-10 relative z-20">
        <div className="bg-white rounded-3xl p-8 md:p-12 shadow-xl border border-slate-100 flex flex-col md:flex-row gap-10 items-center">
          <div className="flex-1">
            <h2 className="text-2xl md:text-3xl font-bold text-slate-900 mb-4">{t('risk.service_title')}</h2>
            <p className="text-slate-600 text-lg mb-8 leading-relaxed">{t('risk.service_desc')}</p>
            
            <div className="grid sm:grid-cols-2 gap-4">
              <div className="bg-blue-50/50 p-4 rounded-xl border border-blue-100 flex items-start gap-3">
                <svg className="w-6 h-6 text-blue-500 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                <span className="font-bold text-blue-900">{t('risk.service_not_bank')}</span>
              </div>
              <div className="bg-blue-50/50 p-4 rounded-xl border border-blue-100 flex items-start gap-3">
                <svg className="w-6 h-6 text-blue-500 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                <span className="font-bold text-blue-900">{t('risk.service_no_deposit')}</span>
              </div>
              <div className="bg-blue-50/50 p-4 rounded-xl border border-blue-100 flex items-start gap-3">
                <svg className="w-6 h-6 text-blue-500 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                <span className="font-bold text-blue-900">{t('risk.service_no_guarantee_profit')}</span>
              </div>
              <div className="bg-blue-50/50 p-4 rounded-xl border border-blue-100 flex items-start gap-3">
                <svg className="w-6 h-6 text-blue-500 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                <span className="font-bold text-blue-900">{t('risk.service_no_guarantee_borrow')}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/*  用户风险提示  */}
      <section className="mx-auto max-w-[1200px] px-5 pb-20">
        <h2 className="text-3xl font-bold text-slate-900 mb-8 text-center">{t('risk.user_risk_title')}</h2>
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-[#FEF2F2] border border-[#FCA5A5] rounded-2xl p-6 relative hover:-translate-y-1 transition-transform">
            <div className="absolute top-0 right-0 bg-[#EF4444] text-white text-xs font-bold px-3 py-1 rounded-bl-2xl rounded-tr-2xl">Risk 1</div>
            <h4 className="font-bold text-[#991B1B] text-lg mb-3 mt-2">{t('risk.risk_1_title')}</h4>
            <p className="text-[#7F1D1D] text-sm">{t('risk.risk_1_desc')}</p>
          </div>
          <div className="bg-[#FEF2F2] border border-[#FCA5A5] rounded-2xl p-6 relative hover:-translate-y-1 transition-transform">
            <div className="absolute top-0 right-0 bg-[#EF4444] text-white text-xs font-bold px-3 py-1 rounded-bl-2xl rounded-tr-2xl">Risk 2</div>
            <h4 className="font-bold text-[#991B1B] text-lg mb-3 mt-2">{t('risk.risk_2_title')}</h4>
            <p className="text-[#7F1D1D] text-sm">{t('risk.risk_2_desc')}</p>
          </div>
          <div className="bg-[#FEF2F2] border border-[#FCA5A5] rounded-2xl p-6 relative hover:-translate-y-1 transition-transform">
            <div className="absolute top-0 right-0 bg-[#EF4444] text-white text-xs font-bold px-3 py-1 rounded-bl-2xl rounded-tr-2xl">Risk 3</div>
            <h4 className="font-bold text-[#991B1B] text-lg mb-3 mt-2">{t('risk.risk_3_title')}</h4>
            <p className="text-[#7F1D1D] text-sm">{t('risk.risk_3_desc')}</p>
          </div>
          <div className="bg-[#FEF2F2] border border-[#FCA5A5] rounded-2xl p-6 relative hover:-translate-y-1 transition-transform">
            <div className="absolute top-0 right-0 bg-[#EF4444] text-white text-xs font-bold px-3 py-1 rounded-bl-2xl rounded-tr-2xl">Risk 4</div>
            <h4 className="font-bold text-[#991B1B] text-lg mb-3 mt-2">{t('risk.risk_4_title')}</h4>
            <p className="text-[#7F1D1D] text-sm">{t('risk.risk_4_desc')}</p>
          </div>
        </div>
      </section>

      {/*  借款风险与逾期说明  */}
      <section className="bg-white py-20 border-y border-slate-100">
        <div className="mx-auto max-w-[1200px] px-5">
          <div className="grid md:grid-cols-2 gap-12">
            
            {/*  借款风险说明  */}
            <div>
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 rounded-xl bg-orange-100 text-orange-600 flex items-center justify-center">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                </div>
                <h3 className="text-2xl font-bold text-slate-900">{t('risk.borrow_risk_title')}</h3>
              </div>
              <div className="space-y-6">
                <div className="border-l-4 border-orange-400 pl-5">
                  <h4 className="font-bold text-slate-900 text-lg mb-2">{t('risk.borrow_fee_title')}</h4>
                  <p className="text-slate-600">{t('risk.borrow_fee_desc')}</p>
                </div>
                <div className="border-l-4 border-orange-400 pl-5">
                  <h4 className="font-bold text-slate-900 text-lg mb-2">{t('risk.borrow_confirm_title')}</h4>
                  <p className="text-slate-600 mb-2">{t('risk.borrow_confirm_desc')}</p>
                  <ul className="list-disc list-inside text-sm text-slate-500 ml-2 space-y-1">
                    <li>{t('risk.borrow_confirm_1')}</li>
                    <li>{t('risk.borrow_confirm_2')}</li>
                    <li>{t('risk.borrow_confirm_3')}</li>
                  </ul>
                </div>
                <div className="border-l-4 border-orange-400 pl-5">
                  <h4 className="font-bold text-slate-900 text-lg mb-2">{t('risk.borrow_credit_title')}</h4>
                  <p className="text-slate-600">{t('risk.borrow_credit_desc')}</p>
                </div>
              </div>
            </div>
            
            {/*  逾期与信用说明  */}
            <div>
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 rounded-xl bg-red-100 text-red-600 flex items-center justify-center">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                </div>
                <h3 className="text-2xl font-bold text-slate-900">{t('risk.overdue_title')}</h3>
              </div>
              <div className="space-y-6">
                <div className="border-l-4 border-red-400 pl-5">
                  <h4 className="font-bold text-slate-900 text-lg mb-2">{t('risk.overdue_remind_title')}</h4>
                  <p className="text-slate-600">{t('risk.overdue_remind_desc')}</p>
                </div>
                <div className="border-l-4 border-red-400 pl-5">
                  <h4 className="font-bold text-slate-900 text-lg mb-2">{t('risk.overdue_conseq_title')}</h4>
                  <p className="text-slate-600 mb-2">{t('risk.overdue_conseq_desc')}</p>
                  <ul className="list-disc list-inside text-sm text-slate-500 ml-2 space-y-1">
                    <li>{t('risk.overdue_conseq_1')}</li>
                    <li>{t('risk.overdue_conseq_2')}</li>
                    <li>{t('risk.overdue_conseq_3')}</li>
                  </ul>
                </div>
                <div className="border-l-4 border-red-600 pl-5">
                  <h4 className="font-bold text-red-700 text-lg mb-2">{t('risk.overdue_severe_title')}</h4>
                  <p className="text-red-600 font-medium">{t('risk.overdue_severe_desc')}</p>
                </div>
              </div>
            </div>
            
          </div>
        </div>
      </section>

      {/*  官方声明 (极重要) & 安全建议  */}
      <section className="mx-auto max-w-[1200px] px-5 py-20">
        <div className="grid md:grid-cols-2 gap-8">
          {/*  官方声明  */}
          <div className="bg-slate-900 rounded-[2rem] p-8 md:p-12 text-white shadow-xl relative overflow-hidden">
            <div className="absolute -right-10 -top-10 text-white/5">
              <svg className="w-64 h-64" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>
            </div>
            <div className="relative z-10">
              <h2 className="text-3xl font-bold mb-6 flex items-center gap-3 text-blue-400">
                <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                {t('risk.statement_title')}
              </h2>
              <p className="text-lg text-slate-300 mb-8 font-medium">{t('risk.statement_desc')}</p>
              
              <div className="space-y-4 mb-8">
                <p className="text-slate-400 font-bold">{t('risk.statement_not_guarantee')}</p>
                <ul className="space-y-3">
                  <li className="flex items-center gap-3 text-slate-300">
                    <svg className="w-5 h-5 text-red-400 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                    {t('risk.statement_ng_1')}
                  </li>
                  <li className="flex items-center gap-3 text-slate-300">
                    <svg className="w-5 h-5 text-red-400 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                    {t('risk.statement_ng_2')}
                  </li>
                  <li className="flex items-center gap-3 text-slate-300">
                    <svg className="w-5 h-5 text-red-400 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                    {t('risk.statement_ng_3')}
                  </li>
                </ul>
              </div>
              
              <div className="bg-blue-900/50 border border-blue-800 p-4 rounded-xl text-blue-200 font-bold text-center">
                {t('risk.statement_user_risk')}
              </div>
            </div>
          </div>
          
          {/*  安全建议  */}
          <div className="bg-white rounded-[2rem] p-8 md:p-12 border border-slate-200 shadow-sm flex flex-col justify-center">
            <h2 className="text-3xl font-bold text-slate-900 mb-8">{t('risk.safety_title')}</h2>
            <div className="space-y-6">
              <div className="flex gap-4 items-start">
                <div className="w-12 h-12 rounded-full bg-green-100 text-green-600 flex items-center justify-center shrink-0">
                  <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.74-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .38z"/></svg>
                </div>
                <div>
                  <h4 className="font-bold text-slate-900 text-lg mb-1">{t('risk.safety_tg_title')}</h4>
                  <p className="text-slate-600">{t('risk.safety_tg_desc')}</p>
                </div>
              </div>
              
              <div className="flex gap-4 items-start">
                <div className="w-12 h-12 rounded-full bg-red-100 text-red-600 flex items-center justify-center shrink-0">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636"></path></svg>
                </div>
                <div>
                  <h4 className="font-bold text-slate-900 text-lg mb-1">{t('risk.safety_scam_title')}</h4>
                  <p className="text-slate-600">{t('risk.safety_scam_desc')}</p>
                </div>
              </div>
              
              <div className="flex gap-4 items-start">
                <div className="w-12 h-12 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center shrink-0">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                </div>
                <div>
                  <h4 className="font-bold text-slate-900 text-lg mb-1">{t('risk.safety_proof_title')}</h4>
                  <p className="text-slate-600">{t('risk.safety_proof_desc')}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/*  FAQ  */}
      <section className="bg-white py-20 border-t border-slate-100">
        <div className="mx-auto max-w-[800px] px-5">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-slate-900">FAQ</h2>
          </div>
          <div className="space-y-4">
            <details className="group rounded-3xl border border-slate-200 bg-white [&_summary::-webkit-details-marker]:hidden">
              <summary className="flex cursor-pointer items-center justify-between p-6 font-bold text-lg text-slate-900">
                {t('risk.faq_1_q')}
                <span className="transition group-open:rotate-180">
                  <svg fill="none" height="24" shape-rendering="geometricPrecision" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" viewBox="0 0 24 24" width="24"><path d="M6 9l6 6 6-6"></path></svg>
                </span>
              </summary>
              <div className="px-6 pb-6 text-slate-600">
                <p>{t('risk.faq_1_a')}</p>
              </div>
            </details>
            <details className="group rounded-3xl border border-slate-200 bg-white [&_summary::-webkit-details-marker]:hidden">
              <summary className="flex cursor-pointer items-center justify-between p-6 font-bold text-lg text-slate-900">
                {t('risk.faq_2_q')}
                <span className="transition group-open:rotate-180">
                  <svg fill="none" height="24" shape-rendering="geometricPrecision" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" viewBox="0 0 24 24" width="24"><path d="M6 9l6 6 6-6"></path></svg>
                </span>
              </summary>
              <div className="px-6 pb-6 text-slate-600">
                <p>{t('risk.faq_2_a')}</p>
              </div>
            </details>
            <details className="group rounded-3xl border border-slate-200 bg-white [&_summary::-webkit-details-marker]:hidden">
              <summary className="flex cursor-pointer items-center justify-between p-6 font-bold text-lg text-slate-900">
                {t('risk.faq_3_q')}
                <span className="transition group-open:rotate-180">
                  <svg fill="none" height="24" shape-rendering="geometricPrecision" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" viewBox="0 0 24 24" width="24"><path d="M6 9l6 6 6-6"></path></svg>
                </span>
              </summary>
              <div className="px-6 pb-6 text-slate-600">
                <p>{t('risk.faq_3_a')}</p>
              </div>
            </details>
            <details className="group rounded-3xl border border-slate-200 bg-white [&_summary::-webkit-details-marker]:hidden">
              <summary className="flex cursor-pointer items-center justify-between p-6 font-bold text-lg text-slate-900">
                {t('risk.faq_4_q')}
                <span className="transition group-open:rotate-180">
                  <svg fill="none" height="24" shape-rendering="geometricPrecision" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" viewBox="0 0 24 24" width="24"><path d="M6 9l6 6 6-6"></path></svg>
                </span>
              </summary>
              <div className="px-6 pb-6 text-slate-600">
                <p>{t('risk.faq_4_a')}</p>
              </div>
            </details>
          </div>
        </div>
      </section>

      {/*  CTA  */}
      <section className="mx-auto max-w-[1200px] px-5 py-24">
        <div className="bg-gradient-to-br from-[#0A5BFF] to-[#00AEEF] rounded-[3rem] p-10 md:p-16 text-center text-white shadow-2xl relative overflow-hidden">
          <div className="absolute top-0 right-0 -mt-20 -mr-20 w-64 h-64 bg-white opacity-10 rounded-full blur-3xl"></div>
          <div className="absolute bottom-0 left-0 -mb-20 -ml-20 w-64 h-64 bg-white opacity-10 rounded-full blur-3xl"></div>
          
          <div className="relative z-10 max-w-2xl mx-auto">
            <h2 className="text-3xl md:text-4xl font-bold mb-8">{t('risk.cta_title')}</h2>
            <div className="flex flex-col items-center justify-center gap-8">
              <div className="bg-white p-4 rounded-3xl shadow-lg inline-block">
                <img className="w-48 h-48 rounded-2xl" alt="KhmerX Mini App QR" src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https%3A%2F%2Ft.me%2FKhmerXBot%2Fapp" />
                <div className="text-slate-500 text-sm font-medium mt-3">Scan with Camera</div>
              </div>
              <a className="inline-flex justify-center items-center rounded-2xl bg-white px-10 py-5 text-xl font-bold text-blue-600 shadow-xl hover:shadow-2xl hover:scale-105 transition-all duration-300" href="https://t.me/KhmerXBot/app">
                <svg className="w-6 h-6 mr-3" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.74-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .38z"/></svg>
                {t('risk.cta_btn')}
              </a>
            </div>
          </div>
        </div>
      </section>
      </div>
    </>
  );
}
