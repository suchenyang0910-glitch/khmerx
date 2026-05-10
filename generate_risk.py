import os

# --- Risk Page Template ---
risk_template = """<!doctype html>
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
    <meta property="og:url" content="https://khmerx.org/{lang}/risk" />
    <meta property="og:image" content="https://khmerx.org/logo.jpg" />
    <meta name="twitter:card" content="summary" />
    <meta name="twitter:title" content="{title}" />
    <meta name="twitter:description" content="{desc}" />
    <link rel="canonical" href="https://khmerx.org/{lang}/risk" />
    <link rel="alternate" href="https://khmerx.org/km/risk" hreflang="km" />
    <link rel="alternate" href="https://khmerx.org/en/risk" hreflang="en" />
    <link rel="alternate" href="https://khmerx.org/zh/risk" hreflang="zh" />
    <link rel="alternate" href="https://khmerx.org/km/risk" hreflang="x-default" />
    <script type="application/ld+json">
      {{
        "@context": "https://schema.org",
        "@type": "FinancialService",
        "name": "KhmerX",
        "description": "{desc}",
        "url": "https://khmerx.org/{lang}",
        "telephone": "",
        "email": "support@khmerx.org",
        "areaServed": "Cambodia",
        "knowsAbout": ["Micro Lending", "Peer-to-Peer Lending", "Risk Management"]
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
    </style>
  </head>
  <body>
    <script type="module" src="/src/site.ts"></script>
    <main class="min-h-screen bg-[#F5F7FA] pb-24 text-slate-900 font-sans">
      
      <!-- Header -->
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
            <a class="hover:text-blue-600 transition-colors" href="/{lang}/fees">{nav_fees}</a>
            <a class="hover:text-blue-600 transition-colors" href="/{lang}/faq">{nav_faq}</a>
            <a class="hover:text-blue-600 transition-colors" href="/{lang}/contact">{nav_contact}</a>
          </nav>
          <div class="flex items-center gap-4">
            <div class="hidden md:flex gap-1 text-sm bg-slate-100 p-1 rounded-xl">
              <a data-lang="km" class="rounded-lg px-3 py-1.5 transition-colors font-medium {km_active}" href="/km/risk">ខ្មែរ</a>
              <a data-lang="en" class="rounded-lg px-3 py-1.5 transition-colors font-medium {en_active}" href="/en/risk">EN</a>
              <a data-lang="zh" class="rounded-lg px-3 py-1.5 transition-colors font-medium {zh_active}" href="/zh/risk">中文</a>
            </div>
            <a class="hidden md:inline-flex rounded-xl bg-gradient-to-r from-[#0A5BFF] to-[#00AEEF] px-5 py-2.5 text-sm font-bold text-white shadow-md hover:shadow-lg hover:scale-105 transition-all" href="https://t.me/KhmerXBot/app">{nav_cta}</a>
            <button class="md:hidden p-2 text-slate-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
            </button>
          </div>
        </div>
      </header>

      <!-- Hero 区 -->
      <section class="relative bg-slate-900 border-b border-slate-800 overflow-hidden text-white">
        <div class="absolute inset-0 bg-[url('https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=Dark%20blue%20financial%20security%20shield%20network%20technology%20background%20abstract%20modern%20clean%20business%20style&image_size=landscape_16_9')] bg-cover bg-center opacity-30 mix-blend-overlay"></div>
        <div class="relative mx-auto max-w-[1200px] px-5 py-20 md:py-28">
          <div class="grid gap-12 md:grid-cols-2 md:items-center">
            <div class="max-w-xl z-10">
              <div class="mb-6 inline-flex rounded-full bg-blue-500/20 px-4 py-2 text-sm font-bold text-blue-300 border border-blue-500/30">
                <svg class="w-4 h-4 inline mr-2 -mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path></svg>
                KhmerX Safety & Rules
              </div>
              <h1 class="text-4xl font-extrabold leading-tight tracking-tight md:text-5xl lg:text-6xl mb-6">
                {hero_title}
              </h1>
              <p class="text-lg leading-relaxed text-slate-300 md:text-xl font-medium">
                {hero_subtitle}
              </p>
            </div>
            
            <div class="relative z-10 flex justify-center md:justify-end">
              <div class="relative w-48 h-48 sm:w-64 sm:h-64 animate-float">
                <div class="absolute inset-0 bg-blue-500 rounded-full blur-3xl opacity-40"></div>
                <svg class="relative w-full h-full text-blue-400 drop-shadow-2xl" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
                </svg>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- KhmerX 服务说明（官方定位） -->
      <section class="mx-auto max-w-[1200px] px-5 py-20 -mt-10 relative z-20">
        <div class="bg-white rounded-3xl p-8 md:p-12 shadow-xl border border-slate-100 flex flex-col md:flex-row gap-10 items-center">
          <div class="flex-1">
            <h2 class="text-2xl md:text-3xl font-bold text-slate-900 mb-4">{service_title}</h2>
            <p class="text-slate-600 text-lg mb-8 leading-relaxed">{service_desc}</p>
            
            <div class="grid sm:grid-cols-2 gap-4">
              <div class="bg-blue-50/50 p-4 rounded-xl border border-blue-100 flex items-start gap-3">
                <svg class="w-6 h-6 text-blue-500 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                <span class="font-bold text-blue-900">{service_not_bank}</span>
              </div>
              <div class="bg-blue-50/50 p-4 rounded-xl border border-blue-100 flex items-start gap-3">
                <svg class="w-6 h-6 text-blue-500 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                <span class="font-bold text-blue-900">{service_no_deposit}</span>
              </div>
              <div class="bg-blue-50/50 p-4 rounded-xl border border-blue-100 flex items-start gap-3">
                <svg class="w-6 h-6 text-blue-500 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                <span class="font-bold text-blue-900">{service_no_guarantee_profit}</span>
              </div>
              <div class="bg-blue-50/50 p-4 rounded-xl border border-blue-100 flex items-start gap-3">
                <svg class="w-6 h-6 text-blue-500 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                <span class="font-bold text-blue-900">{service_no_guarantee_borrow}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 用户风险提示 -->
      <section class="mx-auto max-w-[1200px] px-5 pb-20">
        <h2 class="text-3xl font-bold text-slate-900 mb-8 text-center">{user_risk_title}</h2>
        <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <div class="bg-[#FEF2F2] border border-[#FCA5A5] rounded-2xl p-6 relative hover:-translate-y-1 transition-transform">
            <div class="absolute top-0 right-0 bg-[#EF4444] text-white text-xs font-bold px-3 py-1 rounded-bl-2xl rounded-tr-2xl">Risk 1</div>
            <h4 class="font-bold text-[#991B1B] text-lg mb-3 mt-2">{risk_1_title}</h4>
            <p class="text-[#7F1D1D] text-sm">{risk_1_desc}</p>
          </div>
          <div class="bg-[#FEF2F2] border border-[#FCA5A5] rounded-2xl p-6 relative hover:-translate-y-1 transition-transform">
            <div class="absolute top-0 right-0 bg-[#EF4444] text-white text-xs font-bold px-3 py-1 rounded-bl-2xl rounded-tr-2xl">Risk 2</div>
            <h4 class="font-bold text-[#991B1B] text-lg mb-3 mt-2">{risk_2_title}</h4>
            <p class="text-[#7F1D1D] text-sm">{risk_2_desc}</p>
          </div>
          <div class="bg-[#FEF2F2] border border-[#FCA5A5] rounded-2xl p-6 relative hover:-translate-y-1 transition-transform">
            <div class="absolute top-0 right-0 bg-[#EF4444] text-white text-xs font-bold px-3 py-1 rounded-bl-2xl rounded-tr-2xl">Risk 3</div>
            <h4 class="font-bold text-[#991B1B] text-lg mb-3 mt-2">{risk_3_title}</h4>
            <p class="text-[#7F1D1D] text-sm">{risk_3_desc}</p>
          </div>
          <div class="bg-[#FEF2F2] border border-[#FCA5A5] rounded-2xl p-6 relative hover:-translate-y-1 transition-transform">
            <div class="absolute top-0 right-0 bg-[#EF4444] text-white text-xs font-bold px-3 py-1 rounded-bl-2xl rounded-tr-2xl">Risk 4</div>
            <h4 class="font-bold text-[#991B1B] text-lg mb-3 mt-2">{risk_4_title}</h4>
            <p class="text-[#7F1D1D] text-sm">{risk_4_desc}</p>
          </div>
        </div>
      </section>

      <!-- 借款风险与逾期说明 -->
      <section class="bg-white py-20 border-y border-slate-100">
        <div class="mx-auto max-w-[1200px] px-5">
          <div class="grid md:grid-cols-2 gap-12">
            
            <!-- 借款风险说明 -->
            <div>
              <div class="flex items-center gap-3 mb-6">
                <div class="w-10 h-10 rounded-xl bg-orange-100 text-orange-600 flex items-center justify-center">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                </div>
                <h3 class="text-2xl font-bold text-slate-900">{borrow_risk_title}</h3>
              </div>
              <div class="space-y-6">
                <div class="border-l-4 border-orange-400 pl-5">
                  <h4 class="font-bold text-slate-900 text-lg mb-2">{borrow_fee_title}</h4>
                  <p class="text-slate-600">{borrow_fee_desc}</p>
                </div>
                <div class="border-l-4 border-orange-400 pl-5">
                  <h4 class="font-bold text-slate-900 text-lg mb-2">{borrow_confirm_title}</h4>
                  <p class="text-slate-600 mb-2">{borrow_confirm_desc}</p>
                  <ul class="list-disc list-inside text-sm text-slate-500 ml-2 space-y-1">
                    <li>{borrow_confirm_1}</li>
                    <li>{borrow_confirm_2}</li>
                    <li>{borrow_confirm_3}</li>
                  </ul>
                </div>
                <div class="border-l-4 border-orange-400 pl-5">
                  <h4 class="font-bold text-slate-900 text-lg mb-2">{borrow_credit_title}</h4>
                  <p class="text-slate-600">{borrow_credit_desc}</p>
                </div>
              </div>
            </div>
            
            <!-- 逾期与信用说明 -->
            <div>
              <div class="flex items-center gap-3 mb-6">
                <div class="w-10 h-10 rounded-xl bg-red-100 text-red-600 flex items-center justify-center">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                </div>
                <h3 class="text-2xl font-bold text-slate-900">{overdue_title}</h3>
              </div>
              <div class="space-y-6">
                <div class="border-l-4 border-red-400 pl-5">
                  <h4 class="font-bold text-slate-900 text-lg mb-2">{overdue_remind_title}</h4>
                  <p class="text-slate-600">{overdue_remind_desc}</p>
                </div>
                <div class="border-l-4 border-red-400 pl-5">
                  <h4 class="font-bold text-slate-900 text-lg mb-2">{overdue_conseq_title}</h4>
                  <p class="text-slate-600 mb-2">{overdue_conseq_desc}</p>
                  <ul class="list-disc list-inside text-sm text-slate-500 ml-2 space-y-1">
                    <li>{overdue_conseq_1}</li>
                    <li>{overdue_conseq_2}</li>
                    <li>{overdue_conseq_3}</li>
                  </ul>
                </div>
                <div class="border-l-4 border-red-600 pl-5">
                  <h4 class="font-bold text-red-700 text-lg mb-2">{overdue_severe_title}</h4>
                  <p class="text-red-600 font-medium">{overdue_severe_desc}</p>
                </div>
              </div>
            </div>
            
          </div>
        </div>
      </section>

      <!-- 官方声明 (极重要) & 安全建议 -->
      <section class="mx-auto max-w-[1200px] px-5 py-20">
        <div class="grid md:grid-cols-2 gap-8">
          <!-- 官方声明 -->
          <div class="bg-slate-900 rounded-[2rem] p-8 md:p-12 text-white shadow-xl relative overflow-hidden">
            <div class="absolute -right-10 -top-10 text-white/5">
              <svg class="w-64 h-64" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>
            </div>
            <div class="relative z-10">
              <h2 class="text-3xl font-bold mb-6 flex items-center gap-3 text-blue-400">
                <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                {statement_title}
              </h2>
              <p class="text-lg text-slate-300 mb-8 font-medium">{statement_desc}</p>
              
              <div class="space-y-4 mb-8">
                <p class="text-slate-400 font-bold">{statement_not_guarantee}</p>
                <ul class="space-y-3">
                  <li class="flex items-center gap-3 text-slate-300">
                    <svg class="w-5 h-5 text-red-400 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                    {statement_ng_1}
                  </li>
                  <li class="flex items-center gap-3 text-slate-300">
                    <svg class="w-5 h-5 text-red-400 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                    {statement_ng_2}
                  </li>
                  <li class="flex items-center gap-3 text-slate-300">
                    <svg class="w-5 h-5 text-red-400 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                    {statement_ng_3}
                  </li>
                </ul>
              </div>
              
              <div class="bg-blue-900/50 border border-blue-800 p-4 rounded-xl text-blue-200 font-bold text-center">
                {statement_user_risk}
              </div>
            </div>
          </div>
          
          <!-- 安全建议 -->
          <div class="bg-white rounded-[2rem] p-8 md:p-12 border border-slate-200 shadow-sm flex flex-col justify-center">
            <h2 class="text-3xl font-bold text-slate-900 mb-8">{safety_title}</h2>
            <div class="space-y-6">
              <div class="flex gap-4 items-start">
                <div class="w-12 h-12 rounded-full bg-green-100 text-green-600 flex items-center justify-center shrink-0">
                  <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.74-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .38z"/></svg>
                </div>
                <div>
                  <h4 class="font-bold text-slate-900 text-lg mb-1">{safety_tg_title}</h4>
                  <p class="text-slate-600">{safety_tg_desc}</p>
                </div>
              </div>
              
              <div class="flex gap-4 items-start">
                <div class="w-12 h-12 rounded-full bg-red-100 text-red-600 flex items-center justify-center shrink-0">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636"></path></svg>
                </div>
                <div>
                  <h4 class="font-bold text-slate-900 text-lg mb-1">{safety_scam_title}</h4>
                  <p class="text-slate-600">{safety_scam_desc}</p>
                </div>
              </div>
              
              <div class="flex gap-4 items-start">
                <div class="w-12 h-12 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center shrink-0">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                </div>
                <div>
                  <h4 class="font-bold text-slate-900 text-lg mb-1">{safety_proof_title}</h4>
                  <p class="text-slate-600">{safety_proof_desc}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- FAQ -->
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

      <!-- CTA -->
      <section class="mx-auto max-w-[1200px] px-5 py-24">
        <div class="bg-gradient-to-br from-[#0A5BFF] to-[#00AEEF] rounded-[3rem] p-10 md:p-16 text-center text-white shadow-2xl relative overflow-hidden">
          <div class="absolute top-0 right-0 -mt-20 -mr-20 w-64 h-64 bg-white opacity-10 rounded-full blur-3xl"></div>
          <div class="absolute bottom-0 left-0 -mb-20 -ml-20 w-64 h-64 bg-white opacity-10 rounded-full blur-3xl"></div>
          
          <div class="relative z-10 max-w-2xl mx-auto">
            <h2 class="text-3xl md:text-4xl font-bold mb-8">{cta_title}</h2>
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

      <!-- Footer -->
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
    "title": "KhmerX 风险说明 | Telegram ABA 小额周转",
    "desc": "了解 KhmerX 的服务性质与借款风险。KhmerX 是信息平台而非银行，不保证借款成功，请在使用前确认所有交易风险。",
    "keywords": "Cambodia loan risk, ABA loan risk, Telegram finance safety, KhmerX 风险, 柬埔寨借款风险",
    "km_active": "", "en_active": "", "zh_active": "bg-white shadow-sm text-blue-600",
    "nav_borrow": "如何借款", "nav_fees": "费用说明", "nav_faq": "FAQ", "nav_contact": "联系我们", "nav_cta": "打开 Mini App",
    
    "hero_title": "风险与安全说明",
    "hero_subtitle": "请在使用 KhmerX 前，确认并理解相关风险与平台规则。",
    
    "service_title": "KhmerX 服务说明",
    "service_desc": "KhmerX 是面向柬埔寨用户的小额周转信息服务平台。用户可通过 Telegram Mini App 发布借款需求，并通过双方 ABA 账户转账完成交易。我们致力于提供透明、便捷的信息匹配服务。",
    "service_not_bank": "KhmerX 不是银行", "service_no_deposit": "KhmerX 不吸收存款",
    "service_no_guarantee_profit": "KhmerX 不保证收益", "service_no_guarantee_borrow": "KhmerX 不保证借款成功",
    
    "user_risk_title": "借款前必读的 4 大风险",
    "risk_1_title": "到账金额", "risk_1_desc": "由于预扣费用，请务必确认实际到账金额与到期还款金额的区别。",
    "risk_2_title": "借款期限", "risk_2_desc": "请确认借款期限与准确的到期时间，避免非预期的逾期。",
    "risk_3_title": "逾期后果", "risk_3_desc": "逾期可能导致您的平台额度下降、甚至被限制后续的借款请求。",
    "risk_4_title": "交易确认", "risk_4_desc": "请仔细核对并确认 ABA 转账信息，确保交易凭证的真实有效。",
    
    "borrow_risk_title": "借款风险说明",
    "borrow_fee_title": "借款费用", "borrow_fee_desc": "借款可能包含固定费用与服务费，将在放款时一次性扣除。",
    "borrow_confirm_title": "提前确认", "borrow_confirm_desc": "借款前请务必确认：",
    "borrow_confirm_1": "实际到账金额", "borrow_confirm_2": "到期还款金额", "borrow_confirm_3": "借款期限天数",
    "borrow_credit_title": "信用影响", "borrow_credit_desc": "您的还款记录将直接影响信用评级及未来的可用额度。",
    
    "overdue_title": "逾期与信用说明",
    "overdue_remind_title": "到期提醒", "overdue_remind_desc": "系统会在到期前 24 小时向您的 Telegram 发送还款提醒。",
    "overdue_conseq_title": "逾期后果", "overdue_conseq_desc": "逾期可能导致：",
    "overdue_conseq_1": "信用分下降", "overdue_conseq_2": "可借额度降低", "overdue_conseq_3": "限制发布新借款",
    "overdue_severe_title": "严重逾期", "overdue_severe_desc": "严重逾期或恶意拖欠可能被永久限制使用平台服务。",
    
    "statement_title": "KhmerX 官方严正声明",
    "statement_desc": "KhmerX 仅作为信息服务平台，为用户提供信息发布与匹配工具。所有资金交易均在用户双方的 ABA 账户间直接进行。",
    "statement_not_guarantee": "平台明确不保证以下事项：",
    "statement_ng_1": "借款需求一定会成功匹配", "statement_ng_2": "借出资金一定能获得收益", "statement_ng_3": "借出资金一定能按时收回",
    "statement_user_risk": "用户需自行承担并确认所有的交易风险。",
    
    "safety_title": "安全建议与防骗指南",
    "safety_tg_title": "官方 Telegram", "safety_tg_desc": "请务必确认您正在使用官方的 Telegram Bot 与小程序，不要轻信相似名称的仿冒账号。",
    "safety_scam_title": "防范诈骗", "safety_scam_desc": "KhmerX 官方客服绝对不会主动要求用户向私人账号或任何“安全账户”转账。",
    "safety_proof_title": "凭证保留", "safety_proof_desc": "请在完成每次 ABA 转账后，妥善保留转账记录与凭证截图，以便在产生争议时作为依据。",
    
    "faq_1_q": "KhmerX 是否保证借款？", "faq_1_a": "不保证。KhmerX 是信息匹配平台，借款能否成功取决于是否有借出方愿意接受您的需求。",
    "faq_2_q": "为什么到账金额不同？", "faq_2_a": "平台采用固定费用模式，利息和服务费在放款时已提前扣除，所以实际到账金额少于借款金额。",
    "faq_3_q": "逾期会怎样？", "faq_3_a": "逾期将降低您的信用评分和额度，严重者将无法再使用平台，借出方也有权依法追讨。",
    "faq_4_q": "KhmerX 是否是银行？", "faq_4_a": "不是。KhmerX 不吸收公众存款，也不发放自有资金，仅仅提供信息撮合服务。",
    
    "cta_title": "确认风险后再开始使用 KhmerX", "cta_btn": "打开 Telegram Mini App",
    "footer_risk": "KhmerX 是本地小额周转信息服务平台，不保证借款成功，不提供担保。"
}

content_en = {
    "lang": "en",
    "title": "KhmerX Risk Notice | Telegram ABA Micro Lending",
    "desc": "Understand the nature of KhmerX services and borrowing risks. KhmerX is an information platform, not a bank. Please confirm all transaction risks before use.",
    "keywords": "Cambodia loan risk, ABA loan risk, Telegram finance safety, KhmerX risk, Micro lending safety",
    "km_active": "", "en_active": "bg-white shadow-sm text-blue-600", "zh_active": "",
    "nav_borrow": "How to Borrow", "nav_fees": "Fees", "nav_faq": "FAQ", "nav_contact": "Contact", "nav_cta": "Open Mini App",
    
    "hero_title": "Risk & Safety Notice",
    "hero_subtitle": "Please confirm and understand the associated risks before using KhmerX.",
    
    "service_title": "KhmerX Service Description",
    "service_desc": "KhmerX is a micro lending information service platform for Cambodian users. Users can publish requests via Telegram Mini App and complete transactions through ABA transfers. We provide transparent information matching.",
    "service_not_bank": "KhmerX is NOT a bank", "service_no_deposit": "KhmerX does NOT accept deposits",
    "service_no_guarantee_profit": "KhmerX does NOT guarantee profits", "service_no_guarantee_borrow": "KhmerX does NOT guarantee loans",
    
    "user_risk_title": "4 Major Risks to Read Before Borrowing",
    "risk_1_title": "Receive Amount", "risk_1_desc": "Confirm the difference between the actual receive amount and repayment amount due to upfront fees.",
    "risk_2_title": "Duration", "risk_2_desc": "Confirm the exact duration and due date to avoid unexpected overdue status.",
    "risk_3_title": "Overdue Consequence", "risk_3_desc": "Overdue may lead to decreased limits and restrictions on future borrowing requests.",
    "risk_4_title": "Transaction Check", "risk_4_desc": "Carefully verify ABA transfer information and ensure the validity of receipts.",
    
    "borrow_risk_title": "Borrowing Risks",
    "borrow_fee_title": "Borrowing Fees", "borrow_fee_desc": "Loans may include fixed fees and service charges, deducted upfront at disbursement.",
    "borrow_confirm_title": "Confirm in Advance", "borrow_confirm_desc": "Please confirm before borrowing:",
    "borrow_confirm_1": "Actual receive amount", "borrow_confirm_2": "Total repayment amount", "borrow_confirm_3": "Borrowing duration",
    "borrow_credit_title": "Credit Impact", "borrow_credit_desc": "Your repayment history will directly affect your credit rating and future available limits.",
    
    "overdue_title": "Overdue & Credit Rules",
    "overdue_remind_title": "Due Reminder", "overdue_remind_desc": "The system will send a reminder to your Telegram 24 hours before the due date.",
    "overdue_conseq_title": "Overdue Consequences", "overdue_conseq_desc": "Overdue may result in:",
    "overdue_conseq_1": "Credit score drop", "overdue_conseq_2": "Lower borrowing limit", "overdue_conseq_3": "Restriction on new requests",
    "overdue_severe_title": "Severe Overdue", "overdue_severe_desc": "Severe or malicious overdue may result in permanent restriction from platform services.",
    
    "statement_title": "KhmerX Official Statement",
    "statement_desc": "KhmerX acts solely as an information service platform. All financial transactions occur directly between users' ABA accounts.",
    "statement_not_guarantee": "The platform explicitly DOES NOT guarantee:",
    "statement_ng_1": "Borrowing requests will be successfully matched", "statement_ng_2": "Lent funds will generate profit", "statement_ng_3": "Lent funds will be repaid on time",
    "statement_user_risk": "Users must bear and confirm all transaction risks themselves.",
    
    "safety_title": "Safety Advice & Anti-Scam Guide",
    "safety_tg_title": "Official Telegram", "safety_tg_desc": "Ensure you are using the official Telegram Bot and Mini App. Do not trust lookalike accounts.",
    "safety_scam_title": "Anti-Scam", "safety_scam_desc": "KhmerX official support will NEVER ask you to transfer money to private accounts.",
    "safety_proof_title": "Keep Proofs", "safety_proof_desc": "Retain ABA transfer records and receipt screenshots for every transaction as proof in case of disputes.",
    
    "faq_1_q": "Does KhmerX guarantee my loan will be funded?", "faq_1_a": "No. KhmerX is a matching platform. Funding depends on whether a lender accepts your request.",
    "faq_2_q": "Why is the received amount different?", "faq_2_a": "Fees are deducted upfront. The actual receive amount is the borrow amount minus fees.",
    "faq_3_q": "What happens if I'm overdue?", "faq_3_a": "Your credit score will drop, your limit will decrease, and you may be banned. Lenders can also pursue debt collection.",
    "faq_4_q": "Is KhmerX a bank?", "faq_4_a": "No. KhmerX does not accept deposits or lend its own money. We only provide an information matching service.",
    
    "cta_title": "Confirm Risks Before Using KhmerX", "cta_btn": "Open Telegram Mini App",
    "footer_risk": "KhmerX is a local micro lending information service platform. We do not guarantee successful borrowing and provide no guarantees."
}

content_km = {
    "lang": "km",
    "title": "ការជូនដំណឹងអំពីហានិភ័យ KhmerX | សុវត្ថិភាពការខ្ចីប្រាក់",
    "desc": "ស្វែងយល់ពីសេវាកម្មនិងហានិភ័យរបស់ KhmerX ។ យើងមិនមែនជាធនាគារទេ សូមបញ្ជាក់រាល់ហានិភ័យមុនពេលប្រើប្រាស់។",
    "keywords": "Cambodia loan risk, ABA loan risk, Telegram finance safety, ហានិភ័យ KhmerX",
    "km_active": "bg-white shadow-sm text-blue-600", "en_active": "", "zh_active": "",
    "nav_borrow": "របៀបខ្ចីប្រាក់", "nav_fees": "ថ្លៃសេវា", "nav_faq": "សំណួរដែលសួរញឹកញាប់", "nav_contact": "ទំនាក់ទំនង", "nav_cta": "បើក Mini App",
    
    "hero_title": "ការជូនដំណឹងអំពីហានិភ័យ",
    "hero_subtitle": "សូមបញ្ជាក់និងយល់ពីហានិភ័យពាក់ព័ន្ធមុនពេលប្រើប្រាស់ KhmerX ។",
    
    "service_title": "ការពិពណ៌នាសេវាកម្ម KhmerX",
    "service_desc": "KhmerX គឺជាវេទិកាសេវាព័ត៌មានខ្ចីប្រាក់តូច។ អ្នកប្រើប្រាស់អាចបង្ហោះសំណើតាម Telegram និងបញ្ចប់ប្រតិបត្តិការតាម ABA ។ យើងគ្រាន់តែជាវេទិកាផ្តល់ព័ត៌មានប៉ុណ្ណោះ។",
    "service_not_bank": "KhmerX មិនមែនជាធនាគារទេ", "service_no_deposit": "មិនទទួលប្រាក់បញ្ញើទេ",
    "service_no_guarantee_profit": "មិនធានាប្រាក់ចំណេញទេ", "service_no_guarantee_borrow": "មិនធានាការខ្ចីប្រាក់ទេ",
    
    "user_risk_title": "ហានិភ័យធំៗទាំង 4 ត្រូវអានមុនពេលខ្ចី",
    "risk_1_title": "ប្រាក់ទទួលបាន", "risk_1_desc": "បញ្ជាក់ភាពខុសគ្នារវាងប្រាក់ទទួលបានជាក់ស្តែង និងប្រាក់សងដោយសារការកាត់ថ្លៃសេវាមុន។",
    "risk_2_title": "រយៈពេល", "risk_2_desc": "បញ្ជាក់រយៈពេលនិងថ្ងៃកំណត់ដើម្បីជៀសវាងការយឺតយ៉ាវ។",
    "risk_3_title": "ការយឺតយ៉ាវ", "risk_3_desc": "ការយឺតយ៉ាវអាចបណ្តាលឱ្យធ្លាក់ចុះដែនកំណត់និងរឹតបន្តឹងការខ្ចី។",
    "risk_4_title": "ការបញ្ជាក់ប្រតិបត្តិការ", "risk_4_desc": "ផ្ទៀងផ្ទាត់ព័ត៌មាន ABA និងធានាសុពលភាពនៃវិក័យប័ត្រ។",
    
    "borrow_risk_title": "ហានិភ័យនៃការខ្ចីប្រាក់",
    "borrow_fee_title": "ថ្លៃសេវាខ្ចីប្រាក់", "borrow_fee_desc": "ប្រាក់កម្ចីរួមបញ្ចូលថ្លៃសេវាថេរ ដែលកាត់ចេញនៅពេលផ្តល់ប្រាក់។",
    "borrow_confirm_title": "បញ្ជាក់ជាមុន", "borrow_confirm_desc": "សូមបញ្ជាក់មុនពេលខ្ចី៖",
    "borrow_confirm_1": "ប្រាក់ទទួលបានជាក់ស្តែង", "borrow_confirm_2": "ចំនួនប្រាក់សងសរុប", "borrow_confirm_3": "រយៈពេលខ្ចីប្រាក់",
    "borrow_credit_title": "ផលប៉ះពាល់ឥណទាន", "borrow_credit_desc": "ប្រវត្តិសងប្រាក់របស់អ្នកប៉ះពាល់ផ្ទាល់ដល់ចំណាត់ថ្នាក់ឥណទានរបស់អ្នក។",
    
    "overdue_title": "ច្បាប់យឺតយ៉ាវ និងឥណទាន",
    "overdue_remind_title": "ការរំលឹកដល់កំណត់", "overdue_remind_desc": "ប្រព័ន្ធនឹងផ្ញើការរំលឹក 24 ម៉ោងមុនថ្ងៃកំណត់។",
    "overdue_conseq_title": "ផលវិបាកនៃការយឺតយ៉ាវ", "overdue_conseq_desc": "ការយឺតយ៉ាវអាចបណ្តាលឱ្យ៖",
    "overdue_conseq_1": "ធ្លាក់ចុះពិន្ទុឥណទាន", "overdue_conseq_2": "បន្ថយដែនកំណត់", "overdue_conseq_3": "រឹតបន្តឹងសំណើថ្មី",
    "overdue_severe_title": "យឺតយ៉ាវធ្ងន់ធ្ងរ", "overdue_severe_desc": "ការយឺតយ៉ាវធ្ងន់ធ្ងរអាចបណ្តាលឱ្យត្រូវហាមឃាត់ជាអចិន្ត្រៃយ៍ពីវេទិកា។",
    
    "statement_title": "សេចក្តីថ្លែងការណ៍ផ្លូវការរបស់ KhmerX",
    "statement_desc": "KhmerX ដើរតួជាវេទិកាព័ត៌មានប៉ុណ្ណោះ។ រាល់ប្រតិបត្តិការហិរញ្ញវត្ថុកើតឡើងដោយផ្ទាល់រវាងគណនី ABA របស់អ្នកប្រើប្រាស់។",
    "statement_not_guarantee": "វេទិកាមិនធានាដាច់ខាតនូវ៖",
    "statement_ng_1": "សំណើខ្ចីនឹងទទួលបានជោគជ័យ", "statement_ng_2": "ប្រាក់ឱ្យខ្ចីនឹងទទួលបានប្រាក់ចំណេញ", "statement_ng_3": "ប្រាក់ឱ្យខ្ចីនឹងត្រូវសងទាន់ពេល",
    "statement_user_risk": "អ្នកប្រើប្រាស់ត្រូវទទួលខុសត្រូវនិងបញ្ជាក់រាល់ហានិភ័យប្រតិបត្តិការដោយខ្លួនឯង។",
    
    "safety_title": "ដំបូន្មានសុវត្ថិភាព និងការប្រឆាំងការបោកប្រាស់",
    "safety_tg_title": "Telegram ផ្លូវការ", "safety_tg_desc": "ត្រូវប្រាកដថាអ្នកប្រើប្រាស់ Telegram ផ្លូវការ។ កុំជឿគណនីក្លែងក្លាយ។",
    "safety_scam_title": "ប្រឆាំងការបោកប្រាស់", "safety_scam_desc": "សេវាអតិថិជនផ្លូវការរបស់ KhmerX នឹងមិនស្នើសុំឱ្យអ្នកផ្ទេរប្រាក់ទៅគណនីឯកជនឡើយ។",
    "safety_proof_title": "រក្សាទុកភស្តុតាង", "safety_proof_desc": "រក្សាទុកកំណត់ត្រាផ្ទេរប្រាក់ ABA និងរូបថតអេក្រង់សម្រាប់រាល់ប្រតិបត្តិការ។",
    
    "faq_1_q": "តើ KhmerX ធានាថាការខ្ចីប្រាក់នឹងជោគជ័យទេ?", "faq_1_a": "ទេវាមិនធានាទេ។ វាអាស្រ័យលើថាតើមានអ្នកឱ្យខ្ចីព្រមទទួលសំណើរបស់អ្នកឬអត់។",
    "faq_2_q": "ហេតុអ្វីបានជាប្រាក់ទទួលបានខុសគ្នា?", "faq_2_a": "ថ្លៃសេវាត្រូវបានកាត់ជាមុន។ ប្រាក់ទទួលបានជាក់ស្តែង = ប្រាក់ខ្ចី - ថ្លៃសេវា។",
    "faq_3_q": "តើមានអ្វីកើតឡើងបើខ្ញុំយឺតយ៉ាវ?", "faq_3_a": "ពិន្ទុឥណទាននឹងធ្លាក់ចុះ ដែនកំណត់នឹងថយចុះ ហើយអ្នកអាចនឹងត្រូវហាមឃាត់។",
    "faq_4_q": "តើ KhmerX ជាធនាគារមែនទេ?", "faq_4_a": "ទេ យើងគ្រាន់តែជាវេទិកាផ្គូផ្គងព័ត៌មានប៉ុណ្ណោះ។",
    
    "cta_title": "បញ្ជាក់ហានិភ័យមុនពេលប្រើប្រាស់ KhmerX", "cta_btn": "បើក Telegram Mini App",
    "footer_risk": "KhmerX គឺជាវេទិកាសេវាព័ត៌មានខ្ចីប្រាក់តូចក្នុងស្រុក។ យើងមិនធានាថាការខ្ចីប្រាក់នឹងជោគជ័យទេ ហើយមិនផ្តល់ការធានាណាមួយឡើយ។"
}

with open(r'D:\projects\khmerx\frontend\website\zh\risk\index.html', 'w', encoding='utf-8') as f:
    f.write(risk_template.format(**content_zh))
with open(r'D:\projects\khmerx\frontend\website\en\risk\index.html', 'w', encoding='utf-8') as f:
    f.write(risk_template.format(**content_en))
with open(r'D:\projects\khmerx\frontend\website\km\risk\index.html', 'w', encoding='utf-8') as f:
    f.write(risk_template.format(**content_km))

print("Risk pages generated.")
