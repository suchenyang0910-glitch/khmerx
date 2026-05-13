package com.khmerx.aire.risk.controller;

import com.khmerx.aire.risk.model.RiskRule;
import com.khmerx.aire.risk.service.RiskRuleService;
import com.khmerx.aire.risk.service.AuditService;
import com.khmerx.aire.risk.service.RbacService;
import jakarta.validation.constraints.NotBlank;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
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
    private final AuditService auditService;
    private final RbacService rbacService;

    public RiskRuleController(RiskRuleService riskRuleService, AuditService auditService, RbacService rbacService) {
        this.riskRuleService = riskRuleService;
        this.auditService = auditService;
        this.rbacService = rbacService;
    }

    @GetMapping
    public List<RiskRule> list(@RequestParam("scenarioType") @NotBlank String scenarioType) {
        rbacService.requirePermission("rules.read");
        return riskRuleService.getEnabledRules(scenarioType);
    }

    @PostMapping("/reload")
    public Map<String, Object> reload(@RequestParam("scenarioType") @NotBlank String scenarioType) {
        rbacService.requirePermission("rules.publish");
        riskRuleService.invalidate(scenarioType);
        int count = riskRuleService.getEnabledRules(scenarioType).size();
        auditService.write(getAuthenticatedMerchantId(), "rules.reload", "risk_rules", scenarioType, Map.of("count", count));
        return Map.of("scenarioType", scenarioType, "count", count);
    }

    private String getAuthenticatedMerchantId() {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        if (auth == null || auth.getPrincipal() == null) {
            return null;
        }
        return String.valueOf(auth.getPrincipal());
    }
}
