import os

# --- FAQ Page Template ---
faq_template = """<!doctype html>
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
    <meta property="og:url" content="https://khmerx.org/{lang}/faq" />
    <meta property="og:image" content="https://khmerx.org/logo.jpg" />
    <meta name="twitter:card" content="summary" />
    <meta name="twitter:title" content="{title}" />
    <meta name="twitter:description" content="{desc}" />
    <link rel="canonical" href="https://khmerx.org/{lang}/faq" />
    <link rel="alternate" href="https://khmerx.org/km/faq" hreflang="km" />
    <link rel="alternate" href="https://khmerx.org/en/faq" hreflang="en" />
    <link rel="alternate" href="https://khmerx.org/zh/faq" hreflang="zh" />
    <link rel="alternate" href="https://khmerx.org/km/faq" hreflang="x-default" />
    <script type="application/ld+json">
      {{
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
          {{
            "@type": "Question",
            "name": "{q1_q}",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "{q1_a}"
            }}
          }},
          {{
            "@type": "Question",
            "name": "{q2_q}",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "{q2_a}"
            }}
          }},
          {{
            "@type": "Question",
            "name": "{q3_q}",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "{q3_a}"
            }}
          }},
          {{
            "@type": "Question",
            "name": "{q4_q}",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "{q4_a}"
            }}
          }},
          {{
            "@type": "Question",
            "name": "{q5_q}",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "{q5_a}"
            }}
          }},
          {{
            "@type": "Question",
            "name": "{q6_q}",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "{q6_a}"
            }}
          }},
          {{
            "@type": "Question",
            "name": "{q7_q}",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "{q7_a}"
            }}
          }},
          {{
            "@type": "Question",
            "name": "{q8_q}",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "{q8_a}"
            }}
          }},
          {{
            "@type": "Question",
            "name": "{q9_q}",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "{q9_a}"
            }}
          }},
          {{
            "@type": "Question",
            "name": "{q10_q}",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "{q10_a}"
            }}
          }},
          {{
            "@type": "Question",
            "name": "{q11_q}",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "{q11_a}"
            }}
          }}
        ]
      }}
    </script>
    <style>
      .faq-item summary::-webkit-details-marker {{
        display: none;
      }}
      html {{
        scroll-behavior: smooth;
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
            <a class="text-blue-600 transition-colors" href="/{lang}/faq">{nav_faq}</a>
            <a class="hover:text-blue-600 transition-colors" href="/{lang}/contact">{nav_contact}</a>
          </nav>
          <div class="flex items-center gap-4">
            <div class="hidden md:flex gap-1 text-sm bg-slate-100 p-1 rounded-xl">
              <a data-lang="km" class="rounded-lg px-3 py-1.5 transition-colors font-medium {km_active}" href="/km/faq">ខ្មែរ</a>
              <a data-lang="en" class="rounded-lg px-3 py-1.5 transition-colors font-medium {en_active}" href="/en/faq">EN</a>
              <a data-lang="zh" class="rounded-lg px-3 py-1.5 transition-colors font-medium {zh_active}" href="/zh/faq">中文</a>
            </div>
            <a class="hidden md:inline-flex rounded-xl bg-gradient-to-r from-[#0A5BFF] to-[#00AEEF] px-5 py-2.5 text-sm font-bold text-white shadow-md hover:shadow-lg hover:scale-105 transition-all" href="https://t.me/KhmerXBot/app">{nav_cta}</a>
          </div>
        </div>
      </header>

      <!-- Hero 区 -->
      <section class="relative bg-gradient-to-b from-blue-50 to-[#F5F7FA] pt-20 pb-12">
        <div class="mx-auto max-w-[800px] px-5 text-center">
          <h1 class="text-4xl md:text-5xl font-extrabold text-slate-900 mb-6">{hero_title}</h1>
          <p class="text-lg text-slate-600 mb-10">{hero_subtitle}</p>
          
          <!-- 搜索框 -->
          <div class="relative max-w-2xl mx-auto">
            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <svg class="w-6 h-6 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
            </div>
            <input type="text" id="faq-search" class="w-full pl-12 pr-4 py-4 rounded-[18px] border-2 border-slate-200 focus:border-blue-500 focus:ring-0 text-lg shadow-sm transition-colors outline-none" placeholder="{search_placeholder}" />
          </div>
        </div>
      </section>

      <!-- FAQ 分类导航 -->
      <section class="mx-auto max-w-[1000px] px-5 mb-12">
        <div class="flex flex-wrap justify-center gap-3">
          <a href="#cat-borrow" class="flex items-center gap-2 bg-white px-5 py-3 rounded-2xl shadow-sm border border-slate-200 hover:border-blue-500 hover:text-blue-600 transition-colors font-medium">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            {cat_borrow}
          </a>
          <a href="#cat-fees" class="flex items-center gap-2 bg-white px-5 py-3 rounded-2xl shadow-sm border border-slate-200 hover:border-blue-500 hover:text-blue-600 transition-colors font-medium">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
            {cat_fees}
          </a>
          <a href="#cat-repay" class="flex items-center gap-2 bg-white px-5 py-3 rounded-2xl shadow-sm border border-slate-200 hover:border-blue-500 hover:text-blue-600 transition-colors font-medium">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"></path></svg>
            {cat_repay}
          </a>
          <a href="#cat-credit" class="flex items-center gap-2 bg-white px-5 py-3 rounded-2xl shadow-sm border border-slate-200 hover:border-blue-500 hover:text-blue-600 transition-colors font-medium">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>
            {cat_credit}
          </a>
          <a href="#cat-tg" class="flex items-center gap-2 bg-white px-5 py-3 rounded-2xl shadow-sm border border-slate-200 hover:border-blue-500 hover:text-blue-600 transition-colors font-medium">
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.74-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .38z"/></svg>
            Telegram
          </a>
        </div>
      </section>

      <!-- FAQ 列表 -->
      <section class="mx-auto max-w-[800px] px-5 pb-20" id="faq-list">
        
        <div class="mb-12 faq-category" id="cat-borrow">
          <h2 class="text-2xl font-bold text-slate-900 mb-6 flex items-center gap-3">
            <svg class="w-6 h-6 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            {cat_borrow}
          </h2>
          <div class="space-y-4">
            <details class="faq-item group bg-white rounded-2xl border border-slate-200 overflow-hidden hover:border-blue-300 transition-colors">
              <summary class="flex items-center justify-between p-6 cursor-pointer font-bold text-lg text-slate-800 hover:bg-blue-50/50">
                <span class="faq-q">{q1_q}</span>
                <span class="text-blue-500 group-open:rotate-180 transition-transform"><svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <div class="px-6 pb-6 text-slate-600 leading-relaxed border-t border-slate-100 pt-4 faq-a">{q1_a}</div>
            </details>
            <details class="faq-item group bg-white rounded-2xl border border-slate-200 overflow-hidden hover:border-blue-300 transition-colors">
              <summary class="flex items-center justify-between p-6 cursor-pointer font-bold text-lg text-slate-800 hover:bg-blue-50/50">
                <span class="faq-q">{q2_q}</span>
                <span class="text-blue-500 group-open:rotate-180 transition-transform"><svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <div class="px-6 pb-6 text-slate-600 leading-relaxed border-t border-slate-100 pt-4 faq-a">{q2_a}</div>
            </details>
            <details class="faq-item group bg-white rounded-2xl border border-slate-200 overflow-hidden hover:border-blue-300 transition-colors">
              <summary class="flex items-center justify-between p-6 cursor-pointer font-bold text-lg text-slate-800 hover:bg-blue-50/50">
                <span class="faq-q">{q3_q}</span>
                <span class="text-blue-500 group-open:rotate-180 transition-transform"><svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <div class="px-6 pb-6 text-slate-600 leading-relaxed border-t border-slate-100 pt-4 faq-a">{q3_a}</div>
            </details>
          </div>
        </div>

        <div class="mb-12 faq-category" id="cat-fees">
          <h2 class="text-2xl font-bold text-slate-900 mb-6 flex items-center gap-3">
            <svg class="w-6 h-6 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
            {cat_fees}
          </h2>
          <div class="space-y-4">
            <details class="faq-item group bg-white rounded-2xl border border-slate-200 overflow-hidden hover:border-blue-300 transition-colors">
              <summary class="flex items-center justify-between p-6 cursor-pointer font-bold text-lg text-slate-800 hover:bg-blue-50/50">
                <span class="faq-q">{q4_q}</span>
                <span class="text-blue-500 group-open:rotate-180 transition-transform"><svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <div class="px-6 pb-6 text-slate-600 leading-relaxed border-t border-slate-100 pt-4 faq-a">{q4_a}</div>
            </details>
            <details class="faq-item group bg-white rounded-2xl border border-slate-200 overflow-hidden hover:border-blue-300 transition-colors">
              <summary class="flex items-center justify-between p-6 cursor-pointer font-bold text-lg text-slate-800 hover:bg-blue-50/50">
                <span class="faq-q">{q5_q}</span>
                <span class="text-blue-500 group-open:rotate-180 transition-transform"><svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <div class="px-6 pb-6 text-slate-600 leading-relaxed border-t border-slate-100 pt-4 faq-a">{q5_a}</div>
            </details>
          </div>
        </div>

        <div class="mb-12 faq-category" id="cat-repay">
          <h2 class="text-2xl font-bold text-slate-900 mb-6 flex items-center gap-3">
            <svg class="w-6 h-6 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"></path></svg>
            {cat_repay}
          </h2>
          <div class="space-y-4">
            <details class="faq-item group bg-white rounded-2xl border border-slate-200 overflow-hidden hover:border-blue-300 transition-colors">
              <summary class="flex items-center justify-between p-6 cursor-pointer font-bold text-lg text-slate-800 hover:bg-blue-50/50">
                <span class="faq-q">{q6_q}</span>
                <span class="text-blue-500 group-open:rotate-180 transition-transform"><svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <div class="px-6 pb-6 text-slate-600 leading-relaxed border-t border-slate-100 pt-4 faq-a">{q6_a}</div>
            </details>
            <details class="faq-item group bg-white rounded-2xl border border-slate-200 overflow-hidden hover:border-blue-300 transition-colors">
              <summary class="flex items-center justify-between p-6 cursor-pointer font-bold text-lg text-slate-800 hover:bg-blue-50/50">
                <span class="faq-q">{q7_q}</span>
                <span class="text-blue-500 group-open:rotate-180 transition-transform"><svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <div class="px-6 pb-6 text-slate-600 leading-relaxed border-t border-slate-100 pt-4 faq-a">{q7_a}</div>
            </details>
          </div>
        </div>

        <div class="mb-12 faq-category" id="cat-credit">
          <h2 class="text-2xl font-bold text-slate-900 mb-6 flex items-center gap-3">
            <svg class="w-6 h-6 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>
            {cat_credit}
          </h2>
          <div class="space-y-4">
            <details class="faq-item group bg-white rounded-2xl border border-slate-200 overflow-hidden hover:border-blue-300 transition-colors">
              <summary class="flex items-center justify-between p-6 cursor-pointer font-bold text-lg text-slate-800 hover:bg-blue-50/50">
                <span class="faq-q">{q8_q}</span>
                <span class="text-blue-500 group-open:rotate-180 transition-transform"><svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <div class="px-6 pb-6 text-slate-600 leading-relaxed border-t border-slate-100 pt-4 faq-a">{q8_a}</div>
            </details>
            <details class="faq-item group bg-white rounded-2xl border border-slate-200 overflow-hidden hover:border-blue-300 transition-colors">
              <summary class="flex items-center justify-between p-6 cursor-pointer font-bold text-lg text-slate-800 hover:bg-blue-50/50">
                <span class="faq-q">{q9_q}</span>
                <span class="text-blue-500 group-open:rotate-180 transition-transform"><svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <div class="px-6 pb-6 text-slate-600 leading-relaxed border-t border-slate-100 pt-4 faq-a">{q9_a}</div>
            </details>
          </div>
        </div>

        <div class="mb-12 faq-category" id="cat-tg">
          <h2 class="text-2xl font-bold text-slate-900 mb-6 flex items-center gap-3">
            <svg class="w-6 h-6 text-blue-500" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.74-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .38z"/></svg>
            Telegram
          </h2>
          <div class="space-y-4">
            <details class="faq-item group bg-white rounded-2xl border border-slate-200 overflow-hidden hover:border-blue-300 transition-colors">
              <summary class="flex items-center justify-between p-6 cursor-pointer font-bold text-lg text-slate-800 hover:bg-blue-50/50">
                <span class="faq-q">{q10_q}</span>
                <span class="text-blue-500 group-open:rotate-180 transition-transform"><svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <div class="px-6 pb-6 text-slate-600 leading-relaxed border-t border-slate-100 pt-4 faq-a">{q10_a}</div>
            </details>
            <details class="faq-item group bg-white rounded-2xl border border-slate-200 overflow-hidden hover:border-blue-300 transition-colors">
              <summary class="flex items-center justify-between p-6 cursor-pointer font-bold text-lg text-slate-800 hover:bg-blue-50/50">
                <span class="faq-q">{q11_q}</span>
                <span class="text-blue-500 group-open:rotate-180 transition-transform"><svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <div class="px-6 pb-6 text-slate-600 leading-relaxed border-t border-slate-100 pt-4 faq-a">{q11_a}</div>
            </details>
          </div>
        </div>

        <div id="faq-empty" class="hidden text-center py-12">
          <svg class="w-16 h-16 text-slate-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
          <h3 class="text-xl font-bold text-slate-700 mb-2">{empty_title}</h3>
          <p class="text-slate-500">{empty_desc}</p>
        </div>
      </section>

      <!-- 风险与规则说明 -->
      <section class="mx-auto max-w-[800px] px-5 pb-12">
        <div class="bg-[#FFFBEB] border-2 border-[#FDE68A] rounded-2xl p-6 md:p-8 flex gap-4 items-start">
          <svg class="w-8 h-8 text-[#F59E0B] shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
          <div>
            <h4 class="font-bold text-[#92400E] text-lg mb-2">{risk_title}</h4>
            <p class="text-[#B45309] mb-4">{risk_desc}</p>
            <ul class="list-disc list-inside text-[#B45309] font-medium space-y-1">
              <li>{risk_1}</li>
              <li>{risk_2}</li>
              <li>{risk_3}</li>
            </ul>
          </div>
        </div>
      </section>

      <!-- 联系客服 -->
      <section class="mx-auto max-w-[800px] px-5 pb-20">
        <div class="bg-white rounded-3xl p-8 border border-slate-200 text-center shadow-sm">
          <h3 class="text-2xl font-bold text-slate-900 mb-3">{contact_title}</h3>
          <p class="text-slate-500 mb-6">{contact_desc}</p>
          <a class="inline-flex items-center justify-center rounded-xl border-2 border-blue-600 bg-white px-8 py-3 text-lg font-bold text-blue-600 hover:bg-blue-50 transition-colors" href="https://t.me/KhmerXBot">
            <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.74-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .38z"/></svg>
            {contact_btn}
          </a>
        </div>
      </section>

      <!-- CTA -->
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
    <script>
      // FAQ Search Logic
      const searchInput = document.getElementById('faq-search');
      const faqItems = document.querySelectorAll('.faq-item');
      const faqCategories = document.querySelectorAll('.faq-category');
      const emptyState = document.getElementById('faq-empty');

      if(searchInput) {{
        searchInput.addEventListener('input', (e) => {{
          const term = e.target.value.toLowerCase();
          let hasVisible = false;

          faqItems.forEach(item => {{
            const q = item.querySelector('.faq-q').textContent.toLowerCase();
            const a = item.querySelector('.faq-a').textContent.toLowerCase();
            
            if(q.includes(term) || a.includes(term)) {{
              item.style.display = 'block';
              if(term) item.setAttribute('open', '');
              else item.removeAttribute('open');
              hasVisible = true;
            }} else {{
              item.style.display = 'none';
            }}
          }});

          // Hide empty categories
          faqCategories.forEach(cat => {{
            const visibleItems = cat.querySelectorAll('.faq-item[style="display: block;"], .faq-item:not([style])');
            if(visibleItems.length === 0 && term) {{
              cat.style.display = 'none';
            }} else {{
              cat.style.display = 'block';
            }}
          }});

          if(!hasVisible && term) {{
            emptyState.classList.remove('hidden');
          }} else {{
            emptyState.classList.add('hidden');
          }}
        }});
      }}
    </script>
  </body>
</html>"""

