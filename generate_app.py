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
    <meta property="og:url" content="https://khmerx.org/{lang}/app" />
    <meta property="og:image" content="https://khmerx.org/logo.jpg" />
    <meta name="twitter:card" content="summary" />
    <meta name="twitter:title" content="{title}" />
    <meta name="twitter:description" content="{desc}" />
    <link rel="canonical" href="https://khmerx.org/{lang}/app" />
    <link rel="alternate" href="https://khmerx.org/km/app" hreflang="km" />
    <link rel="alternate" href="https://khmerx.org/en/app" hreflang="en" />
    <link rel="alternate" href="https://khmerx.org/zh/app" hreflang="zh" />
    <link rel="alternate" href="https://khmerx.org/km/app" hreflang="x-default" />
    <script type="application/ld+json">
      {{
        "@context": "https://schema.org",
        "@type": "MobileApplication",
        "name": "KhmerX Telegram Mini App",
        "operatingSystem": "Android, iOS",
        "applicationCategory": "FinanceApplication",
        "url": "https://t.me/KhmerXBot/app",
        "description": "{desc}"
      }}
    </script>
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
    <style>
      @keyframes float {{
        0% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-15px); }}
        100% {{ transform: translateY(0px); }}
      }}
      .animate-float {{
        animation: float 5s ease-in-out infinite;
      }}
      .animate-float-delay {{
        animation: float 5s ease-in-out infinite;
        animation-delay: 2s;
      }}
    </style>
    <script>
      document.addEventListener("DOMContentLoaded", () => {{
        const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
        const hasTelegram = window.TelegramWebviewProxy || (window.Telegram && window.Telegram.WebApp) || /Telegram/i.test(navigator.userAgent);
        
        const qrSection = document.getElementById('qr-section');
        const mobileCta = document.getElementById('mobile-cta');
        const dlBtn = document.getElementById('dl-telegram-btn');
        
        if (isMobile) {{
          qrSection.style.display = 'none';
          if (!hasTelegram) {{
            dlBtn.style.display = 'inline-flex';
          }} else {{
            // Auto open if likely has Telegram
            setTimeout(() => {{
              window.location.href = 'tg://resolve?domain=KhmerXBot&startapp';
            }}, 1500);
          }}
        }} else {{
          // PC
          mobileCta.style.display = 'none';
          qrSection.style.display = 'flex';
        }}
      }});
    </script>
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
          
          <div class="flex items-center gap-4">
            <a href="/{lang}" class="text-sm font-medium text-slate-500 hover:text-blue-600 mr-2">{nav_home}</a>
            <div class="flex gap-1 text-sm bg-slate-100 p-1 rounded-xl">
              <a data-lang="km" class="rounded-lg px-3 py-1.5 transition-colors font-medium {km_active}" href="/km/app">ខ្មែរ</a>
              <a data-lang="en" class="rounded-lg px-3 py-1.5 transition-colors font-medium {en_active}" href="/en/app">EN</a>
              <a data-lang="zh" class="rounded-lg px-3 py-1.5 transition-colors font-medium {zh_active}" href="/zh/app">中文</a>
            </div>
          </div>
        </div>
      </header>

      <!-- Hero 区 -->
      <section class="relative bg-slate-900 overflow-hidden text-white flex-1 flex flex-col justify-center">
        <div class="absolute inset-0 bg-[url('https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=Dark%20blue%20telegram%20mini%20app%20interface%20technology%20background%20abstract%20modern%20clean%20business%20style&image_size=landscape_16_9')] bg-cover bg-center opacity-30 mix-blend-overlay"></div>
        <div class="absolute inset-0 bg-gradient-to-b from-transparent to-slate-900/90"></div>
        
        <div class="relative mx-auto max-w-[1200px] px-5 py-16 md:py-24 flex-1 w-full">
          <div class="grid gap-12 md:grid-cols-2 md:items-center h-full">
            <div class="max-w-xl z-10 flex flex-col justify-center">
              <div class="mb-6 inline-flex rounded-full bg-blue-500/20 px-4 py-2 text-sm font-bold text-blue-300 border border-blue-500/30 w-max">
                Telegram · ABA · Cambodia
              </div>
              <h1 class="text-4xl font-extrabold leading-tight tracking-tight md:text-5xl lg:text-6xl mb-6">
                {hero_title}
              </h1>
              <p class="text-lg leading-relaxed text-slate-300 md:text-xl font-medium mb-10">
                {hero_subtitle}
              </p>
              
              <!-- CTA 区 -->
              <div id="mobile-cta" class="flex flex-col sm:flex-row gap-4">
                <a href="https://t.me/KhmerXBot/app" class="inline-flex justify-center items-center rounded-2xl bg-gradient-to-r from-[#0A5BFF] to-[#00AEEF] px-8 py-4 text-lg font-bold text-white shadow-[0_8px_30px_rgb(10,91,255,0.4)] hover:shadow-[0_8px_40px_rgb(10,91,255,0.6)] hover:scale-105 transition-all duration-300 h-[56px]">
                  <svg class="w-6 h-6 mr-3" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.74-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .38z"/></svg>
                  {cta_open}
                </a>
                <a id="dl-telegram-btn" href="https://telegram.org/" style="display: none;" class="inline-flex justify-center items-center rounded-2xl bg-slate-800 border border-slate-700 px-8 py-4 text-lg font-bold text-white shadow-lg hover:bg-slate-700 hover:scale-105 transition-all duration-300 h-[56px]">
                  <svg class="w-6 h-6 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
                  {cta_dl}
                </a>
              </div>
              
              <!-- QR 区 (PC) -->
              <div id="qr-section" class="hidden flex-col items-start gap-4">
                <div class="bg-white p-4 rounded-3xl shadow-xl flex gap-6 items-center border border-slate-200">
                  <img class="w-32 h-32 rounded-xl" alt="KhmerX Mini App QR" src="https://api.qrserver.com/v1/create-qr-code/?size=240x240&data=https%3A%2F%2Ft.me%2FKhmerXBot%2Fapp" />
                  <div class="pr-4">
                    <h4 class="font-bold text-slate-900 text-lg mb-1">{qr_title}</h4>
                    <p class="text-slate-500 text-sm">{qr_desc}</p>
                  </div>
                </div>
              </div>

            </div>
            
            <div class="relative z-10 hidden md:flex justify-center md:justify-end items-center h-[500px]">
              <!-- Mockups -->
              <div class="relative w-full max-w-md h-full">
                <!-- Phone 1 -->
                <div class="absolute right-0 top-10 w-48 h-auto rounded-[2rem] border-4 border-slate-800 bg-slate-900 shadow-2xl overflow-hidden animate-float z-10 rotate-6">
                  <img src="https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=Telegram%20Mini%20App%20UI%20Mockup%20Finance%20Dashboard%20Clean%20Modern%20Mobile%20Interface%20Blue%20Tones&image_size=portrait_16_9" alt="App Preview 1" class="w-full h-full object-cover" />
                </div>
                <!-- Phone 2 -->
                <div class="absolute left-10 top-20 w-48 h-auto rounded-[2rem] border-4 border-slate-800 bg-slate-900 shadow-2xl overflow-hidden animate-float-delay z-20 -rotate-3">
                  <img src="https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=Telegram%20Mini%20App%20UI%20Mockup%20Loan%20Application%20Form%20Clean%20Modern%20Mobile%20Interface%20Blue%20Tones&image_size=portrait_16_9" alt="App Preview 2" class="w-full h-full object-cover" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Telegram 打开方式 -->
      <section class="mx-auto max-w-[1200px] px-5 py-20 bg-white rounded-t-[3rem] -mt-10 relative z-20 w-full shadow-lg border-t border-slate-100">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-slate-900">{steps_title}</h2>
        </div>
        <div class="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
          <div class="bg-slate-50 rounded-3xl p-8 text-center border border-slate-100 relative">
            <div class="w-12 h-12 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center font-bold text-xl mx-auto mb-4">1</div>
            <h4 class="font-bold text-slate-900 text-lg mb-2">{step1_title}</h4>
            <p class="text-slate-500 text-sm">{step1_desc}</p>
          </div>
          <div class="bg-slate-50 rounded-3xl p-8 text-center border border-slate-100 relative">
            <div class="w-12 h-12 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center font-bold text-xl mx-auto mb-4">2</div>
            <h4 class="font-bold text-slate-900 text-lg mb-2">{step2_title}</h4>
            <p class="text-slate-500 text-sm">{step2_desc}</p>
          </div>
          <div class="bg-blue-50 rounded-3xl p-8 text-center border border-blue-100 relative">
            <div class="w-12 h-12 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold text-xl mx-auto mb-4">3</div>
            <h4 class="font-bold text-blue-900 text-lg mb-2">{step3_title}</h4>
            <p class="text-blue-700 text-sm">{step3_desc}</p>
          </div>
        </div>
      </section>

      <!-- FAQ & 风险说明 -->
      <section class="bg-[#F5F7FA] py-20 border-t border-slate-200 flex-1">
        <div class="mx-auto max-w-[800px] px-5">
          <div class="text-center mb-12">
            <h2 class="text-3xl font-bold text-slate-900">FAQ</h2>
          </div>
          <div class="space-y-4 mb-16">
            <details class="group rounded-3xl border border-slate-200 bg-white [&_summary::-webkit-details-marker]:hidden">
              <summary class="flex cursor-pointer items-center justify-between p-6 font-bold text-lg text-slate-900">
                {faq1_q}
                <span class="transition group-open:rotate-180">
                  <svg fill="none" height="24" shape-rendering="geometricPrecision" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" viewBox="0 0 24 24" width="24"><path d="M6 9l6 6 6-6"></path></svg>
                </span>
              </summary>
              <div class="px-6 pb-6 text-slate-600"><p>{faq1_a}</p></div>
            </details>
            <details class="group rounded-3xl border border-slate-200 bg-white [&_summary::-webkit-details-marker]:hidden">
              <summary class="flex cursor-pointer items-center justify-between p-6 font-bold text-lg text-slate-900">
                {faq2_q}
                <span class="transition group-open:rotate-180">
                  <svg fill="none" height="24" shape-rendering="geometricPrecision" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" viewBox="0 0 24 24" width="24"><path d="M6 9l6 6 6-6"></path></svg>
                </span>
              </summary>
              <div class="px-6 pb-6 text-slate-600"><p>{faq2_a}</p></div>
            </details>
            <details class="group rounded-3xl border border-slate-200 bg-white [&_summary::-webkit-details-marker]:hidden">
              <summary class="flex cursor-pointer items-center justify-between p-6 font-bold text-lg text-slate-900">
                {faq3_q}
                <span class="transition group-open:rotate-180">
                  <svg fill="none" height="24" shape-rendering="geometricPrecision" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" viewBox="0 0 24 24" width="24"><path d="M6 9l6 6 6-6"></path></svg>
                </span>
              </summary>
              <div class="px-6 pb-6 text-slate-600"><p>{faq3_a}</p></div>
            </details>
            <details class="group rounded-3xl border border-slate-200 bg-white [&_summary::-webkit-details-marker]:hidden">
              <summary class="flex cursor-pointer items-center justify-between p-6 font-bold text-lg text-slate-900">
                {faq4_q}
                <span class="transition group-open:rotate-180">
                  <svg fill="none" height="24" shape-rendering="geometricPrecision" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" viewBox="0 0 24 24" width="24"><path d="M6 9l6 6 6-6"></path></svg>
                </span>
              </summary>
              <div class="px-6 pb-6 text-slate-600"><p>{faq4_a}</p></div>
            </details>
          </div>

          <!-- 风险说明 -->
          <div class="bg-yellow-50 border border-yellow-200 rounded-3xl p-8 flex gap-4">
            <svg class="w-8 h-8 text-yellow-600 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
            <div>
              <h4 class="font-bold text-yellow-900 text-lg mb-2">{risk_title}</h4>
              <p class="text-yellow-800 text-sm mb-2">{risk_desc1}</p>
              <p class="text-yellow-900 text-sm font-bold">{risk_desc2}</p>
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
              <a href="/km/app" class="hover:text-white transition-colors">ខ្មែរ</a>
              <a href="/en/app" class="hover:text-white transition-colors">English</a>
              <a href="/zh/app" class="hover:text-white transition-colors">中文</a>
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
    "title": "打开 KhmerX Mini App | Telegram ABA Cambodia",
    "desc": "通过 Telegram 快速使用 KhmerX 小额周转服务。支持 ABA 转账，本地化体验。",
    "keywords": "Telegram Mini App, Cambodia Telegram, KhmerX App, ABA Cambodia",
    "nav_home": "返回首页",
    "hero_title": "打开 KhmerX Mini App",
    "hero_subtitle": "通过 Telegram 使用 KhmerX 小额周转服务。",
    "cta_open": "打开 Telegram Mini App",
    "cta_dl": "下载 Telegram",
    "qr_title": "扫描二维码打开 Telegram",
    "qr_desc": "使用手机相机扫描以打开 KhmerX Bot",
    "steps_title": "如何打开 KhmerX？",
    "step1_title": "安装 Telegram",
    "step1_desc": "确保您的手机上已安装 Telegram 应用。",
    "step2_title": "打开 KhmerX Bot",
    "step2_desc": "点击按钮或扫描二维码进入官方 Bot。",
    "step3_title": "点击“打开 Mini App”",
    "step3_desc": "在对话框内点击底部按钮即可进入平台。",
    "faq1_q": "KhmerX 是否需要 Telegram？",
    "faq1_a": "是的，KhmerX 的所有服务均通过 Telegram Mini App 提供，以保证安全与便捷。",
    "faq2_q": "如何打开 Mini App？",
    "faq2_a": "进入 @KhmerXBot，点击底部的 Open App 或 Menu 中的相关按钮即可。",
    "faq3_q": "是否支持 ABA？",
    "faq3_a": "是的，所有资金交易都在用户双方的 ABA 账户间直接完成转账。",
    "faq4_q": "为什么打不开？",
    "faq4_a": "请检查网络连接或确保您的 Telegram 已更新至最新版本支持 WebApp 功能。",
    "risk_title": "安全防骗提示",
    "risk_desc1": "请务必确认您正在使用官方 Telegram 与二维码，谨防钓鱼诈骗。",
    "risk_desc2": "KhmerX 不会通过私人 Telegram 主动要求您进行任何转账。",
    "footer_desc": "KhmerX 是本地小额周转信息服务平台，不保证借款成功，不提供担保。"
}

