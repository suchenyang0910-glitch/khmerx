package com.khmerx.aire.risk.controller;

import com.khmerx.aire.risk.dto.RiskDecisionResponse;
import com.khmerx.aire.risk.dto.RiskEvaluateRequest;
import com.khmerx.aire.risk.service.RiskEvaluateService;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/risk")
public class RiskEvaluateController {
    private final RiskEvaluateService riskEvaluateService;

    public RiskEvaluateController(RiskEvaluateService riskEvaluateService) {
        this.riskEvaluateService = riskEvaluateService;
    }

    @PostMapping("/check")
    public RiskDecisionResponse check(@Valid @RequestBody RiskEvaluateRequest request) {
        return riskEvaluateService.evaluate(request);
    }
}
