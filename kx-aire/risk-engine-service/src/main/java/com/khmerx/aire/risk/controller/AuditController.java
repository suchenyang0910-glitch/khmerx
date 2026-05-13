package com.khmerx.aire.risk.controller;

import com.khmerx.aire.risk.dto.PageResponse;
import com.khmerx.aire.risk.mapper.AuditLogMapper;
import com.khmerx.aire.risk.model.AuditLog;
import com.khmerx.aire.risk.service.RbacService;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@Validated
@RestController
@RequestMapping("/system/audit")
public class AuditController {
    private final AuditLogMapper auditLogMapper;
    private final RbacService rbacService;

    public AuditController(AuditLogMapper auditLogMapper, RbacService rbacService) {
        this.auditLogMapper = auditLogMapper;
        this.rbacService = rbacService;
    }

    @GetMapping
    public PageResponse<AuditLog> list(
            @RequestParam(value = "actorId", required = false) String actorId,
            @RequestParam(value = "action", required = false) String action,
            @RequestParam(value = "objectType", required = false) String objectType,
            @RequestParam(value = "objectId", required = false) String objectId,
            @RequestParam(value = "page", defaultValue = "1") @Min(1) int page,
            @RequestParam(value = "pageSize", defaultValue = "20") @Min(1) @Max(100) int pageSize
    ) {
        rbacService.requirePermission("audit.read");
        int safePage = Math.max(1, page);
        int safePageSize = Math.min(100, Math.max(1, pageSize));
        int offset = (safePage - 1) * safePageSize;

        long total = auditLogMapper.count(actorId, action, objectType, objectId);
        List<AuditLog> items = auditLogMapper.list(actorId, action, objectType, objectId, safePageSize, offset);
        return new PageResponse<>(items, total, safePage, safePageSize);
    }
}
