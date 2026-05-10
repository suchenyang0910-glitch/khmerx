import os

# --- Contact Page Template ---
contact_template = """<!doctype html>
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
    <meta property="og:url" content="https://khmerx.org/{lang}/contact" />
    <meta property="og:image" content="https://khmerx.org/logo.jpg" />
    <meta name="twitter:card" content="summary" />
    <meta name="twitter:title" content="{title}" />
    <meta name="twitter:description" content="{desc}" />
    <link rel="canonical" href="https://khmerx.org/{lang}/contact" />
    <link rel="alternate" href="https://khmerx.org/km/contact" hreflang="km" />
    <link rel="alternate" href="https://khmerx.org/en/contact" hreflang="en" />
    <link rel="alternate" href="https://khmerx.org/zh/contact" hreflang="zh" />
    <link rel="alternate" href="https://khmerx.org/km/contact" hreflang="x-default" />
    <script type="application/ld+json">
      {{
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "KhmerX",
        "url": "https://khmerx.org",
        "logo": "https://khmerx.org/logo.jpg",
        "sameAs": [
          "https://t.me/KhmerXBot"
        ],
        "contactPoint": {{
          "@type": "ContactPoint",
          "contactType": "customer support",
          "email": "support@khmerx.org"
        }}
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
            <a class="text-blue-600 transition-colors" href="/{lang}/contact">{nav_contact}</a>
          </nav>
          <div class="flex items-center gap-4">
            <div class="hidden md:flex gap-1 text-sm bg-slate-100 p-1 rounded-xl">
              <a data-lang="km" class="rounded-lg px-3 py-1.5 transition-colors font-medium {km_active}" href="/km/contact">ខ្មែរ</a>
              <a data-lang="en" class="rounded-lg px-3 py-1.5 transition-colors font-medium {en_active}" href="/en/contact">EN</a>
              <a data-lang="zh" class="rounded-lg px-3 py-1.5 transition-colors font-medium {zh_active}" href="/zh/contact">中文</a>
            </div>
            <a class="hidden md:inline-flex rounded-xl bg-gradient-to-r from-[#0A5BFF] to-[#00AEEF] px-5 py-2.5 text-sm font-bold text-white shadow-md hover:shadow-lg hover:scale-105 transition-all" href="https://t.me/KhmerXBot/app">{nav_cta}</a>
          </div>
        </div>
      </header>

      <!-- Hero 区 -->
      <section class="relative bg-white border-b border-slate-100 overflow-hidden">
        <div class="absolute inset-0 bg-gradient-to-b from-blue-50/50 to-white"></div>
        <div class="relative mx-auto max-w-[1200px] px-5 py-16 md:py-24">
          <div class="grid gap-12 md:grid-cols-2 md:items-center">
            <div class="max-w-xl z-10">
              <h1 class="text-4xl font-extrabold leading-tight tracking-tight text-slate-900 md:text-5xl lg:text-6xl mb-6">
                {hero_title}
              </h1>
              <p class="text-lg leading-relaxed text-slate-600 md:text-xl mb-10">
                {hero_subtitle}
              </p>
            </div>
            
            <div class="relative z-10 flex justify-center md:justify-end">
              <div class="relative w-[300px] sm:w-[340px] animate-float">
                <div class="absolute inset-0 bg-blue-500 rounded-[3rem] blur-3xl opacity-20 transform translate-y-10"></div>
                <img src="https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=Telegram%20customer%20support%20chat%20UI%20mockup%20blue%20white%20gradient%20background%20modern%20clean%20business%20style&image_size=portrait_9_16" alt="KhmerX Telegram Support" class="relative rounded-[2.5rem] shadow-2xl border-[6px] border-slate-800 object-cover w-full h-[500px] bg-slate-100" />
                
                <div class="absolute -bottom-6 -left-8 bg-white p-4 rounded-2xl shadow-xl border border-slate-100 flex items-center gap-3 animate-float" style="animation-delay: 1.5s;">
                  <div class="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center text-blue-600">
                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.74-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .38z"/></svg>
                  </div>
                  <div>
                    <div class="text-xs text-slate-500">Official Support</div>
                    <div class="font-bold text-slate-800">Online Now</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 联系方式卡片 -->
      <section class="mx-auto max-w-[1200px] px-5 py-20 -mt-10 relative z-20">
        <div class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          <!-- Card 1 -->
          <div class="bg-white rounded-3xl p-8 shadow-lg border border-slate-100 flex flex-col items-center text-center hover:-translate-y-2 transition-transform">
            <div class="w-16 h-16 bg-[#0088cc]/10 text-[#0088cc] rounded-2xl flex items-center justify-center mb-6">
              <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.74-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .38z"/></svg>
            </div>
            <h3 class="text-xl font-bold text-slate-900 mb-2">Telegram Mini App</h3>
            <p class="text-slate-500 mb-8 flex-1">{card_1_desc}</p>
            <a href="https://t.me/KhmerXBot/app" class="w-full inline-flex justify-center items-center rounded-xl bg-blue-600 px-6 py-3 font-bold text-white hover:bg-blue-700 transition-colors">
              {card_1_btn}
            </a>
          </div>
          
          <!-- Card 2 -->
          <div class="bg-white rounded-3xl p-8 shadow-lg border border-blue-200 ring-2 ring-blue-500/20 flex flex-col items-center text-center hover:-translate-y-2 transition-transform">
            <div class="absolute top-0 right-0 -mt-3 -mr-3 flex h-6 w-6">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-6 w-6 bg-blue-500"></span>
            </div>
            <div class="w-16 h-16 bg-blue-100 text-blue-600 rounded-2xl flex items-center justify-center mb-6">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"></path></svg>
            </div>
            <h3 class="text-xl font-bold text-slate-900 mb-2">{card_2_title}</h3>
            <p class="text-slate-500 mb-8 flex-1">{card_2_desc}</p>
            <a href="https://t.me/KhmerXBot" class="w-full inline-flex justify-center items-center rounded-xl bg-gradient-to-r from-blue-600 to-[#00AEEF] px-6 py-3 font-bold text-white shadow-md hover:shadow-lg transition-all">
              {card_2_btn}
            </a>
          </div>
          
          <!-- Card 3 -->
          <div class="bg-white rounded-3xl p-8 shadow-lg border border-slate-100 flex flex-col items-center text-center hover:-translate-y-2 transition-transform md:col-span-2 lg:col-span-1">
            <div class="w-16 h-16 bg-slate-100 text-slate-600 rounded-2xl flex items-center justify-center mb-6">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>
            </div>
            <h3 class="text-xl font-bold text-slate-900 mb-2">Email</h3>
            <p class="text-slate-500 mb-8 flex-1">{card_3_desc}</p>
            <a href="mailto:support@khmerx.org" class="w-full inline-flex justify-center items-center rounded-xl border-2 border-slate-200 px-6 py-3 font-bold text-slate-700 hover:border-slate-300 hover:bg-slate-50 transition-colors">
              support@khmerx.org
            </a>
          </div>
        </div>
      </section>

      <!-- 客服支持与工作时间 -->
      <section class="mx-auto max-w-[1200px] px-5 pb-20">
        <div class="grid gap-8 md:grid-cols-2">
          <!-- 支持范围 -->
          <div class="bg-white rounded-3xl p-8 border border-slate-200">
            <h3 class="text-2xl font-bold text-slate-900 mb-6">{support_title}</h3>
            <ul class="space-y-4 mb-8">
              <li class="flex items-center gap-3 text-slate-600">
                <svg class="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                {support_1}
              </li>
              <li class="flex items-center gap-3 text-slate-600">
                <svg class="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                {support_2}
              </li>
              <li class="flex items-center gap-3 text-slate-600">
                <svg class="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                {support_3}
              </li>
              <li class="flex items-center gap-3 text-slate-600">
                <svg class="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                {support_4}
              </li>
            </ul>
            <div class="text-sm text-slate-500 bg-slate-50 p-4 rounded-xl border border-slate-100">
              {support_tip}
            </div>
          </div>
          
          <!-- 工作时间 -->
          <div class="bg-slate-900 text-white rounded-3xl p-8 relative overflow-hidden">
            <div class="absolute top-0 right-0 w-32 h-32 bg-blue-500 rounded-full blur-3xl opacity-20 -mr-10 -mt-10"></div>
            <h3 class="text-2xl font-bold mb-8 relative z-10">{time_title}</h3>
            
            <div class="flex items-start gap-4 mb-8 relative z-10">
              <div class="w-12 h-12 rounded-full bg-blue-500/20 flex items-center justify-center text-blue-400 shrink-0">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
              </div>
              <div>
                <div class="text-lg font-bold">{time_days}</div>
                <div class="text-3xl font-extrabold text-blue-400 mt-1">09:00 - 21:00</div>
                <div class="text-slate-400 mt-1">(Cambodia Time)</div>
              </div>
            </div>
            
            <div class="bg-slate-800/50 p-4 rounded-xl border border-slate-700 text-sm text-slate-300 relative z-10">
              {time_tip}
            </div>
          </div>
        </div>
      </section>

      <!-- 安全与风险提醒（重点） -->
      <section class="mx-auto max-w-[1200px] px-5 pb-20">
        <div class="bg-[#FFFBEB] border-2 border-[#FDE68A] rounded-[2rem] p-8 md:p-12 shadow-sm">
          <div class="flex flex-col md:flex-row gap-6 items-start">
            <div class="w-16 h-16 bg-[#F59E0B] rounded-2xl flex items-center justify-center text-white shrink-0 shadow-lg">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
            </div>
            <div>
              <h2 class="text-2xl font-bold text-[#92400E] mb-4">{risk_title}</h2>
              <div class="space-y-4 text-[#B45309] font-medium text-lg">
                <p>{risk_1}</p>
                <p>{risk_2}</p>
                <div class="bg-[#FEF3C7] px-4 py-3 rounded-xl border border-[#FDE68A] inline-block mt-2">
                  <span class="font-bold text-[#92400E]">{risk_3}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- FAQ 快捷入口 -->
      <section class="mx-auto max-w-[800px] px-5 pb-20 text-center">
        <h3 class="text-2xl font-bold text-slate-900 mb-8">{faq_title}</h3>
        <div class="grid sm:grid-cols-2 gap-4 mb-8 text-left">
          <a href="/{lang}/faq" class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm hover:border-blue-400 hover:shadow-md transition-all flex items-center justify-between group">
            <span class="font-medium text-slate-700 group-hover:text-blue-600 transition-colors">{faq_1}</span>
            <svg class="w-5 h-5 text-slate-400 group-hover:text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
          </a>
          <a href="/{lang}/faq" class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm hover:border-blue-400 hover:shadow-md transition-all flex items-center justify-between group">
            <span class="font-medium text-slate-700 group-hover:text-blue-600 transition-colors">{faq_2}</span>
            <svg class="w-5 h-5 text-slate-400 group-hover:text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
          </a>
          <a href="/{lang}/faq" class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm hover:border-blue-400 hover:shadow-md transition-all flex items-center justify-between group">
            <span class="font-medium text-slate-700 group-hover:text-blue-600 transition-colors">{faq_3}</span>
            <svg class="w-5 h-5 text-slate-400 group-hover:text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
          </a>
          <a href="/{lang}/faq" class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm hover:border-blue-400 hover:shadow-md transition-all flex items-center justify-between group">
            <span class="font-medium text-slate-700 group-hover:text-blue-600 transition-colors">{faq_4}</span>
            <svg class="w-5 h-5 text-slate-400 group-hover:text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
          </a>
        </div>
        <a href="/{lang}/faq" class="inline-flex items-center text-blue-600 font-bold hover:text-blue-800 transition-colors">
          {faq_btn}
          <svg class="w-5 h-5 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path></svg>
        </a>
      </section>

      <!-- CTA 引导 -->
      <section class="mx-auto max-w-[1200px] px-5 pb-24">
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
    "title": "联系 KhmerX | Telegram 与 ABA 小额周转支持",
    "desc": "如需借款帮助、交易问题或风险咨询，请通过官方 Telegram 联系 KhmerX 客服。我们提供全天候的柬埔寨本地小额周转支持。",
    "keywords": "KhmerX contact, Telegram Cambodia, ABA support Cambodia, Telegram loan support, KhmerX 客服",
    "km_active": "", "en_active": "", "zh_active": "bg-white shadow-sm text-blue-600",
    "nav_borrow": "如何借款", "nav_fees": "费用说明", "nav_faq": "FAQ", "nav_contact": "联系我们", "nav_cta": "打开 Mini App",
    
    "hero_title": "联系 KhmerX",
    "hero_subtitle": "如需借款帮助、交易问题或风险咨询，请通过官方 Telegram 联系 KhmerX。",
    
    "card_1_desc": "通过 Telegram 快速发布需求、匹配借款。", "card_1_btn": "打开 Mini App",
    "card_2_title": "Telegram 客服", "card_2_desc": "获取借款与交易的官方人工帮助。", "card_2_btn": "联系 Telegram",
    "card_3_desc": "非紧急事务可通过邮件联系我们。",
    
    "support_title": "支持范围",
    "support_1": "借款问题", "support_2": "还款问题", "support_3": "ABA 转账问题", "support_4": "凭证上传问题",
    "support_tip": "提示：为了更快速地解决问题，请优先通过 Telegram 联系 KhmerX 客服。",
    
    "time_title": "工作时间", "time_days": "周一 - 周日",
    "time_tip": "非工作时间消息可能延迟回复，请您耐心等待。",
    
    "risk_title": "安全与风险提醒",
    "risk_1": "KhmerX 官方客服绝对不会通过私人 Telegram 账号主动要求您转账。",
    "risk_2": "请确认您正在与官方 Telegram 账号进行沟通。",
    "risk_3": "提醒：请勿向任何陌生人转账，保护您的资金安全！",
    
    "faq_title": "常见问题",
    "faq_1": "如何借款？", "faq_2": "如何还款？", "faq_3": "为什么到账金额不同？", "faq_4": "逾期会怎样？",
    "faq_btn": "查看完整 FAQ",
    
    "cta_title": "立即打开 Telegram Mini App", "cta_btn": "打开 Mini App",
    "footer_risk": "KhmerX 是本地小额周转信息服务平台，不保证借款成功，不提供担保。"
}

content_en = {
    "lang": "en",
    "title": "Contact KhmerX | Telegram & ABA Loan Support",
    "desc": "Contact KhmerX official Telegram support for borrowing help, transaction issues, or risk inquiries. We provide reliable micro lending support in Cambodia.",
    "keywords": "KhmerX contact, Telegram Cambodia, ABA support Cambodia, Telegram loan support, KhmerX support",
    "km_active": "", "en_active": "bg-white shadow-sm text-blue-600", "zh_active": "",
    "nav_borrow": "How to Borrow", "nav_fees": "Fees", "nav_faq": "FAQ", "nav_contact": "Contact", "nav_cta": "Open Mini App",
    
    "hero_title": "Contact KhmerX",
    "hero_subtitle": "For borrowing help, transaction issues, or risk inquiries, please contact KhmerX via official Telegram.",
    
    "card_1_desc": "Publish requests and borrow via Telegram quickly.", "card_1_btn": "Open Mini App",
    "card_2_title": "Telegram Support", "card_2_desc": "Get official human assistance for your borrowing needs.", "card_2_btn": "Contact Telegram",
    "card_3_desc": "For non-urgent business or partnership inquiries.",
    
    "support_title": "Support Scope",
    "support_1": "Borrowing Issues", "support_2": "Repayment Issues", "support_3": "ABA Transfer Issues", "support_4": "Proof Upload Issues",
    "support_tip": "Tip: For faster resolution, please prioritize contacting KhmerX via Telegram.",
    
    "time_title": "Working Hours", "time_days": "Mon - Sun",
    "time_tip": "Messages sent outside working hours may experience delayed responses. Thank you for your patience.",
    
    "risk_title": "Safety & Risk Warning",
    "risk_1": "KhmerX official support will NEVER proactively ask you to transfer money via private Telegram accounts.",
    "risk_2": "Please ensure you are communicating with the official Telegram account.",
    "risk_3": "Warning: Do not transfer money to strangers to protect your funds!",
    
    "faq_title": "Quick FAQ",
    "faq_1": "How to borrow?", "faq_2": "How to repay?", "faq_3": "Why is receive amount different?", "faq_4": "What if I'm overdue?",
    "faq_btn": "View Full FAQ",
    
    "cta_title": "Open Telegram Mini App Now", "cta_btn": "Open Mini App",
    "footer_risk": "KhmerX is a local micro lending information service platform. We do not guarantee successful borrowing and provide no guarantees."
}

content_km = {
    "lang": "km",
    "title": "ទាក់ទង KhmerX | ជំនួយការខ្ចីប្រាក់តាម Telegram និង ABA",
    "desc": "ទាក់ទងសេវាអតិថិជន Telegram ផ្លូវការរបស់ KhmerX សម្រាប់ជំនួយការខ្ចីប្រាក់ បញ្ហាប្រតិបត្តិការ ឬសំណួរហានិភ័យ។",
    "keywords": "KhmerX contact, Telegram Cambodia, ABA support Cambodia, សេវាអតិថិជន KhmerX",
    "km_active": "bg-white shadow-sm text-blue-600", "en_active": "", "zh_active": "",
    "nav_borrow": "របៀបខ្ចីប្រាក់", "nav_fees": "ថ្លៃសេវា", "nav_faq": "សំណួរដែលសួរញឹកញាប់", "nav_contact": "ទំនាក់ទំនង", "nav_cta": "បើក Mini App",
    
    "hero_title": "ទាក់ទង KhmerX",
    "hero_subtitle": "សម្រាប់ជំនួយការខ្ចីប្រាក់ បញ្ហាប្រតិបត្តិការ ឬការប្រឹក្សាហានិភ័យ សូមទាក់ទង KhmerX តាមរយៈ Telegram ផ្លូវការ។",
    
    "card_1_desc": "បង្ហោះសំណើនិងខ្ចីប្រាក់តាម Telegram យ៉ាងរហ័ស។", "card_1_btn": "បើក Mini App",
    "card_2_title": "សេវាអតិថិជន Telegram", "card_2_desc": "ទទួលបានជំនួយផ្លូវការសម្រាប់ការខ្ចីនិងប្រតិបត្តិការ។", "card_2_btn": "ទាក់ទង Telegram",
    "card_3_desc": "សម្រាប់បញ្ហាមិនបន្ទាន់ សូមទាក់ទងតាមអ៊ីមែល។",
    
    "support_title": "វិសាលភាពនៃការគាំទ្រ",
    "support_1": "បញ្ហាខ្ចីប្រាក់", "support_2": "បញ្ហាសងប្រាក់", "support_3": "បញ្ហាផ្ទេរប្រាក់ ABA", "support_4": "បញ្ហាបញ្ចូលភស្តុតាង",
    "support_tip": "ការណែនាំ៖ ដើម្បីដោះស្រាយបញ្ហាបានលឿន សូមទាក់ទង KhmerX តាមរយៈ Telegram ជាមុន។",
    
    "time_title": "ម៉ោងធ្វើការ", "time_days": "ច័ន្ទ - អាទិត្យ",
    "time_tip": "សារដែលផ្ញើក្រៅម៉ោងធ្វើការអាចនឹងមានការឆ្លើយតបយឺត។ សូមអរគុណចំពោះការអត់ធ្មត់របស់អ្នក។",
    
    "risk_title": "ការព្រមានសុវត្ថិភាព និងហានិភ័យ",
    "risk_1": "សេវាអតិថិជនផ្លូវការរបស់ KhmerX នឹងមិនស្នើសុំឱ្យអ្នកផ្ទេរប្រាក់តាមគណនី Telegram ឯកជនជាដាច់ខាត។",
    "risk_2": "សូមប្រាកដថាអ្នកកំពុងទាក់ទងជាមួយគណនី Telegram ផ្លូវការ។",
    "risk_3": "ការព្រមាន៖ កុំផ្ទេរប្រាក់ទៅជនចម្លែកដើម្បីការពារថវិការបស់អ្នក!",
    
    "faq_title": "សំណួរញឹកញាប់រហ័ស",
    "faq_1": "តើត្រូវខ្ចីប្រាក់យ៉ាងដូចម្តេច?", "faq_2": "តើត្រូវសងប្រាក់យ៉ាងដូចម្តេច?", "faq_3": "ហេតុអ្វីប្រាក់ទទួលបានខុសគ្នា?", "faq_4": "តើមានអ្វីកើតឡើងបើខ្ញុំយឺតយ៉ាវ?",
    "faq_btn": "មើលសំណួរញឹកញាប់ទាំងអស់",
    
    "cta_title": "បើក Telegram Mini App ឥឡូវនេះ", "cta_btn": "បើក Mini App",
    "footer_risk": "KhmerX គឺជាវេទិកាសេវាព័ត៌មានខ្ចីប្រាក់តូចក្នុងស្រុក។ យើងមិនធានាថាការខ្ចីប្រាក់នឹងជោគជ័យទេ ហើយមិនផ្តល់ការធានាណាមួយឡើយ។"
}

with open(r'D:\projects\khmerx\frontend\website\zh\contact\index.html', 'w', encoding='utf-8') as f:
    f.write(contact_template.format(**content_zh))
with open(r'D:\projects\khmerx\frontend\website\en\contact\index.html', 'w', encoding='utf-8') as f:
    f.write(contact_template.format(**content_en))
with open(r'D:\projects\khmerx\frontend\website\km\contact\index.html', 'w', encoding='utf-8') as f:
    f.write(contact_template.format(**content_km))

print("Contact pages generated.")
