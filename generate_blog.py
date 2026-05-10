import os

# --- Blog Page Template ---
blog_template = """<!doctype html>
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
    <meta property="og:url" content="https://khmerx.org/{lang}/blog" />
    <meta property="og:image" content="https://khmerx.org/logo.jpg" />
    <meta name="twitter:card" content="summary" />
    <meta name="twitter:title" content="{title}" />
    <meta name="twitter:description" content="{desc}" />
    <link rel="canonical" href="https://khmerx.org/{lang}/blog" />
    <link rel="alternate" href="https://khmerx.org/km/blog" hreflang="km" />
    <link rel="alternate" href="https://khmerx.org/en/blog" hreflang="en" />
    <link rel="alternate" href="https://khmerx.org/zh/blog" hreflang="zh" />
    <link rel="alternate" href="https://khmerx.org/km/blog" hreflang="x-default" />
    <style>
      .line-clamp-2 {{
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
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
            <a class="text-blue-600 transition-colors" href="/{lang}/blog">Blog</a>
            <a class="hover:text-blue-600 transition-colors" href="/{lang}/faq">{nav_faq}</a>
          </nav>
          <div class="flex items-center gap-4">
            <div class="hidden md:flex gap-1 text-sm bg-slate-100 p-1 rounded-xl">
              <a data-lang="km" class="rounded-lg px-3 py-1.5 transition-colors font-medium {km_active}" href="/km/blog">ខ្មែរ</a>
              <a data-lang="en" class="rounded-lg px-3 py-1.5 transition-colors font-medium {en_active}" href="/en/blog">EN</a>
              <a data-lang="zh" class="rounded-lg px-3 py-1.5 transition-colors font-medium {zh_active}" href="/zh/blog">中文</a>
            </div>
            <a class="hidden md:inline-flex rounded-xl bg-gradient-to-r from-[#0A5BFF] to-[#00AEEF] px-5 py-2.5 text-sm font-bold text-white shadow-md hover:shadow-lg hover:scale-105 transition-all" href="https://t.me/KhmerXBot/app">{nav_cta}</a>
            <button class="md:hidden p-2 text-slate-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
            </button>
          </div>
        </div>
      </header>

      <!-- Hero 区 -->
      <section class="bg-white border-b border-slate-100 pt-20 pb-16">
        <div class="mx-auto max-w-[1200px] px-5 text-center">
          <h1 class="text-4xl md:text-5xl font-extrabold text-slate-900 mb-6">{hero_title}</h1>
          <p class="text-lg text-slate-600 max-w-2xl mx-auto">{hero_subtitle}</p>
        </div>
      </section>

      <!-- 分类导航 -->
      <section class="bg-white border-b border-slate-100 sticky top-[73px] z-40">
        <div class="mx-auto max-w-[1200px] px-5">
          <div class="flex overflow-x-auto py-4 gap-6 scrollbar-hide text-sm font-medium">
            <a href="/{lang}/blog" class="text-blue-600 whitespace-nowrap border-b-2 border-blue-600 pb-1 px-1">All Posts</a>
            <a href="/{lang}/blog/aba" class="text-slate-500 hover:text-blue-600 whitespace-nowrap px-1">{cat_aba}</a>
            <a href="/{lang}/blog/telegram" class="text-slate-500 hover:text-blue-600 whitespace-nowrap px-1">{cat_tg}</a>
            <a href="/{lang}/blog/loan" class="text-slate-500 hover:text-blue-600 whitespace-nowrap px-1">{cat_loan}</a>
            <a href="/{lang}/blog/phnom-penh" class="text-slate-500 hover:text-blue-600 whitespace-nowrap px-1">{cat_pp}</a>
          </div>
        </div>
      </section>

      <!-- 博客列表主体 -->
      <section class="mx-auto max-w-[1200px] px-5 py-12">
        <div class="grid lg:grid-cols-3 gap-12">
          
          <div class="lg:col-span-2 space-y-12">
            <!-- 精选文章 (Feature) -->
            <article class="bg-white rounded-[2rem] overflow-hidden shadow-sm border border-slate-200 group hover:shadow-lg transition-shadow">
              <a href="/{lang}/blog/article/how-to-use-aba" class="block">
                <div class="aspect-[16/9] bg-slate-100 overflow-hidden relative">
                  <img src="https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=ABA%20bank%20transfer%20mobile%20app%20UI%20mockup%20Cambodia%20Phnom%20Penh%20financial%20technology%20blue%20tones&image_size=landscape_16_9" alt="ABA Transfer Guide" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" loading="lazy" />
                  <div class="absolute top-4 left-4 bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">{cat_aba}</div>
                </div>
                <div class="p-8">
                  <div class="text-sm text-slate-500 mb-3 flex items-center gap-4">
                    <span>Oct 20, 2026</span>
                    <span>5 min read</span>
                  </div>
                  <h2 class="text-2xl font-bold text-slate-900 mb-4 group-hover:text-blue-600 transition-colors">{feat_1_title}</h2>
                  <p class="text-slate-600 leading-relaxed line-clamp-2 mb-6">{feat_1_desc}</p>
                  <span class="inline-flex items-center text-blue-600 font-bold hover:text-blue-800">
                    {read_more}
                    <svg class="w-5 h-5 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path></svg>
                  </span>
                </div>
              </a>
            </article>

            <div class="grid sm:grid-cols-2 gap-8">
              <!-- Article 2 -->
              <article class="bg-white rounded-3xl overflow-hidden shadow-sm border border-slate-200 group hover:shadow-md transition-shadow">
                <a href="/{lang}/blog/article/telegram-finance-guide" class="block">
                  <div class="aspect-[16/9] bg-slate-100 overflow-hidden relative">
                    <img src="https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=Telegram%20app%20chat%20interface%20with%20financial%20dashboard%20bot%20digital%20finance%20blue%20clean%20style&image_size=landscape_16_9" alt="Telegram Finance Guide" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" loading="lazy" />
                    <div class="absolute top-4 left-4 bg-slate-800 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">{cat_tg}</div>
                  </div>
                  <div class="p-6">
                    <div class="text-xs text-slate-500 mb-2">Oct 18, 2026</div>
                    <h3 class="text-lg font-bold text-slate-900 mb-2 group-hover:text-blue-600 transition-colors line-clamp-2">{list_2_title}</h3>
                    <p class="text-sm text-slate-600 line-clamp-2 mb-4">{list_2_desc}</p>
                  </div>
                </a>
              </article>
              
              <!-- Article 3 -->
              <article class="bg-white rounded-3xl overflow-hidden shadow-sm border border-slate-200 group hover:shadow-md transition-shadow">
                <a href="/{lang}/blog/article/micro-loan-tips" class="block">
                  <div class="aspect-[16/9] bg-slate-100 overflow-hidden relative">
                    <img src="https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=Small%20amount%20of%20money%20financial%20planning%20calculator%20coins%20business%20desk%20clean%20bright%20lighting&image_size=landscape_16_9" alt="Micro Loan Tips" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" loading="lazy" />
                    <div class="absolute top-4 left-4 bg-green-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">{cat_loan}</div>
                  </div>
                  <div class="p-6">
                    <div class="text-xs text-slate-500 mb-2">Oct 15, 2026</div>
                    <h3 class="text-lg font-bold text-slate-900 mb-2 group-hover:text-blue-600 transition-colors line-clamp-2">{list_3_title}</h3>
                    <p class="text-sm text-slate-600 line-clamp-2 mb-4">{list_3_desc}</p>
                  </div>
                </a>
              </article>
            </div>
            
            <div class="text-center pt-8 border-t border-slate-200">
              <button class="inline-flex items-center px-6 py-3 rounded-xl border-2 border-slate-200 font-bold text-slate-700 hover:border-slate-300 hover:bg-white transition-colors">
                Load More Posts
              </button>
            </div>
          </div>
          
          <!-- Sidebar -->
          <div class="space-y-8">
            <!-- 热门关键词 -->
            <div class="bg-white rounded-3xl p-6 border border-slate-200">
              <h3 class="font-bold text-slate-900 mb-4 flex items-center gap-2">
                <svg class="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 20l4-16m2 16l4-16M6 9h14M4 15h14"></path></svg>
                {tag_title}
              </h3>
              <div class="flex flex-wrap gap-2">
                <a href="#" class="px-3 py-1.5 bg-slate-100 hover:bg-blue-100 hover:text-blue-700 text-slate-600 rounded-lg text-sm transition-colors">{tag_1}</a>
                <a href="#" class="px-3 py-1.5 bg-slate-100 hover:bg-blue-100 hover:text-blue-700 text-slate-600 rounded-lg text-sm transition-colors">{tag_2}</a>
                <a href="#" class="px-3 py-1.5 bg-slate-100 hover:bg-blue-100 hover:text-blue-700 text-slate-600 rounded-lg text-sm transition-colors">{tag_3}</a>
                <a href="#" class="px-3 py-1.5 bg-slate-100 hover:bg-blue-100 hover:text-blue-700 text-slate-600 rounded-lg text-sm transition-colors">{tag_4}</a>
                <a href="#" class="px-3 py-1.5 bg-slate-100 hover:bg-blue-100 hover:text-blue-700 text-slate-600 rounded-lg text-sm transition-colors">ABA Transfer</a>
                <a href="#" class="px-3 py-1.5 bg-slate-100 hover:bg-blue-100 hover:text-blue-700 text-slate-600 rounded-lg text-sm transition-colors">Telegram Bot</a>
              </div>
            </div>
            
            <!-- CTA Widget -->
            <div class="bg-gradient-to-br from-[#0A5BFF] to-[#00AEEF] rounded-3xl p-8 text-white text-center shadow-lg relative overflow-hidden">
              <div class="absolute top-0 right-0 w-32 h-32 bg-white rounded-full blur-3xl opacity-20 -mr-10 -mt-10"></div>
              <h3 class="text-2xl font-bold mb-4 relative z-10">{sidebar_cta_title}</h3>
              <p class="text-blue-100 mb-6 relative z-10 text-sm">{sidebar_cta_desc}</p>
              <div class="bg-white p-3 rounded-2xl shadow-lg inline-block mb-6 relative z-10">
                <img class="w-32 h-32 rounded-xl" alt="KhmerX Mini App QR" src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=https%3A%2F%2Ft.me%2FKhmerXBot%2Fapp" />
              </div>
              <a class="block w-full rounded-xl bg-white px-6 py-3 font-bold text-blue-600 shadow-md hover:shadow-lg transition-shadow relative z-10" href="https://t.me/KhmerXBot/app">
                {sidebar_cta_btn}
              </a>
            </div>
          </div>
          
        </div>
      </section>

      <!-- Footer -->
      <footer class="bg-slate-950 px-5 py-12 text-slate-400">
        <div class="mx-auto max-w-[1200px]">
          <div class="flex flex-col md:flex-row items-center justify-between gap-4 text-sm">
            <div>© <span data-year></span> KhmerX. All rights reserved.</div>
            <div class="flex gap-6">
              <a href="/{lang}/terms" class="hover:text-white transition-colors">Terms</a>
              <a href="/{lang}/privacy" class="hover:text-white transition-colors">Privacy Policy</a>
            </div>
          </div>
        </div>
      </footer>
    </main>
  </body>
</html>"""

