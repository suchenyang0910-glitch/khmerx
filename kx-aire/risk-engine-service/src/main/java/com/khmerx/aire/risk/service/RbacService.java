package com.khmerx.aire.risk.service;

import com.khmerx.aire.risk.dto.AdminUserCreateRequest;
import com.khmerx.aire.risk.dto.AdminUserDto;
import com.khmerx.aire.risk.dto.MeResponse;
import com.khmerx.aire.risk.dto.PageResponse;
import com.khmerx.aire.risk.dto.RoleDto;
import com.khmerx.aire.risk.mapper.AdminUserMapper;
import com.khmerx.aire.risk.mapper.PermissionMapper;
import com.khmerx.aire.risk.mapper.RoleMapper;
import com.khmerx.aire.risk.mapper.RolePermissionMapper;
import com.khmerx.aire.risk.mapper.UserRoleMapper;
import com.khmerx.aire.risk.model.AdminUser;
import com.khmerx.aire.risk.model.Permission;
import com.khmerx.aire.risk.model.Role;
import com.khmerx.aire.risk.web.ApiForbiddenException;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.UUID;

@Service
public class RbacService {
    private final AdminUserMapper adminUserMapper;
    private final RoleMapper roleMapper;
    private final PermissionMapper permissionMapper;
    private final UserRoleMapper userRoleMapper;
    private final RolePermissionMapper rolePermissionMapper;
    private final AuditService auditService;

    public RbacService(
            AdminUserMapper adminUserMapper,
            RoleMapper roleMapper,
            PermissionMapper permissionMapper,
            UserRoleMapper userRoleMapper,
            RolePermissionMapper rolePermissionMapper,
            AuditService auditService
    ) {
        this.adminUserMapper = adminUserMapper;
        this.roleMapper = roleMapper;
        this.permissionMapper = permissionMapper;
        this.userRoleMapper = userRoleMapper;
        this.rolePermissionMapper = rolePermissionMapper;
        this.auditService = auditService;
    }

    public MeResponse me() {
        String merchantId = getAuthenticatedMerchantId();
        ensureProvisioned(merchantId);
        List<String> roleKeys = userRoleMapper.listRoleKeysByUser(merchantId, merchantId);
        List<String> roleIds = userRoleMapper.listRoleIdsByUser(merchantId, merchantId);
        List<String> permKeys = roleIds.isEmpty() ? List.of() : rolePermissionMapper.listPermKeysByRoleIds(roleIds);
        return new MeResponse(merchantId, roleKeys, permKeys);
    }

    public void requirePermission(String permKey) {
        if (!hasPermission(permKey)) {
            throw new ApiForbiddenException("forbidden");
        }
    }

    public boolean hasPermission(String permKey) {
        String merchantId = getAuthenticatedMerchantId();
        ensureProvisioned(merchantId);
        List<String> roleIds = userRoleMapper.listRoleIdsByUser(merchantId, merchantId);
        if (roleIds.isEmpty()) {
            return false;
        }
        List<String> permKeys = rolePermissionMapper.listPermKeysByRoleIds(roleIds);
        return permKeys.contains(permKey);
    }

    public PageResponse<AdminUserDto> listUsers(String keyword, int page, int pageSize) {
        requirePermission("system.read");
        String merchantId = getAuthenticatedMerchantId();
        ensureProvisioned(merchantId);
        int safePage = Math.max(1, page);
        int safePageSize = Math.min(100, Math.max(1, pageSize));
        int offset = (safePage - 1) * safePageSize;

        long total = adminUserMapper.count(merchantId, keyword);
        List<AdminUser> users = adminUserMapper.list(merchantId, keyword, safePageSize, offset);
        List<AdminUserDto> items = new ArrayList<>();
        for (AdminUser u : users) {
            List<String> roleKeys = userRoleMapper.listRoleKeysByUser(merchantId, u.getUserId());
            items.add(new AdminUserDto(u.getUserId(), u.getEmail(), u.getDisplayName(), u.getStatus(), u.getCreatedAt(), roleKeys));
        }
        return new PageResponse<>(items, total, safePage, safePageSize);
    }