content_en = {
    "lang": "en",
    "zh_active": "",
    "en_active": "bg-white shadow-sm text-blue-600",
    "km_active": "",
    "title": "Open KhmerX Mini App | Telegram ABA Cambodia",
    "desc": "Quickly access KhmerX micro-lending services via Telegram. Supports ABA transfers, localized experience.",
    "keywords": "Telegram Mini App, Cambodia Telegram, KhmerX App, ABA Cambodia",
    "nav_home": "Back to Home",
    "hero_title": "Open KhmerX Mini App",
    "hero_subtitle": "Use KhmerX micro-lending services through Telegram.",
    "cta_open": "Open Telegram Mini App",
    "cta_dl": "Download Telegram",
    "qr_title": "Scan QR to open Telegram",
    "qr_desc": "Use your phone's camera to open KhmerX Bot",
    "steps_title": "How to open KhmerX?",
    "step1_title": "Install Telegram",
    "step1_desc": "Make sure you have the Telegram app installed on your phone.",
    "step2_title": "Open KhmerX Bot",
    "step2_desc": "Click the button or scan the QR code to enter the official Bot.",
    "step3_title": "Click 'Open Mini App'",
    "step3_desc": "Click the bottom button in the chat to enter the platform.",
    "faq1_q": "Does KhmerX require Telegram?",
    "faq1_a": "Yes, all KhmerX services are provided via the Telegram Mini App for security and convenience.",
    "faq2_q": "How do I open the Mini App?",
    "faq2_a": "Go to @KhmerXBot and click the Open App button at the bottom or in the Menu.",
    "faq3_q": "Does it support ABA?",
    "faq3_a": "Yes, all fund transactions are completed directly between users' ABA accounts.",
    "faq4_q": "Why can't I open it?",
    "faq4_a": "Please check your network connection or ensure your Telegram is updated to the latest version supporting WebApp features.",
    "risk_title": "Security & Anti-Fraud Notice",
    "risk_desc1": "Please ensure you are using the official Telegram and QR code. Beware of phishing scams.",
    "risk_desc2": "KhmerX will NEVER ask you to transfer money via private Telegram messages.",
    "footer_desc": "KhmerX is a local micro-lending information platform. It does not guarantee successful loans or provide guarantees."
}

