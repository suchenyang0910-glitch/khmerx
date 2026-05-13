package com.khmerx.aire.risk.service;

import com.khmerx.aire.risk.dto.RiskDecisionResponse;
import com.khmerx.aire.risk.dto.RiskEvaluateRequest;
import com.khmerx.aire.risk.mapper.ApiLogMapper;
import com.khmerx.aire.risk.mapper.BlacklistMapper;
import com.khmerx.aire.risk.mapper.RiskOrderMapper;
import com.khmerx.aire.risk.mapper.RiskEventMapper;
import com.khmerx.aire.risk.model.ApiLog;
import com.khmerx.aire.risk.model.RiskOrder;
import com.khmerx.aire.risk.model.RiskEvent;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.dao.DuplicateKeyException;
import org.springframework.expression.Expression;
import org.springframework.expression.ExpressionParser;
import org.springframework.expression.spel.standard.SpelExpressionParser;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.expression.spel.support.SimpleEvaluationContext;
import org.springframework.context.expression.MapAccessor;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.ArrayList;
import java.util.List;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.UUID;
import java.util.StringJoiner;

@Service
public class RiskEvaluateService {
    private final RiskOrderMapper riskOrderMapper;
    private final RiskRuleService riskRuleService;
    private final BlacklistMapper blacklistMapper;
    private final ApiLogMapper apiLogMapper;
    private final RiskEventMapper riskEventMapper;
    private final ObjectMapper objectMapper;
    private final ExpressionParser expressionParser = new SpelExpressionParser();

    public RiskEvaluateService(
            RiskOrderMapper riskOrderMapper,
            RiskRuleService riskRuleService,
            BlacklistMapper blacklistMapper,
            ApiLogMapper apiLogMapper,
            RiskEventMapper riskEventMapper,
            ObjectMapper objectMapper
    ) {
        this.riskOrderMapper = riskOrderMapper;
        this.riskRuleService = riskRuleService;
        this.blacklistMapper = blacklistMapper;
        this.apiLogMapper = apiLogMapper;
        this.riskEventMapper = riskEventMapper;
        this.objectMapper = objectMapper;
    }

    public RiskDecisionResponse evaluate(RiskEvaluateRequest request) {
        long start = System.nanoTime();
        String merchantId = getAuthenticatedMerchantId();
        if (StringUtils.hasText(request.getMerchantId()) && !merchantId.equals(request.getMerchantId())) {
            RiskDecisionResponse response = saveAndReturn(merchantId, request, 0.0, "D", "rejected", "merchant_mismatch", List.of());
            writeApiLog(merchantId, "/risk/check", request, response, start);
            return response;
        }

        int blacklistHits = computeBlacklistHits(request);
        if (blacklistHits > 0) {
            request.setBlacklistHits(blacklistHits);
        }

        List<String> matchedRuleIds = new ArrayList<>();
        BigDecimal penalty = BigDecimal.ZERO;
        String action = null;
        String topReason = "risk_check_passed";

        var rules = riskRuleService.getEnabledRules(request.getScenarioType());
        Map<String, Object> root = new LinkedHashMap<>();
        root.put("applyAmount", request.getApplyAmount());
        root.put("userAgeDays", request.getUserAgeDays());
        root.put("offers24hCount", request.getOffers24hCount());
        root.put("activeTradesCount", request.getActiveTradesCount());
        root.put("blacklistHits", request.getBlacklistHits());
        root.put("blacklistHit", request.getBlacklistHits() > 0);
        root.put("scenarioType", request.getScenarioType());
        root.put("userId", request.getUserId());
        root.put("merchantId", merchantId);
        root.put("orderId", request.getOrderId());

        SimpleEvaluationContext context = SimpleEvaluationContext
                .forReadOnlyDataBinding()
                .withRootObject(root)
                .withPropertyAccessors(new MapAccessor())
                .build();

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
        RiskDecisionResponse response = saveAndReturn(merchantId, request, score, riskLevel, decision, topReason, matchedRuleIds);
        writeRiskEvent(merchantId, request, score, riskLevel, decision, topReason, matchedRuleIds);
        writeApiLog(merchantId, "/risk/check", request, response, start);
        return response;
    }

    private void writeRiskEvent(
            String merchantId,
            RiskEvaluateRequest request,
            double score,
            String riskLevel,
            String decision,
            String reason,
            List<String> matchedRuleIds
    ) {
        try {
            RiskEvent event = new RiskEvent();
            event.setEventId(UUID.randomUUID().toString());
            event.setMerchantId(merchantId);
            event.setScenarioType(request.getScenarioType());
            event.setUserId(request.getUserId());
            event.setOrderId(request.getOrderId());
            event.setRiskScore(BigDecimal.valueOf(score));
            event.setRiskLevel(riskLevel);
            event.setDecision(decision);
            event.setReason(reason);

            StringJoiner sj = new StringJoiner(",");
            for (String id : matchedRuleIds) {
                if (StringUtils.hasText(id)) {
                    sj.add(id);
                }
            }
            event.setMatchedRuleIds(sj.toString());
            event.setInputSnapshot(objectMapper.writeValueAsString(request));
            event.setStatus("open");
            riskEventMapper.insert(event);
        } catch (Exception ignored) {
        }
    }

    private void writeApiLog(String merchantId, String apiName, Object request, Object response, long startNano) {
        try {
            int costMs = (int) Math.max(0, (System.nanoTime() - startNano) / 1_000_000L);
            ApiLog log = new ApiLog();
            log.setLogId(UUID.randomUUID().toString());
            log.setMerchantId(merchantId);
            log.setApiName(apiName);
            log.setRequestBody(objectMapper.writeValueAsString(request));
            log.setResponseBody(objectMapper.writeValueAsString(response));
            log.setResponseTime(costMs);
            apiLogMapper.insert(log);
        } catch (Exception ignored) {
        }
    }

    private int computeBlacklistHits(RiskEvaluateRequest request) {
        int hits = 0;
        hits += countIfHit("user", request.getUserId());
        hits += countIfHit("phone", request.getPhone());
        hits += countIfHit("id_card", request.getIdNumber());
        hits += countIfHit("device", request.getDeviceId());
        hits += countIfHit("ip", request.getIpAddress());
        return hits;
    }

    private int countIfHit(String subjectType, String subjectId) {
        if (!StringUtils.hasText(subjectId)) {
            return 0;
        }
        try {
            return blacklistMapper.countHit(subjectType, subjectId) > 0 ? 1 : 0;
        } catch (Exception ignored) {
            return 0;
        }
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