    public AdminUserDto createUser(AdminUserCreateRequest request) {
        requirePermission("system.admin");
        String merchantId = getAuthenticatedMerchantId();
        ensureProvisioned(merchantId);

        AdminUser exists = adminUserMapper.findByEmail(merchantId, request.getEmail());
        if (exists != null) {
            throw new IllegalArgumentException("user_exists");
        }

        String userId = UUID.randomUUID().toString();
        AdminUser u = new AdminUser();
        u.setUserId(userId);
        u.setMerchantId(merchantId);
        u.setEmail(request.getEmail());
        u.setDisplayName(StringUtils.hasText(request.getDisplayName()) ? request.getDisplayName() : request.getEmail());
        u.setStatus(1);
        adminUserMapper.insert(u);

        List<String> roleKeys = request.getRoleKeys() == null ? List.of() : request.getRoleKeys();
        applyUserRolesInternal(merchantId, userId, roleKeys);

        auditService.write(merchantId, "system.user.create", "admin_user", userId, Map.of("email", request.getEmail(), "roleKeys", roleKeys));
        return new AdminUserDto(userId, u.getEmail(), u.getDisplayName(), u.getStatus(), u.getCreatedAt(), userRoleMapper.listRoleKeysByUser(merchantId, userId));
    }

    public void updateUserStatus(String userId, int status) {
        requirePermission("system.admin");
        String merchantId = getAuthenticatedMerchantId();
        ensureProvisioned(merchantId);
        if (merchantId.equals(userId)) {
            throw new IllegalArgumentException("cannot_disable_self");
        }
        adminUserMapper.updateStatus(merchantId, userId, status);
        auditService.write(merchantId, "system.user.status", "admin_user", userId, Map.of("status", status));
    }

    public void updateUserRoles(String userId, List<String> roleKeys) {
        requirePermission("system.admin");
        String merchantId = getAuthenticatedMerchantId();
        ensureProvisioned(merchantId);
        applyUserRolesInternal(merchantId, userId, roleKeys == null ? List.of() : roleKeys);
        auditService.write(merchantId, "system.user.roles", "admin_user", userId, Map.of("roleKeys", roleKeys == null ? List.of() : roleKeys));
    }

    public List<RoleDto> listRoles() {
        requirePermission("system.read");
        String merchantId = getAuthenticatedMerchantId();
        ensureProvisioned(merchantId);
        List<Role> roles = roleMapper.listByMerchant(merchantId);
        List<RoleDto> result = new ArrayList<>();
        for (Role r : roles) {
            List<String> keys = rolePermissionMapper.listPermKeysByRole(r.getRoleId());
            result.add(new RoleDto(r.getRoleId(), r.getRoleKey(), r.getRoleName(), r.getBuiltIn(), keys));
        }
        return result;
    }

    public List<Permission> listPermissions() {
        requirePermission("system.read");
        String merchantId = getAuthenticatedMerchantId();
        ensureProvisioned(merchantId);
        return permissionMapper.listAll();
    }

    public void updateRolePermissions(String roleId, List<String> permissionKeys) {
        requirePermission("system.admin");
        String merchantId = getAuthenticatedMerchantId();
        ensureProvisioned(merchantId);

        Role role = roleMapper.findById(merchantId, roleId);
        if (role == null) {
            throw new IllegalArgumentException("role_not_found");
        }

        Set<String> normalized = new LinkedHashSet<>();
        if (permissionKeys != null) {
            for (String k : permissionKeys) {
                if (StringUtils.hasText(k)) {
                    normalized.add(k);
                }
            }
        }
        rolePermissionMapper.deleteByRole(roleId);
        for (String k : normalized) {
            rolePermissionMapper.insert(UUID.randomUUID().toString(), roleId, k);
        }

        auditService.write(merchantId, "system.role.permissions", "role", roleId, Map.of("permissionKeys", new ArrayList<>(normalized)));
    }

