package com.khmerx.aire.risk.dto;

import java.util.List;

public class MeResponse {
    private String actorId;
    private List<String> roles;
    private List<String> permissions;

    public MeResponse(String actorId, List<String> roles, List<String> permissions) {
        this.actorId = actorId;
        this.roles = roles;
        this.permissions = permissions;
    }

    public String getActorId() {
        return actorId;
    }

    public List<String> getRoles() {
        return roles;
    }

    public List<String> getPermissions() {
        return permissions;
    }
}

