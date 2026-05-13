package com.khmerx.aire.risk.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.khmerx.aire.risk.mapper.AuditLogMapper;
import com.khmerx.aire.risk.model.AuditLog;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

import jakarta.servlet.http.HttpServletRequest;
import java.util.Map;
import java.util.UUID;

@Service
public class AuditService {
    private final AuditLogMapper auditLogMapper;
    private final ObjectMapper objectMapper;
    private final HttpServletRequest httpServletRequest;

    public AuditService(AuditLogMapper auditLogMapper, ObjectMapper objectMapper, HttpServletRequest httpServletRequest) {
        this.auditLogMapper = auditLogMapper;
        this.objectMapper = objectMapper;
        this.httpServletRequest = httpServletRequest;
    }

    public void write(String actorId, String action, String objectType, String objectId, Map<String, Object> diff) {
        try {
            AuditLog log = new AuditLog();
            log.setLogId(UUID.randomUUID().toString());
            log.setActorId(actorId);
            log.setAction(action);
            log.setObjectType(objectType);
            log.setObjectId(objectId);
            log.setDiffJson(objectMapper.writeValueAsString(diff));

            String ip = httpServletRequest.getHeader("x-forwarded-for");
            if (!StringUtils.hasText(ip)) {
                ip = httpServletRequest.getRemoteAddr();
            }
            log.setIp(ip);
            log.setUserAgent(httpServletRequest.getHeader("user-agent"));

            auditLogMapper.insert(log);
        } catch (Exception ignored) {
        }
    }
}

