"""
KhmerX 多语言适配模块（i18n）
支持：km（高棉语）、cn（中文） — 默认中文，逐步过渡到全高棉语

用法:
  from app.i18n import t, LANG

  t("offer.created", lang="km")  # → "សំណើត្រូវបានបង្កើត"
  t("amount_label", lang="cn")   # → "借款金额"
"""
from typing import Optional, Any

# 当前支持的货币显示
# 柬埔寨人看 KHR 更直观，内部计算用 USD
CURRENCY = {
    "km": {"symbol": "៛", "code": "KHR", "rate": 4100},
    "cn": {"symbol": "$", "code": "USD", "rate": 1.0},
}

# 多语言文案
STRINGS = {
    # ── 通用 ──
    "ok": {
        "km": "រួចរាល់",
        "cn": "成功",
    },
    "error": {
        "km": "កំហុស",
        "cn": "错误",
    },
    "loading": {
        "km": "កំពុងផ្ទុក...",
        "cn": "加载中...",
    },
    "submit": {
        "km": "ដាក់ស្នើ",
        "cn": "提交",
    },
    "cancel": {
        "km": "បោះបង់",
        "cn": "取消",
    },
    "confirm": {
        "km": "បញ្ជាក់",
        "cn": "确认",
    },

    # ── 借贷 ──
    "borrow": {
        "km": "ខ្ចីប្រាក់",
        "cn": "借款",
    },
    "lend": {
        "km": "ឱ្យខ្ចី",
        "cn": "放款",
    },
    "loan_amount": {
        "km": "ចំនួនទឹកប្រាក់",
        "cn": "借款金额",
    },
    "loan_term": {
        "km": "រយៈពេលកម្ចី",
        "cn": "借款期限",
    },
    "interest_rate": {
        "km": "អត្រាការប្រាក់",
        "cn": "利率",
    },
    "platform_fee": {
        "km": "ថ្លៃសេវាកម្ម",
        "cn": "平台服务费",
    },
    "total_repayable": {
        "km": "សរុបត្រូវសង",
        "cn": "总应还",
    },
    "repayment_schedule": {
        "km": "កាលវិភាគសងប្រាក់",
        "cn": "还款计划",
    },
    "period": {
        "km": "វគ្គ",
        "cn": "第",
    },
    "due_date": {
        "km": "ថ្ងៃកំណត់",
        "cn": "到期日",
    },
    "principal": {
        "km": "ដើមទុន",
        "cn": "本金",
    },
    "interest": {
        "km": "ការប្រាក់",
        "cn": "利息",
    },
    "status_pending": {
        "km": "រង់ចាំ",
        "cn": "待处理",
    },
    "status_matched": {
        "km": "បានផ្គូផ្គង",
        "cn": "已匹配",
    },
    "status_completed": {
        "km": "បានបញ្ចប់",
        "cn": "已完成",
    },
    "status_cancelled": {
        "km": "បានបោះបង់",
        "cn": "已取消",
    },
    "status_defaulted": {
        "km": "ខកខានសង",
        "cn": "违约",
    },
    "credit_score": {
        "km": "ពិន្ទុឥណទាន",
        "cn": "信用分",
    },
    "days": {
        "km": "ថ្ងៃ",
        "cn": "天",
    },
    "monthly": {
        "km": "ប្រចាំខែ",
        "cn": "月",
    },
    "proof_upload": {
        "km": "ភស្តុតាងនៃការទូទាត់",
        "cn": "打款凭证",
    },
    "aba_account": {
        "km": "គណនី ABA",
        "cn": "ABA 账号",
    },
    "aba_name": {
        "km": "ឈ្មោះ ABA",
        "cn": "ABA 账户名",
    },
    "phone_verify": {
        "km": "ផ្ទៀងផ្ទាត់លេខទូរស័ព្ទ",
        "cn": "手机号验证",
    },
    "kyc_verify": {
        "km": "ផ្ទៀងផ្ទាត់អត្តសញ្ញាណ",
        "cn": "身份验证",
    },
    "create_offer": {
        "km": "បង្កើតសំណើខ្ចី",
        "cn": "创建借款挂单",
    },
    "my_offers": {
        "km": "សំណើរបស់ខ្ញុំ",
        "cn": "我的挂单",
    },
    "my_trades": {
        "km": "ប្រតិបត្តិការរបស់ខ្ញុំ",
        "cn": "我的交易",
    },

    # ── 认证 ──
    "no_rate_warning": {
        "km": "មិនទាន់មានអត្រាប្តូរប្រាក់ថ្ងៃនេះទេ កំពុងប្រើតម្លៃលំនាំដើម",
        "cn": "今日汇率尚未设置，正在使用默认值",
    },

    # ── 认证 ──
    "login": {
        "km": "ចូល",
        "cn": "登录",
    },
    "register": {
        "km": "ចុះឈ្មោះ",
        "cn": "注册",
    },
    "welcome": {
        "km": "សូមស្វាគមន៍មកកាន់ KhmerX",
        "cn": "欢迎来到 KhmerX",
    },

    # ── 产品/订单（旧模块） ──
    "product_list": {
        "km": "បញ្ជីផលិតផល",
        "cn": "商品列表",
    },
    "order_list": {
        "km": "បញ្ជីការបញ្ជាទិញ",
        "cn": "订单列表",
    },
    "price": {
        "km": "តម្លៃ",
        "cn": "价格",
    },
}

