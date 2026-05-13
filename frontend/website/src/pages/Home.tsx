import { useTranslation } from 'react-i18next';
import { Helmet } from 'react-helmet-async';
import { motion } from 'framer-motion';
import { Shield, Clock, FileText, Send } from 'lucide-react';
import { Link, useParams } from 'react-router-dom';

export default function Home() {
  const { t } = useTranslation();
  const { lang } = useParams();

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "KhmerX",
    "url": "https://khmerx.org/" + lang,
    "description": t('home.seo_desc', 'KhmerX Telegram Mini App'),
    "potentialAction": {
      "@type": "SearchAction",
      "target": "https://khmerx.org/" + lang + "/faq?q={search_term_string}",
      "query-input": "required name=search_term_string"
    }
  };

  const faqSchema = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {
        "@type": "Question",
        "name": t('home.faq1_q'),
        "acceptedAnswer": {
          "@type": "Answer",
          "text": t('home.faq1_a')
        }
      },
      {
        "@type": "Question",
        "name": t('home.faq2_q'),
        "acceptedAnswer": {
          "@type": "Answer",
          "text": t('home.faq2_a')
        }
      },
      {
        "@type": "Question",
        "name": t('home.faq3_q'),
        "acceptedAnswer": {
          "@type": "Answer",
          "text": t('home.faq3_a')
        }
      }
    ]
  };

  return (
    <>
      <Helmet>
        <title>{t('home.seo_title')}</title>
        <meta name="description" content={t('home.seo_desc')} />
        <meta name="keywords" content={t('home.seo_keywords')} />
        <script type="application/ld+json">{JSON.stringify(jsonLd)}</script>
        <script type="application/ld+json">{JSON.stringify(faqSchema)}</script>
      </Helmet>

      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-b from-blue-50 to-white px-5 pt-20 pb-32">
        <div className="mx-auto max-w-7xl grid gap-12 lg:grid-cols-2 lg:items-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="max-w-2xl"
          >
            <div className="mb-6 inline-flex rounded-full bg-blue-100 px-4 py-2 text-sm font-semibold text-blue-700">
              {t('home.hero_badge')}
            </div>
            <h1 className="text-4xl font-bold leading-tight tracking-tight text-slate-900 sm:text-5xl lg:text-6xl" dangerouslySetInnerHTML={{__html: t('home.hero_title')}}>
            </h1>
            <p className="mt-6 text-lg leading-relaxed text-slate-600 sm:text-xl" dangerouslySetInnerHTML={{__html: t('home.hero_subtitle')}}>
            </p>
            <div className="mt-10 flex flex-col gap-4 sm:flex-row">
              <a
                href="https://t.me/KhmerXBot/app"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center justify-center rounded-xl bg-[#0A5BFF] px-8 py-4 text-lg font-semibold text-white shadow-lg transition-all hover:bg-blue-700 hover:shadow-xl hover:shadow-blue-500/30"
              >
                {t('home.hero_cta')}
              </a>
              <Link
                to={`/${lang}/borrow`}
                className="inline-flex items-center justify-center rounded-xl border-2 border-slate-200 bg-white px-8 py-4 text-lg font-semibold text-slate-700 transition-colors hover:border-slate-300 hover:bg-slate-50"
              >
                {t('home.hero_secondary')}
              </Link>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="relative mx-auto w-full max-w-[320px] lg:max-w-md"
          >
            <div className="absolute -inset-4 rounded-[3rem] bg-gradient-to-br from-blue-400 to-cyan-300 opacity-30 blur-2xl filter"></div>
            <div className="relative rounded-[2.5rem] border-8 border-slate-900 bg-white shadow-2xl overflow-hidden aspect-[9/19]">
              {/* Mockup Content */}
              <div className="h-full w-full bg-slate-50 p-6 flex flex-col">
                <div className="mt-8 rounded-2xl bg-gradient-to-br from-blue-600 to-blue-400 p-6 text-white shadow-lg">
                  <div className="text-sm opacity-80">Credit Limit</div>
                  <div className="mt-1 text-3xl font-bold">$100.00</div>
                </div>
                <div className="mt-6 flex-1 rounded-2xl bg-white p-5 shadow-sm">
                  <div className="font-semibold text-slate-800">Current Loan</div>
                  <div className="mt-4 space-y-3">
                    <div className="flex justify-between text-sm"><span className="text-slate-500">Amount</span><span className="font-medium">$50.00</span></div>
                    <div className="flex justify-between text-sm"><span className="text-slate-500">Duration</span><span className="font-medium">7 Days</span></div>
                    <div className="flex justify-between text-sm"><span className="text-slate-500">Repay</span><span className="font-bold text-blue-600">$50.00</span></div>
                  </div>
                  <button className="mt-6 w-full rounded-xl bg-slate-900 py-3 font-semibold text-white">Borrow Now</button>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 bg-white px-5">
        <div className="mx-auto max-w-7xl">
          <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-5">
            {[
              { icon: <Send className="h-8 w-8 text-blue-600" />, title: 'home.feat1_title', desc: 'home.feat1_desc' },
              { icon: <Send className="h-8 w-8 text-blue-600" />, title: 'home.feat2_title', desc: 'home.feat2_desc' },
              { icon: <Clock className="h-8 w-8 text-blue-600" />, title: 'home.feat3_title', desc: 'home.feat3_desc' },
              { icon: <Shield className="h-8 w-8 text-blue-600" />, title: 'home.feat4_title', desc: 'home.feat4_desc' },
              { icon: <FileText className="h-8 w-8 text-blue-600" />, title: 'home.feat5_title', desc: 'home.feat5_desc' }
            ].map((feat, i) => (
              <motion.div
                key={i}
                whileHover={{ y: -5 }}
                className="rounded-2xl border border-slate-100 bg-white p-6 shadow-sm transition-all hover:shadow-md"
              >
                <div className="mb-4 inline-flex rounded-xl bg-blue-50 p-3">{feat.icon}</div>
                <h3 className="text-lg font-semibold text-slate-900">{t(feat.title)}</h3>
                <p className="mt-2 text-sm text-slate-600">{t(feat.desc)}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Example Section */}
      <section className="py-24 bg-slate-50 px-5">
        <div className="mx-auto max-w-4xl text-center">
          <h2 className="text-3xl font-bold text-slate-900">{t('home.ex_title')}</h2>

          <div className="mt-12 rounded-3xl bg-white p-8 shadow-lg sm:p-12">
            <div className="grid gap-6 sm:grid-cols-4 divide-y sm:divide-y-0 sm:divide-x divide-slate-100">
              <div className="px-4 py-2">
                <div className="text-sm text-slate-500">{t('home.ex_borrow')}</div>
                <div className="mt-1 text-2xl font-bold text-slate-900">$100</div>
              </div>
              <div className="px-4 py-2">
                <div className="text-sm text-slate-500">{t('home.ex_receive')}</div>
                <div className="mt-1 text-2xl font-bold text-blue-600">$90</div>
              </div>
              <div className="px-4 py-2">
                <div className="text-sm text-slate-500">{t('home.ex_duration')}</div>
                <div className="mt-1 text-2xl font-bold text-slate-900">7 Days</div>
              </div>
              <div className="px-4 py-2">
                <div className="text-sm text-slate-500">{t('home.ex_repay')}</div>
                <div className="mt-1 text-2xl font-bold text-slate-900">$100</div>
              </div>
            </div>
            <div className="mt-8 rounded-xl bg-yellow-50 p-4 text-sm text-yellow-800 flex items-start gap-3 text-left">
              <Shield className="h-5 w-5 shrink-0" />
              <p>{t('home.ex_risk')}</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 bg-white px-5 text-center">
        <div className="mx-auto max-w-3xl">
          <h2 className="text-4xl font-bold text-slate-900">{t('home.cta_title')}</h2>
          <a
            href="https://t.me/KhmerXBot/app"
            target="_blank"
            rel="noopener noreferrer"
            className="mt-10 inline-flex items-center justify-center rounded-xl bg-[#0A5BFF] px-8 py-4 text-lg font-semibold text-white shadow-lg transition-all hover:bg-blue-700 hover:shadow-xl"
          >
            {t('home.hero_cta')}
          </a>
        </div>
      </section>
    </>
  );
}