content_zh = {
    "lang": "zh",
    "title": "KhmerX FAQ | ABA 小额周转常见问题",
    "desc": "查找关于 KhmerX 借款、还款、费用、额度与安全的常见问题解答。KhmerX 是面向柬埔寨的 Telegram + ABA 小额周转平台。",
    "keywords": "KhmerX FAQ, ABA loan FAQ, Cambodia loan FAQ, Telegram loan FAQ, 柬埔寨借款 FAQ",
    "km_active": "", "en_active": "", "zh_active": "bg-white shadow-sm text-blue-600",
    "nav_borrow": "如何借款", "nav_fees": "费用说明", "nav_faq": "FAQ", "nav_contact": "联系我们", "nav_cta": "打开 Mini App",
    
    "hero_title": "常见问题",
    "hero_subtitle": "了解 KhmerX 的借款、还款、费用与风险规则。",
    "search_placeholder": "搜索问题...",
    
    "cat_borrow": "借款", "cat_fees": "费用", "cat_repay": "还款", "cat_credit": "信用",
    
    "q1_q": "KhmerX 是什么？", "q1_a": "KhmerX 是面向柬埔寨用户的小额周转信息服务平台，用户可通过 Telegram Mini App 发布借款需求，并使用 ABA 转账完成交易。",
    "q2_q": "如何开始借款？", "q2_a": "打开 Telegram Mini App，绑定 ABA 信息后即可申请借款。",
    "q3_q": "新用户可以借多少钱？", "q3_a": "新用户通常从小额度开始，完成按时还款后可逐步提高额度。",
    "q4_q": "为什么到账金额少于借款金额？", "q4_a": "KhmerX 使用固定费用模式，借款时会提前扣除部分费用。请在借款前确认到账金额与还款金额。",
    "q5_q": "如何计算费用？", "q5_a": "费用会根据借款金额与期限自动计算，系统会在借款前展示具体金额。",
    "q6_q": "如何还款？", "q6_a": "通过 ABA 完成转账后，在 Mini App 上传还款凭证即可。",
    "q7_q": "什么时候提醒还款？", "q7_a": "系统会在到期前24小时发送提醒。",
    "q8_q": "如何提高额度？", "q8_a": "按时还款、保持良好信用记录，系统会动态提升额度。",
    "q9_q": "逾期会怎样？", "q9_a": "逾期可能导致：信用下降、额度降低、限制借款，严重情况下永久限制。",
    "q10_q": "KhmerX 是否支持 Telegram？", "q10_a": "KhmerX 主要通过 Telegram Mini App 提供服务。",
    "q11_q": "如何打开 Mini App？", "q11_a": "通过 Telegram Bot 即可进入 Mini App。",
    
    "empty_title": "没有找到相关问题", "empty_desc": "尝试更换搜索词，或直接联系客服",
    
    "risk_title": "规则与风险说明",
    "risk_desc": "KhmerX 不保证借款成功，用户需自行确认交易风险。请在借款前确认：",
    "risk_1": "到账金额", "risk_2": "到期还款金额", "risk_3": "借款期限",
    
    "contact_title": "没有找到答案？", "contact_desc": "我们的客服团队随时准备为您提供帮助。", "contact_btn": "联系 Telegram 客服",
    "cta_title": "立即开始使用 KhmerX", "cta_btn": "打开 Telegram Mini App",
    "footer_risk": "KhmerX 是本地小额周转信息服务平台，不保证借款成功，不提供担保。"
}