content_zh = {
    "lang": "zh",
    "title": "KhmerX 内容中心 | ABA 与 Telegram 借款教程",
    "desc": "了解柬埔寨本地小额周转、ABA 转账教程与 Telegram 金融工具的使用方法。KhmerX 官方博客为您提供最实用的金融指南。",
    "keywords": "柬埔寨 ABA, 金边借款, Telegram Mini App, Cambodia micro lending, ABA transfer tutorial",
    "km_active": "", "en_active": "", "zh_active": "bg-white shadow-sm text-blue-600",
    "nav_borrow": "如何借款", "nav_fees": "费用说明", "nav_faq": "FAQ", "nav_contact": "联系我们", "nav_cta": "打开 Mini App",
    
    "hero_title": "KhmerX 内容中心",
    "hero_subtitle": "了解 ABA、Telegram 与柬埔寨本地小额周转的实用指南与教程。",
    
    "cat_aba": "ABA 教程", "cat_tg": "Telegram 教程", "cat_loan": "小额周转", "cat_pp": "金边生活",
    
    "feat_1_title": "如何安全快速地使用 ABA 银行转账？",
    "feat_1_desc": "在柬埔寨，ABA 银行转账是最常用的支付方式。本文详细图解如何通过 ABA 手机银行安全地进行个人转账与收款验证。",
    "read_more": "阅读全文",
    
    "list_2_title": "Telegram Mini App 金融工具完全指南",
    "list_2_desc": "无需下载额外 App，在 Telegram 内即可完成借款申请。了解 KhmerX 是如何通过 Mini App 保护您的隐私与安全的。",
    "list_3_title": "申请小额短期周转前必须知道的 3 件事",
    "list_3_desc": "借款前确认到账金额、了解平息法计算方式、以及重视信用记录对您未来借款额度的影响。",
    
    "tag_title": "热门搜索",
    "tag_1": "柬埔寨 ABA", "tag_2": "金边借款", "tag_3": "Telegram 教程", "tag_4": "小额借款注意事项",
    
    "sidebar_cta_title": "立即打开 KhmerX",
    "sidebar_cta_desc": "无需下载，在 Telegram 极速体验",
    "sidebar_cta_btn": "打开 Telegram"
}

