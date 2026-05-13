package com.khmerx.aire.risk.controller;

import com.khmerx.aire.risk.model.RiskRule;
import com.khmerx.aire.risk.service.RiskRuleService;
import jakarta.validation.constraints.NotBlank;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;

@Validated
@RestController
@RequestMapping("/risk/rules")
public class RiskRuleController {
    private final RiskRuleService riskRuleService;

    public RiskRuleController(RiskRuleService riskRuleService) {
        this.riskRuleService = riskRuleService;
    }

    @GetMapping
    public List<RiskRule> list(@RequestParam("scenarioType") @NotBlank String scenarioType) {
        return riskRuleService.getEnabledRules(scenarioType);
    }

    @PostMapping("/reload")
    public Map<String, Object> reload(@RequestParam("scenarioType") @NotBlank String scenarioType) {
        riskRuleService.invalidate(scenarioType);
        int count = riskRuleService.getEnabledRules(scenarioType).size();
        return Map.of("scenarioType", scenarioType, "count", count);
    }
}

