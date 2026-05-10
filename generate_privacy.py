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
    <meta property="og:url" content="https://khmerx.org/{lang}/privacy" />
    <meta property="og:image" content="https://khmerx.org/logo.jpg" />
    <meta name="twitter:card" content="summary" />
    <meta name="twitter:title" content="{title}" />
    <meta name="twitter:description" content="{desc}" />
    <link rel="canonical" href="https://khmerx.org/{lang}/privacy" />
    <link rel="alternate" href="https://khmerx.org/km/privacy" hreflang="km" />
    <link rel="alternate" href="https://khmerx.org/en/privacy" hreflang="en" />
    <link rel="alternate" href="https://khmerx.org/zh/privacy" hreflang="zh" />
    <link rel="alternate" href="https://khmerx.org/km/privacy" hreflang="x-default" />
    <script type="application/ld+json">
      {{
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "KhmerX",
        "url": "https://khmerx.org",
        "logo": "https://khmerx.org/logo.jpg",
        "contactPoint": {{
          "@type": "ContactPoint",
          "contactType": "customer support",
          "email": "support@khmerx.org",
          "availableLanguage": ["Khmer", "English", "Chinese"]
        }},
        "sameAs": [
          "https://t.me/KhmerXBot"
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
              <a data-lang="km" class="rounded-lg px-3 py-1.5 transition-colors font-medium {km_active}" href="/km/privacy">ខ្មែរ</a>
              <a data-lang="en" class="rounded-lg px-3 py-1.5 transition-colors font-medium {en_active}" href="/en/privacy">EN</a>
              <a data-lang="zh" class="rounded-lg px-3 py-1.5 transition-colors font-medium {zh_active}" href="/zh/privacy">中文</a>
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
        <div class="absolute inset-0 bg-[url('https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=Dark%20blue%20data%20security%20privacy%20lock%20shield%20technology%20background%20abstract%20modern%20clean%20business%20style&image_size=landscape_16_9')] bg-cover bg-center opacity-30 mix-blend-overlay"></div>
        <div class="relative mx-auto max-w-[1200px] px-5 py-20 md:py-28">
          <div class="grid gap-12 md:grid-cols-2 md:items-center">
            <div class="max-w-xl z-10">
              <div class="mb-6 inline-flex rounded-full bg-blue-500/20 px-4 py-2 text-sm font-bold text-blue-300 border border-blue-500/30">
                <svg class="w-4 h-4 inline mr-2 -mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path></svg>
                KhmerX Privacy & Data
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
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
                </svg>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 内容区 -->
      <section class="mx-auto max-w-[800px] px-5 py-20 -mt-10 relative z-20">
        <div class="bg-white rounded-3xl p-8 md:p-12 shadow-xl border border-slate-100 prose prose-slate prose-blue max-w-none">
          
          <h2 class="text-2xl font-bold text-slate-900 mb-6">{sec1_title}</h2>
          <div class="grid sm:grid-cols-2 gap-6 not-prose mb-10">
            <div class="bg-slate-50 rounded-2xl p-6 border border-slate-100">
              <h4 class="font-bold text-slate-900 mb-4 flex items-center gap-2">
                <svg class="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207"></path></svg>
                {sec1_box1_title}
              </h4>
              <ul class="space-y-2 text-sm text-slate-600">
                <li class="flex items-center gap-2"><div class="w-1.5 h-1.5 rounded-full bg-blue-400"></div>Telegram ID</li>
                <li class="flex items-center gap-2"><div class="w-1.5 h-1.5 rounded-full bg-blue-400"></div>{sec1_box1_item1}</li>
                <li class="flex items-center gap-2"><div class="w-1.5 h-1.5 rounded-full bg-blue-400"></div>{sec1_box1_item2}</li>
              </ul>
            </div>
            <div class="bg-slate-50 rounded-2xl p-6 border border-slate-100">
              <h4 class="font-bold text-slate-900 mb-4 flex items-center gap-2">
                <svg class="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"></path></svg>
                {sec1_box2_title}
              </h4>
              <ul class="space-y-2 text-sm text-slate-600">
                <li class="flex items-center gap-2"><div class="w-1.5 h-1.5 rounded-full bg-blue-400"></div>{sec1_box2_item1}</li>
                <li class="flex items-center gap-2"><div class="w-1.5 h-1.5 rounded-full bg-blue-400"></div>{sec1_box2_item2}</li>
                <li class="flex items-center gap-2"><div class="w-1.5 h-1.5 rounded-full bg-blue-400"></div>{sec1_box2_item3}</li>
              </ul>
            </div>
          </div>

          <h2 class="text-2xl font-bold text-slate-900 mt-12 mb-6">{sec2_title}</h2>
          <ul class="not-prose grid sm:grid-cols-2 gap-4 mb-10">
            <li class="flex items-center gap-3 bg-blue-50/50 px-4 py-3 rounded-xl text-slate-700">
              <svg class="w-5 h-5 text-blue-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
              {sec2_item1}
            </li>
            <li class="flex items-center gap-3 bg-blue-50/50 px-4 py-3 rounded-xl text-slate-700">
              <svg class="w-5 h-5 text-blue-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
              {sec2_item2}
            </li>
            <li class="flex items-center gap-3 bg-blue-50/50 px-4 py-3 rounded-xl text-slate-700">
              <svg class="w-5 h-5 text-blue-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
              {sec2_item3}
            </li>
            <li class="flex items-center gap-3 bg-blue-50/50 px-4 py-3 rounded-xl text-slate-700">
              <svg class="w-5 h-5 text-blue-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
              {sec2_item4}
            </li>
          </ul>

          <h2 class="text-2xl font-bold text-slate-900 mt-12 mb-6">{sec3_title}</h2>
          <div class="bg-yellow-50 border border-yellow-200 rounded-2xl p-6 not-prose mb-10">
            <h4 class="font-bold text-yellow-900 mb-2">{sec3_sub1}</h4>
            <p class="text-yellow-800 text-sm mb-4">{sec3_desc1}</p>
            <h4 class="font-bold text-yellow-900 mb-2">{sec3_sub2}</h4>
            <p class="text-yellow-800 text-sm mb-4">{sec3_desc2}</p>
            <div class="bg-white/60 px-4 py-3 rounded-lg border border-yellow-200 text-sm font-medium text-yellow-900">
              ⚠️ {sec3_notice}
            </div>
          </div>

          <h2 class="text-2xl font-bold text-slate-900 mt-12 mb-6">{sec4_title}</h2>
          <div class="space-y-4 text-slate-600 mb-10">
            <p>{sec4_desc}</p>
            <div class="flex flex-wrap gap-3 not-prose">
              <span class="bg-slate-100 text-slate-700 px-3 py-1 rounded-full text-sm font-medium">HTTPS</span>
              <span class="bg-slate-100 text-slate-700 px-3 py-1 rounded-full text-sm font-medium">Database Access Control</span>
              <span class="bg-slate-100 text-slate-700 px-3 py-1 rounded-full text-sm font-medium">Risk Monitoring</span>
            </div>
            <p class="text-sm text-slate-500 italic">{sec4_notice}</p>
          </div>

          <h2 class="text-2xl font-bold text-slate-900 mt-12 mb-6">{sec5_title}</h2>
          <p class="text-slate-600 mb-6">{sec5_desc}</p>

        </div>
      </section>

      <!-- 联系方式 -->
      <section class="mx-auto max-w-[800px] px-5 pb-24">
        <div class="bg-blue-600 rounded-[2rem] p-10 text-center text-white shadow-xl relative overflow-hidden">
          <div class="absolute inset-0 bg-[url('https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=Blue%20technology%20abstract%20waves&image_size=landscape_16_9')] bg-cover bg-center opacity-20 mix-blend-overlay"></div>
          <div class="relative z-10">
            <h2 class="text-2xl md:text-3xl font-bold mb-4">{contact_title}</h2>
            <p class="text-blue-100 mb-8">{contact_desc}</p>
            <a class="inline-flex justify-center items-center rounded-xl bg-white px-8 py-4 text-lg font-bold text-blue-600 shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-300" href="https://t.me/KhmerXBot">
              <svg class="w-6 h-6 mr-2" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.74-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .38z"/></svg>
              {contact_btn}
            </a>
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
              <a href="/km/privacy" class="hover:text-white transition-colors">ខ្មែរ</a>
              <a href="/en/privacy" class="hover:text-white transition-colors">English</a>
              <a href="/zh/privacy" class="hover:text-white transition-colors">中文</a>
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
    "title": "KhmerX 隐私政策 | Telegram 与 ABA 数据说明",
    "desc": "KhmerX 重视用户隐私与数据安全。了解我们收集哪些数据、如何使用数据以及 Telegram 与 ABA 的数据说明。",
    "keywords": "KhmerX privacy, Telegram privacy Cambodia, ABA data policy, Cambodia privacy policy",
    "nav_borrow": "如何借款",
    "nav_fees": "费用说明",
    "nav_contact": "联系我们",
    "nav_cta": "打开 Mini App",
    "hero_title": "隐私政策",
    "hero_subtitle": "KhmerX 重视用户隐私与数据安全。",
    "sec1_title": "KhmerX 收集哪些数据",
    "sec1_box1_title": "Telegram 信息",
    "sec1_box1_item1": "昵称",
    "sec1_box1_item2": "语言设置",
    "sec1_box2_title": "ABA 与交易信息",
    "sec1_box2_item1": "ABA 账号与姓名",
    "sec1_box2_item2": "借还款记录",
    "sec1_box2_item3": "交易凭证",
    "sec2_title": "数据如何使用",
    "sec2_item1": "用户登录与身份验证",
    "sec2_item2": "借款服务信息匹配",
    "sec2_item3": "风控检测与安全审计",
    "sec2_item4": "交易通知与还款提醒",
    "sec3_title": "Telegram 与 ABA 数据说明",
    "sec3_sub1": "Telegram",
    "sec3_desc1": "KhmerX 主要通过 Telegram Mini App 提供服务。",
    "sec3_sub2": "ABA",
    "sec3_desc2": "ABA 信息仅用于用户之间的转账与还款确认。",
    "sec3_notice": "KhmerX 绝不会公开展示用户的 ABA 敏感信息。",
    "sec4_title": "数据安全说明",
    "sec4_desc": "我们采取多重安全措施保护您的数据，包括但不限于：",
    "sec4_notice": "任何互联网服务都无法保证100%的安全，请您也妥善保管好自己的账号。",
    "sec5_title": "用户权利",
    "sec5_desc": "用户可以随时修改 ABA 信息、语言设置、联系客服获取帮助，或者在后期请求删除账户。",
    "contact_title": "有任何隐私相关问题？",
    "contact_desc": "请通过官方 Telegram 联系 KhmerX 客服获取帮助。",
    "contact_btn": "联系 Telegram 客服",
    "footer_desc": "KhmerX 是本地小额周转信息服务平台，不保证借款成功，不提供担保。"
}

content_en = {
    "lang": "en",
    "zh_active": "",
    "en_active": "bg-white shadow-sm text-blue-600",
    "km_active": "",
    "title": "KhmerX Privacy Policy | Telegram & ABA Data Guidelines",
    "desc": "KhmerX values your privacy and data security. Learn what data we collect, how it's used, and our guidelines for Telegram and ABA data.",
    "keywords": "KhmerX privacy, Telegram privacy Cambodia, ABA data policy, Cambodia privacy policy",
    "nav_borrow": "How to Borrow",
    "nav_fees": "Fees",
    "nav_contact": "Contact",
    "nav_cta": "Open Mini App",
    "hero_title": "Privacy Policy",
    "hero_subtitle": "KhmerX values your privacy and data security.",
    "sec1_title": "What Data We Collect",
    "sec1_box1_title": "Telegram Information",
    "sec1_box1_item1": "Nickname",
    "sec1_box1_item2": "Language Settings",
    "sec1_box2_title": "ABA & Transaction Data",
    "sec1_box2_item1": "ABA Account & Name",
    "sec1_box2_item2": "Loan & Repayment Records",
    "sec1_box2_item3": "Transaction Receipts",
    "sec2_title": "How We Use Your Data",
    "sec2_item1": "User Login & Authentication",
    "sec2_item2": "Loan Service Matching",
    "sec2_item3": "Risk Monitoring & Security",
    "sec2_item4": "Transaction & Repayment Alerts",
    "sec3_title": "Telegram & ABA Data Guidelines",
    "sec3_sub1": "Telegram",
    "sec3_desc1": "KhmerX primarily provides services via the Telegram Mini App.",
    "sec3_sub2": "ABA",
    "sec3_desc2": "ABA information is used solely for transfers and repayment confirmation between users.",
    "sec3_notice": "KhmerX will never publicly display users' sensitive ABA information.",
    "sec4_title": "Data Security",
    "sec4_desc": "We implement multiple security measures to protect your data, including:",
    "sec4_notice": "No internet service can guarantee 100% security. Please keep your account safe.",
    "sec5_title": "User Rights",
    "sec5_desc": "Users can modify ABA information, language settings, contact support, or request account deletion.",
    "contact_title": "Privacy Questions?",
    "contact_desc": "Please contact KhmerX support via official Telegram for assistance.",
    "contact_btn": "Contact Telegram Support",
    "footer_desc": "KhmerX is a local micro-lending information platform. It does not guarantee successful loans or provide guarantees."
}

content_km = {
    "lang": "km",
    "zh_active": "",
    "en_active": "",
    "km_active": "bg-white shadow-sm text-blue-600",
    "title": "គោលការណ៍ឯកជនភាព KhmerX | ព័ត៌មានទិន្នន័យ Telegram និង ABA",
    "desc": "KhmerX យកចិត្តទុកដាក់លើឯកជនភាព និងសុវត្ថិភាពទិន្នន័យរបស់អ្នក។",
    "keywords": "KhmerX privacy, Telegram privacy Cambodia, ABA data policy, Cambodia privacy policy",
    "nav_borrow": "របៀបខ្ចីប្រាក់",
    "nav_fees": "ការប្រាក់",
    "nav_contact": "ទំនាក់ទំនង",
    "nav_cta": "បើក Mini App",
    "hero_title": "គោលការណ៍ឯកជនភាព",
    "hero_subtitle": "KhmerX យកចិត្តទុកដាក់លើឯកជនភាព និងសុវត្ថិភាពទិន្នន័យរបស់អ្នក។",
    "sec1_title": "ទិន្នន័យដែលយើងប្រមូល",
    "sec1_box1_title": "ព័ត៌មាន Telegram",
    "sec1_box1_item1": "ឈ្មោះហៅក្រៅ",
    "sec1_box1_item2": "ការកំណត់ភាសា",
    "sec1_box2_title": "ទិន្នន័យ ABA និងប្រតិបត្តិការ",
    "sec1_box2_item1": "គណនី ABA និងឈ្មោះ",
    "sec1_box2_item2": "កំណត់ត្រាខ្ចីប្រាក់ និងសងប្រាក់",
    "sec1_box2_item3": "បង្កាន់ដៃប្រតិបត្តិការ",
    "sec2_title": "របៀបដែលយើងប្រើប្រាស់ទិន្នន័យ",
    "sec2_item1": "ការចូលប្រើ និងបញ្ជាក់អត្តសញ្ញាណ",
    "sec2_item2": "ការផ្គូផ្គងសេវាខ្ចីប្រាក់",
    "sec2_item3": "ការត្រួតពិនិត្យហានិភ័យ និងសុវត្ថិភាព",
    "sec2_item4": "ការជូនដំណឹងអំពីប្រតិបត្តិការ និងការសងប្រាក់",
    "sec3_title": "គោលការណ៍ទិន្នន័យ Telegram និង ABA",
    "sec3_sub1": "Telegram",
    "sec3_desc1": "KhmerX ផ្តល់សេវាកម្មជាចម្បងតាមរយៈ Telegram Mini App។",
    "sec3_sub2": "ABA",
    "sec3_desc2": "ព័ត៌មាន ABA ត្រូវបានប្រើប្រាស់សម្រាប់តែការផ្ទេរប្រាក់ និងការបញ្ជាក់រវាងអ្នកប្រើប្រាស់ប៉ុណ្ណោះ។",
    "sec3_notice": "KhmerX នឹងមិនបង្ហាញព័ត៌មាន ABA រសើបរបស់អ្នកប្រើប្រាស់ជាសាធារណៈឡើយ។",
    "sec4_title": "សុវត្ថិភាពទិន្នន័យ",
    "sec4_desc": "យើងអនុវត្តវិធានការសុវត្ថិភាពជាច្រើនដើម្បីការពារទិន្នន័យរបស់អ្នក រួមមាន៖",
    "sec4_notice": "គ្មានសេវាកម្មអ៊ីនធឺណិតណាមួយអាចធានាសុវត្ថិភាព 100% នោះទេ។ សូមរក្សាគណនីរបស់អ្នកឱ្យមានសុវត្ថិភាព។",
    "sec5_title": "សិទ្ធិអ្នកប្រើប្រាស់",
    "sec5_desc": "អ្នកប្រើប្រាស់អាចកែប្រែព័ត៌មាន ABA ការកំណត់ភាសា ទាក់ទងផ្នែកជំនួយ ឬស្នើសុំលុបគណនីបាន។",
    "contact_title": "មានសំណួរអំពីឯកជនភាពទេ?",
    "contact_desc": "សូមទាក់ទងផ្នែកជំនួយ KhmerX តាមរយៈ Telegram ផ្លូវការសម្រាប់ជំនួយ។",
    "contact_btn": "ទាក់ទងផ្នែកជំនួយ Telegram",
    "footer_desc": "KhmerX គឺជាវេទិកាព័ត៌មានខ្ចីប្រាក់ខ្នាតតូចក្នុងស្រុក។ មិនធានាថាការខ្ចីប្រាក់នឹងទទួលបានជោគជ័យ ឬផ្តល់ការធានាឡើយ។"
}

import os

for c in [content_zh, content_en, content_km]:
    html = template.format(**c)
    lang = c['lang']
    os.makedirs(f"frontend/website/{lang}/privacy", exist_ok=True)
    with open(f"frontend/website/{lang}/privacy/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated {lang}/privacy/index.html")