content_en = {
    "lang": "en",
    "title": "KhmerX FAQ | ABA Micro Lending Questions",
    "desc": "Find answers to frequently asked questions about KhmerX borrowing, repayment, fees, and safety. KhmerX is a Cambodia-focused micro lending platform.",
    "keywords": "KhmerX FAQ, ABA loan FAQ, Cambodia loan FAQ, Telegram loan FAQ, Micro lending FAQ",
    "km_active": "", "en_active": "bg-white shadow-sm text-blue-600", "zh_active": "",
    "nav_borrow": "How to Borrow", "nav_fees": "Fees", "nav_faq": "FAQ", "nav_contact": "Contact", "nav_cta": "Open Mini App",
    
    "hero_title": "Frequently Asked Questions",
    "hero_subtitle": "Learn about KhmerX's borrowing, repayment, fees, and risk rules.",
    "search_placeholder": "Search questions...",
    
    "cat_borrow": "Borrow", "cat_fees": "Fees", "cat_repay": "Repay", "cat_credit": "Credit",
    
    "q1_q": "What is KhmerX?", "q1_a": "KhmerX is a micro lending information service platform for Cambodian users. Users can publish requests via Telegram Mini App and complete transactions via ABA transfers.",
    "q2_q": "How do I start borrowing?", "q2_a": "Open the Telegram Mini App, bind your ABA information, and you can apply for a loan.",
    "q3_q": "How much can new users borrow?", "q3_a": "New users usually start with a small limit. By repaying on time, the limit can be gradually increased.",
    "q4_q": "Why is the received amount less than the borrowed amount?", "q4_a": "KhmerX uses a flat-rate fee model. Fees are deducted upfront when borrowing. Please confirm the received amount and repayment amount before borrowing.",
    "q5_q": "How are fees calculated?", "q5_a": "Fees are automatically calculated based on the borrow amount and duration. The system will display the exact amount before you confirm the borrowing.",
    "q6_q": "How do I repay?", "q6_a": "After completing the transfer via ABA, simply upload the repayment receipt screenshot in the Mini App.",
    "q7_q": "When will I be reminded to repay?", "q7_a": "The system will send a reminder 24 hours before the due date.",
    "q8_q": "How can I increase my limit?", "q8_a": "Repay on time and maintain a good credit record. The system will dynamically increase your limit.",
    "q9_q": "What happens if I am overdue?", "q9_a": "Overdue payments may result in: lower credit score, reduced limits, borrowing restrictions, and permanent bans in severe cases.",
    "q10_q": "Does KhmerX support Telegram?", "q10_a": "KhmerX primarily provides services through the Telegram Mini App.",
    "q11_q": "How do I open the Mini App?", "q11_a": "You can access the Mini App directly through our official Telegram Bot.",
    
    "empty_title": "No questions found", "empty_desc": "Try different keywords or contact our support.",
    
    "risk_title": "Rules & Risk Notice",
    "risk_desc": "KhmerX does not guarantee successful borrowing. Users must confirm transaction risks. Please confirm before borrowing:",
    "risk_1": "Actual receive amount", "risk_2": "Total repayment amount", "risk_3": "Borrowing duration",
    
    "contact_title": "Didn't find your answer?", "contact_desc": "Our support team is ready to help you.", "contact_btn": "Contact Telegram Support",
    "cta_title": "Start Using KhmerX Now", "cta_btn": "Open Telegram Mini App",
    "footer_risk": "KhmerX is a local micro lending information service platform. We do not guarantee successful borrowing and provide no guarantees."
}

