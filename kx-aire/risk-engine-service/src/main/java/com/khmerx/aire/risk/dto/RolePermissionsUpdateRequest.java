package com.khmerx.aire.risk.dto;

import java.util.List;

public class RolePermissionsUpdateRequest {
    private List<String> permissionKeys;

    public List<String> getPermissionKeys() {
        return permissionKeys;
    }

    public void setPermissionKeys(List<String> permissionKeys) {
        this.permissionKeys = permissionKeys;
    }
}

