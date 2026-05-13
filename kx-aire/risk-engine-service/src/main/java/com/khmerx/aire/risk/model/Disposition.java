package com.khmerx.aire.risk.model;

import java.time.LocalDateTime;

public class Disposition {
    private String dispositionId;
    private String eventId;
    private String action;
    private String remark;
    private String operatorId;
    private LocalDateTime createdAt;

    public String getDispositionId() {
        return dispositionId;
    }

    public void setDispositionId(String dispositionId) {
        this.dispositionId = dispositionId;
    }

    public String getEventId() {
        return eventId;
    }

    public void setEventId(String eventId) {
        this.eventId = eventId;
    }

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

    public String getOperatorId() {
        return operatorId;
    }

    public void setOperatorId(String operatorId) {
        this.operatorId = operatorId;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }
}

