package com.khmerx.aire.risk.dto;

import com.khmerx.aire.risk.model.Disposition;
import com.khmerx.aire.risk.model.RiskEvent;

import java.util.List;

public class RiskEventDetailResponse {
    private RiskEvent event;
    private List<Disposition> dispositions;

    public RiskEventDetailResponse(RiskEvent event, List<Disposition> dispositions) {
        this.event = event;
        this.dispositions = dispositions;
    }

    public RiskEvent getEvent() {
        return event;
    }

    public List<Disposition> getDispositions() {
        return dispositions;
    }
}

