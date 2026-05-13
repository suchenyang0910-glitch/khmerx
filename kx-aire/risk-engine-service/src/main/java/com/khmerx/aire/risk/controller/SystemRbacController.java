package com.khmerx.aire.risk.controller;

import com.khmerx.aire.risk.dto.AdminUserCreateRequest;
import com.khmerx.aire.risk.dto.AdminUserDto;
import com.khmerx.aire.risk.dto.MeResponse;
import com.khmerx.aire.risk.dto.PageResponse;
import com.khmerx.aire.risk.dto.RoleDto;
import com.khmerx.aire.risk.dto.RolePermissionsUpdateRequest;
import com.khmerx.aire.risk.dto.UserRolesUpdateRequest;
import com.khmerx.aire.risk.dto.UserStatusUpdateRequest;
import com.khmerx.aire.risk.model.Permission;
import com.khmerx.aire.risk.service.RbacService;
import jakarta.validation.Valid;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;

@Validated
@RestController
@RequestMapping("/system")
public class SystemRbacController {
    private final RbacService rbacService;

    public SystemRbacController(RbacService rbacService) {
        this.rbacService = rbacService;
    }

    @GetMapping("/me")
    public MeResponse me() {
        return rbacService.me();
    }

    @GetMapping("/users")
    public PageResponse<AdminUserDto> users(
            @RequestParam(value = "keyword", required = false) String keyword,
            @RequestParam(value = "page", defaultValue = "1") @Min(1) int page,
            @RequestParam(value = "pageSize", defaultValue = "20") @Min(1) @Max(100) int pageSize
    ) {
        return rbacService.listUsers(keyword, page, pageSize);
    }

    @PostMapping("/users")
    public AdminUserDto createUser(@Valid @RequestBody AdminUserCreateRequest request) {
        return rbacService.createUser(request);
    }

    @PostMapping("/users/{userId}/status")
    public Map<String, Object> updateStatus(@PathVariable("userId") String userId, @Valid @RequestBody UserStatusUpdateRequest request) {
        rbacService.updateUserStatus(userId, request.getStatus());
        return Map.of("ok", true);
    }

    @PostMapping("/users/{userId}/roles")
    public Map<String, Object> updateRoles(@PathVariable("userId") String userId, @RequestBody UserRolesUpdateRequest request) {
        rbacService.updateUserRoles(userId, request == null ? List.of() : request.getRoleKeys());
        return Map.of("ok", true);
    }

    @GetMapping("/roles")
    public List<RoleDto> roles() {
        return rbacService.listRoles();
    }

    @GetMapping("/permissions")
    public List<Permission> permissions() {
        return rbacService.listPermissions();
    }

    @PostMapping("/roles/{roleId}/permissions")
    public Map<String, Object> updateRolePermissions(@PathVariable("roleId") String roleId, @RequestBody RolePermissionsUpdateRequest request) {
        rbacService.updateRolePermissions(roleId, request == null ? List.of() : request.getPermissionKeys());
        return Map.of("ok", true);
    }
}