content_km = {
    "lang": "km",
    "title": "KhmerX FAQ | សំណួរញឹកញាប់អំពីការខ្ចីប្រាក់ ABA",
    "desc": "ស្វែងរកចម្លើយចំពោះសំណួរដែលសួរញឹកញាប់អំពីការខ្ចីប្រាក់ សងប្រាក់ ថ្លៃសេវា និងសុវត្ថិភាពរបស់ KhmerX។",
    "keywords": "KhmerX FAQ, ABA loan FAQ, Cambodia loan FAQ, Telegram loan FAQ",
    "km_active": "bg-white shadow-sm text-blue-600", "en_active": "", "zh_active": "",
    "nav_borrow": "របៀបខ្ចីប្រាក់", "nav_fees": "ថ្លៃសេវា", "nav_faq": "សំណួរដែលសួរញឹកញាប់", "nav_contact": "ទំនាក់ទំនង", "nav_cta": "បើក Mini App",
    
    "hero_title": "សំណួរញឹកញាប់",
    "hero_subtitle": "ស្វែងយល់ពីច្បាប់នៃការខ្ចីប្រាក់ សងប្រាក់ ថ្លៃសេវា និងហានិភ័យរបស់ KhmerX ។",
    "search_placeholder": "ស្វែងរកសំណួរ...",
    
    "cat_borrow": "ខ្ចីប្រាក់", "cat_fees": "ថ្លៃសេវា", "cat_repay": "សងប្រាក់", "cat_credit": "ឥណទាន",
    
    "q1_q": "KhmerX គឺជាអ្វី?", "q1_a": "KhmerX គឺជាវេទិកាសេវាព័ត៌មានខ្ចីប្រាក់តូចសម្រាប់អ្នកប្រើប្រាស់កម្ពុជា។ អ្នកអាចបង្ហោះសំណើតាមរយៈ Telegram Mini App និងបញ្ចប់ប្រតិបត្តិការតាមរយៈ ABA ។",
    "q2_q": "តើត្រូវចាប់ផ្តើមខ្ចីប្រាក់យ៉ាងដូចម្តេច?", "q2_a": "បើក Telegram Mini App ភ្ជាប់ព័ត៌មាន ABA របស់អ្នក ហើយអ្នកអាចដាក់ពាក្យស្នើសុំខ្ចីប្រាក់បាន។",
    "q3_q": "តើអ្នកប្រើប្រាស់ថ្មីអាចខ្ចីបានប៉ុន្មាន?", "q3_a": "អ្នកប្រើប្រាស់ថ្មីជាទូទៅចាប់ផ្តើមពីដែនកំណត់តូច។ ដែនកំណត់អាចត្រូវបានដំឡើងបន្តិចម្តងៗបន្ទាប់ពីការសងទាន់ពេលវេលា។",
    "q4_q": "ហេតុអ្វីបានជាប្រាក់ទទួលបានតិចជាងប្រាក់ខ្ចី?", "q4_a": "KhmerX ប្រើម៉ូដែលថ្លៃសេវាថេរ ដោយកាត់ថ្លៃសេវាទុកជាមុន។ សូមបញ្ជាក់ចំនួនប្រាក់ទទួលបាន និងចំនួនប្រាក់សងមុនពេលខ្ចី។",
    "q5_q": "តើថ្លៃសេវាគណនាយ៉ាងដូចម្តេច?", "q5_a": "ថ្លៃសេវាត្រូវបានគណនាដោយស្វ័យប្រវត្តិផ្អែកលើចំនួនប្រាក់ខ្ចី និងរយៈពេល។ ប្រព័ន្ធនឹងបង្ហាញចំនួនជាក់លាក់មុនពេលខ្ចី។",
    "q6_q": "តើត្រូវសងប្រាក់យ៉ាងដូចម្តេច?", "q6_a": "បន្ទាប់ពីបញ្ចប់ការផ្ទេរប្រាក់តាម ABA គ្រាន់តែបញ្ចូលវិក័យប័ត្រផ្ទេរប្រាក់ក្នុង Mini App ។",
    "q7_q": "តើពេលណាទើបរំលឹកឱ្យសងប្រាក់?", "q7_a": "ប្រព័ន្ធនឹងផ្ញើការរំលឹក 24 ម៉ោងមុនថ្ងៃកំណត់។",
    "q8_q": "តើត្រូវបង្កើនដែនកំណត់យ៉ាងដូចម្តេច?", "q8_a": "សងឱ្យទាន់ពេលវេលា និងរក្សាប្រវត្តិឥណទានល្អ ប្រព័ន្ធនឹងដំឡើងដែនកំណត់របស់អ្នកដោយស្វ័យប្រវត្តិ។",
    "q9_q": "តើមានអ្វីកើតឡើងប្រសិនបើខ្ញុំយឺតយ៉ាវ?", "q9_a": "ការយឺតយ៉ាវអាចបណ្តាលឱ្យ៖ ធ្លាក់ចុះឥណទាន ថយចុះដែនកំណត់ រឹតបន្តឹងការខ្ចី និងហាមឃាត់ជាអចិន្ត្រៃយ៍ក្នុងករណីធ្ងន់ធ្ងរ។",
    "q10_q": "តើ KhmerX គាំទ្រ Telegram ទេ?", "q10_a": "KhmerX ផ្តល់សេវាកម្មចម្បងតាមរយៈ Telegram Mini App ។",
    "q11_q": "តើត្រូវបើក Mini App យ៉ាងដូចម្តេច?", "q11_a": "អ្នកអាចចូល Mini App តាមរយៈ Telegram Bot ផ្លូវការរបស់យើង។",
    
    "empty_title": "រកមិនឃើញសំណួរទេ", "empty_desc": "សាកល្បងពាក្យគន្លឹះផ្សេង ឬទាក់ទងសេវាអតិថិជន។",
    
    "risk_title": "ច្បាប់ និងការព្រមានហានិភ័យ",
    "risk_desc": "KhmerX មិនធានាថាការខ្ចីប្រាក់នឹងជោគជ័យទេ។ អ្នកប្រើប្រាស់ត្រូវបញ្ជាក់ហានិភ័យដោយខ្លួនឯង។ សូមបញ្ជាក់មុនពេលខ្ចី៖",
    "risk_1": "ចំនួនប្រាក់ទទួលបានជាក់ស្តែង", "risk_2": "ចំនួនប្រាក់សងសរុប", "risk_3": "រយៈពេលខ្ចីប្រាក់",
    
    "contact_title": "រកមិនឃើញចម្លើយមែនទេ?", "contact_desc": "ក្រុមការងាររបស់យើងត្រៀមខ្លួនជានិច្ចដើម្បីជួយអ្នក។", "contact_btn": "ទាក់ទងផ្នែកសេវាអតិថិជន Telegram",
    "cta_title": "ចាប់ផ្តើមប្រើប្រាស់ KhmerX ឥឡូវនេះ", "cta_btn": "បើក Telegram Mini App",
    "footer_risk": "KhmerX គឺជាវេទិកាសេវាព័ត៌មានខ្ចីប្រាក់តូចក្នុងស្រុក។ យើងមិនធានាថាការខ្ចីប្រាក់នឹងជោគជ័យទេ ហើយមិនផ្តល់ការធានាណាមួយឡើយ។"
}

with open(r'D:\projects\khmerx\frontend\website\zh\faq\index.html', 'w', encoding='utf-8') as f:
    f.write(faq_template.format(**content_zh))
with open(r'D:\projects\khmerx\frontend\website\en\faq\index.html', 'w', encoding='utf-8') as f:
    f.write(faq_template.format(**content_en))
with open(r'D:\projects\khmerx\frontend\website\km\faq\index.html', 'w', encoding='utf-8') as f:
    f.write(faq_template.format(**content_km))

print("FAQ pages generated.")
