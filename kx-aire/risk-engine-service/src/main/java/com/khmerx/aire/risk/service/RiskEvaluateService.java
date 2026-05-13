package com.khmerx.aire.risk.service;

import com.khmerx.aire.risk.dto.RiskDecisionResponse;
import com.khmerx.aire.risk.dto.RiskEvaluateRequest;
import com.khmerx.aire.risk.mapper.RiskOrderMapper;
import com.khmerx.aire.risk.model.RiskOrder;
import org.springframework.dao.DuplicateKeyException;
import org.springframework.expression.Expression;
import org.springframework.expression.ExpressionParser;
import org.springframework.expression.spel.standard.SpelExpressionParser;
import org.springframework.expression.spel.support.StandardEvaluationContext;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.ArrayList;
import java.util.List;

@Service
public class RiskEvaluateService {
    private final RiskOrderMapper riskOrderMapper;
    private final RiskRuleService riskRuleService;
    private final ExpressionParser expressionParser = new SpelExpressionParser();

    public RiskEvaluateService(RiskOrderMapper riskOrderMapper, RiskRuleService riskRuleService) {
        this.riskOrderMapper = riskOrderMapper;
        this.riskRuleService = riskRuleService;
    }

    public RiskDecisionResponse evaluate(RiskEvaluateRequest request) {
        String merchantId = getAuthenticatedMerchantId();
        if (StringUtils.hasText(request.getMerchantId()) && !merchantId.equals(request.getMerchantId())) {
            return saveAndReturn(merchantId, request, 0.0, "D", "rejected", "merchant_mismatch", List.of());
        }

        List<String> matchedRuleIds = new ArrayList<>();
        BigDecimal penalty = BigDecimal.ZERO;
        String action = null;
        String topReason = "risk_check_passed";

        var rules = riskRuleService.getEnabledRules(request.getScenarioType());
        StandardEvaluationContext context = new StandardEvaluationContext();
        context.setVariable("applyAmount", request.getApplyAmount());
        context.setVariable("userAgeDays", request.getUserAgeDays());
        context.setVariable("offers24hCount", request.getOffers24hCount());
        context.setVariable("activeTradesCount", request.getActiveTradesCount());
        context.setVariable("blacklistHits", request.getBlacklistHits());
        context.setVariable("scenarioType", request.getScenarioType());
        context.setVariable("userId", request.getUserId());
        context.setVariable("merchantId", merchantId);
        context.setVariable("orderId", request.getOrderId());

        for (var rule : rules) {
            if (!StringUtils.hasText(rule.getRuleExpression())) {
                continue;
            }
            boolean hit = false;
            try {
                Expression expr = expressionParser.parseExpression(rule.getRuleExpression());
                Boolean value = expr.getValue(context, Boolean.class);
                hit = Boolean.TRUE.equals(value);
            } catch (Exception ignored) {
            }
            if (!hit) {
                continue;
            }

            matchedRuleIds.add(rule.getRuleId());
            if (rule.getScoreWeight() != null) {
                penalty = penalty.add(rule.getScoreWeight());
            }
            if (isHigherPriority(rule.getRiskAction(), action)) {
                action = rule.getRiskAction();
                topReason = "rule_hit:" + rule.getRuleId();
            }
        }

        double score = Math.max(0.0, 100.0 - penalty.doubleValue());
        String riskLevel = mapRiskLevel(score);
        String decision = mapDecision(action, score);
        return saveAndReturn(merchantId, request, score, riskLevel, decision, topReason, matchedRuleIds);
    }

    private RiskDecisionResponse saveAndReturn(String merchantId, RiskEvaluateRequest request, double score, String level, String decision, String reason, List<String> matchedRuleIds) {
        RiskOrder order = new RiskOrder();
        order.setOrderId(request.getOrderId());
        order.setMerchantId(merchantId);
        order.setUserId(request.getUserId());
        order.setScenarioType(request.getScenarioType());
        order.setApplyAmount(BigDecimal.valueOf(request.getApplyAmount()).setScale(2, RoundingMode.HALF_UP));
        order.setRiskScore(BigDecimal.valueOf(score).setScale(2, RoundingMode.HALF_UP));
        order.setRiskLevel(level);
        order.setApproveStatus(decision);
        try {
            riskOrderMapper.insert(order);
        } catch (DuplicateKeyException ignored) {
        }
        return new RiskDecisionResponse(decision, level, reason, score, matchedRuleIds);
    }

    private String getAuthenticatedMerchantId() {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        if (authentication == null) {
            return null;
        }
        return authentication.getName();
    }

    private boolean isHigherPriority(String candidate, String current) {
        return priority(candidate) > priority(current);
    }

    private int priority(String action) {
        if (!StringUtils.hasText(action)) {
            return 0;
        }
        String a = action.trim().toLowerCase();
        if (a.equals("reject") || a.equals("rejected")) {
            return 3;
        }
        if (a.equals("manual_review")) {
            return 2;
        }
        if (a.equals("alert")) {
            return 1;
        }
        return 0;
    }

    private String mapDecision(String action, double score) {
        int p = priority(action);
        if (p >= 3) {
            return "rejected";
        }
        if (p == 2) {
            return "manual_review";
        }
        if (score < 50) {
            return "manual_review";
        }
        return "approved";
    }

    private String mapRiskLevel(double score) {
        if (score >= 90) {
            return "AAA";
        }
        if (score >= 80) {
            return "AA";
        }
        if (score >= 70) {
            return "A";
        }
        if (score >= 60) {
            return "B";
        }
        if (score >= 50) {
            return "C";
        }
        return "D";
    }
}
