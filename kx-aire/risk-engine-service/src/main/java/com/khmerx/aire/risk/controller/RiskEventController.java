package com.khmerx.aire.risk.controller;

import com.khmerx.aire.risk.dto.DispositionCreateRequest;
import com.khmerx.aire.risk.dto.PageResponse;
import com.khmerx.aire.risk.dto.RiskEventDetailResponse;
import com.khmerx.aire.risk.model.Disposition;
import com.khmerx.aire.risk.model.RiskEvent;
import com.khmerx.aire.risk.service.RiskEventService;
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

import java.util.Map;

@Validated
@RestController
@RequestMapping("/risk/events")
public class RiskEventController {
    private final RiskEventService riskEventService;

    public RiskEventController(RiskEventService riskEventService) {
        this.riskEventService = riskEventService;
    }

    @GetMapping
    public PageResponse<RiskEvent> list(
            @RequestParam(value = "scenarioType", required = false) String scenarioType,
            @RequestParam(value = "status", required = false) String status,
            @RequestParam(value = "keyword", required = false) String keyword,
            @RequestParam(value = "from", required = false) String from,
            @RequestParam(value = "to", required = false) String to,
            @RequestParam(value = "page", defaultValue = "1") @Min(1) int page,
            @RequestParam(value = "pageSize", defaultValue = "20") @Min(1) @Max(100) int pageSize
    ) {
        return riskEventService.list(scenarioType, status, keyword, from, to, page, pageSize);
    }

    @GetMapping("/{eventId}")
    public RiskEventDetailResponse detail(@PathVariable("eventId") String eventId) {
        return riskEventService.getDetail(eventId);
    }

    @PostMapping("/{eventId}/dispositions")
    public Map<String, Object> createDisposition(
            @PathVariable("eventId") String eventId,
            @Valid @RequestBody DispositionCreateRequest request
    ) {
        Disposition d = riskEventService.createDisposition(eventId, request);
        if (d == null) {
            return Map.of("ok", false);
        }
        return Map.of("ok", true, "dispositionId", d.getDispositionId());
    }
}

