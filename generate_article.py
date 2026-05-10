import os

# --- Blog Article Page Template ---
article_template = """<!doctype html>
<html lang="{lang}">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title} | KhmerX Blog</title>
    <meta name="description" content="{desc}" />
    <meta name="keywords" content="{keywords}" />
    <meta property="og:type" content="article" />
    <meta property="og:site_name" content="KhmerX Blog" />
    <meta property="og:title" content="{title}" />
    <meta property="og:description" content="{desc}" />
    <meta property="og:url" content="https://khmerx.org/{lang}/blog/article/{slug}" />
    <meta property="og:image" content="{cover_img}" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{title}" />
    <meta name="twitter:description" content="{desc}" />
    <meta name="twitter:image" content="{cover_img}" />
    <link rel="canonical" href="https://khmerx.org/{lang}/blog/article/{slug}" />
    <script type="application/ld+json">
      {{
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "mainEntityOfPage": {{
          "@type": "WebPage",
          "@id": "https://khmerx.org/{lang}/blog/article/{slug}"
        }},
        "headline": "{title}",
        "description": "{desc}",
        "image": "{cover_img}",  
        "author": {{
          "@type": "Organization",
          "name": "KhmerX Team",
          "url": "https://khmerx.org"
        }},  
        "publisher": {{
          "@type": "Organization",
          "name": "KhmerX",
          "logo": {{
            "@type": "ImageObject",
            "url": "https://khmerx.org/logo.jpg"
          }}
        }},
        "datePublished": "2026-05-10",
        "dateModified": "2026-05-10"
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
            "name": "Blog",
            "item": "https://khmerx.org/{lang}/blog"
          }},
          {{
            "@type": "ListItem",
            "position": 3,
            "name": "{title}"
          }}
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
          }}
        ]
      }}
    </script>
    <style>
      .prose h2 {{ color: #0f172a; margin-top: 2.5rem; margin-bottom: 1rem; font-weight: 800; font-size: 1.5rem; }}
      .prose h3 {{ color: #1e293b; margin-top: 2rem; margin-bottom: 0.75rem; font-weight: 700; font-size: 1.25rem; }}
      .prose p {{ color: #475569; line-height: 1.8; margin-bottom: 1.25rem; }}
      .prose ul {{ list-style-type: disc; padding-left: 1.5rem; color: #475569; margin-bottom: 1.25rem; }}
      .prose li {{ margin-bottom: 0.5rem; }}
      .prose img {{ border-radius: 1rem; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); margin: 2rem 0; }}
      .prose strong {{ color: #0f172a; }}
    </style>
  </head>
  <body>
    <script type="module" src="/src/site.ts"></script>
    <main class="min-h-screen bg-white pb-24 font-sans">
      
      <!-- Sticky Header -->
      <header class="sticky top-0 z-50 border-b bg-white/90 backdrop-blur-md">
        <div class="mx-auto flex max-w-[1200px] items-center justify-between px-5 py-4">
          <a href="/{lang}" class="flex items-center gap-3 group">
            <img src="/logo.jpg" alt="KhmerX Logo" class="h-10 w-10 rounded-xl object-cover shadow-sm group-hover:scale-105 transition-transform" />
            <div>
              <div class="font-bold text-lg text-slate-900">KhmerX</div>
            </div>
          </a>
          <nav class="hidden gap-8 text-sm font-medium text-slate-600 md:flex">
            <a class="text-blue-600 transition-colors" href="/{lang}/blog">Blog</a>
            <a class="hover:text-blue-600 transition-colors" href="/{lang}/faq">{nav_faq}</a>
            <a class="hover:text-blue-600 transition-colors" href="/{lang}/contact">{nav_contact}</a>
          </nav>
          <div class="flex items-center gap-4">
            <a class="inline-flex rounded-xl bg-gradient-to-r from-[#0A5BFF] to-[#00AEEF] px-5 py-2.5 text-sm font-bold text-white shadow-md hover:shadow-lg hover:scale-105 transition-all" href="https://t.me/KhmerXBot/app">{nav_cta}</a>
          </div>
        </div>
      </header>

      <!-- 文章头部 -->
      <article class="mx-auto max-w-[800px] px-5 pt-16 pb-12">
        <!-- 分类与标签 -->
        <div class="flex gap-2 mb-6">
          <a href="/{lang}/blog/{category_slug}" class="inline-flex rounded-full bg-blue-100 px-3 py-1 text-xs font-bold text-blue-700 uppercase tracking-wider hover:bg-blue-200 transition-colors">{category}</a>
        </div>
        
        <!-- H1 标题 -->
        <h1 class="text-3xl md:text-4xl lg:text-5xl font-extrabold text-slate-900 leading-tight mb-6">
          {title}
        </h1>
        
        <!-- 描述 -->
        <p class="text-xl text-slate-500 mb-8 leading-relaxed">
          {desc}
        </p>
        
        <!-- 作者与时间 -->
        <div class="flex items-center gap-4 py-6 border-y border-slate-100 mb-10">
          <div class="w-12 h-12 rounded-full bg-slate-200 overflow-hidden">
            <img src="/logo.jpg" alt="KhmerX Team" class="w-full h-full object-cover grayscale" />
          </div>
          <div>
            <div class="font-bold text-slate-900">KhmerX Team</div>
            <div class="text-sm text-slate-500 flex items-center gap-2">
              <span>May 10, 2026</span>
              <span>·</span>
              <span>5 min read</span>
            </div>
          </div>
        </div>
        
        <!-- 封面图 -->
        <div class="aspect-[16/9] rounded-[2rem] overflow-hidden mb-12 shadow-lg border border-slate-100">
          <img src="{cover_img}" alt="{title}" class="w-full h-full object-cover" />
        </div>
        
        <!-- 正文内容 (Prose) -->
        <div class="prose prose-lg max-w-none">
          {content}
        </div>
        
        <!-- 风险提示模块 -->
        <div class="mt-12 bg-[#FFFBEB] border-2 border-[#FDE68A] rounded-2xl p-6 flex gap-4 items-start">
          <svg class="w-8 h-8 text-[#F59E0B] shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
          <div>
            <h4 class="font-bold text-[#92400E] text-lg mb-2">{risk_title}</h4>
            <p class="text-[#B45309] font-medium">{risk_desc}</p>
            <ul class="list-disc list-inside text-[#B45309] mt-2 space-y-1">
              <li>{risk_1}</li>
              <li>{risk_2}</li>
              <li>{risk_3}</li>
            </ul>
          </div>
        </div>
        
        <!-- 文章 FAQ -->
        <div class="mt-16 border-t border-slate-100 pt-12">
          <h3 class="text-2xl font-bold text-slate-900 mb-8">FAQ</h3>
          <div class="space-y-4">
            <details class="group rounded-2xl border border-slate-200 bg-white [&_summary::-webkit-details-marker]:hidden">
              <summary class="flex cursor-pointer items-center justify-between p-5 font-bold text-lg text-slate-900 hover:bg-slate-50 transition-colors">
                {faq_1_q}
                <span class="transition group-open:rotate-180 text-blue-500">
                  <svg fill="none" height="24" shape-rendering="geometricPrecision" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" viewBox="0 0 24 24" width="24"><path d="M6 9l6 6 6-6"></path></svg>
                </span>
              </summary>
              <div class="px-5 pb-5 text-slate-600 border-t border-slate-100 pt-4">
                <p>{faq_1_a}</p>
              </div>
            </details>
            <details class="group rounded-2xl border border-slate-200 bg-white [&_summary::-webkit-details-marker]:hidden">
              <summary class="flex cursor-pointer items-center justify-between p-5 font-bold text-lg text-slate-900 hover:bg-slate-50 transition-colors">
                {faq_2_q}
                <span class="transition group-open:rotate-180 text-blue-500">
                  <svg fill="none" height="24" shape-rendering="geometricPrecision" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" viewBox="0 0 24 24" width="24"><path d="M6 9l6 6 6-6"></path></svg>
                </span>
              </summary>
              <div class="px-5 pb-5 text-slate-600 border-t border-slate-100 pt-4">
                <p>{faq_2_a}</p>
              </div>
            </details>
          </div>
        </div>
        
        <!-- 内链导航 -->
        <div class="mt-12 flex flex-wrap gap-4 pt-8 border-t border-slate-100">
          <a href="/{lang}/borrow" class="inline-flex items-center gap-2 text-sm font-bold text-slate-600 bg-slate-100 px-4 py-2 rounded-xl hover:bg-blue-100 hover:text-blue-700 transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            {link_borrow}
          </a>
          <a href="/{lang}/faq" class="inline-flex items-center gap-2 text-sm font-bold text-slate-600 bg-slate-100 px-4 py-2 rounded-xl hover:bg-blue-100 hover:text-blue-700 transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            {link_faq}
          </a>
        </div>
      </article>

      <!-- 相关推荐模块 -->
      <section class="bg-slate-50 py-16 border-y border-slate-200">
        <div class="mx-auto max-w-[1200px] px-5">
          <h3 class="text-2xl font-bold text-slate-900 mb-8">{related_title}</h3>
          <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-8">
            <!-- Related 1 -->
            <a href="/{lang}/blog/article/telegram-finance-guide" class="bg-white rounded-2xl overflow-hidden shadow-sm border border-slate-200 group hover:shadow-md transition-shadow block">
              <div class="aspect-video bg-slate-100 overflow-hidden relative">
                <img src="https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=Telegram%20app%20chat%20interface%20with%20financial%20dashboard%20bot%20digital%20finance%20blue%20clean%20style&image_size=landscape_16_9" alt="Telegram Guide" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" loading="lazy" />
                <div class="absolute top-3 left-3 bg-slate-800 text-white text-[10px] font-bold px-2 py-1 rounded-full uppercase tracking-wider">Telegram</div>
              </div>
              <div class="p-5">
                <h4 class="font-bold text-slate-900 mb-2 group-hover:text-blue-600 transition-colors line-clamp-2">{related_1_title}</h4>
                <span class="text-blue-600 text-sm font-bold inline-flex items-center">
                  {read_btn}
                  <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
                </span>
              </div>
            </a>
            <!-- Related 2 -->
            <a href="/{lang}/blog/article/micro-loan-tips" class="bg-white rounded-2xl overflow-hidden shadow-sm border border-slate-200 group hover:shadow-md transition-shadow block">
              <div class="aspect-video bg-slate-100 overflow-hidden relative">
                <img src="https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=Small%20amount%20of%20money%20financial%20planning%20calculator%20coins%20business%20desk%20clean%20bright%20lighting&image_size=landscape_16_9" alt="Micro Loan Tips" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" loading="lazy" />
                <div class="absolute top-3 left-3 bg-green-600 text-white text-[10px] font-bold px-2 py-1 rounded-full uppercase tracking-wider">Loan</div>
              </div>
              <div class="p-5">
                <h4 class="font-bold text-slate-900 mb-2 group-hover:text-blue-600 transition-colors line-clamp-2">{related_2_title}</h4>
                <span class="text-blue-600 text-sm font-bold inline-flex items-center">
                  {read_btn}
                  <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
                </span>
              </div>
            </a>
          </div>
        </div>
      </section>

      <!-- Telegram CTA（最重要） -->
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

# Example Article Content (How to use ABA)
content_zh = {
    "lang": "zh",
    "slug": "how-to-use-aba",
    "title": "如何安全快速地使用 ABA 银行转账？",
    "desc": "在柬埔寨，ABA 银行转账是最常用的支付方式。本文详细图解如何通过 ABA 手机银行安全地进行个人转账与收款验证，以及在 KhmerX 上的应用。",
    "keywords": "ABA 转账教程, 柬埔寨 ABA, ABA bank transfer, KhmerX ABA, ABA 收款",
    "cover_img": "https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=ABA%20bank%20transfer%20mobile%20app%20UI%20mockup%20Cambodia%20Phnom%20Penh%20financial%20technology%20blue%20tones&image_size=landscape_16_9",
    "category": "ABA 教程",
    "category_slug": "aba",
    "km_active": "", "en_active": "", "zh_active": "bg-white shadow-sm text-blue-600",
    "nav_borrow": "如何借款", "nav_fees": "费用说明", "nav_faq": "FAQ", "nav_contact": "联系我们", "nav_cta": "打开 Mini App",
    
    "content": """