content_en = {
    "lang": "en",
    "title": "KhmerX Blog | ABA & Telegram Lending Guides",
    "desc": "Learn about Cambodia micro lending, ABA transfer tutorials, and Telegram finance tools. The official KhmerX blog provides practical financial guides.",
    "keywords": "Cambodia micro lending, ABA transfer, Telegram finance, Phnom Penh loan, Cambodia payment guide",
    "km_active": "", "en_active": "bg-white shadow-sm text-blue-600", "zh_active": "",
    "nav_borrow": "How to Borrow", "nav_fees": "Fees", "nav_faq": "FAQ", "nav_contact": "Contact", "nav_cta": "Open Mini App",
    
    "hero_title": "KhmerX Blog",
    "hero_subtitle": "Learn about ABA transfers, Telegram tools, and practical guides for local micro lending in Cambodia.",
    
    "cat_aba": "ABA Guides", "cat_tg": "Telegram Tools", "cat_loan": "Micro Lending", "cat_pp": "Phnom Penh Life",
    
    "feat_1_title": "How to Use ABA Bank Transfer Safely and Quickly?",
    "feat_1_desc": "ABA transfer is the most common payment method in Cambodia. This article provides a detailed visual guide on how to safely transfer and verify receipts via the ABA Mobile App.",
    "read_more": "Read Article",
    
    "list_2_title": "Complete Guide to Telegram Mini App Finance Tools",
    "list_2_desc": "No need to download extra apps, complete your loan application right inside Telegram. Learn how KhmerX protects your privacy using Mini Apps.",
    "list_3_title": "3 Things You Must Know Before Applying for a Micro Loan",
    "list_3_desc": "Confirm actual receive amounts, understand flat-rate fee calculations, and learn why your credit record matters for future limits.",
    
    "tag_title": "Trending Topics",
    "tag_1": "Cambodia Micro Lending", "tag_2": "ABA Transfer", "tag_3": "Telegram Finance", "tag_4": "Phnom Penh Loan",
    
    "sidebar_cta_title": "Open KhmerX Now",
    "sidebar_cta_desc": "No download needed. Experience it in Telegram.",
    "sidebar_cta_btn": "Open Telegram"
}

