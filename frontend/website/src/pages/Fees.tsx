import { useTranslation } from 'react-i18next';
import { Helmet } from 'react-helmet-async';
import { useParams } from 'react-router-dom';

export default function Fees() {
  const { t } = useTranslation();
  const { lang } = useParams();

  return (
    <>
      <Helmet>
        <title>{t('fees.title')}</title>
        <meta name="description" content={t('fees.desc')} />
        <meta name="keywords" content={t('fees.keywords')} />
        <script type="application/ld+json">{`{
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
          {
            "@type": "Question",
            "name": "${t('fees.faq_1_q')}",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "${t('fees.faq_1_a')}"
            }
          },
          {
            "@type": "Question",
            "name": "${t('fees.faq_2_q')}",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "${t('fees.faq_2_a')}"
            }
          },
          {
            "@type": "Question",
            "name": "${t('fees.faq_3_q')}",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "${t('fees.faq_3_a')}"
            }
          },
          {
            "@type": "Question",
            "name": "${t('fees.faq_4_q')}",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "${t('fees.faq_4_a')}"
            }
          }
        ]
      }`}</script>
      </Helmet>

      <div className="flex-1">
        {/*  1. Header  */}
      <header className="sticky top-0 z-50 border-b bg-white/90 backdrop-blur-md">
        <div className="mx-auto flex max-w-[1200px] items-center justify-between px-5 py-4">
          <a href="/{lang}" className="flex items-center gap-3 group">
            <img src="/logo.jpg" alt="KhmerX Logo" className="h-10 w-10 rounded-xl object-cover shadow-sm group-hover:scale-105 transition-transform" />
            <div>
              <div className="font-bold text-lg">KhmerX</div>
            </div>
          </a>
          <nav className="hidden gap-8 text-sm font-medium text-slate-600 md:flex">
            <a className="hover:text-blue-600 transition-colors" href="/{lang}/borrow">{t('fees.nav_borrow')}</a>
            <a className="text-blue-600 transition-colors" href="/{lang}/fees">{t('fees.nav_fees')}</a>
            <a className="hover:text-blue-600 transition-colors" href="/{lang}/faq">{t('fees.nav_faq')}</a>
            <a className="hover:text-blue-600 transition-colors" href="/{lang}/contact">{t('fees.nav_contact')}</a>
          </nav>
          <div className="flex items-center gap-4">
            <div className="hidden md:flex gap-1 text-sm bg-slate-100 p-1 rounded-xl">
              <a data-lang="km" className="rounded-lg px-3 py-1.5 transition-colors font-medium {t('fees.km_active')}" href="/km/fees">ខ្មែរ</a>
              <a data-lang="en" className="rounded-lg px-3 py-1.5 transition-colors font-medium {t('fees.en_active')}" href="/en/fees">EN</a>
              <a data-lang="zh" className="rounded-lg px-3 py-1.5 transition-colors font-medium {t('fees.zh_active')}" href="/zh/fees">中文</a>
            </div>
            <a className="hidden md:inline-flex rounded-xl bg-gradient-to-r from-[#0A5BFF] to-[#00AEEF] px-5 py-2.5 text-sm font-bold text-white shadow-md hover:shadow-lg hover:scale-105 transition-all" href="https://t.me/KhmerXBot/app">{t('fees.nav_cta')}</a>
            <button className="md:hidden p-2 text-slate-600">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
            </button>
          </div>
        </div>
      </header>

      {/*  2. Hero 区  */}
      <section className="relative overflow-hidden bg-white border-b border-slate-100">
        <div className="absolute inset-0 bg-gradient-to-b from-blue-50/50 to-white"></div>
        <div className="relative mx-auto max-w-[1200px] px-5 py-16 md:py-24">
          <div className="grid gap-12 md:grid-cols-2 md:items-center">
            <div className="max-w-xl z-10">
              <h1 className="text-4xl font-extrabold leading-tight tracking-tight text-slate-900 md:text-5xl lg:text-6xl">
                {t('fees.hero_title')}
              </h1>
              <p className="mt-6 text-lg leading-relaxed text-slate-600 md:text-xl font-medium">
                {t('fees.hero_subtitle')}
              </p>
              <div className="mt-10">
                <a className="inline-flex justify-center items-center rounded-2xl bg-gradient-to-r from-[#0A5BFF] to-[#00AEEF] px-8 py-4 text-lg font-bold text-white shadow-xl shadow-blue-500/30 hover:shadow-blue-500/50 hover:-translate-y-1 transition-all duration-300 w-full sm:w-auto" href="https://t.me/KhmerXBot/app">
                  <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.74-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .38z"/></svg>
                  {t('fees.hero_cta')}
                </a>
              </div>
            </div>
            <div className="relative z-10 flex justify-center md:justify-end">
              <div className="relative w-[300px] sm:w-[360px] animate-float">
                <div className="absolute inset-0 bg-blue-500 rounded-[3rem] blur-3xl opacity-20 transform translate-y-10"></div>
                <img src="https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=3D%20illustration%20of%20financial%20fees%20calculator%20coins%20and%20receipts%20modern%20clean%20blue%20and%20gold%20colors%20gradient%20background%20high%20quality&image_size=square_hd" alt="KhmerX Fees Illustration" className="relative rounded-[2.5rem] shadow-2xl border-[8px] border-white object-cover w-full h-auto bg-slate-100" />
                
                <div className="absolute -bottom-6 -left-6 bg-white p-5 rounded-2xl shadow-xl border border-slate-100 animate-float" style={{ animationDelay: '1.5s' }}>
                  <div className="text-sm font-bold text-slate-800 flex items-center gap-2">
                    <svg className="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    {t('fees.hero_float_1')}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/*  3. 费用原则说明  */}
      <section className="mx-auto max-w-[1200px] px-5 py-20">
        <div className="grid gap-10 md:grid-cols-2 items-center">
          <div>
            <h2 className="text-3xl font-bold text-slate-900 mb-6">{t('fees.principle_title')}</h2>
            <div className="prose prose-lg text-slate-600">
              <p>{t('fees.principle_desc_1')}</p>
              <p>{t('fees.principle_desc_2')}</p>
            </div>
          </div>
          
          <div className="bg-[#FFFBEB] border-2 border-[#FCD34D] rounded-3xl p-8 shadow-sm relative overflow-hidden">
            <div className="absolute top-0 right-0 w-32 h-32 bg-[#FDE68A] rounded-full blur-3xl opacity-50 -mr-10 -mt-10"></div>
            
            <div className="relative z-10">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-12 h-12 bg-[#F59E0B] rounded-xl flex items-center justify-center text-white shrink-0 shadow-md">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                </div>
                <h3 className="text-2xl font-bold text-[#92400E]">{t('fees.principle_risk_title')}</h3>
              </div>
              
              <ul className="space-y-4 text-lg font-bold text-[#B45309]">
                <li className="flex items-center gap-3 bg-white/60 p-4 rounded-2xl">
                  <span className="w-8 h-8 rounded-full bg-[#FDE68A] flex items-center justify-center text-[#92400E] shrink-0">1</span>
                  {t('fees.principle_risk_1')}
                </li>
                <li className="flex items-center gap-3 bg-white/60 p-4 rounded-2xl">
                  <span className="w-8 h-8 rounded-full bg-[#FDE68A] flex items-center justify-center text-[#92400E] shrink-0">2</span>
                  {t('fees.principle_risk_2')}
                </li>
                <li className="flex items-center gap-3 bg-white/60 p-4 rounded-2xl">
                  <span className="w-8 h-8 rounded-full bg-[#FDE68A] flex items-center justify-center text-[#92400E] shrink-0">3</span>
                  {t('fees.principle_risk_3')}
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/*  4. 借款示例（重点）  */}
      <section className="bg-white py-20 border-y border-slate-100">
        <div className="mx-auto max-w-[1200px] px-5">
          <div className="text-center max-w-2xl mx-auto mb-16">
            <h2 className="text-3xl font-bold text-slate-900">{t('fees.ex_title')}</h2>
            <p className="mt-4 text-slate-600">{t('fees.ex_subtitle')}</p>
          </div>
          
          <div className="grid gap-6 md:grid-cols-3">
            {/*  Example 1  */}
            <div className="bg-white rounded-3xl p-8 shadow-sm border border-slate-100 hover:shadow-xl hover:-translate-y-2 transition-all duration-300">
              <div className="inline-block bg-blue-100 text-blue-700 font-bold px-4 py-1.5 rounded-full text-sm mb-6">{t('fees.ex_1_badge')}</div>
              <div className="space-y-5">
                <div className="flex justify-between items-center pb-4 border-b border-slate-100">
                  <span className="text-slate-500">{t('fees.ex_borrow')}</span>
                  <span className="text-xl font-bold text-slate-900">$100</span>
                </div>
                <div className="flex justify-between items-center pb-4 border-b border-slate-100">
                  <span className="text-slate-500">{t('fees.ex_fee')}</span>
                  <span className="text-lg font-medium text-slate-700">$10</span>
                </div>
                <div className="flex justify-between items-center pb-4 border-b border-slate-100">
                  <span className="text-slate-500">{t('fees.ex_receive')}</span>
                  <span className="text-xl font-bold text-blue-600">$90</span>
                </div>
                <div className="flex justify-between items-center pb-4 border-b border-slate-100">
                  <span className="text-slate-500">{t('fees.ex_duration')}</span>
                  <span className="text-lg font-medium text-slate-700">{t('fees.ex_1_duration')}</span>
                </div>
                <div className="flex justify-between items-center pt-2">
                  <span className="font-bold text-slate-900">{t('fees.ex_repay')}</span>
                  <span className="text-3xl font-extrabold text-slate-900">$100</span>
                </div>
              </div>
            </div>
            
            {/*  Example 2  */}
            <div className="bg-white rounded-3xl p-8 shadow-sm border border-slate-100 hover:shadow-xl hover:-translate-y-2 transition-all duration-300 relative overflow-hidden">
              <div className="absolute top-0 right-0 w-2 h-full bg-blue-500"></div>
              <div className="inline-block bg-blue-100 text-blue-700 font-bold px-4 py-1.5 rounded-full text-sm mb-6">{t('fees.ex_2_badge')}</div>
              <div className="space-y-5">
                <div className="flex justify-between items-center pb-4 border-b border-slate-100">
                  <span className="text-slate-500">{t('fees.ex_borrow')}</span>
                  <span className="text-xl font-bold text-slate-900">$100</span>
                </div>
                <div className="flex justify-between items-center pb-4 border-b border-slate-100">
                  <span className="text-slate-500">{t('fees.ex_fee')}</span>
                  <span className="text-lg font-medium text-slate-700">$18</span>
                </div>
                <div className="flex justify-between items-center pb-4 border-b border-slate-100">
                  <span className="text-slate-500">{t('fees.ex_receive')}</span>
                  <span className="text-xl font-bold text-blue-600">$82</span>
                </div>
                <div className="flex justify-between items-center pb-4 border-b border-slate-100">
                  <span className="text-slate-500">{t('fees.ex_duration')}</span>
                  <span className="text-lg font-medium text-slate-700">{t('fees.ex_2_duration')}</span>
                </div>
                <div className="flex justify-between items-center pt-2">
                  <span className="font-bold text-slate-900">{t('fees.ex_repay')}</span>
                  <span className="text-3xl font-extrabold text-slate-900">$100</span>
                </div>
              </div>
            </div>
            
            {/*  Example 3  */}
            <div className="bg-white rounded-3xl p-8 shadow-sm border border-slate-100 hover:shadow-xl hover:-translate-y-2 transition-all duration-300">
              <div className="inline-block bg-blue-100 text-blue-700 font-bold px-4 py-1.5 rounded-full text-sm mb-6">{t('fees.ex_3_badge')}</div>
              <div className="space-y-5">
                <div className="flex justify-between items-center pb-4 border-b border-slate-100">
                  <span className="text-slate-500">{t('fees.ex_borrow')}</span>
                  <span className="text-xl font-bold text-slate-900">$100</span>
                </div>
                <div className="flex justify-between items-center pb-4 border-b border-slate-100">
                  <span className="text-slate-500">{t('fees.ex_fee')}</span>
                  <span className="text-lg font-medium text-slate-700">$30</span>
                </div>
                <div className="flex justify-between items-center pb-4 border-b border-slate-100">
                  <span className="text-slate-500">{t('fees.ex_receive')}</span>
                  <span className="text-xl font-bold text-blue-600">$70</span>
                </div>
                <div className="flex justify-between items-center pb-4 border-b border-slate-100">
                  <span className="text-slate-500">{t('fees.ex_duration')}</span>
                  <span className="text-lg font-medium text-slate-700">{t('fees.ex_3_duration')}</span>
                </div>
                <div className="flex justify-between items-center pt-2">
                  <span className="font-bold text-slate-900">{t('fees.ex_repay')}</span>
                  <span className="text-3xl font-extrabold text-slate-900">$100</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/*  5. 平息法解释模块 & 6. 不同期限费用表  */}
      <section className="mx-auto max-w-[1200px] px-5 py-20">
        <div className="grid gap-12 lg:grid-cols-5">
          {/*  平息法解释  */}
          <div className="lg:col-span-2">
            <h2 className="text-2xl font-bold text-slate-900 mb-6">{t('fees.math_title')}</h2>
            <div className="bg-slate-900 text-white rounded-3xl p-8 shadow-xl">
              <p className="text-slate-300 mb-6">{t('fees.math_desc')}</p>
              
              <div className="bg-slate-800 rounded-2xl p-5 mb-8 border border-slate-700">
                <div className="text-sm text-slate-400 mb-2">{t('fees.math_formula_label')}</div>
                <div className="font-mono text-lg font-bold text-blue-400">{t('fees.math_formula')}</div>
              </div>
              
              <div className="space-y-4 font-mono text-sm">
                <div className="flex justify-between items-center">
                  <span className="text-slate-400">7 {t('fees.math_days')}:</span>
                  <span>100 × 10% = <span className="text-white font-bold">10</span></span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-400">14 {t('fees.math_days')}:</span>
                  <span>100 × 18% = <span className="text-white font-bold">18</span></span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-400">30 {t('fees.math_days')}:</span>
                  <span>100 × 30% = <span className="text-white font-bold">30</span></span>
                </div>
              </div>
            </div>
          </div>
          
          {/*  不同期限费用表  */}
          <div className="lg:col-span-3">
            <h2 className="text-2xl font-bold text-slate-900 mb-6">{t('fees.table_title')}</h2>
            <div className="bg-white rounded-3xl shadow-sm border border-slate-200 overflow-hidden">
              <div className="table-container overflow-x-auto">
                <table className="w-full text-left border-collapse min-w-[500px]">
                  <thead>
                    <tr className="bg-blue-50 border-b border-blue-100">
                      <th className="py-4 px-6 font-bold text-blue-900">{t('fees.table_th_duration')}</th>
                      <th className="py-4 px-6 font-bold text-blue-900">{t('fees.table_th_fee')}</th>
                      <th className="py-4 px-6 font-bold text-blue-900">{t('fees.table_th_receive')}</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    <tr className="hover:bg-slate-50 transition-colors">
                      <td className="py-4 px-6 font-medium text-slate-900">7 {t('fees.table_days')}</td>
                      <td className="py-4 px-6 text-slate-600">8% - 12%</td>
                      <td className="py-4 px-6 font-medium text-blue-600">88% - 92%</td>
                    </tr>
                    <tr className="hover:bg-slate-50 transition-colors">
                      <td className="py-4 px-6 font-medium text-slate-900">14 {t('fees.table_days')}</td>
                      <td className="py-4 px-6 text-slate-600">15% - 20%</td>
                      <td className="py-4 px-6 font-medium text-blue-600">80% - 85%</td>
                    </tr>
                    <tr className="hover:bg-slate-50 transition-colors bg-blue-50/30">
                      <td className="py-4 px-6 font-medium text-slate-900">30 {t('fees.table_days')}</td>
                      <td className="py-4 px-6 text-slate-600">25% - 35%</td>
                      <td className="py-4 px-6 font-medium text-blue-600">65% - 75%</td>
                    </tr>
                    <tr className="hover:bg-slate-50 transition-colors text-slate-400">
                      <td className="py-4 px-6 font-medium">45 {t('fees.table_days')}</td>
                      <td className="py-4 px-6">{t('fees.table_dynamic')}</td>
                      <td className="py-4 px-6">{t('fees.table_dynamic')}</td>
                    </tr>
                    <tr className="hover:bg-slate-50 transition-colors text-slate-400">
                      <td className="py-4 px-6 font-medium">60 {t('fees.table_days')}</td>
                      <td className="py-4 px-6">{t('fees.table_dynamic')}</td>
                      <td className="py-4 px-6">{t('fees.table_dynamic')}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/*  7. 逾期规则  */}
      <section className="mx-auto max-w-[1200px] px-5 pb-20">
        <div className="bg-[#FEF2F2] border-2 border-[#FCA5A5] rounded-[2.5rem] p-8 md:p-12">
          <div className="flex flex-col md:flex-row gap-8 items-start">
            <div className="w-16 h-16 bg-[#EF4444] rounded-2xl flex items-center justify-center text-white shrink-0 shadow-lg">
              <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
            </div>
            
            <div className="flex-1">
              <h2 className="text-3xl font-bold text-[#991B1B] mb-6">{t('fees.overdue_title')}</h2>
              
              <div className="grid gap-6 md:grid-cols-2">
                <div className="bg-white/80 backdrop-blur rounded-2xl p-6">
                  <h4 className="font-bold text-[#991B1B] mb-2 flex items-center gap-2">
                    <svg className="w-5 h-5 text-[#EF4444]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    {t('fees.overdue_reminder_title')}
                  </h4>
                  <p className="text-[#7F1D1D] text-sm">{t('fees.overdue_reminder_desc')}</p>
                </div>
                
                <div className="bg-white/80 backdrop-blur rounded-2xl p-6">
                  <h4 className="font-bold text-[#991B1B] mb-2 flex items-center gap-2">
                    <svg className="w-5 h-5 text-[#EF4444]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                    {t('fees.overdue_severe_title')}
                  </h4>
                  <p className="text-[#7F1D1D] text-sm">{t('fees.overdue_severe_desc')}</p>
                </div>
              </div>
              
              <div className="mt-6 bg-white/80 backdrop-blur rounded-2xl p-6">
                <h4 className="font-bold text-[#991B1B] mb-4">{t('fees.overdue_conseq_title')}</h4>
                <ul className="grid sm:grid-cols-3 gap-4">
                  <li className="flex items-center gap-2 text-[#7F1D1D] font-medium bg-[#FEE2E2] px-4 py-2 rounded-xl">
                    <div className="w-2 h-2 rounded-full bg-[#EF4444]"></div>
                    {t('fees.overdue_conseq_1')}
                  </li>
                  <li className="flex items-center gap-2 text-[#7F1D1D] font-medium bg-[#FEE2E2] px-4 py-2 rounded-xl">
                    <div className="w-2 h-2 rounded-full bg-[#EF4444]"></div>
                    {t('fees.overdue_conseq_2')}
                  </li>
                  <li className="flex items-center gap-2 text-[#7F1D1D] font-medium bg-[#FEE2E2] px-4 py-2 rounded-xl">
                    <div className="w-2 h-2 rounded-full bg-[#EF4444]"></div>
                    {t('fees.overdue_conseq_3')}
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/*  8. FAQ  */}
      <section className="bg-white py-20 border-t border-slate-100">
        <div className="mx-auto max-w-[800px] px-5">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-slate-900">FAQ</h2>
          </div>
          <div className="space-y-4">
            <details className="group rounded-3xl border border-slate-200 bg-white [&_summary::-webkit-details-marker]:hidden">
              <summary className="flex cursor-pointer items-center justify-between p-6 font-bold text-lg text-slate-900">
                {t('fees.faq_1_q')}
                <span className="transition group-open:rotate-180">
                  <svg fill="none" height="24" shape-rendering="geometricPrecision" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" viewBox="0 0 24 24" width="24"><path d="M6 9l6 6 6-6"></path></svg>
                </span>
              </summary>
              <div className="px-6 pb-6 text-slate-600">
                <p>{t('fees.faq_1_a')}</p>
              </div>
            </details>
            <details className="group rounded-3xl border border-slate-200 bg-white [&_summary::-webkit-details-marker]:hidden">
              <summary className="flex cursor-pointer items-center justify-between p-6 font-bold text-lg text-slate-900">
                {t('fees.faq_2_q')}
                <span className="transition group-open:rotate-180">
                  <svg fill="none" height="24" shape-rendering="geometricPrecision" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" viewBox="0 0 24 24" width="24"><path d="M6 9l6 6 6-6"></path></svg>
                </span>
              </summary>
              <div className="px-6 pb-6 text-slate-600">
                <p>{t('fees.faq_2_a')}</p>
              </div>
            </details>
            <details className="group rounded-3xl border border-slate-200 bg-white [&_summary::-webkit-details-marker]:hidden">
              <summary className="flex cursor-pointer items-center justify-between p-6 font-bold text-lg text-slate-900">
                {t('fees.faq_3_q')}
                <span className="transition group-open:rotate-180">
                  <svg fill="none" height="24" shape-rendering="geometricPrecision" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" viewBox="0 0 24 24" width="24"><path d="M6 9l6 6 6-6"></path></svg>
                </span>
              </summary>
              <div className="px-6 pb-6 text-slate-600">
                <p>{t('fees.faq_3_a')}</p>
              </div>
            </details>
            <details className="group rounded-3xl border border-slate-200 bg-white [&_summary::-webkit-details-marker]:hidden">
              <summary className="flex cursor-pointer items-center justify-between p-6 font-bold text-lg text-slate-900">
                {t('fees.faq_4_q')}
                <span className="transition group-open:rotate-180">
                  <svg fill="none" height="24" shape-rendering="geometricPrecision" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" viewBox="0 0 24 24" width="24"><path d="M6 9l6 6 6-6"></path></svg>
                </span>
              </summary>
              <div className="px-6 pb-6 text-slate-600">
                <p>{t('fees.faq_4_a')}</p>
              </div>
            </details>
          </div>
        </div>
      </section>

      {/*  9. CTA 引导  */}
      <section className="mx-auto max-w-[1200px] px-5 py-24">
        <div className="bg-gradient-to-br from-[#0A5BFF] to-[#00AEEF] rounded-[3rem] p-10 md:p-16 text-center text-white shadow-2xl relative overflow-hidden">
          <div className="absolute top-0 right-0 -mt-20 -mr-20 w-64 h-64 bg-white opacity-10 rounded-full blur-3xl"></div>
          <div className="absolute bottom-0 left-0 -mb-20 -ml-20 w-64 h-64 bg-white opacity-10 rounded-full blur-3xl"></div>
          
          <div className="relative z-10 max-w-2xl mx-auto">
            <h2 className="text-3xl md:text-5xl font-bold mb-8">{t('fees.cta_title')}</h2>
            <div className="flex flex-col items-center justify-center gap-8">
              <div className="bg-white p-4 rounded-3xl shadow-lg inline-block">
                <img className="w-48 h-48 rounded-2xl" alt="KhmerX Mini App QR" src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https%3A%2F%2Ft.me%2FKhmerXBot%2Fapp" />
                <div className="text-slate-500 text-sm font-medium mt-3">Scan with Camera</div>
              </div>
              <a className="inline-flex justify-center items-center rounded-2xl bg-white px-10 py-5 text-xl font-bold text-blue-600 shadow-xl hover:shadow-2xl hover:scale-105 transition-all duration-300" href="https://t.me/KhmerXBot/app">
                <svg className="w-6 h-6 mr-3" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.74-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .38z"/></svg>
                {t('fees.cta_btn')}
              </a>
            </div>
          </div>
        </div>
      </section>

      {/*  10. Footer  */}
      <footer className="bg-slate-950 px-5 py-12 text-slate-400">
        <div className="mx-auto max-w-[1200px]">
          <div className="grid gap-8 md:grid-cols-4 border-b border-slate-800 pb-12">
            <div className="col-span-2">
              <a href="/{lang}" className="flex items-center gap-3 mb-6">
                <img src="/logo.jpg" alt="KhmerX Logo" className="h-8 w-8 rounded-lg object-cover grayscale opacity-80" />
                <div className="font-bold text-lg text-white">KhmerX</div>
              </a>
              <p className="text-sm leading-relaxed max-w-md">
                {t('fees.footer_risk')}
              </p>
            </div>
            <div>
              <h4 className="text-white font-bold mb-6">Links</h4>
              <ul className="space-y-4 text-sm">
                <li><a href="https://t.me/KhmerXBot" className="hover:text-white transition-colors">Telegram Support</a></li>
                <li><a href="mailto:support@khmerx.org" className="hover:text-white transition-colors">support@khmerx.org</a></li>
              </ul>
            </div>
            <div>
              <h4 className="text-white font-bold mb-6">Legal</h4>
              <ul className="space-y-4 text-sm">
                <li><a href="/{lang}/terms" className="hover:text-white transition-colors">User Agreement</a></li>
                <li><a href="/{lang}/privacy" className="hover:text-white transition-colors">Privacy Policy</a></li>
              </ul>
            </div>
          </div>
          <div className="flex flex-col md:flex-row items-center justify-between pt-8 gap-4 text-sm">
            <div>© <span data-year></span> KhmerX. All rights reserved.</div>
            <div className="flex gap-4">
              <a href="/km" className="hover:text-white transition-colors">ខ្មែរ</a>
              <a href="/en" className="hover:text-white transition-colors">English</a>
              <a href="/zh" className="hover:text-white transition-colors">中文</a>
            </div>
          </div>
        </div>
      </footer>
      </div>
    </>
  );
}
