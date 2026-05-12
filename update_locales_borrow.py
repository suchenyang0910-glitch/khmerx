import json
import os

locales = {
    "zh": {},
    "en": {},
    "km": {}
}

# --- BORROW ---
locales["zh"]["borrow"] = {
    "title": "如何通过 KhmerX 借款 | ABA 小额周转",
    "desc": "了解如何通过 Telegram Mini App 在 KhmerX 快速发布借款需求，全流程支持 ABA 转账。",
    "keywords": "ABA 借款, Cambodia loan, Telegram loan, 小额周转, Phnom Penh loan",
    "hero_title": "如何通过 KhmerX 借款",
    "hero_subtitle": "通过 Telegram Mini App，快速发布小额短期借款需求。",
    "cta_open": "打开 Mini App",
    "cta_fees": "查看费用说明",
    "steps_title": "借款流程",
    "step1_title": "打开 Telegram Mini App", "step1_desc": "通过 Telegram 进入 KhmerX。",
    "step2_title": "绑定 ABA 信息", "step2_desc": "填写 ABA 账号与姓名。",
    "step3_title": "选择金额与期限", "step3_desc": "选择借款金额和借款天数。",
    "step4_title": "确认费用与到账金额", "step4_desc": "系统会显示实际到账金额。",
    "step5_title": "完成 ABA 转账与还款", "step5_desc": "通过 ABA 转账完成还款。",
    "cond_title": "借款条件",
    "cond_new_title": "新用户", "cond_new_l1": "最高 $50", "cond_new_l2": "7天期限",
    "cond_reg_title": "普通用户", "cond_reg_desc": "按时还款后可提高额度。系统会根据信用记录动态调整额度。",
    "risk_title": "风险提示",
    "risk_desc": "请确认实际到账金额与到期还款金额。KhmerX 不保证借款成功，请用户自行确认风险。",
    "faq1_q": "如何开始借款？", "faq1_a": "打开 Telegram Mini App，绑定 ABA 信息后即可申请借款。",
    "faq2_q": "是否支持 ABA？", "faq2_a": "是的，所有交易均通过 ABA 转账完成。",
    "faq3_q": "多久可以到账？", "faq3_a": "匹配成功后，出借人会通过 ABA 实时转账给您。",
    "faq4_q": "逾期会怎样？", "faq4_a": "逾期可能导致额度降低或限制借款。",
    "faq5_q": "如何提高额度？", "faq5_a": "按时还款、保持良好信用记录，系统会动态提升额度。"
}

locales["en"]["borrow"] = {
    "title": "How to Borrow with KhmerX | ABA Micro Lending",
    "desc": "Learn how to quickly post loan requests via Telegram Mini App on KhmerX, supporting ABA transfers.",
    "keywords": "ABA loan, Cambodia loan, Telegram loan, Micro lending, Phnom Penh loan",
    "hero_title": "How to Borrow with KhmerX",
    "hero_subtitle": "Quickly publish small short-term borrowing requests via Telegram Mini App.",
    "cta_open": "Open Mini App",
    "cta_fees": "View Fees",
    "steps_title": "Borrowing Process",
    "step1_title": "Open Telegram Mini App", "step1_desc": "Enter KhmerX via Telegram.",
    "step2_title": "Bind ABA Info", "step2_desc": "Fill in ABA account and name.",
    "step3_title": "Select Amount & Term", "step3_desc": "Choose loan amount and duration.",
    "step4_title": "Confirm Fees", "step4_desc": "System shows actual received amount.",
    "step5_title": "Repay via ABA", "step5_desc": "Complete ABA transfer and upload proof.",
    "cond_title": "Borrowing Conditions",
    "cond_new_title": "New Users", "cond_new_l1": "Up to $50", "cond_new_l2": "7 days term",
    "cond_reg_title": "Regular Users", "cond_reg_desc": "Limit increases after on-time repayment. The system dynamically adjusts limits based on credit.",
    "risk_title": "Risk Warning",
    "risk_desc": "Please confirm the actual received amount and repayment amount. KhmerX does not guarantee successful loans.",
    "faq1_q": "How to start borrowing?", "faq1_a": "Open the Telegram Mini App, bind your ABA info, and apply.",
    "faq2_q": "Is ABA supported?", "faq2_a": "Yes, all transactions are completed via ABA transfer.",
    "faq3_q": "How fast is the transfer?", "faq3_a": "Once matched, the lender transfers directly to your ABA account.",
    "faq4_q": "What if overdue?", "faq4_a": "Overdue may lead to reduced limits or borrowing restrictions.",
    "faq5_q": "How to increase limit?", "faq5_a": "Repay on time to build a good credit record."
}

