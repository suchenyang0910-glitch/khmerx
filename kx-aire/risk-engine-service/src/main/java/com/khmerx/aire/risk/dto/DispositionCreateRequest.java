package com.khmerx.aire.risk.dto;

import jakarta.validation.constraints.NotBlank;

public class DispositionCreateRequest {
    @NotBlank
    private String action;

    private String remark;

    public String getAction() {
        return action;
    }

    public void setAction(String action) {
        this.action = action;
    }

    public String getRemark() {
        return remark;
    }

    public void setRemark(String remark) {
        this.remark = remark;
    }
}

