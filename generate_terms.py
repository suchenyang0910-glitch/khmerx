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
    <meta property="og:url" content="https://khmerx.org/{lang}/terms" />
    <meta property="og:image" content="https://khmerx.org/logo.jpg" />
    <meta name="twitter:card" content="summary" />
    <meta name="twitter:title" content="{title}" />
    <meta name="twitter:description" content="{desc}" />
    <link rel="canonical" href="https://khmerx.org/{lang}/terms" />
    <link rel="alternate" href="https://khmerx.org/km/terms" hreflang="km" />
    <link rel="alternate" href="https://khmerx.org/en/terms" hreflang="en" />
    <link rel="alternate" href="https://khmerx.org/zh/terms" hreflang="zh" />
    <link rel="alternate" href="https://khmerx.org/km/terms" hreflang="x-default" />
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
              <a data-lang="km" class="rounded-lg px-3 py-1.5 transition-colors font-medium {km_active}" href="/km/terms">ខ្មែរ</a>
              <a data-lang="en" class="rounded-lg px-3 py-1.5 transition-colors font-medium {en_active}" href="/en/terms">EN</a>
              <a data-lang="zh" class="rounded-lg px-3 py-1.5 transition-colors font-medium {zh_active}" href="/zh/terms">中文</a>
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
        <div class="absolute inset-0 bg-[url('https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=Dark%20blue%20legal%20document%20contract%20rules%20shield%20technology%20background%20abstract%20modern%20clean%20business%20style&image_size=landscape_16_9')] bg-cover bg-center opacity-30 mix-blend-overlay"></div>
        <div class="relative mx-auto max-w-[1200px] px-5 py-20 md:py-28">
          <div class="grid gap-12 md:grid-cols-2 md:items-center">
            <div class="max-w-xl z-10">
              <div class="mb-6 inline-flex rounded-full bg-blue-500/20 px-4 py-2 text-sm font-bold text-blue-300 border border-blue-500/30">
                <svg class="w-4 h-4 inline mr-2 -mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>
                KhmerX Rules & Agreements
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
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 内容区 -->
      <section class="mx-auto max-w-[800px] px-5 py-20 -mt-10 relative z-20">
        <div class="bg-white rounded-3xl p-8 md:p-12 shadow-xl border border-slate-100 prose prose-slate prose-blue max-w-none">
          
          <div class="bg-blue-50 border border-blue-100 rounded-2xl p-6 not-prose mb-10">
            <h2 class="text-xl font-bold text-blue-900 mb-4 flex items-center gap-2">
              <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
              {sec1_title}
            </h2>
            <p class="text-blue-800 text-sm mb-4 leading-relaxed">{sec1_desc}</p>
            <ul class="space-y-2 text-sm font-bold text-blue-900">
              <li class="flex items-center gap-2"><svg class="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>{sec1_li1}</li>
              <li class="flex items-center gap-2"><svg class="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>{sec1_li2}</li>
              <li class="flex items-center gap-2"><svg class="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>{sec1_li3}</li>
              <li class="flex items-center gap-2"><svg class="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>{sec1_li4}</li>
            </ul>
          </div>

          <h2 class="text-2xl font-bold text-slate-900 mt-12 mb-6">{sec2_title}</h2>
          <ul class="space-y-2">
            <li>{sec2_li1}</li>
            <li>{sec2_li2}</li>
            <li>{sec2_li3}</li>
            <li>{sec2_li4}</li>
          </ul>
          <p class="text-sm italic mt-4 text-slate-500">{sec2_notice}</p>

          <h2 class="text-2xl font-bold text-slate-900 mt-12 mb-6">{sec3_title}</h2>
          <p><strong>{sec3_sub1}</strong><br/>{sec3_desc1}</p>
          <p><strong>{sec3_sub2}</strong><br/>{sec3_desc2}</p>
          <p><strong>{sec3_sub3}</strong><br/>{sec3_desc3}</p>

          <h2 class="text-2xl font-bold text-slate-900 mt-12 mb-6">{sec4_title}</h2>
          <p><strong>{sec4_sub1}</strong><br/>{sec4_desc1}</p>
          <p><strong>{sec4_sub2}</strong><br/>{sec4_desc2}</p>
          <p><strong>{sec4_sub3}</strong><br/>{sec4_desc3}</p>

          <div class="bg-red-50 border border-red-100 rounded-2xl p-6 not-prose mb-10 mt-12">
            <h2 class="text-xl font-bold text-red-900 mb-4 flex items-center gap-2">
              <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
              {sec5_title}
            </h2>
            <p class="text-red-800 text-sm mb-4 leading-relaxed">{sec5_desc}</p>
            <ul class="space-y-2 text-sm text-red-800 list-disc list-inside">
              <li>{sec5_li1}</li>
              <li>{sec5_li2}</li>
              <li>{sec5_li3}</li>
              <li>{sec5_li4}</li>
            </ul>
          </div>

          <h2 class="text-2xl font-bold text-slate-900 mt-12 mb-6">{sec6_title}</h2>
          <ul class="space-y-2">
            <li>{sec6_li1}</li>
            <li>{sec6_li2}</li>
            <li>{sec6_li3}</li>
            <li>{sec6_li4}</li>
            <li>{sec6_li5}</li>
          </ul>
          <p class="text-sm font-medium mt-4 text-slate-700">{sec6_notice}</p>

          <h2 class="text-2xl font-bold text-slate-900 mt-12 mb-6">{sec7_title}</h2>
          <p>{sec7_desc}</p>
          <ul class="space-y-2 font-medium">
            <li>{sec7_li1}</li>
            <li>{sec7_li2}</li>
            <li>{sec7_li3}</li>
            <li>{sec7_li4}</li>
          </ul>

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
              <a href="/km/terms" class="hover:text-white transition-colors">ខ្មែរ</a>
              <a href="/en/terms" class="hover:text-white transition-colors">English</a>
              <a href="/zh/terms" class="hover:text-white transition-colors">中文</a>
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
    "title": "KhmerX 用户协议 | Telegram ABA 小额周转",
    "desc": "使用 KhmerX 前，请确认并理解相关规则。KhmerX 是面向柬埔寨用户的小额周转信息服务平台。",
    "keywords": "KhmerX terms, Cambodia loan terms, Telegram finance terms, ABA loan agreement",
    "nav_borrow": "如何借款",
    "nav_fees": "费用说明",
    "nav_contact": "联系我们",
    "nav_cta": "打开 Mini App",
    "hero_title": "用户协议",
    "hero_subtitle": "使用 KhmerX 前，请确认并理解相关规则。",
    "sec1_title": "KhmerX 服务说明",
    "sec1_desc": "KhmerX 是面向柬埔寨用户的小额周转信息服务平台。",
    "sec1_li1": "KhmerX 不是银行",
    "sec1_li2": "KhmerX 不吸收存款",
    "sec1_li3": "KhmerX 不保证借款成功",
    "sec1_li4": "KhmerX 不保证收益",
    "sec2_title": "用户资格",
    "sec2_li1": "使用 Telegram 进行注册与操作",
    "sec2_li2": "提供真实有效的 ABA 账户信息",
    "sec2_li3": "提供真实身份信息",
    "sec2_li4": "遵守当地法律法规",
    "sec2_notice": "KhmerX 有权限制或拒绝高风险账户的使用。",
    "sec3_title": "借款规则",
    "sec3_sub1": "借款说明",
    "sec3_desc1": "借款前请务必确认借款金额、到账金额、到期还款金额与借款期限。",
    "sec3_sub2": "费用说明",
    "sec3_desc2": "借款可能包含固定费用与服务费。",
    "sec3_sub3": "用户确认",
    "sec3_desc3": "用户提交借款即视为确认相关费用与规则。",
    "sec4_title": "还款规则",
    "sec4_sub1": "还款方式",
    "sec4_desc1": "用户需通过 ABA 账户完成还款转账。",
    "sec4_sub2": "凭证上传",
    "sec4_desc2": "还款转账完成后，需在平台上传还款凭证截图。",
    "sec4_sub3": "到期提醒",
    "sec4_desc3": "系统可能在到期前 24 小时发送提醒。",
    "sec5_title": "风险与平台免责",
    "sec5_desc": "KhmerX 仅为信息服务平台，不承担任何资金交易风险。",
    "sec5_li1": "平台不保证借款一定成功或按时收回。",
    "sec5_li2": "平台不承担借款损失、交易损失或用户纠纷。",
    "sec5_li3": "用户需自行确认交易对方的真实性与风险。",
    "sec5_li4": "任何交易都可能存在第三方风险，平台不予担保。",
    "sec6_title": "违规行为",
    "sec6_li1": "提供虚假信息",
    "sec6_li2": "多账号恶意刷信用或额度",
    "sec6_li3": "伪造交易或还款凭证",
    "sec6_li4": "恶意逾期或拒绝还款",
    "sec6_li5": "其他任何欺诈行为",
    "sec6_notice": "KhmerX 有权永久限制违规账户。",
    "sec7_title": "平台限制与安全",
    "sec7_desc": "为了保护平台与用户安全，KhmerX 有权：",
    "sec7_li1": "限制高风险账户",
    "sec7_li2": "冻结异常交易行为",
    "sec7_li3": "动态调整或限制借款额度",
    "sec7_li4": "拒绝向特定用户提供服务",
    "contact_title": "有任何协议相关问题？",
    "contact_desc": "请通过官方 Telegram 联系 KhmerX 客服。",
    "contact_btn": "联系 Telegram 客服",
    "footer_desc": "KhmerX 是本地小额周转信息服务平台，不保证借款成功，不提供担保。"
}

