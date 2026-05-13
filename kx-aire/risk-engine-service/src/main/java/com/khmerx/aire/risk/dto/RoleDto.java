package com.khmerx.aire.risk.dto;

import java.util.List;

public class RoleDto {
    private String roleId;
    private String roleKey;
    private String roleName;
    private Integer builtIn;
    private List<String> permissionKeys;

    public RoleDto(String roleId, String roleKey, String roleName, Integer builtIn, List<String> permissionKeys) {
        this.roleId = roleId;
        this.roleKey = roleKey;
        this.roleName = roleName;
        this.builtIn = builtIn;
        this.permissionKeys = permissionKeys;
    }

    public String getRoleId() {
        return roleId;
    }

    public String getRoleKey() {
        return roleKey;
    }

    public String getRoleName() {
        return roleName;
    }

    public Integer getBuiltIn() {
        return builtIn;
    }

    public List<String> getPermissionKeys() {
        return permissionKeys;
    }
}

