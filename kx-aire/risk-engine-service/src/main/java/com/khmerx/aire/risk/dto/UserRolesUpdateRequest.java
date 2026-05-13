package com.khmerx.aire.risk.dto;

import java.util.List;

public class UserRolesUpdateRequest {
    private List<String> roleKeys;

    public List<String> getRoleKeys() {
        return roleKeys;
    }

    public void setRoleKeys(List<String> roleKeys) {
        this.roleKeys = roleKeys;
    }
}

