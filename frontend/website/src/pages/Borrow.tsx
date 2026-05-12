import { useTranslation } from 'react-i18next';
import { Helmet } from 'react-helmet-async';
import { motion } from 'framer-motion';
import { Send, User, DollarSign, CheckCircle2, RefreshCw, ShieldAlert } from 'lucide-react'; 
import { useParams } from 'react-router-dom';

export default function Borrow() {
  const { t } = useTranslation();
  const { lang } = useParams();

  const steps = [
    { icon: <Send className="w-8 h-8"/>, title: 'borrow.step1_title', desc: 'borrow.step1_desc' },
    { icon: <User className="w-8 h-8"/>, title: 'borrow.step2_title', desc: 'borrow.step2_desc' },
    { icon: <DollarSign className="w-8 h-8"/>, title: 'borrow.step3_title', desc: 'borrow.step3_desc' },
    { icon: <CheckCircle2 className="w-8 h-8"/>, title: 'borrow.step4_title', desc: 'borrow.step4_desc' },
    { icon: <RefreshCw className="w-8 h-8"/>, title: 'borrow.step5_title', desc: 'borrow.step5_desc' },
  ];

  const faqSchema = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      { "@type": "Question", "name": t('borrow.faq1_q'), "acceptedAnswer": { "@type": "Answer", "text": t('borrow.faq1_a') } },
      { "@type": "Question", "name": t('borrow.faq2_q'), "acceptedAnswer": { "@type": "Answer", "text": t('borrow.faq2_a') } },
      { "@type": "Question", "name": t('borrow.faq3_q'), "acceptedAnswer": { "@type": "Answer", "text": t('borrow.faq3_a') } },
      { "@type": "Question", "name": t('borrow.faq4_q'), "acceptedAnswer": { "@type": "Answer", "text": t('borrow.faq4_a') } },
      { "@type": "Question", "name": t('borrow.faq5_q'), "acceptedAnswer": { "@type": "Answer", "text": t('borrow.faq5_a') } }
    ]
  };

  return (
    <>
      <Helmet>
        <title>{t('borrow.title')}</title>
        <meta name="description" content={t('borrow.desc')} />
        <meta name="keywords" content={t('borrow.keywords')} />
        <script type="application/ld+json">{JSON.stringify(faqSchema)}</script>
      </Helmet>

      {/* Hero Section */}
      <section className="bg-slate-900 px-5 py-24 text-center text-white relative overflow-hidden">
        <div className="absolute inset-0 bg-[url('https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=Telegram%20Mini%20App%20loan%20dashboard%20blue%20tones%20finance&image_size=landscape_16_9')] bg-cover bg-center opacity-20"></div>
        <div className="relative z-10 mx-auto max-w-3xl">
          <h1 className="text-4xl font-extrabold sm:text-5xl">{t('borrow.hero_title')}</h1>
          <p className="mt-6 text-lg text-slate-300">{t('borrow.hero_subtitle')}</p>
          <div className="mt-10 flex flex-wrap justify-center gap-4">
            <a href="https://t.me/KhmerXBot/app" className="rounded-xl bg-blue-600 px-8 py-4 font-bold text-white hover:bg-blue-500 transition-colors">
              {t('borrow.cta_open')}
            </a>
            <a href={`/${lang}/fees`} className="rounded-xl bg-white/10 px-8 py-4 font-bold text-white hover:bg-white/20 transition-colors border border-white/20">
              {t('borrow.cta_fees')}
            </a>
          </div>
        </div>
      </section>

      {/* Steps */}
      <section className="bg-slate-50 px-5 py-20">
        <div className="mx-auto max-w-5xl">
          <h2 className="mb-12 text-center text-3xl font-bold text-slate-900">{t('borrow.steps_title')}</h2>
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {steps.map((step, idx) => (
              <motion.div whileHover={{ y: -5 }} key={idx} className="rounded-2xl bg-white p-8 shadow-sm border border-slate-100">
                <div className="mb-6 inline-flex rounded-2xl bg-blue-50 p-4 text-blue-600">
                  {step.icon}
                </div>
                <h3 className="text-xl font-bold text-slate-900">{t(step.title)}</h3>
                <p className="mt-2 text-slate-600">{t(step.desc)}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Conditions */}
      <section className="bg-white px-5 py-20">
        <div className="mx-auto max-w-5xl">
          <div className="grid md:grid-cols-2 gap-10 items-center">
            <div>
              <h2 className="text-3xl font-bold text-slate-900 mb-6">{t('borrow.cond_title')}</h2>
              <div className="space-y-4">
                <div className="bg-slate-50 p-6 rounded-2xl border border-slate-100">
                  <h4 className="font-bold text-slate-900 mb-2">{t('borrow.cond_new_title')}</h4>
                  <ul className="list-disc list-inside text-slate-600">
                    <li>{t('borrow.cond_new_l1')}</li>
                    <li>{t('borrow.cond_new_l2')}</li>
                  </ul>
                </div>
                <div className="bg-slate-50 p-6 rounded-2xl border border-slate-100">
                  <h4 className="font-bold text-slate-900 mb-2">{t('borrow.cond_reg_title')}</h4>
                  <p className="text-slate-600">{t('borrow.cond_reg_desc')}</p>
                </div>
              </div>
            </div>
            <div className="bg-yellow-50 rounded-3xl p-8 border border-yellow-200">
              <ShieldAlert className="w-12 h-12 text-yellow-600 mb-4" />
              <h3 className="text-xl font-bold text-yellow-900 mb-2">{t('borrow.risk_title')}</h3>
              <p className="text-yellow-800">{t('borrow.risk_desc')}</p>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}
