import os

template = """<!doctype html>
<html lang="{lang}">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title}</title>
    <meta name="description" content="{desc}" />
    <meta name="keywords" content="{keywords}" />
    <meta property="og:type" content="website" />
    <meta property="og:site_name" content="KhmerX" />
    <meta property="og:title" content="{title}" />
    <meta property="og:description" content="{desc}" />
    <meta property="og:url" content="https://khmerx.org/{lang}/fees" />
    <meta property="og:image" content="https://khmerx.org/logo.jpg" />
    <meta name="twitter:card" content="summary" />
    <meta name="twitter:title" content="{title}" />
    <meta name="twitter:description" content="{desc}" />
    <link rel="canonical" href="https://khmerx.org/{lang}/fees" />
    <link rel="alternate" href="https://khmerx.org/km/fees" hreflang="km" />
    <link rel="alternate" href="https://khmerx.org/en/fees" hreflang="en" />
    <link rel="alternate" href="https://khmerx.org/zh/fees" hreflang="zh" />
    <link rel="alternate" href="https://khmerx.org/km/fees" hreflang="x-default" />
    <script type="application/ld+json">
      {{
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
          {{
            "@type": "Question",
            "name": "{faq_1_q}",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "{faq_1_a}"
            }}
          }},
          {{
            "@type": "Question",
            "name": "{faq_2_q}",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "{faq_2_a}"
            }}
          }},
          {{
            "@type": "Question",
            "name": "{faq_3_q}",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "{faq_3_a}"
            }}
          }},
          {{
            "@type": "Question",
            "name": "{faq_4_q}",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "{faq_4_a}"
            }}
          }}
        ]
      }}
    </script>
    <style>
      @keyframes float {{
        0% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-10px); }}
        100% {{ transform: translateY(0px); }}
      }}
      .animate-float {{
        animation: float 4s ease-in-out infinite;
      }}
      .table-container {{
        scrollbar-width: thin;
        scrollbar-color: #cbd5e1 transparent;
      }}
      .table-container::-webkit-scrollbar {{
        height: 6px;
      }}
      .table-container::-webkit-scrollbar-thumb {{
        background-color: #cbd5e1;
        border-radius: 3px;
      }}
    </style>
  </head>
  <body>
    <script type="module" src="/src/site.ts"></script>
    <main class="min-h-screen bg-[#F5F7FA] pb-24 text-slate-900 font-sans">
      
      <!-- 1. Header -->
      <header class="sticky top-0 z-50 border-b bg-white/90 backdrop-blur-md">
        <div class="mx-auto flex max-w-[1200px] items-center justify-between px-5 py-4">
          <a href="/{lang}" class="flex items-center gap-3 group">
            <img src="/logo.jpg" alt="KhmerX Logo" class="h-10 w-10 rounded-xl object-cover shadow-sm group-hover:scale-105 transition-transform" />
            <div>
              <div class="font-bold text-lg">KhmerX</div>
            </div>
          </a>
          <nav class="hidden gap-8 text-sm font-medium text-slate-600 md:flex">
            <a class="hover:text-blue-600 transition-colors" href="/{lang}/borrow">{nav_borrow}</a>
            <a class="text-blue-600 transition-colors" href="/{lang}/fees">{nav_fees}</a>
            <a class="hover:text-blue-600 transition-colors" href="/{lang}/faq">{nav_faq}</a>
            <a class="hover:text-blue-600 transition-colors" href="/{lang}/contact">{nav_contact}</a>
          </nav>
          <div class="flex items-center gap-4">
            <div class="hidden md:flex gap-1 text-sm bg-slate-100 p-1 rounded-xl">
              <a data-lang="km" class="rounded-lg px-3 py-1.5 transition-colors font-medium {km_active}" href="/km/fees">ខ្មែរ</a>
              <a data-lang="en" class="rounded-lg px-3 py-1.5 transition-colors font-medium {en_active}" href="/en/fees">EN</a>
              <a data-lang="zh" class="rounded-lg px-3 py-1.5 transition-colors font-medium {zh_active}" href="/zh/fees">中文</a>
            </div>
            <a class="hidden md:inline-flex rounded-xl bg-gradient-to-r from-[#0A5BFF] to-[#00AEEF] px-5 py-2.5 text-sm font-bold text-white shadow-md hover:shadow-lg hover:scale-105 transition-all" href="https://t.me/KhmerXBot/app">{nav_cta}</a>
            <button class="md:hidden p-2 text-slate-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
            </button>
          </div>
        </div>
      </header>

      <!-- 2. Hero 区 -->
      <section class="relative overflow-hidden bg-white border-b border-slate-100">
        <div class="absolute inset-0 bg-gradient-to-b from-blue-50/50 to-white"></div>
        <div class="relative mx-auto max-w-[1200px] px-5 py-16 md:py-24">
          <div class="grid gap-12 md:grid-cols-2 md:items-center">
            <div class="max-w-xl z-10">
              <h1 class="text-4xl font-extrabold leading-tight tracking-tight text-slate-900 md:text-5xl lg:text-6xl">
                {hero_title}
              </h1>
              <p class="mt-6 text-lg leading-relaxed text-slate-600 md:text-xl font-medium">
                {hero_subtitle}
              </p>
              <div class="mt-10">
                <a class="inline-flex justify-center items-center rounded-2xl bg-gradient-to-r from-[#0A5BFF] to-[#00AEEF] px-8 py-4 text-lg font-bold text-white shadow-xl shadow-blue-500/30 hover:shadow-blue-500/50 hover:-translate-y-1 transition-all duration-300 w-full sm:w-auto" href="https://t.me/KhmerXBot/app">
                  <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.74-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .38z"/></svg>
                  {hero_cta}
                </a>
              </div>
            </div>
            <div class="relative z-10 flex justify-center md:justify-end">
              <div class="relative w-[300px] sm:w-[360px] animate-float">
                <div class="absolute inset-0 bg-blue-500 rounded-[3rem] blur-3xl opacity-20 transform translate-y-10"></div>
                <img src="https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=3D%20illustration%20of%20financial%20fees%20calculator%20coins%20and%20receipts%20modern%20clean%20blue%20and%20gold%20colors%20gradient%20background%20high%20quality&image_size=square_hd" alt="KhmerX Fees Illustration" class="relative rounded-[2.5rem] shadow-2xl border-[8px] border-white object-cover w-full h-auto bg-slate-100" />
                
                <div class="absolute -bottom-6 -left-6 bg-white p-5 rounded-2xl shadow-xl border border-slate-100 animate-float" style="animation-delay: 1.5s;">
                  <div class="text-sm font-bold text-slate-800 flex items-center gap-2">
                    <svg class="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    {hero_float_1}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 3. 费用原则说明 -->
      <section class="mx-auto max-w-[1200px] px-5 py-20">
        <div class="grid gap-10 md:grid-cols-2 items-center">
          <div>
            <h2 class="text-3xl font-bold text-slate-900 mb-6">{principle_title}</h2>
            <div class="prose prose-lg text-slate-600">
              <p>{principle_desc_1}</p>
              <p>{principle_desc_2}</p>
            </div>
          </div>
          
          <div class="bg-[#FFFBEB] border-2 border-[#FCD34D] rounded-3xl p-8 shadow-sm relative overflow-hidden">
            <div class="absolute top-0 right-0 w-32 h-32 bg-[#FDE68A] rounded-full blur-3xl opacity-50 -mr-10 -mt-10"></div>
            
            <div class="relative z-10">
              <div class="flex items-center gap-3 mb-6">
                <div class="w-12 h-12 bg-[#F59E0B] rounded-xl flex items-center justify-center text-white shrink-0 shadow-md">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                </div>
                <h3 class="text-2xl font-bold text-[#92400E]">{principle_risk_title}</h3>
              </div>
              
              <ul class="space-y-4 text-lg font-bold text-[#B45309]">
                <li class="flex items-center gap-3 bg-white/60 p-4 rounded-2xl">
                  <span class="w-8 h-8 rounded-full bg-[#FDE68A] flex items-center justify-center text-[#92400E] shrink-0">1</span>
                  {principle_risk_1}
                </li>
                <li class="flex items-center gap-3 bg-white/60 p-4 rounded-2xl">
                  <span class="w-8 h-8 rounded-full bg-[#FDE68A] flex items-center justify-center text-[#92400E] shrink-0">2</span>
                  {principle_risk_2}
                </li>
                <li class="flex items-center gap-3 bg-white/60 p-4 rounded-2xl">
                  <span class="w-8 h-8 rounded-full bg-[#FDE68A] flex items-center justify-center text-[#92400E] shrink-0">3</span>
                  {principle_risk_3}
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <!-- 4. 借款示例（重点） -->
      <section class="bg-white py-20 border-y border-slate-100">
        <div class="mx-auto max-w-[1200px] px-5">
          <div class="text-center max-w-2xl mx-auto mb-16">
            <h2 class="text-3xl font-bold text-slate-900">{ex_title}</h2>
            <p class="mt-4 text-slate-600">{ex_subtitle}</p>
          </div>
          
          <div class="grid gap-6 md:grid-cols-3">
            <!-- Example 1 -->
            <div class="bg-white rounded-3xl p-8 shadow-sm border border-slate-100 hover:shadow-xl hover:-translate-y-2 transition-all duration-300">
              <div class="inline-block bg-blue-100 text-blue-700 font-bold px-4 py-1.5 rounded-full text-sm mb-6">{ex_1_badge}</div>
              <div class="space-y-5">
                <div class="flex justify-between items-center pb-4 border-b border-slate-100">
                  <span class="text-slate-500">{ex_borrow}</span>
                  <span class="text-xl font-bold text-slate-900">$100</span>
                </div>
                <div class="flex justify-between items-center pb-4 border-b border-slate-100">
                  <span class="text-slate-500">{ex_fee}</span>
                  <span class="text-lg font-medium text-slate-700">$10</span>
                </div>
                <div class="flex justify-between items-center pb-4 border-b border-slate-100">
                  <span class="text-slate-500">{ex_receive}</span>
                  <span class="text-xl font-bold text-blue-600">$90</span>
                </div>
                <div class="flex justify-between items-center pb-4 border-b border-slate-100">
                  <span class="text-slate-500">{ex_duration}</span>
                  <span class="text-lg font-medium text-slate-700">{ex_1_duration}</span>
                </div>
                <div class="flex justify-between items-center pt-2">
                  <span class="font-bold text-slate-900">{ex_repay}</span>
                  <span class="text-3xl font-extrabold text-slate-900">$100</span>
                </div>
              </div>
            </div>
            
            <!-- Example 2 -->
            <div class="bg-white rounded-3xl p-8 shadow-sm border border-slate-100 hover:shadow-xl hover:-translate-y-2 transition-all duration-300 relative overflow-hidden">
              <div class="absolute top-0 right-0 w-2 h-full bg-blue-500"></div>
              <div class="inline-block bg-blue-100 text-blue-700 font-bold px-4 py-1.5 rounded-full text-sm mb-6">{ex_2_badge}</div>
              <div class="space-y-5">
                <div class="flex justify-between items-center pb-4 border-b border-slate-100">
                  <span class="text-slate-500">{ex_borrow}</span>
                  <span class="text-xl font-bold text-slate-900">$100</span>
                </div>
                <div class="flex justify-between items-center pb-4 border-b border-slate-100">
                  <span class="text-slate-500">{ex_fee}</span>
                  <span class="text-lg font-medium text-slate-700">$18</span>
                </div>
                <div class="flex justify-between items-center pb-4 border-b border-slate-100">
                  <span class="text-slate-500">{ex_receive}</span>
                  <span class="text-xl font-bold text-blue-600">$82</span>
                </div>
                <div class="flex justify-between items-center pb-4 border-b border-slate-100">
                  <span class="text-slate-500">{ex_duration}</span>
                  <span class="text-lg font-medium text-slate-700">{ex_2_duration}</span>
                </div>
                <div class="flex justify-between items-center pt-2">
                  <span class="font-bold text-slate-900">{ex_repay}</span>
                  <span class="text-3xl font-extrabold text-slate-900">$100</span>
                </div>
              </div>
            </div>
            
            <!-- Example 3 -->
            <div class="bg-white rounded-3xl p-8 shadow-sm border border-slate-100 hover:shadow-xl hover:-translate-y-2 transition-all duration-300">
              <div class="inline-block bg-blue-100 text-blue-700 font-bold px-4 py-1.5 rounded-full text-sm mb-6">{ex_3_badge}</div>
              <div class="space-y-5">
                <div class="flex justify-between items-center pb-4 border-b border-slate-100">
                  <span class="text-slate-500">{ex_borrow}</span>
                  <span class="text-xl font-bold text-slate-900">$100</span>
                </div>
                <div class="flex justify-between items-center pb-4 border-b border-slate-100">
                  <span class="text-slate-500">{ex_fee}</span>
                  <span class="text-lg font-medium text-slate-700">$30</span>
                </div>
                <div class="flex justify-between items-center pb-4 border-b border-slate-100">
                  <span class="text-slate-500">{ex_receive}</span>
                  <span class="text-xl font-bold text-blue-600">$70</span>
                </div>
                <div class="flex justify-between items-center pb-4 border-b border-slate-100">
                  <span class="text-slate-500">{ex_duration}</span>
                  <span class="text-lg font-medium text-slate-700">{ex_3_duration}</span>
                </div>
                <div class="flex justify-between items-center pt-2">
                  <span class="font-bold text-slate-900">{ex_repay}</span>
                  <span class="text-3xl font-extrabold text-slate-900">$100</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 5. 平息法解释模块 & 6. 不同期限费用表 -->
      <section class="mx-auto max-w-[1200px] px-5 py-20">
        <div class="grid gap-12 lg:grid-cols-5">
          <!-- 平息法解释 -->
          <div class="lg:col-span-2">
            <h2 class="text-2xl font-bold text-slate-900 mb-6">{math_title}</h2>
            <div class="bg-slate-900 text-white rounded-3xl p-8 shadow-xl">
              <p class="text-slate-300 mb-6">{math_desc}</p>
              
              <div class="bg-slate-800 rounded-2xl p-5 mb-8 border border-slate-700">
                <div class="text-sm text-slate-400 mb-2">{math_formula_label}</div>
                <div class="font-mono text-lg font-bold text-blue-400">{math_formula}</div>
              </div>
              
              <div class="space-y-4 font-mono text-sm">
                <div class="flex justify-between items-center">
                  <span class="text-slate-400">7 {math_days}:</span>
                  <span>100 × 10% = <span class="text-white font-bold">10</span></span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-slate-400">14 {math_days}:</span>
                  <span>100 × 18% = <span class="text-white font-bold">18</span></span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-slate-400">30 {math_days}:</span>
                  <span>100 × 30% = <span class="text-white font-bold">30</span></span>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 不同期限费用表 -->
          <div class="lg:col-span-3">
            <h2 class="text-2xl font-bold text-slate-900 mb-6">{table_title}</h2>
            <div class="bg-white rounded-3xl shadow-sm border border-slate-200 overflow-hidden">
              <div class="table-container overflow-x-auto">
                <table class="w-full text-left border-collapse min-w-[500px]">
                  <thead>
                    <tr class="bg-blue-50 border-b border-blue-100">
                      <th class="py-4 px-6 font-bold text-blue-900">{table_th_duration}</th>
                      <th class="py-4 px-6 font-bold text-blue-900">{table_th_fee}</th>
                      <th class="py-4 px-6 font-bold text-blue-900">{table_th_receive}</th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-slate-100">
                    <tr class="hover:bg-slate-50 transition-colors">
                      <td class="py-4 px-6 font-medium text-slate-900">7 {table_days}</td>
                      <td class="py-4 px-6 text-slate-600">8% - 12%</td>
                      <td class="py-4 px-6 font-medium text-blue-600">88% - 92%</td>
                    </tr>
                    <tr class="hover:bg-slate-50 transition-colors">
                      <td class="py-4 px-6 font-medium text-slate-900">14 {table_days}</td>
                      <td class="py-4 px-6 text-slate-600">15% - 20%</td>
                      <td class="py-4 px-6 font-medium text-blue-600">80% - 85%</td>
                    </tr>
                    <tr class="hover:bg-slate-50 transition-colors bg-blue-50/30">
                      <td class="py-4 px-6 font-medium text-slate-900">30 {table_days}</td>
                      <td class="py-4 px-6 text-slate-600">25% - 35%</td>
                      <td class="py-4 px-6 font-medium text-blue-600">65% - 75%</td>
                    </tr>
                    <tr class="hover:bg-slate-50 transition-colors text-slate-400">
                      <td class="py-4 px-6 font-medium">45 {table_days}</td>
                      <td class="py-4 px-6">{table_dynamic}</td>
                      <td class="py-4 px-6">{table_dynamic}</td>
                    </tr>
                    <tr class="hover:bg-slate-50 transition-colors text-slate-400">
                      <td class="py-4 px-6 font-medium">60 {table_days}</td>
                      <td class="py-4 px-6">{table_dynamic}</td>
                      <td class="py-4 px-6">{table_dynamic}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 7. 逾期规则 -->
      <section class="mx-auto max-w-[1200px] px-5 pb-20">
        <div class="bg-[#FEF2F2] border-2 border-[#FCA5A5] rounded-[2.5rem] p-8 md:p-12">
          <div class="flex flex-col md:flex-row gap-8 items-start">
            <div class="w-16 h-16 bg-[#EF4444] rounded-2xl flex items-center justify-center text-white shrink-0 shadow-lg">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
            </div>
            
            <div class="flex-1">
              <h2 class="text-3xl font-bold text-[#991B1B] mb-6">{overdue_title}</h2>
              
              <div class="grid gap-6 md:grid-cols-2">
                <div class="bg-white/80 backdrop-blur rounded-2xl p-6">
                  <h4 class="font-bold text-[#991B1B] mb-2 flex items-center gap-2">
                    <svg class="w-5 h-5 text-[#EF4444]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    {overdue_reminder_title}
                  </h4>
                  <p class="text-[#7F1D1D] text-sm">{overdue_reminder_desc}</p>
                </div>
                
                <div class="bg-white/80 backdrop-blur rounded-2xl p-6">
                  <h4 class="font-bold text-[#991B1B] mb-2 flex items-center gap-2">
                    <svg class="w-5 h-5 text-[#EF4444]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                    {overdue_severe_title}
                  </h4>
                  <p class="text-[#7F1D1D] text-sm">{overdue_severe_desc}</p>
                </div>
              </div>
              
              <div class="mt-6 bg-white/80 backdrop-blur rounded-2xl p-6">
                <h4 class="font-bold text-[#991B1B] mb-4">{overdue_conseq_title}</h4>
                <ul class="grid sm:grid-cols-3 gap-4">
                  <li class="flex items-center gap-2 text-[#7F1D1D] font-medium bg-[#FEE2E2] px-4 py-2 rounded-xl">
                    <div class="w-2 h-2 rounded-full bg-[#EF4444]"></div>
                    {overdue_conseq_1}
                  </li>
                  <li class="flex items-center gap-2 text-[#7F1D1D] font-medium bg-[#FEE2E2] px-4 py-2 rounded-xl">
                    <div class="w-2 h-2 rounded-full bg-[#EF4444]"></div>
                    {overdue_conseq_2}
                  </li>
                  <li class="flex items-center gap-2 text-[#7F1D1D] font-medium bg-[#FEE2E2] px-4 py-2 rounded-xl">
                    <div class="w-2 h-2 rounded-full bg-[#EF4444]"></div>
                    {overdue_conseq_3}
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 8. FAQ -->
      <section class="bg-white py-20 border-t border-slate-100">
        <div class="mx-auto max-w-[800px] px-5">
          <div class="text-center mb-12">
            <h2 class="text-3xl font-bold text-slate-900">FAQ</h2>
          </div>
          <div class="space-y-4">
            <details class="group rounded-3xl border border-slate-200 bg-white [&_summary::-webkit-details-marker]:hidden">
              <summary class="flex cursor-pointer items-center justify-between p-6 font-bold text-lg text-slate-900">
                {faq_1_q}
                <span class="transition group-open:rotate-180">
                  <svg fill="none" height="24" shape-rendering="geometricPrecision" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" viewBox="0 0 24 24" width="24"><path d="M6 9l6 6 6-6"></path></svg>
                </span>
              </summary>
              <div class="px-6 pb-6 text-slate-600">
                <p>{faq_1_a}</p>
              </div>
            </details>
            <details class="group rounded-3xl border border-slate-200 bg-white [&_summary::-webkit-details-marker]:hidden">
              <summary class="flex cursor-pointer items-center justify-between p-6 font-bold text-lg text-slate-900">
                {faq_2_q}
                <span class="transition group-open:rotate-180">
                  <svg fill="none" height="24" shape-rendering="geometricPrecision" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" viewBox="0 0 24 24" width="24"><path d="M6 9l6 6 6-6"></path></svg>
                </span>
              </summary>
              <div class="px-6 pb-6 text-slate-600">
                <p>{faq_2_a}</p>
              </div>
            </details>
            <details class="group rounded-3xl border border-slate-200 bg-white [&_summary::-webkit-details-marker]:hidden">
              <summary class="flex cursor-pointer items-center justify-between p-6 font-bold text-lg text-slate-900">
                {faq_3_q}
                <span class="transition group-open:rotate-180">
                  <svg fill="none" height="24" shape-rendering="geometricPrecision" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" viewBox="0 0 24 24" width="24"><path d="M6 9l6 6 6-6"></path></svg>
                </span>
              </summary>
              <div class="px-6 pb-6 text-slate-600">
                <p>{faq_3_a}</p>
              </div>
            </details>
            <details class="group rounded-3xl border border-slate-200 bg-white [&_summary::-webkit-details-marker]:hidden">
              <summary class="flex cursor-pointer items-center justify-between p-6 font-bold text-lg text-slate-900">
                {faq_4_q}
                <span class="transition group-open:rotate-180">
                  <svg fill="none" height="24" shape-rendering="geometricPrecision" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" viewBox="0 0 24 24" width="24"><path d="M6 9l6 6 6-6"></path></svg>
                </span>
              </summary>
              <div class="px-6 pb-6 text-slate-600">
                <p>{faq_4_a}</p>
              </div>
            </details>
          </div>
        </div>
      </section>

      <!-- 9. CTA 引导 -->
      <section class="mx-auto max-w-[1200px] px-5 py-24">
        <div class="bg-gradient-to-br from-[#0A5BFF] to-[#00AEEF] rounded-[3rem] p-10 md:p-16 text-center text-white shadow-2xl relative overflow-hidden">
          <div class="absolute top-0 right-0 -mt-20 -mr-20 w-64 h-64 bg-white opacity-10 rounded-full blur-3xl"></div>
          <div class="absolute bottom-0 left-0 -mb-20 -ml-20 w-64 h-64 bg-white opacity-10 rounded-full blur-3xl"></div>
          
          <div class="relative z-10 max-w-2xl mx-auto">
            <h2 class="text-3xl md:text-5xl font-bold mb-8">{cta_title}</h2>
            <div class="flex flex-col items-center justify-center gap-8">
              <div class="bg-white p-4 rounded-3xl shadow-lg inline-block">
                <img class="w-48 h-48 rounded-2xl" alt="KhmerX Mini App QR" src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https%3A%2F%2Ft.me%2FKhmerXBot%2Fapp" />
                <div class="text-slate-500 text-sm font-medium mt-3">Scan with Camera</div>
              </div>
              <a class="inline-flex justify-center items-center rounded-2xl bg-white px-10 py-5 text-xl font-bold text-blue-600 shadow-xl hover:shadow-2xl hover:scale-105 transition-all duration-300" href="https://t.me/KhmerXBot/app">
                <svg class="w-6 h-6 mr-3" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.74-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .38z"/></svg>
                {cta_btn}
              </a>
            </div>
          </div>
        </div>
      </section>

      <!-- 10. Footer -->
      <footer class="bg-slate-950 px-5 py-12 text-slate-400">
        <div class="mx-auto max-w-[1200px]">
          <div class="grid gap-8 md:grid-cols-4 border-b border-slate-800 pb-12">
            <div class="col-span-2">
              <a href="/{lang}" class="flex items-center gap-3 mb-6">
                <img src="/logo.jpg" alt="KhmerX Logo" class="h-8 w-8 rounded-lg object-cover grayscale opacity-80" />
                <div class="font-bold text-lg text-white">KhmerX</div>
              </a>
              <p class="text-sm leading-relaxed max-w-md">
                {footer_risk}
              </p>
            </div>
            <div>
              <h4 class="text-white font-bold mb-6">Links</h4>
              <ul class="space-y-4 text-sm">
                <li><a href="https://t.me/KhmerXBot" class="hover:text-white transition-colors">Telegram Support</a></li>
                <li><a href="mailto:support@khmerx.org" class="hover:text-white transition-colors">support@khmerx.org</a></li>
              </ul>
            </div>
            <div>
              <h4 class="text-white font-bold mb-6">Legal</h4>
              <ul class="space-y-4 text-sm">
                <li><a href="/{lang}/terms" class="hover:text-white transition-colors">User Agreement</a></li>
                <li><a href="/{lang}/privacy" class="hover:text-white transition-colors">Privacy Policy</a></li>
              </ul>
            </div>
          </div>
          <div class="flex flex-col md:flex-row items-center justify-between pt-8 gap-4 text-sm">
            <div>© <span data-year></span> KhmerX. All rights reserved.</div>
            <div class="flex gap-4">
              <a href="/km" class="hover:text-white transition-colors">ខ្មែរ</a>
              <a href="/en" class="hover:text-white transition-colors">English</a>
              <a href="/zh" class="hover:text-white transition-colors">中文</a>
            </div>
          </div>
        </div>
      </footer>
    </main>
  </body>
</html>"""

