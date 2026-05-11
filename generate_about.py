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
    <meta property="og:url" content="https://khmerx.org/{lang}/about" />
    <meta property="og:image" content="https://khmerx.org/logo.jpg" />
    <meta name="twitter:card" content="summary" />
    <meta name="twitter:title" content="{title}" />
    <meta name="twitter:description" content="{desc}" />
    <link rel="canonical" href="https://khmerx.org/{lang}/about" />
    <link rel="alternate" href="https://khmerx.org/km/about" hreflang="km" />
    <link rel="alternate" href="https://khmerx.org/en/about" hreflang="en" />
    <link rel="alternate" href="https://khmerx.org/zh/about" hreflang="zh" />
    <link rel="alternate" href="https://khmerx.org/km/about" hreflang="x-default" />
    <script type="application/ld+json">
      {{
        "@context": "https://schema.org",
        "@type": "AboutPage",
        "name": "{title}",
        "description": "{desc}",
        "url": "https://khmerx.org/{lang}/about",
        "mainEntity": {{
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
            <a class="hover:text-blue-600 transition-colors" href="/{lang}/faq">FAQ</a>
            <a class="hover:text-blue-600 transition-colors" href="/{lang}/contact">{nav_contact}</a>
          </nav>
          <div class="flex items-center gap-4">
            <div class="hidden md:flex gap-1 text-sm bg-slate-100 p-1 rounded-xl">
              <a data-lang="km" class="rounded-lg px-3 py-1.5 transition-colors font-medium {km_active}" href="/km/about">ខ្មែរ</a>
              <a data-lang="en" class="rounded-lg px-3 py-1.5 transition-colors font-medium {en_active}" href="/en/about">EN</a>
              <a data-lang="zh" class="rounded-lg px-3 py-1.5 transition-colors font-medium {zh_active}" href="/zh/about">中文</a>
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
        <div class="absolute inset-0 bg-[url('https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=Cambodia%20Phnom%20Penh%20city%20modern%20finance%20technology%20blue%20tones%20abstract%20clean%20business%20style&image_size=landscape_16_9')] bg-cover bg-center opacity-30 mix-blend-overlay"></div>
        <div class="relative mx-auto max-w-[1200px] px-5 py-20 md:py-28">
          <div class="grid gap-12 md:grid-cols-2 md:items-center">
            <div class="max-w-xl z-10">
              <div class="mb-6 inline-flex rounded-full bg-blue-500/20 px-4 py-2 text-sm font-bold text-blue-300 border border-blue-500/30">
                <svg class="w-4 h-4 inline mr-2 -mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                KhmerX Story
              </div>
              <h1 class="text-4xl font-extrabold leading-tight tracking-tight md:text-5xl lg:text-6xl mb-6">
                {hero_title}
              </h1>
              <p class="text-lg leading-relaxed text-slate-300 md:text-xl font-medium">
                {hero_subtitle}
              </p>
            </div>
            
            <div class="relative z-10 flex justify-center md:justify-end">
              <div class="relative w-64 h-64 sm:w-80 sm:h-80 animate-float">
                <img src="https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=Telegram%20Mini%20App%20on%20Mobile%20Phone%20with%20ABA%20bank%20elements%20blue%20tones%20clean%20modern%20business&image_size=square" alt="KhmerX App" class="w-full h-full object-contain drop-shadow-2xl" />
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- KhmerX 是什么 -->
      <section class="mx-auto max-w-[1200px] px-5 py-20 -mt-10 relative z-20">
        <div class="bg-white rounded-3xl p-8 md:p-12 shadow-xl border border-slate-100 flex flex-col md:flex-row gap-10 items-center">
          <div class="flex-1">
            <h2 class="text-3xl font-bold text-slate-900 mb-6">{sec1_title}</h2>
            <p class="text-slate-600 text-lg mb-8 leading-relaxed">{sec1_desc}</p>
            
            <div class="flex flex-wrap gap-3 mb-8">
              <span class="bg-blue-50 text-blue-700 px-4 py-2 rounded-full font-bold text-sm">Telegram</span>
              <span class="bg-blue-50 text-blue-700 px-4 py-2 rounded-full font-bold text-sm">ABA</span>
              <span class="bg-blue-50 text-blue-700 px-4 py-2 rounded-full font-bold text-sm">Cambodia</span>
              <span class="bg-blue-50 text-blue-700 px-4 py-2 rounded-full font-bold text-sm">{sec1_tag4}</span>
              <span class="bg-blue-50 text-blue-700 px-4 py-2 rounded-full font-bold text-sm">{sec1_tag5}</span>
            </div>

            <div class="bg-slate-900 text-white p-6 rounded-2xl border border-slate-800">
              <h4 class="font-bold text-blue-400 mb-4">{sec1_platform_title}</h4>
              <ul class="space-y-3">
                <li class="flex items-center gap-3">
                  <svg class="w-5 h-5 text-blue-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                  {sec1_li1}
                </li>
                <li class="flex items-center gap-3">
                  <svg class="w-5 h-5 text-blue-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                  {sec1_li2}
                </li>
                <li class="flex items-center gap-3">
                  <svg class="w-5 h-5 text-blue-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                  {sec1_li3}
                </li>
              </ul>
            </div>
          </div>
          
          <div class="w-full md:w-1/3 flex flex-col gap-6">
            <!-- 为什么做 KhmerX -->
            <div class="bg-blue-600 text-white p-8 rounded-3xl shadow-lg relative overflow-hidden">
              <div class="absolute top-0 right-0 -mt-10 -mr-10 w-32 h-32 bg-white opacity-10 rounded-full blur-2xl"></div>
              <h3 class="text-2xl font-bold mb-4 relative z-10">{sec2_title}</h3>
              <p class="text-blue-100 mb-4 relative z-10">{sec2_desc1}</p>
              <p class="font-bold relative z-10">{sec2_desc2}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- KhmerX 如何工作 -->
      <section class="bg-white py-20 border-y border-slate-100">
        <div class="mx-auto max-w-[1200px] px-5">
          <div class="text-center mb-16">
            <h2 class="text-3xl font-bold text-slate-900">{sec3_title}</h2>
          </div>
          
          <div class="grid grid-cols-2 md:grid-cols-5 gap-4 relative">
            <div class="hidden md:block absolute top-1/2 left-10 right-10 h-0.5 bg-slate-100 -z-10 -translate-y-1/2"></div>
            
            <div class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm text-center relative z-10 group hover:-translate-y-2 transition-transform">
              <div class="w-12 h-12 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center font-bold text-xl mx-auto mb-4 group-hover:bg-blue-600 group-hover:text-white transition-colors">1</div>
              <h4 class="font-bold text-slate-900">{step1}</h4>
            </div>
            
            <div class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm text-center relative z-10 group hover:-translate-y-2 transition-transform">
              <div class="w-12 h-12 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center font-bold text-xl mx-auto mb-4 group-hover:bg-blue-600 group-hover:text-white transition-colors">2</div>
              <h4 class="font-bold text-slate-900">{step2}</h4>
            </div>
            
            <div class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm text-center relative z-10 group hover:-translate-y-2 transition-transform">
              <div class="w-12 h-12 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center font-bold text-xl mx-auto mb-4 group-hover:bg-blue-600 group-hover:text-white transition-colors">3</div>
              <h4 class="font-bold text-slate-900">{step3}</h4>
            </div>
            
            <div class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm text-center relative z-10 group hover:-translate-y-2 transition-transform">
              <div class="w-12 h-12 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center font-bold text-xl mx-auto mb-4 group-hover:bg-blue-600 group-hover:text-white transition-colors">4</div>
              <h4 class="font-bold text-slate-900">{step4}</h4>
            </div>
            
            <div class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm text-center relative z-10 group hover:-translate-y-2 transition-transform">
              <div class="w-12 h-12 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center font-bold text-xl mx-auto mb-4 group-hover:bg-blue-600 group-hover:text-white transition-colors">5</div>
              <h4 class="font-bold text-slate-900">{step5}</h4>
            </div>
          </div>
        </div>
      </section>

      <!-- 本地化与 Telegram & 安全与风控 -->
      <section class="mx-auto max-w-[1200px] px-5 py-20">
        <div class="grid md:grid-cols-2 gap-8">
          
          <div class="bg-white rounded-[2rem] p-8 md:p-12 border border-slate-200 shadow-sm">
            <div class="w-12 h-12 bg-blue-100 text-blue-600 rounded-xl flex items-center justify-center mb-6">
              <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.74-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .38z"/></svg>
            </div>
            <h3 class="text-2xl font-bold text-slate-900 mb-6">{sec4_title}</h3>
            <ul class="space-y-4">
              <li class="flex gap-4 items-start">
                <svg class="w-6 h-6 text-blue-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                <div>
                  <h4 class="font-bold text-slate-900">Telegram</h4>
                  <p class="text-slate-600 text-sm">{sec4_li1}</p>
                </div>
              </li>
              <li class="flex gap-4 items-start">
                <svg class="w-6 h-6 text-blue-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                <div>
                  <h4 class="font-bold text-slate-900">{sec4_li2_t}</h4>
                  <p class="text-slate-600 text-sm">{sec4_li2}</p>
                </div>
              </li>
              <li class="flex gap-4 items-start">
                <svg class="w-6 h-6 text-blue-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                <div>
                  <h4 class="font-bold text-slate-900">ABA</h4>
                  <p class="text-slate-600 text-sm">{sec4_li3}</p>
                </div>
              </li>
            </ul>
          </div>
          
          <div class="bg-white rounded-[2rem] p-8 md:p-12 border border-slate-200 shadow-sm">
            <div class="w-12 h-12 bg-indigo-100 text-indigo-600 rounded-xl flex items-center justify-center mb-6">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>
            </div>
            <h3 class="text-2xl font-bold text-slate-900 mb-6">{sec5_title}</h3>
            <div class="grid grid-cols-2 gap-4 mb-6">
              <div class="bg-slate-50 p-4 rounded-xl border border-slate-100 font-bold text-slate-700 text-sm text-center">{sec5_tag1}</div>
              <div class="bg-slate-50 p-4 rounded-xl border border-slate-100 font-bold text-slate-700 text-sm text-center">{sec5_tag2}</div>
              <div class="bg-slate-50 p-4 rounded-xl border border-slate-100 font-bold text-slate-700 text-sm text-center">{sec5_tag3}</div>
              <div class="bg-slate-50 p-4 rounded-xl border border-slate-100 font-bold text-slate-700 text-sm text-center">{sec5_tag4}</div>
            </div>
            <div class="bg-yellow-50 border border-yellow-200 rounded-xl p-4 text-sm text-yellow-800">
              ⚠️ <strong>{sec5_notice_title}</strong>: {sec5_notice}
            </div>
          </div>

        </div>
      </section>

      <!-- 平台原则 -->
      <section class="bg-slate-900 py-20 text-white">
        <div class="mx-auto max-w-[1200px] px-5">
          <div class="text-center mb-16">
            <h2 class="text-3xl font-bold">{sec6_title}</h2>
          </div>
          <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
            <div class="bg-slate-800 p-8 rounded-3xl border border-slate-700 text-center hover:bg-slate-750 transition-colors">
              <h4 class="font-bold text-xl text-blue-400 mb-2">{sec6_1}</h4>
            </div>
            <div class="bg-slate-800 p-8 rounded-3xl border border-slate-700 text-center hover:bg-slate-750 transition-colors">
              <h4 class="font-bold text-xl text-blue-400 mb-2">{sec6_2}</h4>
            </div>
            <div class="bg-slate-800 p-8 rounded-3xl border border-slate-700 text-center hover:bg-slate-750 transition-colors">
              <h4 class="font-bold text-xl text-blue-400 mb-2">{sec6_3}</h4>
            </div>
            <div class="bg-slate-800 p-8 rounded-3xl border border-slate-700 text-center hover:bg-slate-750 transition-colors">
              <h4 class="font-bold text-xl text-blue-400 mb-2">{sec6_4}</h4>
            </div>
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
              <p class="mt-4 opacity-80 text-sm max-w-md mx-auto">{contact_desc} <a href="https://t.me/KhmerXBot" class="underline font-bold">Contact Telegram</a></p>
            </div>
          </div>
        </div>
      </section>

      <!-- Footer -->
      <footer class="bg-slate-950 px-5 py-12 text-slate-400 mt-auto">
        <div class="mx-auto max-w-[1200px]">
          <div class="grid gap-8 md:grid-cols-4 border-b border-slate-800 pb-12">
            <div class="col-span-2">
              <a href="/{lang}" class="flex items-center gap-3 mb-6">
                <img src="/logo.jpg" alt="KhmerX Logo" class="h-8 w-8 rounded-lg object-cover grayscale opacity-80" />
                <div class="font-bold text-lg text-white">KhmerX</div>
              </a>
              <p class="text-sm leading-relaxed max-w-md">
                {footer_desc}
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
              <a href="/km/about" class="hover:text-white transition-colors">ខ្មែរ</a>
              <a href="/en/about" class="hover:text-white transition-colors">English</a>
              <a href="/zh/about" class="hover:text-white transition-colors">中文</a>
            </div>
          </div>
        </div>
      </footer>
    </main>
  </body>
</html>
"""

content_zh = {
    "lang": "zh",
    "zh_active": "bg-white shadow-sm text-blue-600",
    "en_active": "",
    "km_active": "",
    "title": "关于 KhmerX | Telegram ABA Cambodia",
    "desc": "KhmerX 是面向柬埔寨用户的小额周转信息服务平台。通过 Telegram Mini App 提供简单透明的本地化服务。",
    "keywords": "KhmerX, Cambodia Telegram, ABA Cambodia, Cambodia finance tools, KhmerX about",
    "nav_borrow": "如何借款", "nav_fees": "费用说明", "nav_contact": "联系我们", "nav_cta": "打开 Mini App",
    "hero_title": "关于 KhmerX",
    "hero_subtitle": "KhmerX 是面向柬埔寨用户的小额周转信息服务平台。",
    "sec1_title": "KhmerX 是什么？",
    "sec1_desc": "KhmerX 通过 Telegram Mini App，帮助用户完成小额短期周转。我们致力于连接需求，让资金流动更简单。",
    "sec1_tag4": "小额短期", "sec1_tag5": "本地化",
    "sec1_platform_title": "平台明确声明",
    "sec1_li1": "KhmerX 不是银行", "sec1_li2": "KhmerX 不吸收存款", "sec1_li3": "KhmerX 不保证收益",
    "sec2_title": "为什么做 KhmerX？",
    "sec2_desc1": "在柬埔寨，很多本地用户需要小额短期的周转资金，但传统的金融流程复杂、门槛高。",
    "sec2_desc2": "KhmerX 的目标：通过国民级的 Telegram 和 ABA，提供一个更简单、透明的本地化信息匹配体验。",
    "sec3_title": "KhmerX 如何工作？",
    "step1": "打开 Telegram", "step2": "绑定 ABA", "step3": "发布借款", "step4": "上传凭证", "step5": "完成还款",
    "sec4_title": "本地化与 Telegram",
    "sec4_li1": "KhmerX 主要通过 Telegram Mini App 提供服务，无需下载新 App。",
    "sec4_li2_t": "多语言", "sec4_li2": "系统全面支持高棉语、英文和中文。",
    "sec4_li3": "无缝支持本地最常用的 ABA 账户进行点对点转账。",
    "sec5_title": "安全与风控",
    "sec5_tag1": "额度限制", "sec5_tag2": "风险检测", "sec5_tag3": "信用记录", "sec5_tag4": "异常行为限制",
    "sec5_notice_title": "安全提醒", "sec5_notice": "请确认官方 Telegram 与二维码，谨防诈骗。",
    "sec6_title": "KhmerX 平台原则",
    "sec6_1": "透明费用", "sec6_2": "本地化体验", "sec6_3": "简单操作", "sec6_4": "风险提示",
    "cta_title": "立即打开 KhmerX Mini App", "cta_btn": "打开 Telegram",
    "contact_desc": "如需帮助，请通过 Telegram 联系 KhmerX。",
    "footer_desc": "KhmerX 是本地小额周转信息服务平台，不保证借款成功，不提供担保。"
}

content_en = {
    "lang": "en",
    "zh_active": "",
    "en_active": "bg-white shadow-sm text-blue-600",
    "km_active": "",
    "title": "About KhmerX | Telegram ABA Cambodia",
    "desc": "KhmerX is a micro-lending information platform for users in Cambodia. Simple, localized service via Telegram.",
    "keywords": "KhmerX, Cambodia Telegram, ABA Cambodia, Cambodia finance tools, KhmerX about",
    "nav_borrow": "How to Borrow", "nav_fees": "Fees", "nav_contact": "Contact", "nav_cta": "Open Mini App",
    "hero_title": "About KhmerX",
    "hero_subtitle": "KhmerX is a micro-lending information platform for users in Cambodia.",
    "sec1_title": "What is KhmerX?",
    "sec1_desc": "KhmerX helps users with short-term micro-loans via the Telegram Mini App. We aim to connect needs and make money flow simpler.",
    "sec1_tag4": "Micro & Short-term", "sec1_tag5": "Localized",
    "sec1_platform_title": "Platform Disclaimer",
    "sec1_li1": "KhmerX is NOT a bank", "sec1_li2": "KhmerX does NOT accept deposits", "sec1_li3": "KhmerX does NOT guarantee returns",
    "sec2_title": "Why we built KhmerX?",
    "sec2_desc1": "Many local users in Cambodia need short-term micro-loans, but traditional financial processes are complex with high barriers.",
    "sec2_desc2": "Our Goal: To provide a simpler, transparent, localized matching experience using Telegram and ABA.",
    "sec3_title": "How does KhmerX work?",
    "step1": "Open Telegram", "step2": "Bind ABA", "step3": "Post Request", "step4": "Upload Receipt", "step5": "Repay Loan",
    "sec4_title": "Localization & Telegram",
    "sec4_li1": "KhmerX is primarily provided via Telegram Mini App, no new app download required.",
    "sec4_li2_t": "Multi-language", "sec4_li2": "Fully supports Khmer, English, and Chinese.",
    "sec4_li3": "Seamlessly supports peer-to-peer transfers via ABA accounts.",
    "sec5_title": "Security & Risk Control",
    "sec5_tag1": "Limit Control", "sec5_tag2": "Risk Detection", "sec5_tag3": "Credit History", "sec5_tag4": "Anomaly Restriction",
    "sec5_notice_title": "Security Notice", "sec5_notice": "Please confirm official Telegram and QR codes to avoid scams.",
    "sec6_title": "Platform Principles",
    "sec6_1": "Transparent Fees", "sec6_2": "Localized Experience", "sec6_3": "Simple Operations", "sec6_4": "Clear Risk Notices",
    "cta_title": "Open KhmerX Mini App Now", "cta_btn": "Open Telegram",
    "contact_desc": "For assistance, please contact KhmerX via Telegram.",
    "footer_desc": "KhmerX is a local micro-lending information platform. It does not guarantee successful loans or provide guarantees."
}

content_km = {
    "lang": "km",
    "zh_active": "",
    "en_active": "",
    "km_active": "bg-white shadow-sm text-blue-600",
    "title": "អំពី KhmerX | Telegram ABA កម្ពុជា",
    "desc": "KhmerX គឺជាវេទិកាព័ត៌មានខ្ចីប្រាក់ខ្នាតតូចសម្រាប់អ្នកប្រើប្រាស់នៅកម្ពុជា។ ផ្តល់សេវាកម្មងាយស្រួលតាមរយៈ Telegram ។",
    "keywords": "KhmerX, Cambodia Telegram, ABA Cambodia, Cambodia finance tools, KhmerX about",
    "nav_borrow": "របៀបខ្ចីប្រាក់", "nav_fees": "ថ្លៃសេវា", "nav_contact": "ទំនាក់ទំនង", "nav_cta": "បើក Mini App",
    "hero_title": "អំពី KhmerX",
    "hero_subtitle": "KhmerX គឺជាវេទិកាព័ត៌មានខ្ចីប្រាក់ខ្នាតតូចសម្រាប់អ្នកប្រើប្រាស់នៅកម្ពុជា។",
    "sec1_title": "តើ KhmerX ជាអ្វី?",
    "sec1_desc": "KhmerX ជួយអ្នកប្រើប្រាស់ជាមួយនឹងការខ្ចីប្រាក់ខ្នាតតូចរយៈពេលខ្លីតាមរយៈ Telegram Mini App ។ យើងចង់ធ្វើឱ្យលំហូរប្រាក់កាន់តែងាយស្រួល។",
    "sec1_tag4": "ខ្នាតតូចនិងរយៈពេលខ្លី", "sec1_tag5": "ក្នុងស្រុក",
    "sec1_platform_title": "ការបដិសេធរបស់វេទិកា",
    "sec1_li1": "KhmerX មិនមែនជាធនាគារទេ", "sec1_li2": "KhmerX មិនទទួលប្រាក់បញ្ញើទេ", "sec1_li3": "KhmerX មិនធានាប្រាក់ចំណេញទេ",
    "sec2_title": "ហេតុអ្វីបានជាយើងបង្កើត KhmerX?",
    "sec2_desc1": "អ្នកប្រើប្រាស់ក្នុងស្រុកជាច្រើននៅកម្ពុជាត្រូវការប្រាក់កម្ចីខ្នាតតូចរយៈពេលខ្លី ប៉ុន្តែដំណើរការហិរញ្ញវត្ថុបែបប្រពៃណីមានភាពស្មុគស្មាញ។",
    "sec2_desc2": "គោលដៅរបស់យើង៖ ផ្តល់នូវបទពិសោធន៍ផ្គូផ្គងក្នុងស្រុកដែលងាយស្រួលនិងតម្លាភាព ដោយប្រើប្រាស់ Telegram និង ABA ។",
    "sec3_title": "តើ KhmerX ដំណើរការយ៉ាងដូចម្តេច?",
    "step1": "បើក Telegram", "step2": "ភ្ជាប់ ABA", "step3": "បង្ហោះសំណើ", "step4": "បញ្ចូលវិក័យប័ត្រ", "step5": "សងប្រាក់",
    "sec4_title": "ភាសាក្នុងស្រុក & Telegram",
    "sec4_li1": "KhmerX ផ្តល់ជូនជាចម្បងតាមរយៈ Telegram Mini App មិនចាំបាច់ទាញយកកម្មវិធីថ្មីទេ។",
    "sec4_li2_t": "ពហុភាសា", "sec4_li2": "គាំទ្រភាសាខ្មែរ អង់គ្លេស និងចិន។",
    "sec4_li3": "គាំទ្រការផ្ទេរប្រាក់ដោយផ្ទាល់តាមរយៈគណនី ABA យ៉ាងរលូន។",
    "sec5_title": "សុវត្ថិភាពនិងការគ្រប់គ្រងហានិភ័យ",
    "sec5_tag1": "ការគ្រប់គ្រងដែនកំណត់", "sec5_tag2": "ការរកឃើញហានិភ័យ", "sec5_tag3": "ប្រវត្តិឥណទាន", "sec5_tag4": "ការរឹតត្បិតភាពមិនប្រក្រតី",
    "sec5_notice_title": "សេចក្តីជូនដំណឹងសុវត្ថិភាព", "sec5_notice": "សូមបញ្ជាក់ Telegram និងកូដ QR ផ្លូវការដើម្បីចៀសវាងការបោកប្រាស់។",
    "sec6_title": "គោលការណ៍វេទិកា",
    "sec6_1": "ថ្លៃសេវាតម្លាភាព", "sec6_2": "បទពិសោធន៍ក្នុងស្រុក", "sec6_3": "ប្រតិបត្តិការងាយស្រួល", "sec6_4": "ការព្រមានហានិភ័យច្បាស់លាស់",
    "cta_title": "បើក KhmerX Mini App ឥឡូវនេះ", "cta_btn": "បើក Telegram",
    "contact_desc": "សម្រាប់ជំនួយ សូមទាក់ទង KhmerX តាមរយៈ Telegram ។",
    "footer_desc": "KhmerX គឺជាវេទិកាព័ត៌មានខ្ចីប្រាក់ខ្នាតតូចក្នុងស្រុក។ មិនធានាថាការខ្ចីប្រាក់នឹងទទួលបានជោគជ័យ ឬផ្តល់ការធានាឡើយ។"
}

import os

for c in [content_zh, content_en, content_km]:
    html = template.format(**c)
    lang = c['lang']
    os.makedirs(f"frontend/website/{lang}/about", exist_ok=True)
    with open(f"frontend/website/{lang}/about/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated {lang}/about/index.html")