content_km = {
    "lang": "km",
    "zh_active": "",
    "en_active": "",
    "km_active": "bg-white shadow-sm text-blue-600",
    "title": "បើក KhmerX Mini App | Telegram ABA កម្ពុជា",
    "desc": "ប្រើប្រាស់សេវាកម្មខ្ចីប្រាក់ខ្នាតតូច KhmerX យ៉ាងឆាប់រហ័សតាមរយៈ Telegram ។ គាំទ្រការផ្ទេរប្រាក់ ABA ។",
    "keywords": "Telegram Mini App, Cambodia Telegram, KhmerX App, ABA Cambodia",
    "nav_home": "ត្រឡប់ទៅទំព័រដើម",
    "hero_title": "បើក KhmerX Mini App",
    "hero_subtitle": "ប្រើប្រាស់សេវាកម្មខ្ចីប្រាក់ខ្នាតតូច KhmerX តាមរយៈ Telegram ។",
    "cta_open": "បើក Telegram Mini App",
    "cta_dl": "ទាញយក Telegram",
    "qr_title": "ស្កេនកូដ QR ដើម្បីបើក Telegram",
    "qr_desc": "ប្រើកាមេរ៉ាទូរស័ព្ទរបស់អ្នកដើម្បីបើក KhmerX Bot",
    "steps_title": "តើត្រូវបើក KhmerX ដោយរបៀបណា?",
    "step1_title": "ដំឡើង Telegram",
    "step1_desc": "សូមប្រាកដថាអ្នកមានកម្មវិធី Telegram នៅលើទូរស័ព្ទរបស់អ្នក។",
    "step2_title": "បើក KhmerX Bot",
    "step2_desc": "ចុចប៊ូតុង ឬស្កេនកូដ QR ដើម្បីចូល Bot ផ្លូវការ។",
    "step3_title": "ចុច 'បើក Mini App'",
    "step3_desc": "ចុចប៊ូតុងខាងក្រោមនៅក្នុងការសន្ទនាដើម្បីចូលទៅកាន់វេទិកា។",
    "faq1_q": "តើ KhmerX តម្រូវឱ្យមាន Telegram ទេ?",
    "faq1_a": "បាទ រាល់សេវាកម្ម KhmerX ទាំងអស់ត្រូវបានផ្តល់ជូនតាមរយៈ Telegram Mini App ដើម្បីសុវត្ថិភាពនិងភាពងាយស្រួល។",
    "faq2_q": "តើខ្ញុំបើក Mini App ដោយរបៀបណា?",
    "faq2_a": "ចូលទៅកាន់ @KhmerXBot ហើយចុចប៊ូតុង Open App នៅខាងក្រោម ឬនៅក្នុងម៉ឺនុយ។",
    "faq3_q": "តើវាគាំទ្រ ABA ទេ?",
    "faq3_a": "បាទ រាល់ប្រតិបត្តិការថវិកាទាំងអស់ត្រូវបានបញ្ចប់ដោយផ្ទាល់រវាងគណនី ABA របស់អ្នកប្រើប្រាស់។",
    "faq4_q": "ហេតុអ្វីខ្ញុំមិនអាចបើកវាបាន?",
    "faq4_a": "សូមពិនិត្យការតភ្ជាប់បណ្តាញរបស់អ្នក ឬប្រាកដថា Telegram របស់អ្នកត្រូវបានធ្វើបច្ចុប្បន្នភាពទៅកំណែចុងក្រោយដែលគាំទ្រ WebApp ។",
    "risk_title": "សេចក្តីជូនដំណឹងអំពីសុវត្ថិភាព",
    "risk_desc1": "សូមប្រាកដថាអ្នកកំពុងប្រើ Telegram និង QR ផ្លូវការ។ ប្រយ័ត្នចំពោះការបោកប្រាស់។",
    "risk_desc2": "KhmerX នឹងមិនស្នើសុំឱ្យអ្នកផ្ទេរប្រាក់តាមរយៈសារ Telegram ឯកជនឡើយ។",
    "footer_desc": "KhmerX គឺជាវេទិកាព័ត៌មានខ្ចីប្រាក់ខ្នាតតូចក្នុងស្រុក។ មិនធានាថាការខ្ចីប្រាក់នឹងទទួលបានជោគជ័យ ឬផ្តល់ការធានាឡើយ។"
}

import os

for c in [content_zh, content_en, content_km]:
    html = template.format(**c)
    lang = c['lang']
    os.makedirs(f"frontend/website/{lang}/app", exist_ok=True)
    with open(f"frontend/website/{lang}/app/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated {lang}/app/index.html")

