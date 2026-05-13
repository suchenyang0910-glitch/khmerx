import { useTranslation } from 'react-i18next';
import { Helmet } from 'react-helmet-async';
import { useParams } from 'react-router-dom';

export default function Article() {
  const { t } = useTranslation();
  const { lang } = useParams();

  return (
    <>
      <Helmet>
        <title>{t('article.title')}</title>
        <meta name="description" content={t('article.desc')} />
        <meta name="keywords" content={t('article.keywords')} />
        <script type="application/ld+json">{`{
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "mainEntityOfPage": {
          "@type": "WebPage",
          "@id": "https://khmerx.org/${lang}/blog/article/${t('article.slug')}"
        },
        "headline": "${t('article.title')}",
        "description": "${t('article.desc')}",
        "image": "${t('article.cover_img')}",  
        "author": {
          "@type": "Organization",
          "name": "KhmerX Team",
          "url": "https://khmerx.org"
        },  
        "publisher": {
          "@type": "Organization",
          "name": "KhmerX",
          "logo": {
            "@type": "ImageObject",
            "url": "https://khmerx.org/logo.jpg"
          }
        },
        "datePublished": "2026-05-10",
        "dateModified": "2026-05-10"
      }`}</script>
        <script type="application/ld+json">{`{
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
          {
            "@type": "ListItem",
            "position": 1,
            "name": "Home",
            "item": "https://khmerx.org/${lang}"
          },
          {
            "@type": "ListItem",
            "position": 2,
            "name": "Blog",
            "item": "https://khmerx.org/${lang}/blog"
          },
          {
            "@type": "ListItem",
            "position": 3,
            "name": "${t('article.title')}"
          }
        ]
      }`}</script>
        <script type="application/ld+json">{`{
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
          {
            "@type": "Question",
            "name": "${t('article.faq_1_q')}",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "${t('article.faq_1_a')}"
            }
          },
          {
            "@type": "Question",
            "name": "${t('article.faq_2_q')}",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "${t('article.faq_2_a')}"
            }
          }
        ]
      }`}</script>
      </Helmet>

      <div className="flex-1">
        {/*  Sticky Header  */}
      <header className="sticky top-0 z-50 border-b bg-white/90 backdrop-blur-md">
        <div className="mx-auto flex max-w-[1200px] items-center justify-between px-5 py-4">
          <a href={`/${lang}`} className="flex items-center gap-3 group">
            <img src="/logo.jpg" alt="KhmerX Logo" className="h-10 w-10 rounded-xl object-cover shadow-sm group-hover:scale-105 transition-transform" />
            <div>
              <div className="font-bold text-lg text-slate-900">KhmerX</div>
            </div>
          </a>
          <nav className="hidden gap-8 text-sm font-medium text-slate-600 md:flex">
            <a className="text-blue-600 transition-colors" href={`/${lang}/blog`}>Blog</a>
            <a className="hover:text-blue-600 transition-colors" href={`/${lang}/faq`}>{t('article.nav_faq')}</a>
            <a className="hover:text-blue-600 transition-colors" href={`/${lang}/contact`}>{t('article.nav_contact')}</a>
          </nav>
          <div className="flex items-center gap-4">
            <a className="inline-flex rounded-xl bg-gradient-to-r from-[#0A5BFF] to-[#00AEEF] px-5 py-2.5 text-sm font-bold text-white shadow-md hover:shadow-lg hover:scale-105 transition-all" href="https://t.me/KhmerXBot/app">{t('article.nav_cta')}</a>
          </div>
        </div>
      </header>

      {/*  文章头部  */}
      <article className="mx-auto max-w-[800px] px-5 pt-16 pb-12">
        {/*  分类与标签  */}
        <div className="flex gap-2 mb-6">
          <a href={`/${lang}/blog/${t('article.category_slug')}`} className="inline-flex rounded-full bg-blue-100 px-3 py-1 text-xs font-bold text-blue-700 uppercase tracking-wider hover:bg-blue-200 transition-colors">{t('article.category')}</a>
        </div>
        
        {/*  H1 标题  */}
        <h1 className="text-3xl md:text-4xl lg:text-5xl font-extrabold text-slate-900 leading-tight mb-6">
          {t('article.title')}
        </h1>
        
        {/*  描述  */}
        <p className="text-xl text-slate-500 mb-8 leading-relaxed">
          {t('article.desc')}
        </p>
        
        {/*  作者与时间  */}
        <div className="flex items-center gap-4 py-6 border-y border-slate-100 mb-10">
          <div className="w-12 h-12 rounded-full bg-slate-200 overflow-hidden">
            <img src="/logo.jpg" alt="KhmerX Team" className="w-full h-full object-cover grayscale" />
          </div>
          <div>
            <div className="font-bold text-slate-900">KhmerX Team</div>
            <div className="text-sm text-slate-500 flex items-center gap-2">
              <span>May 10, 2026</span>
              <span>·</span>
              <span>5 min read</span>
            </div>
          </div>
        </div>
        
        {/*  封面图  */}
        <div className="aspect-[16/9] rounded-[2rem] overflow-hidden mb-12 shadow-lg border border-slate-100">
          <img src="{t('article.cover_img')}" alt="{t('article.title')}" className="w-full h-full object-cover" />
        </div>
        
        {/*  正文内容 (Prose)  */}
        <div className="prose prose-lg max-w-none">
          {t('article.content')}
        </div>
        
        {/*  风险提示模块  */}
        <div className="mt-12 bg-[#FFFBEB] border-2 border-[#FDE68A] rounded-2xl p-6 flex gap-4 items-start">
          <svg className="w-8 h-8 text-[#F59E0B] shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
          <div>
            <h4 className="font-bold text-[#92400E] text-lg mb-2">{t('article.risk_title')}</h4>
            <p className="text-[#B45309] font-medium">{t('article.risk_desc')}</p>
            <ul className="list-disc list-inside text-[#B45309] mt-2 space-y-1">
              <li>{t('article.risk_1')}</li>
              <li>{t('article.risk_2')}</li>
              <li>{t('article.risk_3')}</li>
            </ul>
          </div>
        </div>
        
        {/*  文章 FAQ  */}
        <div className="mt-16 border-t border-slate-100 pt-12">
          <h3 className="text-2xl font-bold text-slate-900 mb-8">FAQ</h3>
          <div className="space-y-4">
            <details className="group rounded-2xl border border-slate-200 bg-white [&_summary::-webkit-details-marker]:hidden">
              <summary className="flex cursor-pointer items-center justify-between p-5 font-bold text-lg text-slate-900 hover:bg-slate-50 transition-colors">
                {t('article.faq_1_q')}
                <span className="transition group-open:rotate-180 text-blue-500">
                  <svg fill="none" height="24" shape-rendering="geometricPrecision" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" viewBox="0 0 24 24" width="24"><path d="M6 9l6 6 6-6"></path></svg>
                </span>
              </summary>
              <div className="px-5 pb-5 text-slate-600 border-t border-slate-100 pt-4">
                <p>{t('article.faq_1_a')}</p>
              </div>
            </details>
            <details className="group rounded-2xl border border-slate-200 bg-white [&_summary::-webkit-details-marker]:hidden">
              <summary className="flex cursor-pointer items-center justify-between p-5 font-bold text-lg text-slate-900 hover:bg-slate-50 transition-colors">
                {t('article.faq_2_q')}
                <span className="transition group-open:rotate-180 text-blue-500">
                  <svg fill="none" height="24" shape-rendering="geometricPrecision" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" viewBox="0 0 24 24" width="24"><path d="M6 9l6 6 6-6"></path></svg>
                </span>
              </summary>
              <div className="px-5 pb-5 text-slate-600 border-t border-slate-100 pt-4">
                <p>{t('article.faq_2_a')}</p>
              </div>
            </details>
          </div>
        </div>
        
        {/*  内链导航  */}
        <div className="mt-12 flex flex-wrap gap-4 pt-8 border-t border-slate-100">
          <a href={`/${lang}/borrow`} className="inline-flex items-center gap-2 text-sm font-bold text-slate-600 bg-slate-100 px-4 py-2 rounded-xl hover:bg-blue-100 hover:text-blue-700 transition-colors">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            {t('article.link_borrow')}
          </a>
          <a href={`/${lang}/faq`} className="inline-flex items-center gap-2 text-sm font-bold text-slate-600 bg-slate-100 px-4 py-2 rounded-xl hover:bg-blue-100 hover:text-blue-700 transition-colors">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            {t('article.link_faq')}
          </a>
        </div>
      </article>

      {/*  相关推荐模块  */}
      <section className="bg-slate-50 py-16 border-y border-slate-200">
        <div className="mx-auto max-w-[1200px] px-5">
          <h3 className="text-2xl font-bold text-slate-900 mb-8">{t('article.related_title')}</h3>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-8">
            {/*  Related 1  */}
            <a href={`/${lang}/blog/article/telegram-finance-guide`} className="bg-white rounded-2xl overflow-hidden shadow-sm border border-slate-200 group hover:shadow-md transition-shadow block">
              <div className="aspect-video bg-slate-100 overflow-hidden relative">
                <img src="https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=Telegram%20app%20chat%20interface%20with%20financial%20dashboard%20bot%20digital%20finance%20blue%20clean%20style&image_size=landscape_16_9" alt="Telegram Guide" className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" loading="lazy" />
                <div className="absolute top-3 left-3 bg-slate-800 text-white text-[10px] font-bold px-2 py-1 rounded-full uppercase tracking-wider">Telegram</div>
              </div>
              <div className="p-5">
                <h4 className="font-bold text-slate-900 mb-2 group-hover:text-blue-600 transition-colors line-clamp-2">{t('article.related_1_title')}</h4>
                <span className="text-blue-600 text-sm font-bold inline-flex items-center">
                  {t('article.read_btn')}
                  <svg className="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
                </span>
              </div>
            </a>
            {/*  Related 2  */}
            <a href={`/${lang}/blog/article/micro-loan-tips`} className="bg-white rounded-2xl overflow-hidden shadow-sm border border-slate-200 group hover:shadow-md transition-shadow block">
              <div className="aspect-video bg-slate-100 overflow-hidden relative">
                <img src="https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=Small%20amount%20of%20money%20financial%20planning%20calculator%20coins%20business%20desk%20clean%20bright%20lighting&image_size=landscape_16_9" alt="Micro Loan Tips" className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" loading="lazy" />
                <div className="absolute top-3 left-3 bg-green-600 text-white text-[10px] font-bold px-2 py-1 rounded-full uppercase tracking-wider">Loan</div>
              </div>
              <div className="p-5">
                <h4 className="font-bold text-slate-900 mb-2 group-hover:text-blue-600 transition-colors line-clamp-2">{t('article.related_2_title')}</h4>
                <span className="text-blue-600 text-sm font-bold inline-flex items-center">
                  {t('article.read_btn')}
                  <svg className="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
                </span>
              </div>
            </a>
          </div>
        </div>
      </section>

      {/*  Telegram CTA（最重要）  */}
      <section className="mx-auto max-w-[1200px] px-5 py-24">
        <div className="bg-gradient-to-br from-[#0A5BFF] to-[#00AEEF] rounded-[3rem] p-10 md:p-16 text-center text-white shadow-2xl relative overflow-hidden">
          <div className="absolute top-0 right-0 -mt-20 -mr-20 w-64 h-64 bg-white opacity-10 rounded-full blur-3xl"></div>
          <div className="absolute bottom-0 left-0 -mb-20 -ml-20 w-64 h-64 bg-white opacity-10 rounded-full blur-3xl"></div>
          
          <div className="relative z-10 max-w-2xl mx-auto">
            <h2 className="text-3xl md:text-5xl font-bold mb-8">{t('article.cta_title')}</h2>
            <div className="flex flex-col items-center justify-center gap-8">
              <div className="bg-white p-4 rounded-3xl shadow-lg inline-block">
                <img className="w-48 h-48 rounded-2xl" alt="KhmerX Mini App QR" src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https%3A%2F%2Ft.me%2FKhmerXBot%2Fapp" />
                <div className="text-slate-500 text-sm font-medium mt-3">Scan with Camera</div>
              </div>
              <a className="inline-flex justify-center items-center rounded-2xl bg-white px-10 py-5 text-xl font-bold text-blue-600 shadow-xl hover:shadow-2xl hover:scale-105 transition-all duration-300" href="https://t.me/KhmerXBot/app">
                <svg className="w-6 h-6 mr-3" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.74-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .38z"/></svg>
                {t('article.cta_btn')}
              </a>
            </div>
          </div>
        </div>
      </section>
      </div>
    </>
  );
}
