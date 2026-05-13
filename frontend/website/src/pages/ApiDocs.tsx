import { Helmet } from 'react-helmet-async'
import { Link, useParams } from 'react-router-dom'
import { useMemo } from 'react'
import { BookOpen, KeyRound, ListChecks, ShieldCheck } from 'lucide-react'
import type { LucideIcon } from 'lucide-react'
import { track } from '@/utils/analytics'

type DocSection = {
  id: string
  title: string
  icon: LucideIcon
  content: React.ReactNode
}

function CodeBlock(props: { title?: string; code: string; meta?: string }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white shadow-sm overflow-hidden">
      <div className="flex items-center justify-between border-b border-slate-100 px-4 py-3">
        <div className="text-sm font-semibold text-slate-800">{props.title || 'Example'}</div>
        {props.meta ? <div className="text-xs text-slate-500">{props.meta}</div> : null}
      </div>
      <pre className="overflow-auto bg-slate-950 p-4 text-xs text-slate-100">
        <code>{props.code}</code>
      </pre>
    </div>
  )
}

export default function ApiDocs() {
  const { lang } = useParams()

  const sections = useMemo<DocSection[]>(
    () => [
      {
        id: 'overview',
        title: lang === 'zh' ? '概览' : lang === 'km' ? 'សង្ខេប' : 'Overview',
        icon: BookOpen,
        content: (
          <div className="space-y-3 text-sm text-slate-700 leading-relaxed">
            <p>
              {lang === 'zh'
                ? '这里提供 KhmerX 数据接口能力说明与调用示例。接口开通后，你将获得独立的访问凭证与配额。'
                : lang === 'km'
                  ? 'ទីនេះជាឯកសារពន្យល់អំពីសមត្ថភាព API របស់ KhmerX និងឧទាហរណ៍ប្រើប្រាស់។ បន្ទាប់ពីអនុម័ត អ្នកនឹងទទួលបាន credential និង quota។'
                  : 'This page describes KhmerX data APIs and provides examples. Once approved, you will receive credentials and quotas.'}
            </p>
            <div className="flex flex-wrap gap-2">
              <Link
                to={`/${lang}/apply`}
                onClick={() => track('api_doc_apply_click', { source_section: 'overview', lang })}
                className="inline-flex items-center rounded-xl bg-[#0A5BFF] px-5 py-3 text-sm font-semibold text-white shadow-md shadow-blue-500/20 transition-all hover:bg-blue-700"
              >
                {lang === 'zh' ? '在线申请接入' : lang === 'km' ? 'ដាក់ពាក្យចូលប្រើ' : 'Apply for Access'}
              </Link>
              <a
                href="mailto:support@khmerx.org"
                className="inline-flex items-center rounded-xl border border-slate-200 bg-white px-5 py-3 text-sm font-semibold text-slate-700 transition-colors hover:bg-slate-50"
              >
                {lang === 'zh' ? '联系支持' : lang === 'km' ? 'ទំនាក់ទំនង' : 'Contact Support'}
              </a>
            </div>
          </div>
        ),
      },
      {
        id: 'auth',
        title: lang === 'zh' ? '鉴权' : lang === 'km' ? 'ការផ្ទៀងផ្ទាត់' : 'Authentication',
        icon: KeyRound,
        content: (
          <div className="space-y-3 text-sm text-slate-700 leading-relaxed">
            <p>
              {lang === 'zh'
                ? '鉴权方式与签名细节会在开通后提供（含请求头字段、签名算法、错误码）。'
                : lang === 'km'
                  ? 'ព័ត៌មានលម្អិតអំពី authentication និង signature នឹងផ្ដល់ជូនក្រោយពេលអនុម័ត (headers, signature, error codes)។'
                  : 'Authentication and signing details will be provided after approval (headers, signature, error codes).'}
            </p>
            <CodeBlock
              title={lang === 'zh' ? '请求示例' : lang === 'km' ? 'ឧទាហរណ៍ Request' : 'Request Example'}
              meta="curl"
              code={
                "curl -X GET https://api.khmerx.org/api/v1/risk/score\\\n  -H 'X-Api-Key: <your_key>'\\\n  -H 'X-Timestamp: <unix_ms>'\\\n  -H 'X-Signature: <signature>'"
              }
            />
          </div>
        ),
      },
      {
        id: 'endpoints',
        title: lang === 'zh' ? '接口目录' : lang === 'km' ? 'បញ្ជី API' : 'Endpoints',
        icon: ListChecks,
        content: (
          <div className="space-y-4">
            <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
              <div className="text-sm font-semibold text-slate-900">risk_score</div>
              <div className="mt-1 text-xs text-slate-500">GET /api/v1/risk/score</div>
              <div className="mt-3 text-sm text-slate-700">
                {lang === 'zh'
                  ? '返回用户/设备的风控评分与等级建议。'
                  : lang === 'km'
                    ? 'ត្រឡប់ពិន្ទុហានិភ័យ និងការណែនាំកម្រិត។'
                    : 'Returns risk score and recommended risk level.'}
              </div>
            </div>

            <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
              <div className="text-sm font-semibold text-slate-900">kyc</div>
              <div className="mt-1 text-xs text-slate-500">POST /api/v1/kyc/verify</div>
              <div className="mt-3 text-sm text-slate-700">
                {lang === 'zh'
                  ? '提交身份要素并返回校验结果。'
                  : lang === 'km'
                    ? 'ផ្ញើព័ត៌មាន KYC ហើយទទួលលទ្ធផលផ្ទៀងផ្ទាត់។'
                    : 'Submits KYC attributes and returns verification result.'}
              </div>
            </div>
          </div>
        ),
      },
      {
        id: 'limits',
        title: lang === 'zh' ? '限流与稳定性' : lang === 'km' ? 'កម្រិត & ស្ថិរភាព' : 'Rate Limits',
        icon: ShieldCheck,
        content: (
          <div className="space-y-3 text-sm text-slate-700 leading-relaxed">
            <p>
              {lang === 'zh'
                ? '默认限流策略与配额会在开通时确认。建议对 429/5xx 进行指数退避重试。'
                : lang === 'km'
                  ? 'កម្រិតលំនាំដើម និង quota នឹងបញ្ជាក់ពេលអនុម័ត។ សូម retry 429/5xx ដោយ exponential backoff។'
                  : 'Default limits/quotas are confirmed upon approval. Use exponential backoff for 429/5xx.'}
            </p>
          </div>
        ),
      },
    ],
    [lang]
  )

  return (
    <>
      <Helmet>
        <title>{lang === 'zh' ? '数据接口 / API 文档 - KhmerX' : lang === 'km' ? 'API ឯកសារ - KhmerX' : 'API Docs - KhmerX'}</title>
        <meta
          name="description"
          content={
            lang === 'zh'
              ? 'KhmerX 数据接口/API 文档：接入说明、鉴权方式与接口示例。'
              : lang === 'km'
                ? 'ឯកសារ API KhmerX៖ ការចូលប្រើ, authentication និងឧទាហរណ៍។'
                : 'KhmerX API documentation: access, authentication and examples.'
          }
        />
      </Helmet>

      <section className="bg-gradient-to-b from-slate-50 to-white px-5 py-12">
        <div className="mx-auto grid max-w-7xl gap-8 lg:grid-cols-12">
          <div className="lg:col-span-4">
            <div className="sticky top-24 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
              <div className="text-sm font-semibold text-slate-900">{lang === 'zh' ? '目录' : lang === 'km' ? 'មាតិកា' : 'Contents'}</div>
              <div className="mt-3 space-y-1">
                {sections.map((s) => (
                  <a
                    key={s.id}
                    href={`#${s.id}`}
                    onClick={() => track('api_doc_toc_click', { section: s.id, lang })}
                    className="flex items-center gap-2 rounded-lg px-3 py-2 text-sm text-slate-700 transition-colors hover:bg-slate-50"
                  >
                    <s.icon className="h-4 w-4 text-slate-500" />
                    <span>{s.title}</span>
                  </a>
                ))}
              </div>
            </div>
          </div>

          <div className="lg:col-span-8">
            <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
              <div className="text-xs font-semibold text-blue-700">{lang === 'zh' ? '当前版本' : lang === 'km' ? 'កំណែ' : 'Version'}: v1</div>
              <h1 className="mt-2 text-3xl font-bold tracking-tight text-slate-900">{lang === 'zh' ? '数据接口 / API 文档' : lang === 'km' ? 'API ឯកសារ' : 'Data API Docs'}</h1>
              <p className="mt-3 text-slate-600">
                {lang === 'zh'
                  ? '面向开发者与合作方的能力说明与调用示例。'
                  : lang === 'km'
                    ? 'សម្រាប់អ្នកអភិវឌ្ឍន៍ និងដៃគូ។'
                    : 'For developers and partners.'}
              </p>
            </div>

            <div className="mt-6 space-y-6">
              {sections.map((s) => (
                <div key={s.id} id={s.id} className="scroll-mt-28">
                  <div className="flex items-center gap-2">
                    <s.icon className="h-5 w-5 text-blue-600" />
                    <h2 className="text-xl font-bold text-slate-900">{s.title}</h2>
                  </div>
                  <div className="mt-3">{s.content}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>
    </>
  )
}