<h2>什么是 ABA 银行转账？</h2>
<p>ABA 银行（Advanced Bank of Asia）是柬埔寨最大、最普及的商业银行之一。其推出的 <strong>ABA Mobile App</strong> 几乎成为了柬埔寨本地生活与商业交易的“基础设施”。无论是超市购物、打车，还是朋友间的资金往来，ABA 转账都提供了极高的便利性。</p>

<h2>如何在 KhmerX 中使用 ABA 转账？</h2>
<p>在 KhmerX 平台上，所有的资金流转（借出与还款）均通过用户双方的个人 ABA 账户直接进行，平台不触碰任何资金。以下是标准的操作步骤：</p>
<h3>第一步：绑定 ABA 账户</h3>
<p>进入 KhmerX Telegram Mini App 后，首先需要在“个人中心”绑定您的 ABA 账号与真实姓名。请确保填写的姓名与银行开户名完全一致，以免影响后续匹配。</p>
<h3>第二步：获取对方账户</h3>
<p>当借款需求匹配成功后，借出方可以在订单详情中看到借款人的 ABA 账号；同理，到了还款日，借款人也会看到借出方的 ABA 账号。</p>
<h3>第三步：打开 ABA Mobile 转账</h3>
<ul>
  <li>打开您手机上的 ABA Mobile App。</li>
  <li>点击 <strong>Transfers (转账)</strong>，选择 <strong>To ABA Account (转至 ABA 账户)</strong>。</li>
  <li>输入在 KhmerX 上获取的对方账号与金额。</li>
  <li><strong>非常重要：</strong>核对显示的收款人姓名是否与 KhmerX 订单上的姓名一致。</li>
  <li>确认无误后输入 PIN 码完成转账。</li>
