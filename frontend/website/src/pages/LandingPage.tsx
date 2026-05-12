import { useTranslation } from 'react-i18next';
import { Helmet } from 'react-helmet-async';
import { ChevronRight } from 'lucide-react';
import { Link, useParams } from 'react-router-dom';

export default function LandingPage({ slug }: { slug: string }) {
  const { t } = useTranslation();
  const { lang } = useParams();

  // Convert slug (e.g. phnom-penh) to i18n key (e.g. phnom_penh)
  const i18nKey = `landing_${slug.replace(/-/g, '_')}`;

  const faqList = [
    { q: t(`${i18nKey}.faq1_q`), a: t(`${i18nKey}.faq1_a`) },
    { q: t(`${i18nKey}.faq2_q`), a: t(`${i18nKey}.faq2_a`) },
    { q: t(`${i18nKey}.faq3_q`), a: t(`${i18nKey}.faq3_a`) }
  ].filter(f => f.q && f.a && f.q !== `${i18nKey}.faq1_q`); // Filter out missing translations

  return (
    <>
      <Helmet>
        <title>{t(`${i18nKey}.title`)}</title>
        <meta name="description" content={t(`${i18nKey}.desc`)} />
        <meta name="keywords" content={t(`${i18nKey}.keywords`)} />
        <link rel="canonical" href={`https://khmerx.org/${lang}/${slug}`} />
        <script type="application/ld+json">{`{
          "@context": "https://schema.org",
          "@type": "FAQPage",
          "mainEntity": [
            ${faqList.map(faq => `{
              "@type": "Question",
              "name": "${faq.q}",
              "acceptedAnswer": {
                "@type": "Answer",
                "text": "${faq.a}"
              }
            }`).join(',')}
          ]
        }`}</script>
        <script type="application/ld+json">{`{
          "@context": "https://schema.org",
          "@type": "Organization",
          "name": "KhmerX",
          "url": "https://khmerx.org",
          "logo": "https://khmerx.org/logo.jpg",
          "sameAs": [
            "https://t.me/KhmerXBot"
          ],
          "contactPoint": {
            "@type": "ContactPoint",
            "contactType": "customer support",
            "email": "support@khmerx.org"
          }
        }`}</script>
      </Helmet>

      <section className="bg-gradient-to-b from-blue-50 to-white px-5 pt-20 pb-24">
        <div className="mx-auto max-w-4xl text-center">
          <div className="mb-6 flex items-center justify-center gap-2 text-sm font-medium text-slate-500">
            <Link to={`/${lang}`} className="hover:text-blue-600 transition-colors">Home</Link>
            <ChevronRight className="h-4 w-4" />
            <span className="text-blue-600">{t(`${i18nKey}.badge`)}</span>
          </div>
          <h1 className="text-4xl font-bold text-slate-900 md:text-5xl leading-tight">{t(`${i18nKey}.hero_title`)}</h1>
          <p className="mt-6 text-xl text-slate-600">{t(`${i18nKey}.hero_subtitle`)}</p>
        </div>
      </section>

      <section className="bg-white px-5 py-16">
        <div className="mx-auto max-w-3xl">
          {t(`${i18nKey}.hero_img`) && t(`${i18nKey}.hero_img`) !== `${i18nKey}.hero_img` && (
             <img src={t(`${i18nKey}.hero_img`)} alt={t(`${i18nKey}.hero_title`)} className="w-full rounded-3xl shadow-2xl mb-12" />
          )}

          <div 
            className="prose prose-lg prose-slate max-w-none mb-16"
            dangerouslySetInnerHTML={{ __html: t(`${i18nKey}.content_html`) }}
          />

          {faqList.length > 0 && (
            <div className="mt-16">
              <h2 className="text-3xl font-bold text-slate-900 mb-8">FAQ</h2>
              <div className="space-y-4">
                {faqList.map((faq, idx) => (
                  <div key={idx} className="bg-slate-50 rounded-2xl p-6 border border-slate-100">
                    <h3 className="text-xl font-bold text-slate-900 mb-3">{faq.q}</h3>
                    <p className="text-slate-600">{faq.a}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="not-prose mt-16 rounded-3xl bg-slate-50 p-8 text-center border border-slate-100">
            <h3 className="text-2xl font-bold text-slate-900">Try it out today</h3>
            <a href="https://t.me/KhmerXBot/app" target="_blank" rel="noopener noreferrer" className="mt-6 inline-block rounded-xl bg-blue-600 px-8 py-4 font-bold text-white hover:bg-blue-700 transition-colors">
              Open Telegram Mini App
            </a>
          </div>
        </div>
      </section>
    </>
  );
}
