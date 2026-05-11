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
    <meta property="og:url" content="https://khmerx.org/{lang}/{slug}" />
    <meta property="og:image" content="https://khmerx.org/logo.jpg" />
    <meta name="twitter:card" content="summary" />
    <meta name="twitter:title" content="{title}" />
    <meta name="twitter:description" content="{desc}" />
    <link rel="canonical" href="https://khmerx.org/{lang}/{slug}" />
    <link rel="alternate" href="https://khmerx.org/km/{slug}" hreflang="km" />
    <link rel="alternate" href="https://khmerx.org/en/{slug}" hreflang="en" />
    <link rel="alternate" href="https://khmerx.org/zh/{slug}" hreflang="zh" />
    <link rel="alternate" href="https://khmerx.org/km/{slug}" hreflang="x-default" />
    <script type="application/ld+json">
      {{
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "KhmerX",
        "url": "https://khmerx.org",
        "logo": "https://khmerx.org/logo.jpg",
        "sameAs": [
          "https://t.me/KhmerXBot"
        ]
      }}
    </script>
    <script type="application/ld+json">
      {{
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
          {{
            "@type": "Question",
            "name": "{faq1_q}",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "{faq1_a}"
            }}
          }},
          {{
            "@type": "Question",
            "name": "{faq2_q}",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "{faq2_a}"
            }}
          }},
          {{
            "@type": "Question",
            "name": "{faq3_q}",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "{faq3_a}"
            }}
          }}
        ]
      }}
    </script>
    <script type="application/ld+json">
      {{
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{
            "@type": "ListItem",
            "position": 1,
            "name": "Home",
            "item": "https://khmerx.org/{lang}"
          }},
          {{
            "@type": "ListItem",
            "position": 2,
            "name": "{hero_title}",
            "item": "https://khmerx.org/{lang}/{slug}"
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
    </style>
  </head>
  <body>
    <script type="module" src="/src/site.ts"></script>
    <main class="min-h-screen bg-[#F5F7FA] pb-24 text-slate-900 font-sans flex flex-col">
      
      <!-- Header -->
      <header class="sticky top-0 z-50 border-b bg-white/90 backdrop-blur-md">
        <div class="mx-auto flex max-w-[1200px] items-center justify-between px-5 py-4">
          <a href="/{lang}" class="flex items-center gap-3 group">
            <img src="/logo.jpg" alt="KhmerX Logo" class="h-10 w-10 rounded-xl object-cover shadow-sm group-hover:scale-105 transition-transform" />
            <div class="hidden sm:block">
              <div class="font-bold text-lg">KhmerX</div>
            </div>
          </a>
          <nav class="hidden gap-8 text-sm font-medium text-slate-600 md:flex">
            <a class="hover:text-blue-600 transition-colors" href="/{lang}/borrow">{nav_borrow}</a>
            <a class="hover:text-blue-600 transition-colors" href="/{lang}/fees">{nav_fees}</a>
            <a class="hover:text-blue-600 transition-colors" href="/{lang}/blog">{nav_blog}</a>
            <a class="hover:text-blue-600 transition-colors" href="/{lang}/faq">FAQ</a>
          </nav>
          <div class="flex items-center gap-4">
            <div class="flex gap-1 text-sm bg-slate-100 p-1 rounded-xl">
              <a data-lang="km" class="rounded-lg px-3 py-1.5 transition-colors font-medium {km_active}" href="/km/{slug}">ខ្មែរ</a>
              <a data-lang="en" class="rounded-lg px-3 py-1.5 transition-colors font-medium {en_active}" href="/en/{slug}">EN</a>
              <a data-lang="zh" class="rounded-lg px-3 py-1.5 transition-colors font-medium {zh_active}" href="/zh/{slug}">中文</a>
            </div>
            <button class="md:hidden p-2 text-slate-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
            </button>
          </div>
        </div>
      </header>

      <!-- Hero 区 -->
      <section class="relative bg-slate-900 border-b border-slate-800 overflow-hidden text-white">
        <div class="absolute inset-0 bg-[url('{hero_img}')] bg-cover bg-center opacity-30 mix-blend-overlay"></div>
        <div class="absolute inset-0 bg-gradient-to-r from-slate-900 via-slate-900/80 to-transparent"></div>
        <div class="relative mx-auto max-w-[1200px] px-5 py-20 md:py-28">
          <div class="max-w-2xl z-10">
            <div class="mb-6 inline-flex rounded-full bg-blue-500/20 px-4 py-2 text-sm font-bold text-blue-300 border border-blue-500/30">
              {badge}
            </div>
            <h1 class="text-4xl font-extrabold leading-tight tracking-tight md:text-5xl lg:text-6xl mb-6">
              {hero_title}
            </h1>
            <p class="text-lg leading-relaxed text-slate-300 md:text-xl font-medium mb-10">
              {hero_subtitle}
            </p>
            <div class="flex flex-wrap gap-4">
              <a href="https://t.me/KhmerXBot/app" class="inline-flex justify-center items-center rounded-2xl bg-gradient-to-r from-[#0A5BFF] to-[#00AEEF] px-8 py-4 text-lg font-bold text-white shadow-lg hover:scale-105 transition-all duration-300">
                <svg class="w-6 h-6 mr-3" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.74-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .38z"/></svg>
                {cta_open}
              </a>
              <a href="/{lang}/app" class="inline-flex justify-center items-center rounded-2xl bg-white/10 px-8 py-4 text-lg font-bold text-white shadow-lg hover:bg-white/20 transition-all duration-300">
                {cta_learn}
              </a>
            </div>
          </div>
        </div>
      </section>

      <!-- 内容区 -->
      <section class="mx-auto max-w-[1200px] px-5 py-20 -mt-10 relative z-20">
        <div class="grid md:grid-cols-3 gap-8">
          
          <div class="md:col-span-2 space-y-8">
            <div class="bg-white rounded-3xl p-8 md:p-12 shadow-sm border border-slate-100 prose prose-slate prose-blue max-w-none">
              {content_html}
            </div>
            
            <!-- FAQ -->
            <div class="bg-white rounded-3xl p-8 md:p-12 shadow-sm border border-slate-100">
              <h3 class="text-2xl font-bold text-slate-900 mb-8">FAQ</h3>
              <div class="space-y-4">
                <details class="group rounded-2xl border border-slate-200 bg-slate-50 [&_summary::-webkit-details-marker]:hidden">
                  <summary class="flex cursor-pointer items-center justify-between p-5 font-bold text-slate-900">
                    {faq1_q}
                    <span class="transition group-open:rotate-180">
                      <svg fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" viewBox="0 0 24 24" width="24"><path d="M6 9l6 6 6-6"></path></svg>
                    </span>
                  </summary>
                  <div class="px-5 pb-5 text-slate-600 text-sm"><p>{faq1_a}</p></div>
                </details>
                <details class="group rounded-2xl border border-slate-200 bg-slate-50 [&_summary::-webkit-details-marker]:hidden">
                  <summary class="flex cursor-pointer items-center justify-between p-5 font-bold text-slate-900">
                    {faq2_q}
                    <span class="transition group-open:rotate-180">
                      <svg fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" viewBox="0 0 24 24" width="24"><path d="M6 9l6 6 6-6"></path></svg>
                    </span>
                  </summary>
                  <div class="px-5 pb-5 text-slate-600 text-sm"><p>{faq2_a}</p></div>
                </details>
                <details class="group rounded-2xl border border-slate-200 bg-slate-50 [&_summary::-webkit-details-marker]:hidden">
                  <summary class="flex cursor-pointer items-center justify-between p-5 font-bold text-slate-900">
                    {faq3_q}
                    <span class="transition group-open:rotate-180">
                      <svg fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" viewBox="0 0 24 24" width="24"><path d="M6 9l6 6 6-6"></path></svg>
                    </span>
                  </summary>
                  <div class="px-5 pb-5 text-slate-600 text-sm"><p>{faq3_a}</p></div>
                </details>
              </div>
            </div>
          </div>
          
          <!-- Sidebar -->
          <div class="space-y-6">
            <div class="bg-blue-600 rounded-3xl p-8 text-white text-center shadow-lg relative overflow-hidden">
              <div class="absolute inset-0 bg-[url('https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=Blue%20technology%20abstract%20waves&image_size=landscape_16_9')] bg-cover bg-center opacity-20 mix-blend-overlay"></div>
              <div class="relative z-10">
                <div class="w-16 h-16 bg-white/20 rounded-2xl flex items-center justify-center mx-auto mb-6 backdrop-blur-sm">
                  <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"></path></svg>
                </div>
                <h3 class="text-xl font-bold mb-4">{sidebar_title}</h3>
                <p class="text-blue-100 text-sm mb-6">{sidebar_desc}</p>
                <a href="https://t.me/KhmerXBot/app" class="block w-full bg-white text-blue-600 font-bold py-3 rounded-xl hover:shadow-lg transition-all">
                  {cta_open}
                </a>
              </div>
            </div>
            
            <div class="bg-white rounded-3xl p-8 shadow-sm border border-slate-100">
              <h4 class="font-bold text-slate-900 mb-4">{quick_links}</h4>
              <ul class="space-y-3 text-sm">
                <li><a href="/{lang}/borrow" class="text-blue-600 hover:underline">{nav_borrow}</a></li>
                <li><a href="/{lang}/faq" class="text-blue-600 hover:underline">FAQ</a></li>
                <li><a href="/{lang}/blog" class="text-blue-600 hover:underline">{nav_blog}</a></li>
                <li><a href="/{lang}/about" class="text-blue-600 hover:underline">About KhmerX</a></li>
              </ul>
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
          </div>
        </div>
      </footer>
    </main>
  </body>
</html>
"""

pages = [
    {
        "slug": "phnom-penh",
        "zh": {
            "title": "金边 Telegram + ABA 小额周转 | KhmerX",
            "desc": "在金边生活，使用 KhmerX 通过 Telegram Mini App 和 ABA 转账快速解决小额周转需求。",
            "keywords": "Phnom Penh loan, Phnom Penh ABA, Cambodia Telegram",
            "hero_title": "金边 Telegram + ABA 小额周转",
            "hero_subtitle": "在柬埔寨首都金边，通过国民级的 Telegram 与 ABA 快速完成短期的资金匹配。",
            "badge": "Phnom Penh · Local Finance",
            "hero_img": "https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=Phnom%20Penh%20city%20skyline%20modern%20finance%20technology%20blue%20tones&image_size=landscape_16_9",
            "content_html": """
            <h2>金边生活与小额周转需求</h2>
            <p>作为柬埔寨的首都，金边 (Phnom Penh) 拥有活跃的经济与快节奏的生活。对于许多在金边工作的本地人和外籍人士来说，偶尔会遇到短期的资金周转需求。</p>
            <h2>ABA 在金边的普及</h2>
            <p>在金边，几乎所有商家和个人都在使用 <strong>ABA Bank</strong>。无论是扫码支付 (ABA PAY) 还是点对点转账，ABA 已经成为了金边的支付基础设施。</p>
            <h2>Telegram Mini App 的便利性</h2>
            <p>KhmerX 结合了在柬埔寨使用率极高的 <strong>Telegram</strong> 和 <strong>ABA</strong>，为您提供最本地化的信息匹配服务：</p>
            <ul>
                <li>无需下载新的借款 App，直接在 Telegram 内完成操作。</li>
                <li>借还款资金均在双方的 ABA 账户之间直接流动，安全透明。</li>
                <li>支持中、英、高棉多语言，适合金边多元化的社区。</li>
            </ul>
            """,
            "faq1_q": "金边是否支持 ABA 转账借款？", "faq1_a": "是的，KhmerX 上的所有交易都默认支持通过 ABA Bank 进行转账。",
            "faq2_q": "在金边使用 KhmerX 需要去线下门店吗？", "faq2_a": "不需要。KhmerX 是纯线上的信息匹配平台，所有操作都在 Telegram 上完成。",
            "faq3_q": "KhmerX 主要是服务金边用户吗？", "faq3_a": "KhmerX 服务于全柬埔寨用户，但由于 ABA 和 Telegram 的普及度，金边用户是我们的主要服务群体。"
        },
        "en": {
            "title": "Phnom Penh ABA & Telegram Mini App | KhmerX",
            "desc": "Living in Phnom Penh? Use KhmerX via Telegram Mini App and ABA transfers for quick micro-lending solutions.",
            "keywords": "Phnom Penh loan, Phnom Penh ABA, Cambodia Telegram",
            "hero_title": "Phnom Penh ABA & Telegram Mini App",
            "hero_subtitle": "Fast short-term micro-lending matching in Cambodia's capital using Telegram and ABA.",
            "badge": "Phnom Penh · Local Finance",
            "hero_img": "https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=Phnom%20Penh%20city%20skyline%20modern%20finance%20technology%20blue%20tones&image_size=landscape_16_9",
            "content_html": """
            <h2>Living in Phnom Penh & Micro Lending Needs</h2>
            <p>As the capital of Cambodia, Phnom Penh has a vibrant economy and fast-paced lifestyle. Many locals and expats occasionally need short-term funds.</p>
            <h2>The Popularity of ABA in Phnom Penh</h2>
            <p>In Phnom Penh, almost every merchant and individual uses <strong>ABA Bank</strong>. Whether it's ABA PAY or P2P transfers, ABA is the payment infrastructure of the city.</p>
            <h2>The Convenience of Telegram Mini Apps</h2>
            <p>KhmerX combines <strong>Telegram</strong> and <strong>ABA</strong> to provide the most localized matching service:</p>
            <ul>
                <li>No need to download a new loan app; operate directly within Telegram.</li>
                <li>Funds flow directly between users' ABA accounts, ensuring security and transparency.</li>
                <li>Supports Khmer, English, and Chinese, perfect for Phnom Penh's diverse community.</li>
            </ul>
            """,
            "faq1_q": "Are ABA transfers supported for loans in Phnom Penh?", "faq1_a": "Yes, all transactions on KhmerX default to using ABA Bank for transfers.",
            "faq2_q": "Do I need to visit a physical branch in Phnom Penh?", "faq2_a": "No. KhmerX is a 100% online matching platform via Telegram.",
            "faq3_q": "Is KhmerX only for Phnom Penh users?", "faq3_a": "KhmerX serves all users in Cambodia, but due to the high adoption of ABA and Telegram, Phnom Penh is a major hub."
        },
        "km": {
            "title": "សេវាខ្ចីប្រាក់ភ្នំពេញតាម Telegram + ABA | KhmerX",
            "desc": "រស់នៅភ្នំពេញមែនទេ? ប្រើប្រាស់ KhmerX តាមរយៈ Telegram និង ABA សម្រាប់ដំណោះស្រាយហិរញ្ញវត្ថុរហ័ស។",
            "keywords": "Phnom Penh loan, Phnom Penh ABA, Cambodia Telegram",
            "hero_title": "សេវាខ្ចីប្រាក់ភ្នំពេញតាម Telegram និង ABA",
            "hero_subtitle": "ការផ្គូផ្គងប្រាក់កម្ចីខ្នាតតូចរហ័សនៅរាជធានីភ្នំពេញ ដោយប្រើ Telegram និង ABA ។",
            "badge": "ភ្នំពេញ · ហិរញ្ញវត្ថុ",
            "hero_img": "https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=Phnom%20Penh%20city%20skyline%20modern%20finance%20technology%20blue%20tones&image_size=landscape_16_9",
            "content_html": """
            <h2>ការរស់នៅភ្នំពេញ និងតម្រូវការហិរញ្ញវត្ថុ</h2>
            <p>ក្នុងនាមជារាជធានីនៃប្រទេសកម្ពុជា ភ្នំពេញមានសេដ្ឋកិច្ចសកម្ម។ ប្រជាជនក្នុងស្រុកនិងជនបរទេសជាច្រើនតែងតែត្រូវការថវិកាសម្រាប់រយៈពេលខ្លី។</p>
            <h2>ភាពពេញនិយមរបស់ ABA នៅភ្នំពេញ</h2>
            <p>នៅភ្នំពេញ ស្ទើរតែគ្រប់អាជីវករនិងបុគ្គលទាំងអស់ប្រើប្រាស់ <strong>ABA Bank</strong>។ ABA គឺជាហេដ្ឋារចនាសម្ព័ន្ធទូទាត់ប្រាក់ដ៏សំខាន់។</p>
            <h2>ភាពងាយស្រួលនៃ Telegram Mini App</h2>
            <p>KhmerX រួមបញ្ចូល <strong>Telegram</strong> និង <strong>ABA</strong> ដើម្បីផ្តល់សេវាកម្មផ្គូផ្គងក្នុងស្រុកល្អបំផុត៖</p>
            <ul>
                <li>មិនចាំបាច់ទាញយកកម្មវិធីថ្មី ដំណើរការផ្ទាល់ក្នុង Telegram ។</li>
                <li>ការផ្ទេរប្រាក់ធ្វើឡើងដោយផ្ទាល់រវាងគណនី ABA ធានាសុវត្ថិភាព។</li>
                <li>គាំទ្រភាសាខ្មែរ អង់គ្លេស និងចិន។</li>
            </ul>
            """,
            "faq1_q": "តើភ្នំពេញគាំទ្រការផ្ទេរប្រាក់ ABA ទេ?", "faq1_a": "បាទ រាល់ប្រតិបត្តិការនៅលើ KhmerX គឺប្រើប្រាស់ ABA Bank ។",
            "faq2_q": "តើខ្ញុំត្រូវទៅការិយាល័យនៅភ្នំពេញទេ?", "faq2_a": "ទេ KhmerX គឺជាវេទិកាអនឡាញ 100% តាមរយៈ Telegram ។",
            "faq3_q": "តើ KhmerX សម្រាប់តែអ្នកភ្នំពេញឬ?", "faq3_a": "បម្រើអ្នកប្រើប្រាស់ទូទាំងប្រទេសកម្ពុជា ប៉ុន្តែអ្នកភ្នំពេញជាអ្នកប្រើប្រាស់ចម្បង។"
        }
    },
    {
        "slug": "aba-guide",
        "zh": {
            "title": "ABA 转账使用教程 | KhmerX 指南",
            "desc": "学习如何在柬埔寨使用 ABA Bank 进行安全的转账交易，以及在 KhmerX 上的借款操作。",
            "keywords": "ABA Cambodia, ABA transfer, ABA tutorial",
            "hero_title": "ABA 转账使用教程",
            "hero_subtitle": "了解如何在 KhmerX 上安全地使用 ABA Mobile App 进行转账和收款。",
            "badge": "ABA Guide",
            "hero_img": "https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=ABA%20Bank%20Mobile%20App%20Interface%20transfer%20money%20Cambodia%20finance%20blue%20tones&image_size=landscape_16_9",
            "content_html": """
            <h2>什么是 ABA Bank？</h2>
            <p>ABA Bank 是柬埔寨最大的商业银行之一。其手机应用 <strong>ABA Mobile</strong> 是当地最受欢迎的数字支付工具。</p>
            <h2>如何在 KhmerX 使用 ABA？</h2>
            <p>在 KhmerX 平台上，所有的借入和还款操作均通过 ABA 转账完成：</p>
            <ol>
                <li><strong>绑定信息：</strong> 在 KhmerX Mini App 中输入您的 ABA 账号和姓名。</li>
                <li><strong>确认交易对方：</strong> 当借款需求匹配成功后，系统会显示对方的 ABA 信息。</li>
                <li><strong>打开 ABA Mobile：</strong> 切换到您的 ABA App，选择转账功能。</li>
                <li><strong>核对姓名：</strong> 转账前务必核对对方的 ABA 姓名是否与 KhmerX 上显示的一致。</li>
                <li><strong>保留凭证：</strong> 转账成功后，截图保留电子回单，并上传至 KhmerX 确认交易。</li>
            </ol>
            <h2>手续费说明</h2>
            <p>通常情况下，ABA 个人账户之间的美元或瑞尔转账是免手续费的（具体以 ABA 官方政策为准）。</p>
            """,
            "faq1_q": "KhmerX 是否会自动从我的 ABA 扣款？", "faq1_a": "不会。KhmerX 无法访问您的资金，所有转账都必须由您自己在 ABA App 内手动完成。",
            "faq2_q": "转账时输错账号怎么办？", "faq2_a": "转账前 ABA 会显示对方的姓名，请务必仔细核对。如果不慎转错，请直接联系 ABA 银行客服协助。",
            "faq3_q": "支持其他银行吗？", "faq3_a": "目前 KhmerX 平台内的用户主要使用 ABA 进行交易匹配以保证高效。"
        },
        "en": {
            "title": "ABA Transfer Guide | KhmerX",
            "desc": "Learn how to safely use ABA Bank for transfers in Cambodia and for loan operations on KhmerX.",
            "keywords": "ABA Cambodia, ABA transfer, ABA tutorial",
            "hero_title": "ABA Transfer Guide",
            "hero_subtitle": "Learn how to securely transfer and receive funds using the ABA Mobile App on KhmerX.",
            "badge": "ABA Guide",
            "hero_img": "https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=ABA%20Bank%20Mobile%20App%20Interface%20transfer%20money%20Cambodia%20finance%20blue%20tones&image_size=landscape_16_9",
            "content_html": """
            <h2>What is ABA Bank?</h2>
            <p>ABA Bank is one of the largest commercial banks in Cambodia. Its <strong>ABA Mobile</strong> app is the most popular digital payment tool locally.</p>
            <h2>How to use ABA on KhmerX?</h2>
            <p>On KhmerX, all loan disbursements and repayments are done via ABA transfers:</p>
            <ol>
                <li><strong>Bind Info:</strong> Enter your ABA account number and name in the KhmerX Mini App.</li>
                <li><strong>Confirm Counterparty:</strong> Once matched, the system shows the other party's ABA info.</li>
                <li><strong>Open ABA Mobile:</strong> Switch to your ABA App and select Transfer.</li>
                <li><strong>Verify Name:</strong> Always verify the recipient's name matches what is shown on KhmerX before sending.</li>
                <li><strong>Keep Receipt:</strong> After a successful transfer, screenshot the e-receipt and upload it to KhmerX to confirm the transaction.</li>
            </ol>
            <h2>Fee Information</h2>
            <p>Typically, transfers between personal ABA accounts in USD or KHR are free of charge (subject to official ABA policies).</p>
            """,
            "faq1_q": "Will KhmerX auto-deduct from my ABA?", "faq1_a": "No. KhmerX has no access to your funds. All transfers must be done manually by you in your ABA App.",
            "faq2_q": "What if I enter the wrong account number?", "faq2_a": "ABA displays the recipient's name before confirming. Please check carefully. If a mistake happens, contact ABA Bank support immediately.",
            "faq3_q": "Are other banks supported?", "faq3_a": "Currently, users on KhmerX primarily use ABA for efficient transaction matching."
        },
        "km": {
            "title": "ការណែនាំអំពីការផ្ទេរប្រាក់ ABA | KhmerX",
            "desc": "រៀនពីរបៀបប្រើប្រាស់ធនាគារ ABA សម្រាប់ការផ្ទេរប្រាក់ប្រកបដោយសុវត្ថិភាពនៅកម្ពុជានិងនៅលើ KhmerX ។",
            "keywords": "ABA Cambodia, ABA transfer, ABA tutorial",
            "hero_title": "ការណែនាំអំពីការផ្ទេរប្រាក់ ABA",
            "hero_subtitle": "ស្វែងយល់ពីរបៀបផ្ទេរនិងទទួលប្រាក់ដោយសុវត្ថិភាពតាមរយៈ ABA Mobile App នៅលើ KhmerX ។",
            "badge": "ការណែនាំ ABA",
            "hero_img": "https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=ABA%20Bank%20Mobile%20App%20Interface%20transfer%20money%20Cambodia%20finance%20blue%20tones&image_size=landscape_16_9",
            "content_html": """
            <h2>តើ ABA Bank ជាន្វី?</h2>
            <p>ធនាគារ ABA គឺជាធនាគារពាណិជ្ជដ៏ធំបំផុតមួយនៅកម្ពុជា។ កម្មវិធី <strong>ABA Mobile</strong> គឺជាឧបករណ៍ទូទាត់ឌីជីថលដ៏ពេញនិយមបំផុត។</p>
            <h2>របៀបប្រើ ABA នៅលើ KhmerX?</h2>
            <p>នៅលើ KhmerX រាល់ការផ្តល់ប្រាក់កម្ចីនិងការសងប្រាក់គឺធ្វើឡើងតាមរយៈការផ្ទេរ ABA ៖</p>
            <ol>
                <li><strong>ភ្ជាប់ព័ត៌មាន៖</strong> បញ្ចូលលេខគណនី ABA និងឈ្មោះរបស់អ្នកនៅក្នុង KhmerX Mini App ។</li>
                <li><strong>បញ្ជាក់ដៃគូ៖</strong> ពេលផ្គូផ្គងរួច ប្រព័ន្ធនឹងបង្ហាញព័ត៌មាន ABA របស់ភាគីម្ខាងទៀត។</li>
                <li><strong>បើក ABA Mobile៖</strong> ប្តូរទៅកម្មវិធី ABA របស់អ្នក ហើយជ្រើសរើសការផ្ទេរប្រាក់។</li>
                <li><strong>ផ្ទៀងផ្ទាត់ឈ្មោះ៖</strong> តែងតែផ្ទៀងផ្ទាត់ឈ្មោះអ្នកទទួលឱ្យត្រូវគ្នាមុនពេលផ្ញើ។</li>
                <li><strong>រក្សាទុកវិក័យប័ត្រ៖</strong> បន្ទាប់ពីផ្ទេរជោគជ័យ សូមថតរូបអេក្រង់វិក័យប័ត្រ ហើយបញ្ចូលវាទៅ KhmerX ។</li>
            </ol>
            """,
            "faq1_q": "តើ KhmerX នឹងកាត់ប្រាក់ពី ABA ខ្ញុំដោយស្វ័យប្រវត្តិទេ?", "faq1_a": "ទេ KhmerX មិនមានសិទ្ធិចូលប្រើប្រាស់ថវិការបស់អ្នកទេ។ ការផ្ទេរទាំងអស់ត្រូវធ្វើដោយដៃរបស់អ្នកផ្ទាល់។",
            "faq2_q": "ចុះបើខ្ញុំវាយលេខគណនីខុស?", "faq2_a": "ABA បង្ហាញឈ្មោះអ្នកទទួលមុនពេលបញ្ជាក់។ សូមពិនិត្យឱ្យបានច្បាស់។",
            "faq3_q": "តើមានការគាំទ្រធនាគារផ្សេងទេ?", "faq3_a": "បច្ចុប្បន្នអ្នកប្រើប្រាស់នៅលើ KhmerX ប្រើប្រាស់ ABA ជាចម្បង។"
        }
    },
    {
        "slug": "telegram-finance",
        "zh": {
            "title": "Telegram Mini App 与 KhmerX 小额周转",
            "desc": "了解 KhmerX 如何利用 Telegram Mini App 在柬埔寨提供安全便捷的金融信息匹配服务。",
            "keywords": "Telegram Mini App, Telegram finance, Cambodia Telegram",
            "hero_title": "Telegram Mini App 与 KhmerX",
            "hero_subtitle": "无需下载额外 App，在您最熟悉的 Telegram 中完成资金需求匹配。",
            "badge": "Telegram Tech",
            "hero_img": "https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=Telegram%20Mini%20App%20interface%20digital%20finance%20technology%20blue%20background&image_size=landscape_16_9",
            "content_html": """
            <h2>什么是 Telegram Mini App？</h2>
            <p>Telegram Mini App 是一种运行在 Telegram 聊天应用内部的网页应用程序。它允许用户直接在 Telegram 内部体验完整的应用交互，无需跳转到浏览器或下载新软件。</p>
            <h2>KhmerX 为什么选择 Telegram？</h2>
            <p>在柬埔寨，Telegram 是国民级的通讯工具。KhmerX 选择基于 Telegram 构建平台：</p>
            <ul>
                <li><strong>无缝体验：</strong> 随时随地打开 Bot，一键进入借款平台。</li>
                <li><strong>消息通知：</strong> 到期还款提醒、交易状态更新，直接通过 Telegram 官方通知触达，防遗漏。</li>
                <li><strong>安全隐私：</strong> 依托 Telegram 的安全框架，保护用户通讯与登录隐私。</li>
            </ul>
            <h2>防骗与安全说明</h2>
            <p>虽然 Telegram 很方便，但请注意防范冒充官方账号的骗子。KhmerX 官方客服绝对不会主动要求您向任何私人账户转账，所有的资金交易都在用户之间通过 ABA 进行。</p>
            """,
            "faq1_q": "什么是 Telegram Mini App？", "faq1_a": "它是内嵌在 Telegram 里的轻应用，可以提供类似原生 App 的体验。",
            "faq2_q": "KhmerX 会获取我的 Telegram 聊天记录吗？", "faq2_a": "绝对不会。KhmerX 只能获取您的公开资料（如昵称、头像和 ID）用于登录，无法访问您的私人聊天。",
            "faq3_q": "打不开 Mini App 怎么办？", "faq3_a": "请尝试更新 Telegram 到最新版本，或检查网络连接。"
        },
        "en": {
            "title": "Telegram Mini App & KhmerX Finance",
            "desc": "Learn how KhmerX uses Telegram Mini Apps to provide secure micro-lending matching in Cambodia.",
            "keywords": "Telegram Mini App, Telegram finance, Cambodia Telegram",
            "hero_title": "Telegram Mini App & KhmerX",
            "hero_subtitle": "No extra app downloads. Complete your funding needs right within Telegram.",
            "badge": "Telegram Tech",
            "hero_img": "https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=Telegram%20Mini%20App%20interface%20digital%20finance%20technology%20blue%20background&image_size=landscape_16_9",
            "content_html": """
            <h2>What is a Telegram Mini App?</h2>
            <p>A Telegram Mini App is a web application that runs inside the Telegram messenger. It allows users to experience full app functionality without leaving their chats or downloading new software.</p>
            <h2>Why did KhmerX choose Telegram?</h2>
            <p>Telegram is heavily used in Cambodia. KhmerX built its platform on Telegram for:</p>
            <ul>
                <li><strong>Seamless Experience:</strong> Open the Bot anytime, anywhere, and enter the platform with one click.</li>
                <li><strong>Notifications:</strong> Repayment reminders and status updates are delivered directly via Telegram messages.</li>
                <li><strong>Security:</strong> Built on Telegram's secure framework, protecting user login privacy.</li>
            </ul>
            <h2>Security Notice</h2>
            <p>Please be aware of scammers impersonating official accounts. KhmerX official support will NEVER ask you to transfer money to private accounts. All transactions are peer-to-peer via ABA.</p>
            """,
            "faq1_q": "What is a Telegram Mini App?", "faq1_a": "It's a lightweight application embedded within Telegram providing a native app-like experience.",
            "faq2_q": "Can KhmerX read my Telegram chats?", "faq2_a": "Absolutely not. KhmerX can only access your public profile (nickname, ID) for login purposes.",
            "faq3_q": "What if the Mini App doesn't open?", "faq3_a": "Please update your Telegram app to the latest version and check your network."
        },
        "km": {
            "title": "Telegram Mini App និង KhmerX",
            "desc": "ស្វែងយល់ពីរបៀបដែល KhmerX ប្រើប្រាស់ Telegram Mini App សម្រាប់សេវាផ្គូផ្គងហិរញ្ញវត្ថុនៅកម្ពុជា។",
            "keywords": "Telegram Mini App, Telegram finance, Cambodia Telegram",
            "hero_title": "Telegram Mini App និង KhmerX",
            "hero_subtitle": "មិនចាំបាច់ទាញយកកម្មវិធីថ្មី។ បញ្ចប់តម្រូវការហិរញ្ញវត្ថុរបស់អ្នកនៅក្នុង Telegram ។",
            "badge": "បច្ចេកវិទ្យា Telegram",
            "hero_img": "https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=Telegram%20Mini%20App%20interface%20digital%20finance%20technology%20blue%20background&image_size=landscape_16_9",
            "content_html": """
            <h2>តើអ្វីទៅជា Telegram Mini App?</h2>
            <p>Telegram Mini App គឺជាកម្មវិធីបណ្តាញដែលដំណើរការនៅខាងក្នុងកម្មវិធី Telegram ផ្ទាល់។ វាអនុញ្ញាតឱ្យអ្នកប្រើប្រាស់ទទួលបានបទពិសោធន៍ពេញលេញដោយមិនចាំបាច់ចាកចេញពីការជជែក។</p>
            <h2>ហេតុអ្វី KhmerX ជ្រើសរើស Telegram?</h2>
            <p>Telegram ត្រូវបានប្រើប្រាស់យ៉ាងច្រើននៅកម្ពុជា។ KhmerX ជ្រើសរើស Telegram សម្រាប់៖</p>
            <ul>
                <li><strong>បទពិសោធន៍រលូន៖</strong> បើក Bot គ្រប់ពេលដោយចុចតែម្តង។</li>
                <li><strong>ការជូនដំណឹង៖</strong> ការរំលឹកការសងប្រាក់ត្រូវបានបញ្ជូនដោយផ្ទាល់តាមរយៈ Telegram ។</li>
                <li><strong>សុវត្ថិភាព៖</strong> ការពារឯកជនភាពចូលប្រើប្រាស់របស់អ្នកប្រើប្រាស់។</li>
            </ul>
            """,
            "faq1_q": "តើអ្វីទៅជា Telegram Mini App?", "faq1_a": "វាគឺជាកម្មវិធីទម្ងន់ស្រាលដែលបង្កប់ក្នុង Telegram ។",
            "faq2_q": "តើ KhmerX អាចអានសារ Telegram របស់ខ្ញុំទេ?", "faq2_a": "ទេដាច់ខាត។ យើងអាចចូលប្រើប្រាស់បានត្រឹមតែទម្រង់សាធារណៈរបស់អ្នកប៉ុណ្ណោះ។",
            "faq3_q": "ចុះបើ Mini App មិនបើក?", "faq3_a": "សូមធ្វើបច្ចុប្បន្នភាព Telegram របស់អ្នកទៅកំណែចុងក្រោយ។"
        }
    },
    {
        "slug": "cambodia-loan-guide",
        "zh": {
            "title": "柬埔寨小额周转指南 | Cambodia Loan Guide",
            "desc": "在柬埔寨如何快速进行小额借款？了解 KhmerX 的工作方式、风险提示以及使用 ABA 和 Telegram 的指南。",
            "keywords": "Cambodia micro lending, Cambodia loan, ABA loan Cambodia",
            "hero_title": "Cambodia Small Loan Guide",
            "hero_subtitle": "了解在柬埔寨进行小额资金周转的注意事项与最佳实践。",
            "badge": "Cambodia Finance",
            "hero_img": "https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=Cambodia%20riel%20and%20USD%20currency%20finance%20concept%20with%20digital%20growth%20chart%20blue%20tones&image_size=landscape_16_9",
            "content_html": """
            <h2>柬埔寨小额周转市场介绍</h2>
            <p>在柬埔寨，特别是金边、西港等城市，小额短期的资金周转需求非常旺盛。无论是生活应急还是小本生意流转，快速获取资金都是关键。</p>
            <h2>ABA 与 Telegram 的结合</h2>
            <p>目前在柬埔寨最安全、最便捷的交易方式是基于 <strong>Telegram</strong> 沟通和 <strong>ABA Bank</strong> 转账。KhmerX 正是将这两者完美结合的信息平台。</p>
            <h2>KhmerX 的工作方式</h2>
            <p>KhmerX 不是放款机构，而是一个信息撮合平台。借款人和出借人通过平台匹配，随后在线下（通过 ABA 转账）完成资金的交割。</p>
            <h2>风险提示 (Risk Notice)</h2>
            <ul>
                <li><strong>到账金额不同：</strong> 借款通常会提前扣除部分服务费或利息（平息法）。</li>
                <li><strong>按时还款：</strong> 逾期会严重影响您的平台信用分，导致未来无法借款。</li>
                <li><strong>防范诈骗：</strong> 平台不提供担保，转账前请务必确认对方身份，勿信私下转账要求。</li>
            </ul>
            """,
            "faq1_q": "在柬埔寨小额借款需要什么条件？", "faq1_a": "在 KhmerX，您只需拥有 Telegram 账号、有效的 ABA 账户和手机号即可注册发布需求。",
            "faq2_q": "外国人可以在 KhmerX 使用服务吗？", "faq2_a": "只要您在柬埔寨拥有合法的 ABA 账户，都可以使用平台的信息匹配服务。",
            "faq3_q": "KhmerX 提供资金担保吗？", "faq3_a": "不提供。KhmerX 仅作为信息平台，不干涉用户间的实际资金流动，也不承担担保责任。"
        },
        "en": {
            "title": "Cambodia Small Loan Guide | Micro Lending Info",
            "desc": "How to get a quick micro-loan in Cambodia? Learn about KhmerX, risk notices, and how to use ABA and Telegram.",
            "keywords": "Cambodia micro lending, Cambodia loan, ABA loan Cambodia",
            "hero_title": "Cambodia Small Loan Guide",
            "hero_subtitle": "Understand the best practices and risk notices for micro-lending in Cambodia.",
            "badge": "Cambodia Finance",
            "hero_img": "https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=Cambodia%20riel%20and%20USD%20currency%20finance%20concept%20with%20digital%20growth%20chart%20blue%20tones&image_size=landscape_16_9",
            "content_html": """
            <h2>Micro Lending in Cambodia</h2>
            <p>In cities like Phnom Penh, the demand for short-term micro-loans is high. Whether for personal emergencies or small business cash flow, speed is key.</p>
            <h2>Combining ABA & Telegram</h2>
            <p>The most convenient and common transaction method in Cambodia is using <strong>Telegram</strong> for communication and <strong>ABA Bank</strong> for transfers. KhmerX integrates both seamlessly.</p>
            <h2>How KhmerX Works</h2>
            <p>KhmerX is NOT a lender. It is a peer-to-peer information matching platform. Borrowers and lenders match on the platform and settle funds directly via ABA transfers.</p>
            <h2>Risk Notice</h2>
            <ul>
                <li><strong>Received Amount differs:</strong> Loans often have fees/interest deducted upfront.</li>
                <li><strong>Repay on time:</strong> Defaulting will ruin your platform credit score, preventing future use.</li>
                <li><strong>Beware of scams:</strong> KhmerX does not guarantee funds. Always verify identities before transferring via ABA.</li>
            </ul>
            """,
            "faq1_q": "What are the requirements for a micro-loan in Cambodia?", "faq1_a": "On KhmerX, you only need a Telegram account, a valid ABA account, and a phone number.",
            "faq2_q": "Can expats use KhmerX?", "faq2_a": "Yes, as long as you have a valid ABA account in Cambodia, you can use the platform.",
            "faq3_q": "Does KhmerX guarantee the funds?", "faq3_a": "No. KhmerX is strictly an information matching platform and does not provide financial guarantees."
        },
        "km": {
            "title": "ការណែនាំអំពីកម្ចីខ្នាតតូចកម្ពុជា | Cambodia Loan Guide",
            "desc": "ស្វែងយល់ពីរបៀបខ្ចីប្រាក់ខ្នាតតូចនៅកម្ពុជា។ របៀបដំណើរការរបស់ KhmerX និងការព្រមានអំពីហានិភ័យ។",
            "keywords": "Cambodia micro lending, Cambodia loan, ABA loan Cambodia",
            "hero_title": "Cambodia Small Loan Guide",
            "hero_subtitle": "ស្វែងយល់ពីការអនុវត្តល្អបំផុតសម្រាប់ការខ្ចីប្រាក់ខ្នាតតូចនៅកម្ពុជា។",
            "badge": "ហិរញ្ញវត្ថុកម្ពុជា",
            "hero_img": "https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=Cambodia%20riel%20and%20USD%20currency%20finance%20concept%20with%20digital%20growth%20chart%20blue%20tones&image_size=landscape_16_9",
            "content_html": """
            <h2>ការខ្ចីប្រាក់ខ្នាតតូចនៅកម្ពុជា</h2>
            <p>តម្រូវការសម្រាប់ប្រាក់កម្ចីរយៈពេលខ្លីមានកម្រិតខ្ពស់។ ល្បឿនគឺជាគន្លឹះសំខាន់។</p>
            <h2>ការរួមបញ្ចូល ABA និង Telegram</h2>
            <p>វិធីសាស្ត្រប្រតិបត្តិការងាយស្រួលបំផុតនៅកម្ពុជាគឺប្រើប្រាស់ <strong>Telegram</strong> និង <strong>ABA Bank</strong> ។</p>
            <h2>របៀបដែល KhmerX ដំណើរការ</h2>
            <p>KhmerX មិនមែនជាអ្នកផ្តល់ប្រាក់កម្ចីទេ។ វាគឺជាវេទិកាផ្គូផ្គងព័ត៌មាន។ ការទូទាត់ប្រាក់ធ្វើឡើងដោយផ្ទាល់តាមរយៈ ABA ។</p>
            <h2>ការព្រមានហានិភ័យ</h2>
            <ul>
                <li><strong>ចំនួនប្រាក់ទទួលបានខុសគ្នា៖</strong> ប្រាក់កម្ចីតែងតែមានការកាត់កងថ្លៃសេវាជាមុន។</li>
                <li><strong>សងប្រាក់ទាន់ពេល៖</strong> ការខកខាននឹងបំផ្លាញពិន្ទុឥណទានរបស់អ្នក។</li>
                <li><strong>ប្រយ័ត្នការបោកប្រាស់៖</strong> KhmerX មិនធានាថវិកាទេ។ ត្រូវផ្ទៀងផ្ទាត់ជានិច្ចមុនពេលផ្ទេរប្រាក់។</li>
            </ul>
            """,
            "faq1_q": "តើមានលក្ខខណ្ឌអ្វីខ្លះ?", "faq1_a": "អ្នកគ្រាន់តែត្រូវការគណនី Telegram គណនី ABA និងលេខទូរស័ព្ទ។",
            "faq2_q": "តើជនបរទេសអាចប្រើប្រាស់បានទេ?", "faq2_a": "បាទ ដរាបណាអ្នកមានគណនី ABA ត្រឹមត្រូវនៅកម្ពុជា។",
            "faq3_q": "តើ KhmerX ធានាប្រាក់ទេ?", "faq3_a": "ទេ KhmerX គ្រាន់តែជាវេទិកាព័ត៌មានប៉ុណ្ណោះ។"
        }
    }
]

common_nav = {
    "zh": {"nav_borrow": "如何借款", "nav_fees": "费用说明", "nav_blog": "内容中心", "cta_open": "打开 Telegram Mini App", "cta_learn": "了解更多", "sidebar_title": "需要小额资金周转？", "sidebar_desc": "KhmerX 帮您快速匹配。", "quick_links": "快速链接", "footer_desc": "KhmerX 是本地小额周转信息服务平台，不保证借款成功，不提供担保。"},
    "en": {"nav_borrow": "How to Borrow", "nav_fees": "Fees", "nav_blog": "Blog", "cta_open": "Open Telegram Mini App", "cta_learn": "Learn More", "sidebar_title": "Need short-term funds?", "sidebar_desc": "KhmerX helps you match quickly.", "quick_links": "Quick Links", "footer_desc": "KhmerX is a local micro-lending platform. It does not guarantee successful loans."},
    "km": {"nav_borrow": "របៀបខ្ចីប្រាក់", "nav_fees": "ថ្លៃសេវា", "nav_blog": "ប្លុក", "cta_open": "បើក Telegram Mini App", "cta_learn": "ស្វែងយល់បន្ថែម", "sidebar_title": "ត្រូវការថវិកា?", "sidebar_desc": "KhmerX ជួយផ្គូផ្គងយ៉ាងរហ័ស។", "quick_links": "តំណរហ័ស", "footer_desc": "KhmerX គឺជាវេទិកាព័ត៌មានខ្ចីប្រាក់ខ្នាតតូចក្នុងស្រុក។ មិនធានាថាការខ្ចីប្រាក់នឹងទទួលបានជោគជ័យឡើយ។"}
}

for page in pages:
    slug = page['slug']
    for lang in ['zh', 'en', 'km']:
        data = page[lang].copy()
        data['lang'] = lang
        data['slug'] = slug
        data.update(common_nav[lang])
        
        data['zh_active'] = "bg-white shadow-sm text-blue-600" if lang == 'zh' else ""
        data['en_active'] = "bg-white shadow-sm text-blue-600" if lang == 'en' else ""
        data['km_active'] = "bg-white shadow-sm text-blue-600" if lang == 'km' else ""
        
        html = template.format(**data)
        os.makedirs(f"frontend/website/{lang}/{slug}", exist_ok=True)
        with open(f"frontend/website/{lang}/{slug}/index.html", "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Generated {lang}/{slug}/index.html")

