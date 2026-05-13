package com.khmerx.aire.risk.dto;

import java.time.LocalDateTime;
import java.util.List;

public class AdminUserDto {
    private String userId;
    private String email;
    private String displayName;
    private Integer status;
    private LocalDateTime createdAt;
    private List<String> roleKeys;

    public AdminUserDto(String userId, String email, String displayName, Integer status, LocalDateTime createdAt, List<String> roleKeys) {
        this.userId = userId;
        this.email = email;
        this.displayName = displayName;
        this.status = status;
        this.createdAt = createdAt;
        this.roleKeys = roleKeys;
    }

    public String getUserId() {
        return userId;
    }

    public String getEmail() {
        return email;
    }

    public String getDisplayName() {
        return displayName;
    }

    public Integer getStatus() {
        return status;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public List<String> getRoleKeys() {
        return roleKeys;
    }
}