content_zh = {
    "lang": "zh",
    "title": "KhmerX 费用说明 | ABA 小额借款",
    "desc": "详细了解 KhmerX 的借款费用、利息计算和平息法模式。提前确认到账金额与还款金额，避免纠纷，透明借款。",
    "keywords": "ABA loan fees, Cambodia loan interest, Telegram loan fees, 柬埔寨借款利息, ABA 小额借款费用",
    "km_active": "", "en_active": "", "zh_active": "bg-white shadow-sm text-blue-600",
    "nav_borrow": "如何借款", "nav_fees": "费用说明", "nav_faq": "FAQ", "nav_contact": "联系我们", "nav_cta": "打开 Mini App",
    
    "hero_title": "费用与到账说明",
    "hero_subtitle": "请在借款前确认：<br/>实际到账金额与到期还款金额。",
    "hero_cta": "打开 Mini App",
    "hero_float_1": "透明无隐藏费用",
    
    "principle_title": "KhmerX 费用原则",
    "principle_desc_1": "KhmerX 使用 固定费用 + 平息法 模式。所有的借款费用将在借出时提前从本金中扣除，因此您实际到账的金额会少于申请的借款金额。",
    "principle_desc_2": "到期时，您只需按照申请的借款金额统一还款，无需再支付额外的利息。这种方式能让您在借款前就清楚地知道所有的成本。",
    "principle_risk_title": "借款前请务必确认",
    "principle_risk_1": "实际到账金额", "principle_risk_2": "到期还款金额", "principle_risk_3": "借款期限（天数）",
    
    "ex_title": "借款示例",
    "ex_subtitle": "用真实数字向您解释费用结构",
    "ex_1_badge": "示例 1（7天）", "ex_2_badge": "示例 2（14天）", "ex_3_badge": "示例 3（30天）",
    "ex_borrow": "借款金额", "ex_fee": "利息/服务费", "ex_receive": "实际到账", "ex_duration": "期限", "ex_repay": "到期还款",
    "ex_1_duration": "7天", "ex_2_duration": "14天", "ex_3_duration": "30天",
    
    "math_title": "如何计算费用（平息法）",
    "math_desc": "KhmerX 使用固定费用模式。例如：借款 $100，实际到账 $90，到期统一还款 $100。您无需担心复利。",
    "math_formula_label": "数学公式", "math_formula": "费用 = 借款金额 × 固定费率",
    "math_days": "天",
    
    "table_title": "不同期限费用表",
    "table_th_duration": "期限", "table_th_fee": "费用范围", "table_th_receive": "到账比例",
    "table_days": "天", "table_dynamic": "动态",
    
    "overdue_title": "逾期规则与后果",
    "overdue_reminder_title": "到期提醒", "overdue_reminder_desc": "系统会在到期前 24 小时发送提醒消息，请留意 Telegram 通知。",
    "overdue_severe_title": "严重逾期", "overdue_severe_desc": "严重逾期或恶意拖欠可能会被平台永久限制借款资格。",
    "overdue_conseq_title": "逾期可能导致：",
    "overdue_conseq_1": "可用额度降低", "overdue_conseq_2": "信用分大幅下降", "overdue_conseq_3": "限制发布借款需求",
    
    "faq_1_q": "为什么到账金额少于借款金额？", "faq_1_a": "KhmerX 采用平息法，借款利息和服务费会在放款时提前扣除。所以实际到账金额 = 借款金额 - 费用。到期时只需按借款本金还款即可。",
    "faq_2_q": "如何计算费用？", "faq_2_a": "系统会根据您选择的借款期限，按照固定费率计算。例如，借款100美元，期限7天（假设费率10%），费用就是 100 × 10% = 10美元。",
    "faq_3_q": "提前还款是否减少费用？", "faq_3_a": "由于采用固定费用模式，利息已在放款时扣除，提前还款不会退还已扣除的费用，但有助于提升您的信用记录和未来额度。",
    "faq_4_q": "逾期会怎样？", "faq_4_a": "逾期将导致您的信用评分下降，系统会自动降低您的可借额度，甚至限制您发布新的借款需求。借出方也有权通过合法途径追讨。",
    
    "cta_title": "确认费用后再开始借款",
    "cta_btn": "打开 Telegram Mini App",
    "footer_risk": "KhmerX 是本地小额周转信息服务平台，不保证借款成功，不提供担保。"
}

