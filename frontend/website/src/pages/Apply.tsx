import { Helmet } from 'react-helmet-async'
import { useEffect, useMemo, useState } from 'react'
import { Link, useLocation, useParams } from 'react-router-dom'
import { Building2, CheckCircle2, Mail, Phone, Send, User2 } from 'lucide-react'
import { postJson } from '@/utils/api'
import { track } from '@/utils/analytics'

type ApplicantType = 'company' | 'individual'

type IntegrationRequestBody = {
  applicantType: ApplicantType
  orgName: string
  contactName: string
  email: string
  phone?: string
  telegram?: string
  countryOrRegion?: string
  useCase: string
  interestedApis: string[]
  expectedVolumeRange?: string
  expectedLaunchTime?: string
  notes?: string
  consent: boolean
  source?: string
}

type IntegrationRequestResponse = {
  ok: boolean
  requestId: string
}

const API_OPTIONS = [
  { key: 'risk_score', labelZh: '风控评分', labelEn: 'Risk Score', labelKm: 'ពិន្ទុហានិភ័យ' },
  { key: 'kyc', labelZh: 'KYC 校验', labelEn: 'KYC Verification', labelKm: 'ផ្ទៀងផ្ទាត់ KYC' },
  { key: 'blacklist', labelZh: '黑名单查询', labelEn: 'Blacklist Check', labelKm: 'ពិនិត្យបញ្ជីខ្មៅ' },
  { key: 'device_fingerprint', labelZh: '设备指纹', labelEn: 'Device Fingerprint', labelKm: 'ស្នាមម្រាមឧបករណ៍' },
]

function isEmail(v: string) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)
}

