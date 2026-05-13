package com.khmerx.aire.risk.service;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.khmerx.aire.risk.mapper.RiskRuleMapper;
import com.khmerx.aire.risk.model.RiskRule;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

import java.time.Duration;
import java.util.Collections;
import java.util.List;

@Service
public class RiskRuleService {
    private final RiskRuleMapper riskRuleMapper;
    private final StringRedisTemplate stringRedisTemplate;
    private final ObjectMapper objectMapper;

    public RiskRuleService(RiskRuleMapper riskRuleMapper, StringRedisTemplate stringRedisTemplate, ObjectMapper objectMapper) {
        this.riskRuleMapper = riskRuleMapper;
        this.stringRedisTemplate = stringRedisTemplate;
        this.objectMapper = objectMapper;
    }

    public List<RiskRule> getEnabledRules(String scenarioType) {
        if (!StringUtils.hasText(scenarioType)) {
            return Collections.emptyList();
        }
        String cacheKey = "risk:rules:" + scenarioType;
        String cached = stringRedisTemplate.opsForValue().get(cacheKey);
        if (StringUtils.hasText(cached)) {
            try {
                return objectMapper.readValue(cached, new TypeReference<>() {
                });
            } catch (Exception ignored) {
            }
        }

        List<RiskRule> rules = riskRuleMapper.findEnabledByScenario(scenarioType);
        try {
            stringRedisTemplate.opsForValue().set(cacheKey, objectMapper.writeValueAsString(rules), Duration.ofMinutes(5));
        } catch (Exception ignored) {
        }
        return rules;
    }
}

