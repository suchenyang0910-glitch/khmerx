package com.khmerx.aire.risk.dto;

import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotBlank;

public class RiskEvaluateRequest {
    @NotBlank
    private String orderId;

    private String merchantId;

    @NotBlank
    private String userId;

    @NotBlank
    private String scenarioType;

    @DecimalMin(value = "0.01")
    private double applyAmount;

    private int userAgeDays;
    private int offers24hCount;
    private int activeTradesCount;
    private int blacklistHits;

    public String getOrderId() {
        return orderId;
    }

    public void setOrderId(String orderId) {
        this.orderId = orderId;
    }

    public String getMerchantId() {
        return merchantId;
    }

    public void setMerchantId(String merchantId) {
        this.merchantId = merchantId;
    }

    public String getUserId() {
        return userId;
    }

    public void setUserId(String userId) {
        this.userId = userId;
    }

    public String getScenarioType() {
        return scenarioType;
    }

    public void setScenarioType(String scenarioType) {
        this.scenarioType = scenarioType;
    }

    public double getApplyAmount() {
        return applyAmount;
    }

    public void setApplyAmount(double applyAmount) {
        this.applyAmount = applyAmount;
    }

    public int getUserAgeDays() {
        return userAgeDays;
    }

    public void setUserAgeDays(int userAgeDays) {
        this.userAgeDays = userAgeDays;
    }

    public int getOffers24hCount() {
        return offers24hCount;
    }

    public void setOffers24hCount(int offers24hCount) {
        this.offers24hCount = offers24hCount;
    }

    public int getActiveTradesCount() {
        return activeTradesCount;
    }

    public void setActiveTradesCount(int activeTradesCount) {
        this.activeTradesCount = activeTradesCount;
    }

    public int getBlacklistHits() {
        return blacklistHits;
    }

    public void setBlacklistHits(int blacklistHits) {
        this.blacklistHits = blacklistHits;
    }
}