locales["km"]["borrow"] = {
    "title": "របៀបខ្ចីប្រាក់តាម KhmerX | ABA Micro Lending",
    "desc": "ស្វែងយល់ពីរបៀបខ្ចីប្រាក់យ៉ាងរហ័សតាមរយៈ Telegram Mini App នៅលើ KhmerX ។",
    "keywords": "ABA loan, Cambodia loan, Telegram loan, Micro lending",
    "hero_title": "របៀបខ្ចីប្រាក់តាម KhmerX",
    "hero_subtitle": "ស្នើសុំប្រាក់កម្ចីខ្នាតតូចរយៈពេលខ្លីយ៉ាងរហ័សតាមរយៈ Telegram Mini App។",
    "cta_open": "បើក Mini App",
    "cta_fees": "មើលការប្រាក់",
    "steps_title": "ដំណើរការខ្ចីប្រាក់",
    "step1_title": "បើក Telegram Mini App", "step1_desc": "ចូល KhmerX តាមរយៈ Telegram ។",
    "step2_title": "ភ្ជាប់ព័ត៌មាន ABA", "step2_desc": "បំពេញគណនី ABA និងឈ្មោះ ។",
    "step3_title": "ជ្រើសរើសចំនួនប្រាក់", "step3_desc": "ជ្រើសរើសចំនួនប្រាក់ និងរយៈពេល ។",
    "step4_title": "បញ្ជាក់ការប្រាក់", "step4_desc": "ប្រព័ន្ធនឹងបង្ហាញចំនួនប្រាក់ជាក់ស្តែង ។",
    "step5_title": "សងប្រាក់តាម ABA", "step5_desc": "បញ្ចប់ការផ្ទេរប្រាក់ ABA ។",
    "cond_title": "លក្ខខណ្ឌនៃការខ្ចីប្រាក់",
    "cond_new_title": "អ្នកប្រើប្រាស់ថ្មី", "cond_new_l1": "រហូតដល់ $50", "cond_new_l2": "រយៈពេល 7 ថ្ងៃ",
    "cond_reg_title": "អ្នកប្រើប្រាស់ទូទៅ", "cond_reg_desc": "ទំហំទឹកប្រាក់កើនឡើងបន្ទាប់ពីសងទាន់ពេល។",
    "risk_title": "ការព្រមានហានិភ័យ",
    "risk_desc": "សូមបញ្ជាក់ចំនួនប្រាក់ដែលទទួលបានជាក់ស្តែង និងចំនួនប្រាក់ដែលត្រូវសង។",
    "faq1_q": "របៀបចាប់ផ្តើមខ្ចីប្រាក់?", "faq1_a": "បើក Telegram Mini App ភ្ជាប់ព័ត៌មាន ABA ហើយស្នើសុំ។",
    "faq2_q": "តើគាំទ្រ ABA ទេ?", "faq2_a": "បាទ រាល់ប្រតិបត្តិការទាំងអស់ត្រូវបានបញ្ចប់តាមរយៈការផ្ទេរប្រាក់ ABA។",
    "faq3_q": "តើការផ្ទេរប្រាក់លឿនប៉ុណ្ណា?", "faq3_a": "ពេលផ្គូផ្គងរួច អ្នកផ្តល់ប្រាក់កម្ចីផ្ទេរផ្ទាល់ទៅគណនី ABA របស់អ្នក។",
    "faq4_q": "ចុះបើហួសកាលកំណត់?", "faq4_a": "អាចនាំឱ្យមានការកាត់បន្ថយទំហំទឹកប្រាក់។",
    "faq5_q": "របៀបបង្កើនទំហំទឹកប្រាក់?", "faq5_a": "សងទាន់ពេលដើម្បីបង្កើតកំណត់ត្រាឥណទានល្អ។"
}

for lang in ["zh", "en", "km"]:
    filepath = f"frontend/website/src/locales/{lang}.json"
    data = {}
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    
    data["borrow"] = locales[lang]["borrow"]
        
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print("Borrow Locales updated successfully!")