export default function Apply() {
  const { lang } = useParams()
  const location = useLocation()

  const [applicantType, setApplicantType] = useState<ApplicantType>('company')
  const [orgName, setOrgName] = useState('')
  const [contactName, setContactName] = useState('')
  const [email, setEmail] = useState('')
  const [phone, setPhone] = useState('')
  const [telegram, setTelegram] = useState('')
  const [countryOrRegion, setCountryOrRegion] = useState('')
  const [useCase, setUseCase] = useState('')
  const [interestedApis, setInterestedApis] = useState<string[]>([])
  const [expectedVolumeRange, setExpectedVolumeRange] = useState('')
  const [expectedLaunchTime, setExpectedLaunchTime] = useState('')
  const [notes, setNotes] = useState('')
  const [consent, setConsent] = useState(false)

  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [successId, setSuccessId] = useState<string | null>(null)

  useEffect(() => {
    track('integration_apply_start', { lang, path: location.pathname })
  }, [lang, location.pathname])

  const title = useMemo(() => {
    if (lang === 'zh') return '在线申请接入 - KhmerX'
    if (lang === 'km') return 'ដាក់ពាក្យចូលប្រើ - KhmerX'
    return 'Apply for Access - KhmerX'
  }, [lang])

  const fieldLabels = useMemo(() => {
    const z = lang === 'zh'
    const k = lang === 'km'
    return {
      headline: z ? '在线申请接入' : k ? 'ដាក់ពាក្យចូលប្រើ' : 'Apply for Access',
      desc: z
        ? '提交申请后我们会在 1–3 个工作日内联系你，并提供接入资料与测试环境。'
        : k
          ? 'បន្ទាប់ពីដាក់ពាក្យ យើងនឹងទំនាក់ទំនងក្នុង 1–3 ថ្ងៃធ្វើការ និងផ្ដល់ឯកសារ/បរិស្ថានសាកល្បង។'
          : 'After submission, we will contact you within 1–3 business days and provide onboarding materials.',
      applicantType: z ? '申请类型' : k ? 'ប្រភេទអ្នកដាក់ពាក្យ' : 'Applicant Type',
      orgName: z ? '机构/团队名称' : k ? 'ឈ្មោះអង្គការ/ក្រុម' : 'Organization/Team',
      contactName: z ? '联系人姓名' : k ? 'ឈ្មោះអ្នកទំនាក់ទំនង' : 'Contact Name',
      email: z ? '联系邮箱' : k ? 'អ៊ីមែល' : 'Email',
      phone: z ? '联系电话' : k ? 'ទូរស័ព្ទ' : 'Phone',
      telegram: z ? 'Telegram' : k ? 'Telegram' : 'Telegram',
      country: z ? '国家/地区' : k ? 'ប្រទេស/តំបន់' : 'Country/Region',
      useCase: z ? '业务场景描述' : k ? 'ពិពណ៌នាករណីប្រើប្រាស់' : 'Use Case',
      apis: z ? '计划对接接口/数据' : k ? 'API ដែលចង់ប្រើ' : 'Interested APIs',
      volume: z ? '预计调用量' : k ? 'បរិមាណប្រើប្រាស់' : 'Expected Volume',
      launch: z ? '预计上线时间' : k ? 'ពេល上线' : 'Expected Launch',
      notes: z ? '备注' : k ? 'ចំណាំ' : 'Notes',
      consent: z ? '我已阅读并同意隐私政策与服务条款' : k ? 'ខ្ញុំយល់ព្រមលើ Privacy និង Terms' : 'I agree to Privacy Policy and Terms',
      submit: z ? '提交申请' : k ? 'ដាក់ស្នើ' : 'Submit',
      company: z ? '企业/机构' : k ? 'ក្រុមហ៊ុន' : 'Company',
      individual: z ? '个人' : k ? 'បុគ្គល' : 'Individual',
    }
  }, [lang])

  const apiLabels = useMemo(() => {
    return API_OPTIONS.map((o) => ({
      key: o.key,
      label: lang === 'zh' ? o.labelZh : lang === 'km' ? o.labelKm : o.labelEn,
    }))
  }, [lang])

  function validate(): string | null {
    if (!orgName.trim()) return 'orgName'
    if (!contactName.trim()) return 'contactName'
    if (!email.trim() || !isEmail(email.trim())) return 'email'
    if (!phone.trim() && !telegram.trim()) return 'phoneOrTelegram'
    if (!useCase.trim()) return 'useCase'
    if (interestedApis.length === 0) return 'interestedApis'
    if (!consent) return 'consent'
    return null
  }

  async function submit() {
    if (submitting) return
    setError(null)

    const invalid = validate()
    if (invalid) {
      track('integration_apply_validation_error', { field: invalid, lang })
      setError(
        lang === 'zh'
          ? '请完整填写必填项（邮箱格式正确，电话/Telegram 至少填一个，选择至少一个接口，并勾选同意条款）'
          : lang === 'km'
            ? 'សូមបំពេញព័ត៌មានចាំបាច់ (email ត្រឹមត្រូវ, phone/telegram មួយ, ជ្រើស API មួយ, និងយល់ព្រម)'
            : 'Please complete required fields (valid email, phone or telegram, choose at least one API, and consent).'
      )
      return
    }

    setSubmitting(true)
    track('integration_apply_submit', { lang, interestedApis, applicantType })
    try {
      const payload: IntegrationRequestBody = {
        applicantType,
        orgName: orgName.trim(),
        contactName: contactName.trim(),
        email: email.trim(),
        phone: phone.trim() || undefined,
        telegram: telegram.trim() || undefined,
        countryOrRegion: countryOrRegion.trim() || undefined,
        useCase: useCase.trim(),
        interestedApis,
        expectedVolumeRange: expectedVolumeRange.trim() || undefined,
        expectedLaunchTime: expectedLaunchTime.trim() || undefined,
        notes: notes.trim() || undefined,
        consent,
        source: `${location.pathname}${location.hash || ''}`,
      }
      const resp = await postJson<IntegrationRequestResponse>('/api/integration-requests', payload)
      if (!resp.ok) {
        throw new Error('submit_failed')
      }
      setSuccessId(resp.requestId)
      track('integration_apply_success', { lang, request_id: resp.requestId })
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : 'submit_failed'
      setError(lang === 'zh' ? '提交失败，请稍后重试或联系 support@khmerx.org' : lang === 'km' ? 'បញ្ជូនបរាជ័យ សូមសាកល្បងម្ដងទៀត' : 'Submit failed. Please retry or email support@khmerx.org')
      track('integration_apply_fail', { lang, error_code: msg })
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <>
      <Helmet>
        <title>{title}</title>
      </Helmet>

      <section className="bg-gradient-to-b from-blue-50 to-white px-5 py-12">
        <div className="mx-auto max-w-3xl">
          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="text-xs font-semibold text-blue-700">KhmerX</div>
            <h1 className="mt-2 text-3xl font-bold tracking-tight text-slate-900">{fieldLabels.headline}</h1>
            <p className="mt-3 text-slate-600">{fieldLabels.desc}</p>

            {successId ? (
              <div className="mt-6 rounded-2xl border border-emerald-200 bg-emerald-50 p-5">
                <div className="flex items-center gap-2 text-emerald-800">
                  <CheckCircle2 className="h-5 w-5" />
                  <div className="font-semibold">{lang === 'zh' ? '已收到申请' : lang === 'km' ? 'បានទទួលសំណើ' : 'Request Received'}</div>
                </div>
                <div className="mt-2 text-sm text-emerald-800">
                  {lang === 'zh'
                    ? '我们会在 1–3 个工作日内联系你。'
                    : lang === 'km'
                      ? 'យើងនឹងទំនាក់ទំនងក្នុង 1–3 ថ្ងៃធ្វើការ។'
                      : 'We will contact you within 1–3 business days.'}
                </div>
                <div className="mt-2 text-xs text-emerald-900/80">requestId: <span className="font-mono">{successId}</span></div>
                <div className="mt-4 flex flex-wrap gap-2">
                  <Link
                    to={`/${lang}/api`}
                    className="inline-flex items-center rounded-xl bg-emerald-700 px-5 py-3 text-sm font-semibold text-white transition-colors hover:bg-emerald-800"
                  >
                    {lang === 'zh' ? '返回 API 文档' : lang === 'km' ? 'ត្រឡប់ទៅ API' : 'Back to API Docs'}
                  </Link>
                  <a
                    href="mailto:support@khmerx.org"
                    className="inline-flex items-center rounded-xl border border-emerald-200 bg-white px-5 py-3 text-sm font-semibold text-emerald-800 transition-colors hover:bg-emerald-50"
                  >
                    {lang === 'zh' ? '邮件联系' : lang === 'km' ? 'អ៊ីមែល' : 'Email'}
                  </a>
                </div>
              </div>
            ) : null}

            {successId ? null : (
              <div className="mt-6 grid gap-4">
                <div className="grid gap-4 sm:grid-cols-2">
                  <div>
                    <div className="text-sm font-semibold text-slate-800">{fieldLabels.applicantType}</div>
                    <div className="mt-2 flex gap-2">
                      <button
                        type="button"
                        onClick={() => setApplicantType('company')}
                        className={`flex-1 rounded-xl border px-4 py-3 text-sm font-semibold transition-colors ${
                          applicantType === 'company' ? 'border-blue-200 bg-blue-50 text-blue-700' : 'border-slate-200 bg-white text-slate-700 hover:bg-slate-50'
                        }`}
                      >
                        {fieldLabels.company}
                      </button>
                      <button
                        type="button"
                        onClick={() => setApplicantType('individual')}
                        className={`flex-1 rounded-xl border px-4 py-3 text-sm font-semibold transition-colors ${
                          applicantType === 'individual' ? 'border-blue-200 bg-blue-50 text-blue-700' : 'border-slate-200 bg-white text-slate-700 hover:bg-slate-50'
                        }`}
                      >
                        {fieldLabels.individual}
                      </button>
                    </div>
                  </div>

                  <div>
                    <div className="text-sm font-semibold text-slate-800">{fieldLabels.country}</div>
                    <input
                      value={countryOrRegion}
                      onChange={(e) => setCountryOrRegion(e.target.value)}
                      className="mt-2 h-11 w-full rounded-xl border border-slate-200 bg-white px-4 text-sm outline-none transition focus:border-blue-300"
                      placeholder={lang === 'zh' ? '可选' : lang === 'km' ? 'ជាជម្រើស' : 'Optional'}
                    />
                  </div>
                </div>

                <div className="grid gap-4 sm:grid-cols-2">
                  <div>
                    <div className="flex items-center gap-2 text-sm font-semibold text-slate-800"><Building2 className="h-4 w-4" />{fieldLabels.orgName}</div>
                    <input
                      value={orgName}
                      onChange={(e) => setOrgName(e.target.value)}
                      className="mt-2 h-11 w-full rounded-xl border border-slate-200 bg-white px-4 text-sm outline-none transition focus:border-blue-300"
                    />
                  </div>
                  <div>
                    <div className="flex items-center gap-2 text-sm font-semibold text-slate-800"><User2 className="h-4 w-4" />{fieldLabels.contactName}</div>
                    <input
                      value={contactName}
                      onChange={(e) => setContactName(e.target.value)}
                      className="mt-2 h-11 w-full rounded-xl border border-slate-200 bg-white px-4 text-sm outline-none transition focus:border-blue-300"
                    />
                  </div>
                </div>

                <div className="grid gap-4 sm:grid-cols-2">
                  <div>
                    <div className="flex items-center gap-2 text-sm font-semibold text-slate-800"><Mail className="h-4 w-4" />{fieldLabels.email}</div>
                    <input
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      className="mt-2 h-11 w-full rounded-xl border border-slate-200 bg-white px-4 text-sm outline-none transition focus:border-blue-300"
                      placeholder="name@example.com"
                    />
                  </div>
                  <div>
                    <div className="flex items-center gap-2 text-sm font-semibold text-slate-800"><Phone className="h-4 w-4" />{fieldLabels.phone} / {fieldLabels.telegram}</div>
                    <div className="mt-2 grid gap-2 sm:grid-cols-2">
                      <input
                        value={phone}
                        onChange={(e) => setPhone(e.target.value)}
                        className="h-11 w-full rounded-xl border border-slate-200 bg-white px-4 text-sm outline-none transition focus:border-blue-300"
                        placeholder={fieldLabels.phone}
                      />
                      <input
                        value={telegram}
                        onChange={(e) => setTelegram(e.target.value)}
                        className="h-11 w-full rounded-xl border border-slate-200 bg-white px-4 text-sm outline-none transition focus:border-blue-300"
                        placeholder={fieldLabels.telegram}
                      />
                    </div>
                    <div className="mt-1 text-xs text-slate-500">
                      {lang === 'zh' ? '电话与 Telegram 至少填写一个' : lang === 'km' ? 'ត្រូវមាន phone ឬ telegram មួយ' : 'Provide phone or telegram'}
                    </div>
                  </div>
                </div>

                <div>
                  <div className="text-sm font-semibold text-slate-800">{fieldLabels.useCase}</div>
                  <textarea
                    value={useCase}
                    onChange={(e) => setUseCase(e.target.value)}
                    className="mt-2 min-h-[120px] w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm outline-none transition focus:border-blue-300"
                    placeholder={lang === 'zh' ? '描述你的业务场景、对接目的、关键字段等' : lang === 'km' ? 'ពិពណ៌នាករណីប្រើប្រាស់ និងគោលបំណង' : 'Describe your use case and requirements'}
                  />
                </div>

                <div>
                  <div className="text-sm font-semibold text-slate-800">{fieldLabels.apis}</div>
                  <div className="mt-2 grid gap-2 sm:grid-cols-2">
                    {apiLabels.map((o) => (
                      <label key={o.key} className="flex cursor-pointer items-center gap-3 rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm transition-colors hover:bg-slate-50">
                        <input
                          type="checkbox"
                          checked={interestedApis.includes(o.key)}
                          onChange={(e) => {
                            setInterestedApis((prev) => {
                              if (e.target.checked) return [...prev, o.key]
                              return prev.filter((k) => k !== o.key)
                            })
                          }}
                        />
                        <span className="font-medium text-slate-800">{o.label}</span>
                        <span className="ml-auto text-xs text-slate-500">{o.key}</span>
                      </label>
                    ))}
                  </div>
                </div>

                <div className="grid gap-4 sm:grid-cols-2">
                  <div>
                    <div className="text-sm font-semibold text-slate-800">{fieldLabels.volume}</div>
                    <select
                      value={expectedVolumeRange}
                      onChange={(e) => setExpectedVolumeRange(e.target.value)}
                      className="mt-2 h-11 w-full rounded-xl border border-slate-200 bg-white px-4 text-sm outline-none transition focus:border-blue-300"
                    >
                      <option value="">{lang === 'zh' ? '可选' : lang === 'km' ? 'ជាជម្រើស' : 'Optional'}</option>
                      <option value="0-10k/月">0-10k/月</option>
                      <option value="10k-100k/月">10k-100k/月</option>
                      <option value="100k-1M/月">100k-1M/月</option>
                      <option value=">1M/月">&gt;1M/月</option>
                    </select>
                  </div>
                  <div>
                    <div className="text-sm font-semibold text-slate-800">{fieldLabels.launch}</div>
                    <input
                      value={expectedLaunchTime}
                      onChange={(e) => setExpectedLaunchTime(e.target.value)}
                      className="mt-2 h-11 w-full rounded-xl border border-slate-200 bg-white px-4 text-sm outline-none transition focus:border-blue-300"
                      placeholder={lang === 'zh' ? '例如 2026-Q2' : lang === 'km' ? 'ឧ. 2026-Q2' : 'e.g. 2026-Q2'}
                    />
                  </div>
                </div>

                <div>
                  <div className="text-sm font-semibold text-slate-800">{fieldLabels.notes}</div>
                  <textarea
                    value={notes}
                    onChange={(e) => setNotes(e.target.value)}
                    className="mt-2 min-h-[84px] w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm outline-none transition focus:border-blue-300"
                    placeholder={lang === 'zh' ? '可选' : lang === 'km' ? 'ជាជម្រើស' : 'Optional'}
                  />
                </div>

                <label className="flex cursor-pointer items-start gap-3 rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm">
                  <input type="checkbox" checked={consent} onChange={(e) => setConsent(e.target.checked)} className="mt-1" />
                  <span className="text-slate-700">
                    {fieldLabels.consent}{' '}
                    <Link to={`/${lang}/privacy`} className="text-blue-700 hover:text-blue-800">{lang === 'zh' ? '隐私' : lang === 'km' ? 'Privacy' : 'Privacy'}</Link>
                    {' / '}
                    <Link to={`/${lang}/terms`} className="text-blue-700 hover:text-blue-800">{lang === 'zh' ? '条款' : lang === 'km' ? 'Terms' : 'Terms'}</Link>
                  </span>
                </label>

                {error ? <div className="rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">{error}</div> : null}

                <button
                  type="button"
                  onClick={submit}
                  disabled={submitting}
                  className="inline-flex h-12 items-center justify-center gap-2 rounded-2xl bg-[#0A5BFF] px-6 text-sm font-semibold text-white shadow-md shadow-blue-500/20 transition-all hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  <Send className="h-4 w-4" />
                  {submitting ? (lang === 'zh' ? '提交中…' : lang === 'km' ? 'កំពុងដាក់ស្នើ…' : 'Submitting…') : fieldLabels.submit}
                </button>
              </div>
            )}
          </div>
        </div>
      </section>
    </>
  )
}