</ul>

<h2>注意事项与风险防范</h2>
<p>为了保障您的资金安全，请务必注意以下几点：</p>
<ul>
  <li><strong>核对姓名：</strong> 转账前一定要在 ABA App 内核实收款人姓名。如果发现姓名不符，请立即停止转账并在 KhmerX 内取消交易或联系客服。</li>
  <li><strong>保留凭证：</strong> 转账成功后，ABA App 会生成一张包含交易单号（Transaction ID）的电子回单。请务必保存截图，并在 KhmerX 订单页面上传该凭证以完成交易状态更新。</li>
  <li><strong>防范诈骗：</strong> KhmerX 官方客服绝对不会主动要求您向任何“安全账户”或私人账户转账。所有交易只在匹配的双方之间进行。</li>
</ul>
    """,
    
    "risk_title": "借款与还款风险提示",
    "risk_desc": "在进行任何 ABA 转账前，请务必确认：",
    "risk_1": "实际到账金额（已扣除固定费用的金额）", "risk_2": "借款期限与准确的到期日", "risk_3": "到期应还的总金额",
    
    "faq_1_q": "ABA 转账需要手续费吗？", "faq_1_a": "通常情况下，ABA 个人账户之间的本币或美元转账是免费的，具体以 ABA 银行官方规定为准。",
    "faq_2_q": "KhmerX 如何确认我已还款？", "faq_2_a": "您需要在完成 ABA 转账后，将包含 Transaction ID 的转账成功截图上传至 KhmerX 对应的订单中，借出方核实到账后会点击确认，订单即视为完成。",
    
    "link_borrow": "查看借款流程", "link_faq": "浏览常见问题",
    
    "related_title": "相关推荐",
    "related_1_title": "Telegram Mini App 金融工具完全指南",
    "related_2_title": "申请小额短期周转前必须知道的 3 件事",
    "read_btn": "阅读文章",
    
    "cta_title": "立即打开 KhmerX Mini App", "cta_btn": "打开 Telegram"
}

content_en = {
    "lang": "en",
    "slug": "how-to-use-aba",
    "title": "How to Use ABA Bank Transfer Safely and Quickly?",
    "desc": "ABA transfer is the most common payment method in Cambodia. This article provides a detailed guide on how to safely transfer and verify receipts via ABA Mobile App for KhmerX.",
    "keywords": "ABA transfer tutorial, Cambodia ABA, ABA bank transfer, KhmerX ABA, ABA payment guide",
    "cover_img": "https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=ABA%20bank%20transfer%20mobile%20app%20UI%20mockup%20Cambodia%20Phnom%20Penh%20financial%20technology%20blue%20tones&image_size=landscape_16_9",
    "category": "ABA Guides",
    "category_slug": "aba",
    "km_active": "", "en_active": "bg-white shadow-sm text-blue-600", "zh_active": "",
    "nav_borrow": "How to Borrow", "nav_fees": "Fees", "nav_faq": "FAQ", "nav_contact": "Contact", "nav_cta": "Open Mini App",
    
    "content": """