content_en = {
    "lang": "en",
    "zh_active": "",
    "en_active": "bg-white shadow-sm text-blue-600",
    "km_active": "",
    "title": "KhmerX Terms of Service | Telegram ABA Micro Lending",
    "desc": "Before using KhmerX, please read and understand our rules. KhmerX is a micro-lending information platform for users in Cambodia.",
    "keywords": "KhmerX terms, Cambodia loan terms, Telegram finance terms, ABA loan agreement",
    "nav_borrow": "How to Borrow",
    "nav_fees": "Fees",
    "nav_contact": "Contact",
    "nav_cta": "Open Mini App",
    "hero_title": "Terms of Service",
    "hero_subtitle": "Before using KhmerX, please confirm and understand the relevant rules.",
    "sec1_title": "KhmerX Service Statement",
    "sec1_desc": "KhmerX is a micro-lending information matching platform for users in Cambodia.",
    "sec1_li1": "KhmerX is NOT a bank",
    "sec1_li2": "KhmerX does NOT accept deposits",
    "sec1_li3": "KhmerX does NOT guarantee successful loans",
    "sec1_li4": "KhmerX does NOT guarantee returns",
    "sec2_title": "User Eligibility",
    "sec2_li1": "Use Telegram for registration and operations",
    "sec2_li2": "Provide genuine and valid ABA account information",
    "sec2_li3": "Provide genuine identity information",
    "sec2_li4": "Comply with local laws and regulations",
    "sec2_notice": "KhmerX reserves the right to restrict or refuse high-risk accounts.",
    "sec3_title": "Borrowing Rules",
    "sec3_sub1": "Borrowing Details",
    "sec3_desc1": "Before borrowing, you must confirm the loan amount, received amount, repayment amount, and loan term.",
    "sec3_sub2": "Fees",
    "sec3_desc2": "Loans may include fixed fees and service charges.",
    "sec3_sub3": "User Confirmation",
    "sec3_desc3": "Submitting a loan request constitutes confirmation of all related fees and rules.",
    "sec4_title": "Repayment Rules",
    "sec4_sub1": "Repayment Method",
    "sec4_desc1": "Users must repay via an ABA transfer.",
    "sec4_sub2": "Receipt Upload",
    "sec4_desc2": "After transferring, users must upload a screenshot of the repayment receipt.",
    "sec4_sub3": "Due Date Reminder",
    "sec4_desc3": "The system may send a reminder 24 hours before the due date.",
    "sec5_title": "Risks & Platform Disclaimer",
    "sec5_desc": "KhmerX is merely an information platform and bears no responsibility for transaction risks.",
    "sec5_li1": "The platform does not guarantee loans will be funded or repaid on time.",
    "sec5_li2": "The platform is not liable for loan losses, transaction losses, or user disputes.",
    "sec5_li3": "Users must verify the authenticity and risk of counterparties themselves.",
    "sec5_li4": "Any transaction may involve third-party risks which the platform does not guarantee.",
    "sec6_title": "Violations",
    "sec6_li1": "Providing false information",
    "sec6_li2": "Using multiple accounts to manipulate credit or limits",
    "sec6_li3": "Forging transaction or repayment receipts",
    "sec6_li4": "Maliciously defaulting or refusing to repay",
    "sec6_li5": "Any other fraudulent behavior",
    "sec6_notice": "KhmerX reserves the right to permanently restrict violating accounts.",
    "sec7_title": "Platform Restrictions & Security",
    "sec7_desc": "To protect the platform and user security, KhmerX reserves the right to:",
    "sec7_li1": "Restrict high-risk accounts",
    "sec7_li2": "Freeze abnormal transaction behavior",
    "sec7_li3": "Dynamically adjust or limit loan amounts",
    "sec7_li4": "Refuse service to specific users",
    "contact_title": "Questions about our terms?",
    "contact_desc": "Please contact KhmerX support via official Telegram.",
    "contact_btn": "Contact Telegram Support",
    "footer_desc": "KhmerX is a local micro-lending information platform. It does not guarantee successful loans or provide guarantees."
}