    private void ensureProvisioned(String merchantId) {
        if (!StringUtils.hasText(merchantId)) {
            throw new ApiForbiddenException("forbidden");
        }

        for (Map.Entry<String, String> e : defaultPermissions().entrySet()) {
            Permission p = new Permission();
            p.setPermKey(e.getKey());
            p.setPermName(e.getValue());
            permissionMapper.upsert(p);
        }

        AdminUser me = adminUserMapper.findById(merchantId, merchantId);
        if (me == null) {
            AdminUser u = new AdminUser();
            u.setUserId(merchantId);
            u.setMerchantId(merchantId);
            u.setEmail(merchantId + "@merchant.local");
            u.setDisplayName("merchant:" + merchantId);
            u.setStatus(1);
            adminUserMapper.insert(u);
        }

        Role superAdmin = ensureRole(merchantId, "super_admin", "超级管理员", 1);
        Role riskOperator = ensureRole(merchantId, "risk_operator", "风控运营", 1);
        Role auditor = ensureRole(merchantId, "auditor", "审计员（只读）", 1);

        ensureDefaultRolePermissions(superAdmin.getRoleId(), defaultRolePermissions().get("super_admin"));
        ensureDefaultRolePermissions(riskOperator.getRoleId(), defaultRolePermissions().get("risk_operator"));
        ensureDefaultRolePermissions(auditor.getRoleId(), defaultRolePermissions().get("auditor"));

        List<String> existingRoleIds = userRoleMapper.listRoleIdsByUser(merchantId, merchantId);
        if (existingRoleIds.isEmpty()) {
            userRoleMapper.insert(UUID.randomUUID().toString(), merchantId, merchantId, superAdmin.getRoleId());
        }
    }

    private Role ensureRole(String merchantId, String roleKey, String roleName, int builtIn) {
        Role r = roleMapper.findByKey(merchantId, roleKey);
        if (r != null) {
            return r;
        }
        Role created = new Role();
        created.setRoleId(UUID.randomUUID().toString());
        created.setMerchantId(merchantId);
        created.setRoleKey(roleKey);
        created.setRoleName(roleName);
        created.setBuiltIn(builtIn);
        roleMapper.insert(created);
        return roleMapper.findByKey(merchantId, roleKey);
    }

    private void ensureDefaultRolePermissions(String roleId, List<String> defaultPermKeys) {
        List<String> existing = rolePermissionMapper.listPermKeysByRole(roleId);
        if (existing != null && !existing.isEmpty()) {
            return;
        }
        if (defaultPermKeys == null) {
            return;
        }
        for (String k : defaultPermKeys) {
            if (StringUtils.hasText(k)) {
                rolePermissionMapper.insert(UUID.randomUUID().toString(), roleId, k);
            }
        }
    }

    private void applyUserRolesInternal(String merchantId, String userId, List<String> roleKeys) {
        userRoleMapper.deleteByUser(merchantId, userId);

        Set<String> normalized = new LinkedHashSet<>();
        for (String rk : roleKeys) {
            if (StringUtils.hasText(rk)) {
                normalized.add(rk);
            }
        }
        if (normalized.isEmpty()) {
            Role defaultRole = roleMapper.findByKey(merchantId, "auditor");
            if (defaultRole != null) {
                userRoleMapper.insert(UUID.randomUUID().toString(), merchantId, userId, defaultRole.getRoleId());
            }
            return;
        }

        for (String rk : normalized) {
            Role role = roleMapper.findByKey(merchantId, rk);
            if (role != null) {
                userRoleMapper.insert(UUID.randomUUID().toString(), merchantId, userId, role.getRoleId());
            }
        }
    }

    private Map<String, String> defaultPermissions() {
        Map<String, String> m = new LinkedHashMap<>();
        m.put("rules.read", "规则只读");
        m.put("rules.write", "规则编辑");
        m.put("rules.publish", "规则发布");
        m.put("cases.read", "命中事件只读");
        m.put("cases.dispose", "命中事件处置");
        m.put("audit.read", "审计日志查看");
        m.put("system.read", "系统管理只读");
        m.put("system.admin", "系统管理写入");
        m.put("export.csv", "导出");
        return m;
    }

    private Map<String, List<String>> defaultRolePermissions() {
        Map<String, List<String>> m = new LinkedHashMap<>();
        List<String> all = new ArrayList<>(defaultPermissions().keySet());
        m.put("super_admin", all);
        m.put("risk_operator", List.of("rules.read", "rules.write", "rules.publish", "cases.read", "cases.dispose", "audit.read"));
        m.put("auditor", List.of("rules.read", "cases.read", "audit.read", "system.read"));
        return m;
    }

    private String getAuthenticatedMerchantId() {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        if (auth == null || auth.getPrincipal() == null) {
            return null;
        }
        return String.valueOf(auth.getPrincipal());
    }
}

