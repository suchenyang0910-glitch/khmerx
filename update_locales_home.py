import json
import os

locales = {
    "zh": {},
    "en": {},
    "km": {}
}

# --- HOME ---
locales["zh"]["home"] = {
    "seo_title": "KhmerX | ABA 小额周转服务",
    "seo_desc": "通过 Telegram Mini App，快速发布小额短期借款需求。ABA 转账，费用透明。",
    "seo_keywords": "KhmerX, ABA 小额周转, Telegram 借款, 柬埔寨借款",
    "hero_badge": "ABA · Telegram · Cambodia",
    "hero_title": "ABA 小额周转服务",
    "hero_subtitle": "通过 Telegram Mini App，<br/>快速发布小额短期借款需求。",
    "hero_cta": "打开 Telegram Mini App",
    "hero_secondary": "查看借款流程",
    "feat_title": "简单、可信、透明",
    "feat1_title": "ABA 转账", "feat1_desc": "通过 ABA 完成交易",
    "feat2_title": "Telegram 操作", "feat2_desc": "无需下载新 App",
    "feat3_title": "小额短期", "feat3_desc": "灵活满足周转需求",
    "feat4_title": "信用记录", "feat4_desc": "按时还款提升额度",
    "feat5_title": "透明费用", "feat5_desc": "提前知晓到账与还款",
    "ex_title": "透明的借款示例",
    "ex_borrow": "借款", "ex_receive": "到账", "ex_duration": "期限", "ex_repay": "到期还",
    "ex_risk": "请确认实际到账金额与到期还款金额。",
    "steps_title": "借款流程",
    "step1": "打开 Telegram", "step2": "绑定 ABA", "step3": "发布借款", "step4": "上传凭证", "step5": "完成还款",
    "trust_title": "可信赖的本地服务",
    "trust_desc": "KhmerX 不保证借款成功，请用户自行确认交易风险。",
    "faq_title": "常见问题",
    "faq1_q": "KhmerX 是什么？", "faq1_a": "KhmerX 是面向柬埔寨用户的小额周转信息服务平台。",
    "faq2_q": "是否支持 ABA？", "faq2_a": "是的，所有交易均通过 ABA 转账完成。",
    "faq3_q": "如何还款？", "faq3_a": "通过 ABA 转账后，在 Mini App 上传凭证即可。",
    "faq4_q": "逾期会怎样？", "faq4_a": "逾期可能导致额度降低或限制借款。",
    "cta_title": "立即打开 Telegram Mini App"
}

locales["en"]["home"] = {
    "seo_title": "KhmerX | ABA Micro Lending Information Service",
    "seo_desc": "Quickly publish small short-term borrowing requests via Telegram Mini App. ABA transfers, transparent fees.",
    "seo_keywords": "KhmerX, ABA micro lending, Telegram loan, Cambodia loan",
    "hero_badge": "ABA · Telegram · Cambodia",
    "hero_title": "ABA Micro Lending Information Service",
    "hero_subtitle": "Quickly publish small short-term borrowing requests via Telegram Mini App.",
    "hero_cta": "Open Telegram Mini App",
    "hero_secondary": "View Borrowing Process",
    "feat_title": "Simple, Trusted, Transparent",
    "feat1_title": "ABA Transfer", "feat1_desc": "Transactions via ABA",
    "feat2_title": "Telegram App", "feat2_desc": "No new app to download",
    "feat3_title": "Short-Term", "feat3_desc": "Flexible micro loans",
    "feat4_title": "Credit Record", "feat4_desc": "Repay on time to increase limit",
    "feat5_title": "Transparent Fees", "feat5_desc": "Know costs upfront",
    "ex_title": "Transparent Borrowing Example",
    "ex_borrow": "Borrow", "ex_receive": "Receive", "ex_duration": "Duration", "ex_repay": "Repay",
    "ex_risk": "Please confirm the actual received amount and repayment amount.",
    "steps_title": "Borrowing Process",
    "step1": "Open Telegram", "step2": "Bind ABA", "step3": "Post Request", "step4": "Upload Receipt", "step5": "Complete Repayment",
    "trust_title": "Trusted Local Service",
    "trust_desc": "KhmerX does not guarantee successful loans. Users must confirm transaction risks themselves.",
    "faq_title": "FAQ",
    "faq1_q": "What is KhmerX?", "faq1_a": "KhmerX is a micro-lending information matching platform for Cambodia.",
    "faq2_q": "Is ABA supported?", "faq2_a": "Yes, all transactions are completed via ABA transfer.",
    "faq3_q": "How to repay?", "faq3_a": "Transfer via ABA and upload the receipt in the Mini App.",
    "faq4_q": "What if overdue?", "faq4_a": "Overdue may lead to reduced limits or borrowing restrictions.",
    "cta_title": "Open Telegram Mini App Now"
}

