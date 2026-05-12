import { useTranslation } from 'react-i18next';
import { Helmet } from 'react-helmet-async';
import { useParams } from 'react-router-dom';

export default function Blog() {
  const { t } = useTranslation();
  const { lang } = useParams();

  return (
    <>
      <Helmet>
        <title>{t('blog.title')}</title>
        <meta name="description" content={t('blog.desc')} />
        <meta name="keywords" content={t('blog.keywords')} />
      </Helmet>

      <div className="flex-1">
        {/*  Hero 区  */}
      <section className="bg-white border-b border-slate-100 pt-20 pb-16">
        <div className="mx-auto max-w-[1200px] px-5 text-center">
          <h1 className="text-4xl md:text-5xl font-extrabold text-slate-900 mb-6">{t('blog.hero_title')}</h1>
          <p className="text-lg text-slate-600 max-w-2xl mx-auto">{t('blog.hero_subtitle')}</p>
        </div>
      </section>

      {/*  分类导航  */}
      <section className="bg-white border-b border-slate-100 sticky top-[73px] z-40">
        <div className="mx-auto max-w-[1200px] px-5">
          <div className="flex overflow-x-auto py-4 gap-6 scrollbar-hide text-sm font-medium">
            <a href="/{lang}/blog" className="text-blue-600 whitespace-nowrap border-b-2 border-blue-600 pb-1 px-1">All Posts</a>
            <a href="/{lang}/blog/aba" className="text-slate-500 hover:text-blue-600 whitespace-nowrap px-1">{t('blog.cat_aba')}</a>
            <a href="/{lang}/blog/telegram" className="text-slate-500 hover:text-blue-600 whitespace-nowrap px-1">{t('blog.cat_tg')}</a>
            <a href="/{lang}/blog/loan" className="text-slate-500 hover:text-blue-600 whitespace-nowrap px-1">{t('blog.cat_loan')}</a>
            <a href="/{lang}/blog/phnom-penh" className="text-slate-500 hover:text-blue-600 whitespace-nowrap px-1">{t('blog.cat_pp')}</a>
          </div>
        </div>
      </section>

      {/*  博客列表主体  */}
      <section className="mx-auto max-w-[1200px] px-5 py-12">
        <div className="grid lg:grid-cols-3 gap-12">
          
          <div className="lg:col-span-2 space-y-12">
            {/*  精选文章 (Feature)  */}
            <article className="bg-white rounded-[2rem] overflow-hidden shadow-sm border border-slate-200 group hover:shadow-lg transition-shadow">
              <a href="/{lang}/blog/article/how-to-use-aba" className="block">
                <div className="aspect-[16/9] bg-slate-100 overflow-hidden relative">
                  <img src="https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=ABA%20bank%20transfer%20mobile%20app%20UI%20mockup%20Cambodia%20Phnom%20Penh%20financial%20technology%20blue%20tones&image_size=landscape_16_9" alt="ABA Transfer Guide" className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" loading="lazy" />
                  <div className="absolute top-4 left-4 bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">{t('blog.cat_aba')}</div>
                </div>
                <div className="p-8">
                  <div className="text-sm text-slate-500 mb-3 flex items-center gap-4">
                    <span>Oct 20, 2026</span>
                    <span>5 min read</span>
                  </div>
                  <h2 className="text-2xl font-bold text-slate-900 mb-4 group-hover:text-blue-600 transition-colors">{t('blog.feat_1_title')}</h2>
                  <p className="text-slate-600 leading-relaxed line-clamp-2 mb-6">{t('blog.feat_1_desc')}</p>
                  <span className="inline-flex items-center text-blue-600 font-bold hover:text-blue-800">
                    {t('blog.read_more')}
                    <svg className="w-5 h-5 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path></svg>
                  </span>
                </div>
              </a>
            </article>

            <div className="grid sm:grid-cols-2 gap-8">
              {/*  Article 2  */}
              <article className="bg-white rounded-3xl overflow-hidden shadow-sm border border-slate-200 group hover:shadow-md transition-shadow">
                <a href="/{lang}/blog/article/telegram-finance-guide" className="block">
                  <div className="aspect-[16/9] bg-slate-100 overflow-hidden relative">
                    <img src="https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=Telegram%20app%20chat%20interface%20with%20financial%20dashboard%20bot%20digital%20finance%20blue%20clean%20style&image_size=landscape_16_9" alt="Telegram Finance Guide" className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" loading="lazy" />
                    <div className="absolute top-4 left-4 bg-slate-800 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">{t('blog.cat_tg')}</div>
                  </div>
                  <div className="p-6">
                    <div className="text-xs text-slate-500 mb-2">Oct 18, 2026</div>
                    <h3 className="text-lg font-bold text-slate-900 mb-2 group-hover:text-blue-600 transition-colors line-clamp-2">{t('blog.list_2_title')}</h3>
                    <p className="text-sm text-slate-600 line-clamp-2 mb-4">{t('blog.list_2_desc')}</p>
                  </div>
                </a>
              </article>
              
              {/*  Article 3  */}
              <article className="bg-white rounded-3xl overflow-hidden shadow-sm border border-slate-200 group hover:shadow-md transition-shadow">
                <a href="/{lang}/blog/article/micro-loan-tips" className="block">
                  <div className="aspect-[16/9] bg-slate-100 overflow-hidden relative">
                    <img src="https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=Small%20amount%20of%20money%20financial%20planning%20calculator%20coins%20business%20desk%20clean%20bright%20lighting&image_size=landscape_16_9" alt="Micro Loan Tips" className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" loading="lazy" />
                    <div className="absolute top-4 left-4 bg-green-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">{t('blog.cat_loan')}</div>
                  </div>
                  <div className="p-6">
                    <div className="text-xs text-slate-500 mb-2">Oct 15, 2026</div>
                    <h3 className="text-lg font-bold text-slate-900 mb-2 group-hover:text-blue-600 transition-colors line-clamp-2">{t('blog.list_3_title')}</h3>
                    <p className="text-sm text-slate-600 line-clamp-2 mb-4">{t('blog.list_3_desc')}</p>
                  </div>
                </a>
              </article>
            </div>
            
            <div className="text-center pt-8 border-t border-slate-200">
              <button className="inline-flex items-center px-6 py-3 rounded-xl border-2 border-slate-200 font-bold text-slate-700 hover:border-slate-300 hover:bg-white transition-colors">
                Load More Posts
              </button>
            </div>
          </div>
          
          {/*  Sidebar  */}
          <div className="space-y-8">
            {/*  热门关键词  */}
            <div className="bg-white rounded-3xl p-6 border border-slate-200">
              <h3 className="font-bold text-slate-900 mb-4 flex items-center gap-2">
                <svg className="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 20l4-16m2 16l4-16M6 9h14M4 15h14"></path></svg>
                {t('blog.tag_title')}
              </h3>
              <div className="flex flex-wrap gap-2">
                <a href="#" className="px-3 py-1.5 bg-slate-100 hover:bg-blue-100 hover:text-blue-700 text-slate-600 rounded-lg text-sm transition-colors">{t('blog.tag_1')}</a>
                <a href="#" className="px-3 py-1.5 bg-slate-100 hover:bg-blue-100 hover:text-blue-700 text-slate-600 rounded-lg text-sm transition-colors">{t('blog.tag_2')}</a>
                <a href="#" className="px-3 py-1.5 bg-slate-100 hover:bg-blue-100 hover:text-blue-700 text-slate-600 rounded-lg text-sm transition-colors">{t('blog.tag_3')}</a>
                <a href="#" className="px-3 py-1.5 bg-slate-100 hover:bg-blue-100 hover:text-blue-700 text-slate-600 rounded-lg text-sm transition-colors">{t('blog.tag_4')}</a>
                <a href="#" className="px-3 py-1.5 bg-slate-100 hover:bg-blue-100 hover:text-blue-700 text-slate-600 rounded-lg text-sm transition-colors">ABA Transfer</a>
                <a href="#" className="px-3 py-1.5 bg-slate-100 hover:bg-blue-100 hover:text-blue-700 text-slate-600 rounded-lg text-sm transition-colors">Telegram Bot</a>
              </div>
            </div>
            
            {/*  CTA Widget  */}
            <div className="bg-gradient-to-br from-[#0A5BFF] to-[#00AEEF] rounded-3xl p-8 text-white text-center shadow-lg relative overflow-hidden">
              <div className="absolute top-0 right-0 w-32 h-32 bg-white rounded-full blur-3xl opacity-20 -mr-10 -mt-10"></div>
              <h3 className="text-2xl font-bold mb-4 relative z-10">{t('blog.sidebar_cta_title')}</h3>
              <p className="text-blue-100 mb-6 relative z-10 text-sm">{t('blog.sidebar_cta_desc')}</p>
              <div className="bg-white p-3 rounded-2xl shadow-lg inline-block mb-6 relative z-10">
                <img className="w-32 h-32 rounded-xl" alt="KhmerX Mini App QR" src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=https%3A%2F%2Ft.me%2FKhmerXBot%2Fapp" />
              </div>
              <a className="block w-full rounded-xl bg-white px-6 py-3 font-bold text-blue-600 shadow-md hover:shadow-lg transition-shadow relative z-10" href="https://t.me/KhmerXBot/app">
                {t('blog.sidebar_cta_btn')}
              </a>
            </div>
          </div>
          
        </div>
      </section>
      </div>
    </>
  );
}