<h2>What is ABA Bank Transfer?</h2>
<p>ABA Bank (Advanced Bank of Asia) is one of the largest and most popular commercial banks in Cambodia. Its <strong>ABA Mobile App</strong> has practically become the "infrastructure" for local life and business transactions. From grocery shopping to peer-to-peer transfers, ABA provides exceptional convenience.</p>

<h2>How to Use ABA Transfers in KhmerX?</h2>
<p>On the KhmerX platform, all funds (lending and repayment) flow directly between the personal ABA accounts of the users. The platform does not hold any funds. Here are the standard steps:</p>
<h3>Step 1: Bind your ABA Account</h3>
<p>After entering the KhmerX Telegram Mini App, you first need to bind your ABA account number and real name in the "Profile" section. Make sure the name matches exactly with your bank account to avoid matching issues.</p>
<h3>Step 2: Get the Counterparty's Account</h3>
<p>When a loan request is successfully matched, the lender can see the borrower's ABA account in the order details. Similarly, on the repayment date, the borrower will see the lender's ABA account.</p>
<h3>Step 3: Transfer via ABA Mobile</h3>
<ul>
  <li>Open the ABA Mobile App on your phone.</li>
  <li>Tap <strong>Transfers</strong>, then select <strong>To ABA Account</strong>.</li>
  <li>Enter the account number and amount provided on KhmerX.</li>
  <li><strong>CRITICAL:</strong> Verify that the receiver's name displayed matches the name on the KhmerX order.</li>
  <li>Confirm and enter your PIN to complete the transfer.</li>