content_en = {
    "lang": "en",
    "title": "KhmerX Fees Explanation | ABA Micro Lending",
    "desc": "Understand KhmerX's borrowing fees, interest calculations, and flat-rate model. Confirm receive and repayment amounts in advance to avoid disputes.",
    "keywords": "ABA loan fees, Cambodia loan interest, Telegram loan fees, KhmerX interest, ABA micro lending cost",
    "km_active": "", "en_active": "bg-white shadow-sm text-blue-600", "zh_active": "",
    "nav_borrow": "How to Borrow", "nav_fees": "Fees", "nav_faq": "FAQ", "nav_contact": "Contact", "nav_cta": "Open Mini App",
    
    "hero_title": "Fees & Repayment Explanation",
    "hero_subtitle": "Please confirm before borrowing:<br/>Actual receive amount & Total repayment amount.",
    "hero_cta": "Open Mini App",
    "hero_float_1": "Transparent No Hidden Fees",
    
    "principle_title": "KhmerX Fee Principles",
    "principle_desc_1": "KhmerX uses a Flat-Rate Fee model. All borrowing costs are deducted from the principal amount upfront, which means the actual amount you receive will be less than the requested borrowing amount.",
    "principle_desc_2": "At maturity, you only need to repay the requested borrowing amount. No extra interest will be added. This ensures you know all costs clearly before borrowing.",
    "principle_risk_title": "Must Confirm Before Borrowing",
    "principle_risk_1": "Actual Receive Amount", "principle_risk_2": "Total Repayment Amount", "principle_risk_3": "Duration (Days)",
    
    "ex_title": "Borrowing Examples",
    "ex_subtitle": "Explaining the fee structure with real numbers",
    "ex_1_badge": "Example 1 (7 Days)", "ex_2_badge": "Example 2 (14 Days)", "ex_3_badge": "Example 3 (30 Days)",
    "ex_borrow": "Borrow Amount", "ex_fee": "Interest/Fee", "ex_receive": "Actual Receive", "ex_duration": "Duration", "ex_repay": "Total Repay",
    "ex_1_duration": "7 Days", "ex_2_duration": "14 Days", "ex_3_duration": "30 Days",
    
    "math_title": "How Fees are Calculated",
    "math_desc": "KhmerX uses a fixed fee model. For example: Borrow $100, receive $90, and repay $100 at maturity. You don't have to worry about compound interest.",
    "math_formula_label": "Mathematical Formula", "math_formula": "Fee = Borrow Amount × Fixed Rate",
    "math_days": "Days",
    
    "table_title": "Fees by Duration Table",
    "table_th_duration": "Duration", "table_th_fee": "Fee Range", "table_th_receive": "Receive Ratio",
    "table_days": "Days", "table_dynamic": "Dynamic",
    
    "overdue_title": "Overdue Rules & Consequences",
    "overdue_reminder_title": "Due Reminder", "overdue_reminder_desc": "The system will send a reminder 24 hours before the due date. Please check your Telegram.",
    "overdue_severe_title": "Severe Overdue", "overdue_severe_desc": "Severe or malicious overdue payments may result in a permanent ban from the platform.",
    "overdue_conseq_title": "Overdue may result in:",
    "overdue_conseq_1": "Lower credit limit", "overdue_conseq_2": "Huge credit score drop", "overdue_conseq_3": "Borrowing restricted",
    
    "faq_1_q": "Why is the received amount less than the borrowed amount?", "faq_1_a": "KhmerX uses a flat-rate model where interest and service fees are deducted upfront. Actual Receive = Borrow Amount - Fees. You simply repay the original borrow amount at maturity.",
    "faq_2_q": "How are the fees calculated?", "faq_2_a": "The system calculates fees based on a fixed rate for your chosen duration. For example, borrowing $100 for 7 days (assuming a 10% rate), the fee is 100 × 10% = $10.",
    "faq_3_q": "Does early repayment reduce the fee?", "faq_3_a": "Because we use a fixed fee model deducted upfront, early repayment will not refund the deducted fees. However, it will greatly improve your credit record and future limits.",
    "faq_4_q": "What happens if I'm overdue?", "faq_4_a": "Overdue payments will drop your credit score, automatically lower your borrowing limit, and may restrict you from publishing new requests. Lenders can also pursue debt collection.",
    
    "cta_title": "Confirm Fees Before Borrowing",
    "cta_btn": "Open Telegram Mini App",
    "footer_risk": "KhmerX is a local micro lending information service platform. We do not guarantee successful borrowing and provide no guarantees."
}