locales["km"]["home"] = {
    "seo_title": "KhmerX | សេវាខ្ចីប្រាក់តូចតាម ABA",
    "seo_desc": "ស្នើសុំប្រាក់កម្ចីខ្នាតតូចរយៈពេលខ្លីយ៉ាងរហ័សតាមរយៈ Telegram Mini App។",
    "seo_keywords": "KhmerX, ABA loan, Telegram loan, Cambodia loan",
    "hero_badge": "ABA · Telegram · Cambodia",
    "hero_title": "សេវាខ្ចីប្រាក់តូចតាម ABA",
    "hero_subtitle": "ស្នើសុំប្រាក់កម្ចីខ្នាតតូចរយៈពេលខ្លីយ៉ាងរហ័សតាមរយៈ Telegram Mini App។",
    "hero_cta": "បើក Telegram Mini App",
    "hero_secondary": "មើលដំណើរការខ្ចីប្រាក់",
    "feat_title": "ងាយស្រួល គួរឱ្យទុកចិត្ត តម្លាភាព",
    "feat1_title": "ផ្ទេរប្រាក់ ABA", "feat1_desc": "ប្រតិបត្តិការតាម ABA",
    "feat2_title": "កម្មវិធី Telegram", "feat2_desc": "មិនចាំបាច់ទាញយកកម្មវិធីថ្មី",
    "feat3_title": "រយៈពេលខ្លី", "feat3_desc": "កម្ចីខ្នាតតូច",
    "feat4_title": "កំណត់ត្រាឥណទាន", "feat4_desc": "សងទាន់ពេលដើម្បីបង្កើនទំហំទឹកប្រាក់",
    "feat5_title": "ថ្លៃសេវាតម្លាភាព", "feat5_desc": "ដឹងពីការចំណាយជាមុន",
    "ex_title": "ឧទាហរណ៍នៃការខ្ចីប្រាក់ប្រកបដោយតម្លាភាព",
    "ex_borrow": "ខ្ចីប្រាក់", "ex_receive": "ទទួលបាន", "ex_duration": "រយៈពេល", "ex_repay": "សងវិញ",
    "ex_risk": "សូមបញ្ជាក់ចំនួនប្រាក់ដែលទទួលបានជាក់ស្តែង និងចំនួនប្រាក់ដែលត្រូវសង។",
    "steps_title": "ដំណើរការខ្ចីប្រាក់",
    "step1": "បើក Telegram", "step2": "ភ្ជាប់ ABA", "step3": "បង្ហោះសំណើ", "step4": "បញ្ចូលវិក័យប័ត្រ", "step5": "បញ្ចប់ការសងប្រាក់",
    "trust_title": "សេវាកម្មក្នុងស្រុកដែលគួរឱ្យទុកចិត្ត",
    "trust_desc": "KhmerX មិនធានាថាការខ្ចីប្រាក់នឹងទទួលបានជោគជ័យឡើយ។ អ្នកប្រើប្រាស់ត្រូវទទួលខុសត្រូវលើហានិភ័យដោយខ្លួនឯង។",
    "faq_title": "សំណួរដែលសួរញឹកញាប់",
    "faq1_q": "តើ KhmerX ជាអ្វី?", "faq1_a": "KhmerX គឺជាវេទិកាព័ត៌មានផ្គូផ្គងប្រាក់កម្ចីខ្នាតតូចសម្រាប់កម្ពុជា។",
    "faq2_q": "តើគាំទ្រ ABA ទេ?", "faq2_a": "បាទ រាល់ប្រតិបត្តិការទាំងអស់ត្រូវបានបញ្ចប់តាមរយៈការផ្ទេរប្រាក់ ABA។",
    "faq3_q": "របៀបសងប្រាក់?", "faq3_a": "ផ្ទេរប្រាក់តាម ABA ហើយបញ្ចូលវិក័យប័ត្រក្នុង Mini App។",
    "faq4_q": "ចុះបើហួសកាលកំណត់?", "faq4_a": "ការហួសកាលកំណត់អាចនាំឱ្យមានការកាត់បន្ថយទំហំទឹកប្រាក់ឬការរឹតត្បិត។",
    "cta_title": "បើក Telegram Mini App ឥឡូវនេះ"
}

# Write back to locales directory
for lang in ["zh", "en", "km"]:
    # read existing json, merge, write back
    filepath = f"frontend/website/src/locales/{lang}.json"
    data = {}
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except:
                pass
    
    # Merge new structures
    for key, val in locales[lang].items():
        data[key] = val
        
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print("Updated locales successfully.")