</ul>

<h2>Important Notes & Security</h2>
<p>To ensure your funds are safe, please pay attention to the following:</p>
<ul>
  <li><strong>Verify Names:</strong> Always check the receiver's name inside the ABA App before transferring. If it doesn't match, stop immediately and cancel the transaction in KhmerX or contact support.</li>
  <li><strong>Keep Receipts:</strong> After a successful transfer, the ABA App generates an e-receipt with a Transaction ID. Save this screenshot and upload it to the KhmerX order page to update the transaction status.</li>
  <li><strong>Beware of Scams:</strong> KhmerX official support will NEVER ask you to transfer money to any "safe account" or private account. Transactions are strictly between matched users.</li>
</ul>
    """,
    
    "risk_title": "Borrowing & Repayment Risk Notice",
    "risk_desc": "Before making any ABA transfer, please ensure you confirm:",
    "risk_1": "Actual receive amount (amount after deducted fees)", "risk_2": "Borrowing duration and exact due date", "risk_3": "Total amount to repay at maturity",
    
    "faq_1_q": "Are there fees for ABA transfers?", "faq_1_a": "Usually, transfers between personal ABA accounts in USD or KHR are free of charge, subject to ABA Bank's official policies.",
    "faq_2_q": "How does KhmerX know I have repaid?", "faq_2_a": "You must upload the successful ABA transfer screenshot (showing the Transaction ID) to the specific order in KhmerX. Once the lender verifies receipt, the order is marked complete.",
    
    "link_borrow": "View Borrow Process", "link_faq": "Browse FAQ",
    
    "related_title": "Related Posts",
    "related_1_title": "Complete Guide to Telegram Mini App Finance Tools",
    "related_2_title": "3 Things You Must Know Before Applying for a Micro Loan",
    "read_btn": "Read Article",
    
    "cta_title": "Open KhmerX Mini App Now", "cta_btn": "Open Telegram"
}

content_km = {
    "lang": "km",
    "slug": "how-to-use-aba",
    "title": "តើត្រូវប្រើប្រាស់ការផ្ទេរប្រាក់ ABA ឱ្យមានសុវត្ថិភាពយ៉ាងដូចម្តេច?",
    "desc": "នៅកម្ពុជា ការផ្ទេរប្រាក់ ABA គឺជាវិធីសាស្ត្រទូទាត់ទូទៅបំផុត។ អត្ថបទនេះបង្ហាញលម្អិតពីរបៀបផ្ទេរនិងផ្ទៀងផ្ទាត់ដោយសុវត្ថិភាពតាមរយៈ ABA Mobile App ។",
    "keywords": "ABA transfer tutorial, Cambodia ABA, ABA bank transfer, របៀបផ្ទេរប្រាក់ ABA",
    "cover_img": "https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=ABA%20bank%20transfer%20mobile%20app%20UI%20mockup%20Cambodia%20Phnom%20Penh%20financial%20technology%20blue%20tones&image_size=landscape_16_9",
    "category": "ការណែនាំ ABA",
    "category_slug": "aba",
    "km_active": "bg-white shadow-sm text-blue-600", "en_active": "", "zh_active": "",
    "nav_borrow": "របៀបខ្ចីប្រាក់", "nav_fees": "ថ្លៃសេវា", "nav_faq": "សំណួរដែលសួរញឹកញាប់", "nav_contact": "ទំនាក់ទំនង", "nav_cta": "បើក Mini App",
    
    "content": """
