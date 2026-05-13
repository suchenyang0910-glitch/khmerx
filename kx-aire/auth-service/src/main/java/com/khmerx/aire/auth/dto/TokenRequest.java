package com.khmerx.aire.auth.dto;

import jakarta.validation.constraints.NotBlank;

public class TokenRequest {
    @NotBlank
    private String merchantId;

    @NotBlank
    private String apiKey;

    public String getMerchantId() {
        return merchantId;
    }

    public void setMerchantId(String merchantId) {
        this.merchantId = merchantId;
    }

    public String getApiKey() {
        return apiKey;
    }

    public void setApiKey(String apiKey) {
        this.apiKey = apiKey;
    }
}

