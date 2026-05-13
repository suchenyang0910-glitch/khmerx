package com.khmerx.aire.risk.dto;

import java.util.List;

public class RiskDecisionResponse {
    private String decision;
    private String riskLevel;
    private String reason;
    private double riskScore;
    private List<String> matchedRuleIds;

    public RiskDecisionResponse() {
    }

    public RiskDecisionResponse(String decision, String riskLevel, String reason, double riskScore, List<String> matchedRuleIds) {
        this.decision = decision;
        this.riskLevel = riskLevel;
        this.reason = reason;
        this.riskScore = riskScore;
        this.matchedRuleIds = matchedRuleIds;
    }

    public String getDecision() {
        return decision;
    }

    public void setDecision(String decision) {
        this.decision = decision;
    }

    public String getRiskLevel() {
        return riskLevel;
    }

    public void setRiskLevel(String riskLevel) {
        this.riskLevel = riskLevel;
    }

    public String getReason() {
        return reason;
    }

    public void setReason(String reason) {
        this.reason = reason;
    }

    public double getRiskScore() {
        return riskScore;
    }

    public void setRiskScore(double riskScore) {
        this.riskScore = riskScore;
    }

    public List<String> getMatchedRuleIds() {
        return matchedRuleIds;
    }

    public void setMatchedRuleIds(List<String> matchedRuleIds) {
        this.matchedRuleIds = matchedRuleIds;
    }
}