# 中文期数格式
PERIOD_FMT = {
    "km": "វគ្គទី{}",
    "cn": "第{}期",
}


def t(key: str, lang: str = "cn", **kwargs: Any) -> str:
    """获取翻译文本"""
    translations = STRINGS.get(key)
    if not translations:
        return key  # 找不到返回 key 本身

    text = translations.get(lang)
    if not text:
        text = translations.get("cn", key)  # 默认 fallback 中文

    if kwargs:
        text = text.format(**kwargs)

    return text


def fmt_amount(usd_amount: float, lang: str = "cn", currency: str = "") -> str:
    """
    格式化金额显示
    柬埔寨用户默认显示 KHR，中文用户显示 USD
    """
    if currency == "khr" or (not currency and lang == "km"):
        rate = CURRENCY["km"]["rate"]
        khr = round(usd_amount * rate, -2)  # 抹零到百位
        return f"{khr:,.0f} ៛"
    else:
        return f"${usd_amount:,.2f}"


def fmt_period(period: int, lang: str = "cn") -> str:
    """格式化期数"""
    fmt = PERIOD_FMT.get(lang, PERIOD_FMT["cn"])
    return fmt.format(period)


def fmt_days(days: int, lang: str = "cn") -> str:
    """格式化天数"""
    return f"{days} {t('days', lang)}"


def status_text(status: str, lang: str = "cn") -> str:
    """状态转本地化文字"""
    key_map = {
        "pending": "status_pending",
        "matched": "status_matched",
        "completed": "status_completed",
        "cancelled": "status_cancelled",
        "defaulted": "status_defaulted",
        "lend_confirmed": None,  # 没有对应翻译
        "repayment_confirmed": None,
        "repaying": None,
    }
    key = key_map.get(status)
    if key:
        return t(key, lang)
    return status


def localize_offer(offer_dict: dict, lang: str = "cn", currency: str = "") -> dict:
    """将挂单数据本地化"""
    localized = dict(offer_dict)
    localized["_label"] = {
        "amount": fmt_amount(offer_dict.get("amount", 0), lang, currency),
        "fee": fmt_amount(offer_dict.get("fee", 0), lang, currency),
        "total_amount": fmt_amount(offer_dict.get("total_amount", 0), lang, currency),
        "status": status_text(offer_dict.get("status", ""), lang),
        "term": fmt_days(offer_dict.get("term_days", 0), lang),
        "rate": f"{offer_dict.get('rate', 0)}%/ {t('monthly', lang)}",
        "period_label": t("period", lang),
        "amount_label": t("loan_amount", lang),
        "term_label": t("loan_term", lang),
        "rate_label": t("interest_rate", lang),
        "fee_label": t("platform_fee", lang),
        "create_offer": t("create_offer", lang),
        "my_offers": t("my_offers", lang),
        "my_trades": t("my_trades", lang),
    }
    return localized


def localize_trade(trade_dict: dict, lang: str = "cn", currency: str = "") -> dict:
    """将交易数据本地化"""
    localized = dict(trade_dict)
    localized["_label"] = {
        "amount": fmt_amount(trade_dict.get("amount", 0), lang, currency),
        "fee": fmt_amount(trade_dict.get("fee", 0), lang, currency),
        "total_repayable": fmt_amount(trade_dict.get("total_repayable", 0), lang, currency),
        "status": status_text(trade_dict.get("status", ""), lang),
        "term": fmt_days(trade_dict.get("term_days", 0), lang),
        "rate": f"{trade_dict.get('rate', 0)}%/ {t('monthly', lang)}",
        "amount_label": t("loan_amount", lang),
        "term_label": t("loan_term", lang),
        "rate_label": t("interest_rate", lang),
        "fee_label": t("platform_fee", lang),
        "total_label": t("total_repayable", lang),
        "period_label": t("period", lang),
        "due_date_label": t("due_date", lang),
        "principal_label": t("principal", lang),
        "interest_label": t("interest", lang),
        "repayment_schedule": t("repayment_schedule", lang),
        "create_offer": t("create_offer", lang),
        "my_offers": t("my_offers", lang),
        "my_trades": t("my_trades", lang),
        "credit_score": t("credit_score", lang),
    }
    return localized


def localize_schedule(schedule_list: list, lang: str = "cn", currency: str = "") -> list:
    """本地化还款计划列表"""
    localized = []
    for s in schedule_list:
        ls = dict(s)
        ls["_period_label"] = fmt_period(s.get("period", 0), lang)
        ls["_principal"] = fmt_amount(s.get("principal", 0), lang, currency)
        ls["_interest"] = fmt_amount(s.get("interest", 0), lang, currency)
        ls["_total"] = fmt_amount(s.get("total", 0), lang, currency)
        ls["_status"] = status_text(s.get("status", ""), lang)
        localized.append(ls)
    return localized


def localize_auth(user_dict: dict, lang: str = "cn") -> dict:
    """本地化用户认证信息"""
    localized = dict(user_dict)
    localized["_label"] = {
        "welcome": t("welcome", lang),
        "login": t("login", lang),
        "credit_score": t("credit_score", lang),
        "phone_verify": t("phone_verify", lang),
        "kyc_verify": t("kyc_verify", lang),
        "aba_account": t("aba_account", lang),
        "aba_name": t("aba_name", lang),
    }
    return localized
