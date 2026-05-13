package com.khmerx.aire.risk.mapper;

import com.khmerx.aire.risk.model.RiskOrder;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface RiskOrderMapper {
    @Insert("insert into risk_engine.risk_orders(order_id, merchant_id, user_id, scenario_type, apply_amount, risk_score, risk_level, approve_status) values(#{orderId}, #{merchantId}, #{userId}, #{scenarioType}, #{applyAmount}, #{riskScore}, #{riskLevel}, #{approveStatus})")
    int insert(RiskOrder order);
}

