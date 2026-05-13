insert into merchant_center.merchants(merchant_id, company_name, api_key, saas_version, status)
values ('m_demo', 'Demo Merchant', 'demo_key', 'basic', 1)
on conflict (merchant_id) do nothing;

insert into risk_engine.risk_rules(rule_id, rule_name, scenario_type, rule_expression, score_weight, risk_action, status)
values ('r_blacklist_hit', 'blacklist hit', 'phone_rental', 'blacklistHits > 0', 90, 'reject', 1)
on conflict (rule_id) do nothing;

insert into blacklist_center.blacklist_subjects(subject_id, subject_type, blacklist_reason, risk_level, reported_by)
values ('u_blocked_demo', 'user', 'demo blacklist user', 'D', 'system')
on conflict (subject_id) do nothing;

insert into api_center.permissions(perm_key, perm_name) values
('rules.read', '规则只读'),
('rules.write', '规则编辑'),
('rules.publish', '规则发布'),
('cases.read', '命中事件只读'),
('cases.dispose', '命中事件处置'),
('audit.read', '审计日志查看'),
('system.read', '系统管理只读'),
('system.admin', '系统管理写入'),
('export.csv', '导出')
on conflict (perm_key) do nothing;

insert into risk_engine.risk_rules(rule_id, rule_name, scenario_type, rule_expression, score_weight, risk_action, status)
values ('r_new_user_large_amount', 'new user large amount', 'phone_rental', 'userAgeDays < 7 and applyAmount > 300', 35, 'manual_review', 1)
on conflict (rule_id) do nothing;

insert into risk_engine.risk_rules(rule_id, rule_name, scenario_type, rule_expression, score_weight, risk_action, status)
values ('r_high_offer_frequency', 'high offer frequency', 'phone_rental', 'offers24hCount >= 5', 25, 'manual_review', 1)
on conflict (rule_id) do nothing;

insert into risk_engine.risk_rules(rule_id, rule_name, scenario_type, rule_expression, score_weight, risk_action, status)
values ('r_many_active_trades', 'many active trades', 'phone_rental', 'activeTradesCount >= 8', 20, 'manual_review', 1)
on conflict (rule_id) do nothing;