content_km = {
    "lang": "km",
    "zh_active": "",
    "en_active": "",
    "km_active": "bg-white shadow-sm text-blue-600",
    "title": "លក្ខខណ្ឌប្រើប្រាស់ KhmerX | សេវាខ្ចីប្រាក់តាម Telegram ABA",
    "desc": "មុនពេលប្រើប្រាស់ KhmerX សូមយល់ពីច្បាប់របស់យើង។",
    "keywords": "KhmerX terms, Cambodia loan terms, Telegram finance terms, ABA loan agreement",
    "nav_borrow": "របៀបខ្ចីប្រាក់",
    "nav_fees": "ការប្រាក់",
    "nav_contact": "ទំនាក់ទំនង",
    "nav_cta": "បើក Mini App",
    "hero_title": "លក្ខខណ្ឌប្រើប្រាស់",
    "hero_subtitle": "មុនពេលប្រើប្រាស់ KhmerX សូមបញ្ជាក់ និងយល់ពីច្បាប់ពាក់ព័ន្ធ។",
    "sec1_title": "សេចក្តីថ្លែងការណ៍សេវាកម្ម KhmerX",
    "sec1_desc": "KhmerX គឺជាវេទិកាផ្គូផ្គងព័ត៌មានខ្ចីប្រាក់ខ្នាតតូចសម្រាប់អ្នកប្រើប្រាស់នៅកម្ពុជា។",
    "sec1_li1": "KhmerX មិនមែនជាធនាគារទេ",
    "sec1_li2": "KhmerX មិនទទួលប្រាក់បញ្ញើទេ",
    "sec1_li3": "KhmerX មិនធានាថាការខ្ចីប្រាក់នឹងបានសម្រេចទេ",
    "sec1_li4": "KhmerX មិនធានាប្រាក់ចំណេញទេ",
    "sec2_title": "លក្ខណៈសម្បត្តិអ្នកប្រើប្រាស់",
    "sec2_li1": "ប្រើប្រាស់ Telegram សម្រាប់ការចុះឈ្មោះ និងប្រតិបត្តិការ",
    "sec2_li2": "ផ្តល់ព័ត៌មានគណនី ABA ពិតប្រាកដ និងត្រឹមត្រូវ",
    "sec2_li3": "ផ្តល់ព័ត៌មានអត្តសញ្ញាណពិតប្រាកដ",
    "sec2_li4": "គោរពច្បាប់ និងបទប្បញ្ញត្តិក្នុងស្រុក",
    "sec2_notice": "KhmerX រក្សាសិទ្ធិក្នុងការរឹតត្បិត ឬបដិសេធគណនីដែលមានហានិភ័យខ្ពស់។",
    "sec3_title": "ច្បាប់នៃការខ្ចីប្រាក់",
    "sec3_sub1": "ព័ត៌មានលម្អិតនៃការខ្ចី",
    "sec3_desc1": "មុនពេលខ្ចីប្រាក់ អ្នកត្រូវបញ្ជាក់ចំនួនប្រាក់ខ្ចី ចំនួនប្រាក់ទទួលបាន ចំនួនប្រាក់សង និងរយៈពេលខ្ចី។",
    "sec3_sub2": "ថ្លៃសេវា",
    "sec3_desc2": "ការខ្ចីប្រាក់អាចមានរួមបញ្ចូលថ្លៃសេវាថេរ និងសេវាកម្ម។",
    "sec3_sub3": "ការបញ្ជាក់របស់អ្នកប្រើប្រាស់",
    "sec3_desc3": "ការដាក់សំណើសុំខ្ចីប្រាក់ចាត់ទុកជាការបញ្ជាក់លើថ្លៃសេវា និងច្បាប់ពាក់ព័ន្ធទាំងអស់។",
    "sec4_title": "ច្បាប់នៃការសងប្រាក់",
    "sec4_sub1": "វិធីសាស្រ្តសងប្រាក់",
    "sec4_desc1": "អ្នកប្រើប្រាស់ត្រូវសងប្រាក់តាមរយៈការផ្ទេរ ABA។",
    "sec4_sub2": "ការបង្ហោះបង្កាន់ដៃ",
    "sec4_desc2": "បន្ទាប់ពីផ្ទេរប្រាក់រួច អ្នកប្រើប្រាស់ត្រូវបង្ហោះរូបថតអេក្រង់នៃបង្កាន់ដៃសងប្រាក់។",
    "sec4_sub3": "ការរំលឹកថ្ងៃកំណត់",
    "sec4_desc3": "ប្រព័ន្ធអាចនឹងផ្ញើសាររំលឹក 24 ម៉ោងមុនថ្ងៃកំណត់។",
    "sec5_title": "ហានិភ័យ & ការបដិសេធការទទួលខុសត្រូវ",
    "sec5_desc": "KhmerX គ្រាន់តែជាវេទិកាព័ត៌មានប៉ុណ្ណោះ ហើយមិនទទួលខុសត្រូវចំពោះហានិភ័យប្រតិបត្តិការឡើយ។",
    "sec5_li1": "វេទិកាមិនធានាថាប្រាក់កម្ចីនឹងត្រូវបានផ្តល់ ឬសងទាន់ពេលវេលាឡើយ។",
    "sec5_li2": "វេទិកាមិនទទួលខុសត្រូវចំពោះការបាត់បង់ប្រាក់កម្ចី ការបាត់បង់ប្រតិបត្តិការ ឬវិវាទអ្នកប្រើប្រាស់ឡើយ។",
    "sec5_li3": "អ្នកប្រើប្រាស់ត្រូវផ្ទៀងផ្ទាត់ភាពត្រឹមត្រូវ និងហានិភ័យនៃភាគីម្ខាងទៀតដោយខ្លួនឯង។",
    "sec5_li4": "ប្រតិបត្តិការណាមួយអាចពាក់ព័ន្ធនឹងហានិភ័យភាគីទីបី ដែលវេទិកាមិនធានាឡើយ។",
    "sec6_title": "ការបំពានច្បាប់",
    "sec6_li1": "ផ្តល់ព័ត៌មានមិនពិត",
    "sec6_li2": "ប្រើប្រាស់គណនីច្រើនដើម្បីបន្លំពិន្ទុឥណទាន ឬដែនកំណត់",
    "sec6_li3": "ក្លែងបន្លំប្រតិបត្តិការ ឬបង្កាន់ដៃសងប្រាក់",
    "sec6_li4": "មានចេតនាមិនសងប្រាក់ ឬបដិសេធមិនសង",
    "sec6_li5": "អាកប្បកិរិយាបោកប្រាស់ផ្សេងៗទៀត",
    "sec6_notice": "KhmerX រក្សាសិទ្ធិក្នុងការរឹតត្បិតជាអចិន្ត្រៃយ៍នូវគណនីដែលបំពានច្បាប់។",
    "sec7_title": "ការរឹតត្បិត និងសុវត្ថិភាពវេទិកា",
    "sec7_desc": "ដើម្បីការពារវេទិកា និងសុវត្ថិភាពអ្នកប្រើប្រាស់ KhmerX រក្សាសិទ្ធិក្នុងការ៖",
    "sec7_li1": "រឹតត្បិតគណនីដែលមានហានិភ័យខ្ពស់",
    "sec7_li2": "បង្កកអាកប្បកិរិយាប្រតិបត្តិការមិនប្រក្រតី",
    "sec7_li3": "កែសម្រួល ឬកំណត់ចំនួនប្រាក់កម្ចីដោយស្វ័យប្រវត្តិ",
    "sec7_li4": "បដិសេធសេវាកម្មចំពោះអ្នកប្រើប្រាស់ជាក់លាក់",
    "contact_title": "មានសំណួរអំពីលក្ខខណ្ឌរបស់យើង?",
    "contact_desc": "សូមទាក់ទងផ្នែកជំនួយ KhmerX តាមរយៈ Telegram ផ្លូវការ។",
    "contact_btn": "ទាក់ទងផ្នែកជំនួយ Telegram",
    "footer_desc": "KhmerX គឺជាវេទិកាព័ត៌មានខ្ចីប្រាក់ខ្នាតតូចក្នុងស្រុក។ មិនធានាថាការខ្ចីប្រាក់នឹងទទួលបានជោគជ័យ ឬផ្តល់ការធានាឡើយ។"
}

import os

for c in [content_zh, content_en, content_km]:
    html = template.format(**c)
    lang = c['lang']
    os.makedirs(f"frontend/website/{lang}/terms", exist_ok=True)
    with open(f"frontend/website/{lang}/terms/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated {lang}/terms/index.html")