<h2>តើអ្វីទៅជាការផ្ទេរប្រាក់ ABA?</h2>
<p>ធនាគារ ABA គឺជាធនាគារពាណិជ្ជដ៏ធំ និងពេញនិយមបំផុតមួយនៅកម្ពុជា។ <strong>ABA Mobile App</strong> របស់វាបានក្លាយជាផ្នែកសំខាន់នៃជីវិតរស់នៅ និងប្រតិបត្តិការអាជីវកម្មក្នុងស្រុក។</p>

<h2>របៀបប្រើប្រាស់ការផ្ទេរប្រាក់ ABA ក្នុង KhmerX</h2>
<p>នៅលើវេទិកា KhmerX រាល់ការផ្ទេរប្រាក់ត្រូវធ្វើឡើងដោយផ្ទាល់រវាងគណនី ABA ផ្ទាល់ខ្លួនរបស់អ្នកប្រើប្រាស់។ នេះជាជំហានស្តង់ដារ៖</p>
<h3>ជំហានទី 1៖ ភ្ជាប់គណនី ABA របស់អ្នក</h3>
<p>ចូលទៅកាន់ KhmerX Telegram Mini App បន្ទាប់មកភ្ជាប់លេខគណនី ABA និងឈ្មោះពិតរបស់អ្នកក្នុងផ្នែក "ប្រវត្តិរូប"។</p>
<h3>ជំហានទី 2៖ ទទួលគណនីរបស់អ្នកម្ខាងទៀត</h3>
<p>នៅពេលសំណើត្រូវបានផ្គូផ្គង អ្នកអាចមើលឃើញគណនី ABA របស់ភាគីម្ខាងទៀតនៅក្នុងព័ត៌មានលម្អិតនៃការបញ្ជាទិញ។</p>
<h3>ជំហានទី 3៖ ផ្ទេរប្រាក់តាម ABA Mobile</h3>
<ul>
  <li>បើក ABA Mobile App នៅលើទូរស័ព្ទរបស់អ្នក។</li>
  <li>ចុចលើ <strong>Transfers</strong> បន្ទាប់មកជ្រើសរើស <strong>To ABA Account</strong>។</li>
  <li>បញ្ចូលលេខគណនី និងចំនួនទឹកប្រាក់។</li>
  <li><strong>សំខាន់ណាស់៖</strong> ផ្ទៀងផ្ទាត់ឈ្មោះអ្នកទទួលឱ្យត្រូវនឹងឈ្មោះនៅលើ KhmerX ។</li>
  <li>បញ្ជាក់ និងបញ្ចូលលេខ PIN របស់អ្នក។</li>
