package com.khmerx.aire.risk.dto;

import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;

public class UserStatusUpdateRequest {
    @Min(0)
    @Max(1)
    private int status;

    public int getStatus() {
        return status;
    }

    public void setStatus(int status) {
        this.status = status;
    }
}