content_km = {
    "lang": "km",
    "title": "ប្លុក KhmerX | ការណែនាំអំពី ABA និង Telegram",
    "desc": "ស្វែងយល់ពីការខ្ចីប្រាក់តូចនៅកម្ពុជា ការប្រើប្រាស់ ABA និងឧបករណ៍ហិរញ្ញវត្ថុ Telegram ។ ប្លុកផ្លូវការរបស់ KhmerX ផ្តល់នូវការណែនាំជាក់ស្តែង។",
    "keywords": "ខ្ចីលុយ ABA, Telegram Cambodia, ABA transfer, Cambodia micro lending, ប្លុក KhmerX",
    "km_active": "bg-white shadow-sm text-blue-600", "en_active": "", "zh_active": "",
    "nav_borrow": "របៀបខ្ចីប្រាក់", "nav_fees": "ថ្លៃសេវា", "nav_faq": "សំណួរដែលសួរញឹកញាប់", "nav_contact": "ទំនាក់ទំនង", "nav_cta": "បើក Mini App",
    
    "hero_title": "ប្លុក KhmerX",
    "hero_subtitle": "ស្វែងយល់ពីការប្រើប្រាស់ ABA ឧបករណ៍ Telegram និងការណែនាំជាក់ស្តែងសម្រាប់ការខ្ចីប្រាក់តូចនៅកម្ពុជា។",
    
    "cat_aba": "ការណែនាំ ABA", "cat_tg": "ការណែនាំ Telegram", "cat_loan": "ខ្ចីប្រាក់តូច", "cat_pp": "ជីវិតភ្នំពេញ",
    
    "feat_1_title": "តើត្រូវប្រើប្រាស់ការផ្ទេរប្រាក់ ABA ឱ្យមានសុវត្ថិភាពយ៉ាងដូចម្តេច?",
    "feat_1_desc": "នៅកម្ពុជា ការផ្ទេរប្រាក់ ABA គឺជាវិធីសាស្ត្រទូទាត់ទូទៅបំផុត។ អត្ថបទនេះបង្ហាញលម្អិតពីរបៀបផ្ទេរនិងផ្ទៀងផ្ទាត់ដោយសុវត្ថិភាពតាមរយៈ ABA Mobile App ។",
    "read_more": "អានអត្ថបទ",
    
    "list_2_title": "ការណែនាំពេញលេញអំពីឧបករណ៍ហិរញ្ញវត្ថុ Telegram Mini App",
    "list_2_desc": "មិនចាំបាច់ទាញយកកម្មវិធីបន្ថែមទេ បញ្ចប់ការស្នើសុំខ្ចីប្រាក់ក្នុង Telegram តែម្តង។ ស្វែងយល់ពីរបៀបដែល KhmerX ការពារឯកជនភាពរបស់អ្នក។",
    "list_3_title": "រឿង 3 យ៉ាងដែលត្រូវដឹងមុនពេលខ្ចីប្រាក់តូច",
    "list_3_desc": "បញ្ជាក់ចំនួនប្រាក់ទទួលបានជាក់ស្តែង យល់ពីការគណនាថ្លៃសេវា និងដឹងពីសារៈសំខាន់នៃប្រវត្តិឥណទានរបស់អ្នក។",
    
    "tag_title": "ប្រធានបទពេញនិយម",
    "tag_1": "ខ្ចីលុយ ABA", "tag_2": "Telegram Cambodia", "tag_3": "ការណែនាំ ABA", "tag_4": "ខ្ចីប្រាក់តូច",
    
    "sidebar_cta_title": "បើក KhmerX ឥឡូវនេះ",
    "sidebar_cta_desc": "មិនបាច់ទាញយក ប្រើប្រាស់ក្នុង Telegram",
    "sidebar_cta_btn": "បើក Telegram"
}

with open(r'D:\projects\khmerx\frontend\website\zh\blog\index.html', 'w', encoding='utf-8') as f:
    f.write(blog_template.format(**content_zh))
with open(r'D:\projects\khmerx\frontend\website\en\blog\index.html', 'w', encoding='utf-8') as f:
    f.write(blog_template.format(**content_en))
with open(r'D:\projects\khmerx\frontend\website\km\blog\index.html', 'w', encoding='utf-8') as f:
    f.write(blog_template.format(**content_km))

print("Blog list pages generated.")