</ul>

<h2>ការណែនាំអំពីសុវត្ថិភាព</h2>
<ul>
  <li><strong>ផ្ទៀងផ្ទាត់ឈ្មោះ៖</strong> តែងតែពិនិត្យឈ្មោះអ្នកទទួលមុនពេលផ្ទេរប្រាក់។</li>
  <li><strong>រក្សាទុកវិក័យប័ត្រ៖</strong> ថតរូបអេក្រង់វិក័យប័ត្រផ្ទេរប្រាក់ ហើយបញ្ចូលវាក្នុង KhmerX ។</li>
  <li><strong>ប្រយ័ត្នការបោកប្រាស់៖</strong> KhmerX នឹងមិនស្នើសុំឱ្យអ្នកផ្ទេរប្រាក់ទៅគណនីឯកជនឡើយ។</li>
</ul>
    """,
    
    "risk_title": "ការព្រមានអំពីហានិភ័យ",
    "risk_desc": "មុនពេលធ្វើការផ្ទេរប្រាក់ ABA សូមប្រាកដថាអ្នកបានបញ្ជាក់៖",
    "risk_1": "ចំនួនប្រាក់ទទួលបានជាក់ស្តែង", "risk_2": "រយៈពេលនិងថ្ងៃកំណត់", "risk_3": "ចំនួនប្រាក់សងសរុប",
    
    "faq_1_q": "តើការផ្ទេរប្រាក់ ABA មានគិតថ្លៃសេវាទេ?", "faq_1_a": "ជាធម្មតា ការផ្ទេរប្រាក់រវាងគណនី ABA ផ្ទាល់ខ្លួនគឺមិនគិតថ្លៃទេ។",
    "faq_2_q": "តើ KhmerX ដឹងថាខ្ញុំបានសងប្រាក់ដោយរបៀបណា?", "faq_2_a": "អ្នកត្រូវតែបញ្ចូលរូបថតអេក្រង់វិក័យប័ត្រ ABA ដែលមាន Transaction ID ទៅក្នុង Mini App ។",
    
    "link_borrow": "មើលដំណើរការខ្ចីប្រាក់", "link_faq": "សំណួរដែលសួរញឹកញាប់",
    
    "related_title": "អត្ថបទពាក់ព័ន្ធ",
    "related_1_title": "ការណែនាំពេញលេញអំពីឧបករណ៍ហិរញ្ញវត្ថុ Telegram Mini App",
    "related_2_title": "រឿង 3 យ៉ាងដែលត្រូវដឹងមុនពេលខ្ចីប្រាក់តូច",
    "read_btn": "អានអត្ថបទ",
    
    "cta_title": "បើក KhmerX Mini App ឥឡូវនេះ", "cta_btn": "បើក Telegram"
}

import os

os.makedirs(r'D:\projects\khmerx\frontend\website\zh\blog\article', exist_ok=True)
os.makedirs(r'D:\projects\khmerx\frontend\website\en\blog\article', exist_ok=True)
os.makedirs(r'D:\projects\khmerx\frontend\website\km\blog\article', exist_ok=True)

with open(r'D:\projects\khmerx\frontend\website\zh\blog\article\index.html', 'w', encoding='utf-8') as f:
    f.write(article_template.format(**content_zh))
with open(r'D:\projects\khmerx\frontend\website\en\blog\article\index.html', 'w', encoding='utf-8') as f:
    f.write(article_template.format(**content_en))
with open(r'D:\projects\khmerx\frontend\website\km\blog\article\index.html', 'w', encoding='utf-8') as f:
    f.write(article_template.format(**content_km))

print("Blog article pages generated.")
