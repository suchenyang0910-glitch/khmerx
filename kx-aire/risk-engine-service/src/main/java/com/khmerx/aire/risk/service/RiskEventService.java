package com.khmerx.aire.risk.service;

import com.khmerx.aire.risk.dto.DispositionCreateRequest;
import com.khmerx.aire.risk.dto.PageResponse;
import com.khmerx.aire.risk.dto.RiskEventDetailResponse;
import com.khmerx.aire.risk.mapper.DispositionMapper;
import com.khmerx.aire.risk.mapper.RiskEventMapper;
import com.khmerx.aire.risk.model.Disposition;
import com.khmerx.aire.risk.model.RiskEvent;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

import java.util.List;
import java.util.Map;
import java.util.UUID;

@Service
public class RiskEventService {
    private final RiskEventMapper riskEventMapper;
    private final DispositionMapper dispositionMapper;
    private final AuditService auditService;
    private final RbacService rbacService;

    public RiskEventService(RiskEventMapper riskEventMapper, DispositionMapper dispositionMapper, AuditService auditService, RbacService rbacService) {
        this.riskEventMapper = riskEventMapper;
        this.dispositionMapper = dispositionMapper;
        this.auditService = auditService;
        this.rbacService = rbacService;
    }

    public PageResponse<RiskEvent> list(String scenarioType, String status, String keyword, String fromTs, String toTs, int page, int pageSize) {
        rbacService.requirePermission("cases.read");
        int safePage = Math.max(1, page);
        int safePageSize = Math.min(100, Math.max(1, pageSize));
        int offset = (safePage - 1) * safePageSize;
        String merchantId = getAuthenticatedMerchantId();

        long total = riskEventMapper.count(merchantId, scenarioType, status, keyword, fromTs, toTs);
        List<RiskEvent> items = riskEventMapper.list(merchantId, scenarioType, status, keyword, fromTs, toTs, safePageSize, offset);
        return new PageResponse<>(items, total, safePage, safePageSize);
    }

    public RiskEventDetailResponse getDetail(String eventId) {
        rbacService.requirePermission("cases.read");
        String merchantId = getAuthenticatedMerchantId();
        RiskEvent event = riskEventMapper.findById(eventId);
        if (event == null || !merchantId.equals(event.getMerchantId())) {
            return new RiskEventDetailResponse(null, List.of());
        }
        List<Disposition> dispositions = dispositionMapper.listByEventId(eventId);
        return new RiskEventDetailResponse(event, dispositions);
    }

    public Disposition createDisposition(String eventId, DispositionCreateRequest request) {
        rbacService.requirePermission("cases.dispose");
        String merchantId = getAuthenticatedMerchantId();
        RiskEvent event = riskEventMapper.findById(eventId);
        if (event == null || !merchantId.equals(event.getMerchantId())) {
            return null;
        }

        Disposition d = new Disposition();
        d.setDispositionId(UUID.randomUUID().toString());
        d.setEventId(eventId);
        d.setAction(request.getAction());
        d.setRemark(request.getRemark());
        d.setOperatorId(merchantId);
        dispositionMapper.insert(d);

        String nextStatus = mapNextStatus(request.getAction());
        if (StringUtils.hasText(nextStatus)) {
            riskEventMapper.updateStatus(eventId, nextStatus);
        }

        auditService.write(
                merchantId,
                "case.disposition.create",
                "risk_event",
                eventId,
                Map.of(
                        "action", request.getAction(),
                        "remark", request.getRemark() == null ? "" : request.getRemark(),
                        "nextStatus", nextStatus
                )
        );

        return d;
    }

    private String mapNextStatus(String action) {
        if (!StringUtils.hasText(action)) {
            return null;
        }
        if ("manual_review".equalsIgnoreCase(action)) {
            return "processing";
        }
        return "closed";
    }

    private String getAuthenticatedMerchantId() {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        if (auth == null || auth.getPrincipal() == null) {
            return null;
        }
        return String.valueOf(auth.getPrincipal());
    }
}