content_km = {
    "lang": "km",
    "title": "ការពន្យល់អំពីថ្លៃសេវា KhmerX | ការខ្ចីប្រាក់ ABA",
    "desc": "ស្វែងយល់លម្អិតអំពីថ្លៃសេវាខ្ចីប្រាក់របស់ KhmerX ការគណនាការប្រាក់។ បញ្ជាក់ចំនួនទឹកប្រាក់ទទួលបាន និងសងវិញជាមុនដើម្បីជៀសវាងជម្លោះ។",
    "keywords": "ABA loan fees, Cambodia loan interest, Telegram loan fees, ថ្លៃសេវាខ្ចីប្រាក់",
    "km_active": "bg-white shadow-sm text-blue-600", "en_active": "", "zh_active": "",
    "nav_borrow": "របៀបខ្ចីប្រាក់", "nav_fees": "ថ្លៃសេវា", "nav_faq": "សំណួរដែលសួរញឹកញាប់", "nav_contact": "ទំនាក់ទំនង", "nav_cta": "បើក Mini App",
    
    "hero_title": "ការប្រាក់ និងការទូទាត់",
    "hero_subtitle": "សូមបញ្ជាក់មុនពេលខ្ចី៖<br/>ចំនួនប្រាក់ទទួលបានជាក់ស្តែង និងចំនួនប្រាក់សងសរុប។",
    "hero_cta": "បើក Mini App",
    "hero_float_1": "តម្លាភាពគ្មានថ្លៃលាក់កំបាំង",
    
    "principle_title": "គោលការណ៍ថ្លៃសេវា KhmerX",
    "principle_desc_1": "KhmerX ប្រើម៉ូដែលថ្លៃសេវាថេរ។ រាល់ការចំណាយលើការខ្ចីប្រាក់ត្រូវបានកាត់ចេញពីប្រាក់ដើមជាមុន ដែលមានន័យថាចំនួនប្រាក់ដែលអ្នកទទួលបានជាក់ស្តែងនឹងតិចជាងចំនួនដែលបានស្នើសុំ។",
    "principle_desc_2": "នៅពេលដល់កំណត់ អ្នកគ្រាន់តែសងចំនួនប្រាក់ដែលបានស្នើសុំប៉ុណ្ណោះ។ គ្មានការប្រាក់បន្ថែមទេ។ នេះធានាថាអ្នកដឹងពីការចំណាយទាំងអស់យ៉ាងច្បាស់មុនពេលខ្ចី។",
    "principle_risk_title": "ត្រូវតែបញ្ជាក់មុនពេលខ្ចី",
    "principle_risk_1": "ចំនួនប្រាក់ទទួលបានជាក់ស្តែង", "principle_risk_2": "ចំនួនប្រាក់សងសរុប", "principle_risk_3": "រយៈពេល (ថ្ងៃ)",
    
    "ex_title": "ឧទាហរណ៍នៃការខ្ចីប្រាក់",
    "ex_subtitle": "ពន្យល់រចនាសម្ព័ន្ធថ្លៃសេវាជាមួយតួលេខពិត",
    "ex_1_badge": "ឧទាហរណ៍ 1 (7 ថ្ងៃ)", "ex_2_badge": "ឧទាហរណ៍ 2 (14 ថ្ងៃ)", "ex_3_badge": "ឧទាហរណ៍ 3 (30 ថ្ងៃ)",
    "ex_borrow": "ចំនួនប្រាក់ខ្ចី", "ex_fee": "ការប្រាក់/ថ្លៃសេវា", "ex_receive": "ទទួលបានជាក់ស្តែង", "ex_duration": "រយៈពេល", "ex_repay": "សងសរុប",
    "ex_1_duration": "7 ថ្ងៃ", "ex_2_duration": "14 ថ្ងៃ", "ex_3_duration": "30 ថ្ងៃ",
    
    "math_title": "របៀបគណនាថ្លៃសេវា",
    "math_desc": "KhmerX ប្រើម៉ូដែលថ្លៃសេវាថេរ។ ឧទាហរណ៍៖ ខ្ចី $100 ទទួលបាន $90 ហើយសង $100 នៅពេលដល់កំណត់។ អ្នកមិនបាច់បារម្ភពីការប្រាក់បន្តបន្ទាប់ទេ។",
    "math_formula_label": "រូបមន្តគណិតវិទ្យា", "math_formula": "ថ្លៃសេវា = ប្រាក់ខ្ចី × អត្រាថេរ",
    "math_days": "ថ្ងៃ",
    
    "table_title": "តារាងថ្លៃសេវាតាមរយៈពេល",
    "table_th_duration": "រយៈពេល", "table_th_fee": "ចន្លោះថ្លៃសេវា", "table_th_receive": "សមាមាត្រទទួលបាន",
    "table_days": "ថ្ងៃ", "table_dynamic": "ថាមវន្ត",
    
    "overdue_title": "ច្បាប់យឺតយ៉ាវ និងផលវិបាក",
    "overdue_reminder_title": "ការរំលឹកដល់កំណត់", "overdue_reminder_desc": "ប្រព័ន្ធនឹងផ្ញើការរំលឹក 24 ម៉ោងមុនថ្ងៃកំណត់។ សូមពិនិត្យ Telegram របស់អ្នក។",
    "overdue_severe_title": "យឺតយ៉ាវធ្ងន់ធ្ងរ", "overdue_severe_desc": "ការយឺតយ៉ាវធ្ងន់ធ្ងរ ឬមានចេតនាមិនសង អាចបណ្តាលឱ្យត្រូវហាមឃាត់ជាអចិន្ត្រៃយ៍ពីវេទិកា។",
    "overdue_conseq_title": "ការយឺតយ៉ាវអាចបណ្តាលឱ្យ៖",
    "overdue_conseq_1": "ថយចុះដែនកំណត់", "overdue_conseq_2": "ធ្លាក់ចុះពិន្ទុឥណទាន", "overdue_conseq_3": "រឹតបន្តឹងការខ្ចី",
    
    "faq_1_q": "ហេតុអ្វីបានជាប្រាក់ទទួលបានតិចជាងប្រាក់ខ្ចី?", "faq_1_a": "KhmerX ប្រើម៉ូដែលកាត់ទុកជាមុន ដែលការប្រាក់និងថ្លៃសេវាត្រូវបានកាត់ចេញមុនពេលផ្តល់ប្រាក់។ ទទួលបានជាក់ស្តែង = ប្រាក់ខ្ចី - ថ្លៃសេវា។ អ្នកគ្រាន់តែសងប្រាក់ដើមវិញនៅពេលដល់កំណត់។",
    "faq_2_q": "តើថ្លៃសេវាគណនាយ៉ាងដូចម្តេច?", "faq_2_a": "ប្រព័ន្ធគណនាថ្លៃសេវាផ្អែកលើអត្រាថេរសម្រាប់រយៈពេលដែលអ្នកជ្រើសរើស។ ឧទាហរណ៍ ខ្ចី $100 សម្រាប់ 7 ថ្ងៃ (ឧបមាថាអត្រា 10%) ថ្លៃសេវាគឺ 100 × 10% = $10។",
    "faq_3_q": "តើការសងមុនកាលកំណត់កាត់បន្ថយថ្លៃសេវាទេ?", "faq_3_a": "ដោយសារយើងប្រើម៉ូដែលថ្លៃសេវាថេរដែលកាត់ទុកជាមុន ការសងមុនកាលកំណត់នឹងមិនសងថ្លៃសេវាដែលបានកាត់រួចវិញទេ។ ទោះយ៉ាងណាក៏ដោយ វានឹងធ្វើឱ្យប្រវត្តិឥណទានរបស់អ្នកប្រសើរឡើងយ៉ាងខ្លាំង។",
    "faq_4_q": "តើមានអ្វីកើតឡើងប្រសិនបើខ្ញុំយឺតយ៉ាវ?", "faq_4_a": "ការបង់ប្រាក់យឺតយ៉ាវនឹងធ្វើឱ្យពិន្ទុឥណទានរបស់អ្នកធ្លាក់ចុះ បន្ថយដែនកំណត់របស់អ្នកដោយស្វ័យប្រវត្តិ និងអាចរឹតបន្តឹងអ្នកពីការបង្ហោះសំណើថ្មី។ អ្នកឱ្យខ្ចីក៏អាចទាមទារបំណុលផងដែរ។",
    
    "cta_title": "បញ្ជាក់ថ្លៃសេវាមុនពេលខ្ចី",
    "cta_btn": "បើក Telegram Mini App",
    "footer_risk": "KhmerX គឺជាវេទិកាសេវាព័ត៌មានខ្ចីប្រាក់តូចក្នុងស្រុក។ យើងមិនធានាថាការខ្ចីប្រាក់នឹងជោគជ័យទេ ហើយមិនផ្តល់ការធានាណាមួយឡើយ។"
}

with open(r'D:\projects\khmerx\frontend\website\zh\fees\index.html', 'w', encoding='utf-8') as f:
    f.write(template.format(**content_zh))

with open(r'D:\projects\khmerx\frontend\website\en\fees\index.html', 'w', encoding='utf-8') as f:
    f.write(template.format(**content_en))

with open(r'D:\projects\khmerx\frontend\website\km\fees\index.html', 'w', encoding='utf-8') as f:
    f.write(template.format(**content_km))

print("All fees index.html files updated successfully!")
