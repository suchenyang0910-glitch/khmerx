package com.khmerx.aire.risk.mapper;

import com.khmerx.aire.risk.model.RiskRule;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface RiskRuleMapper {
    @Select("select rule_id as ruleId, rule_name as ruleName, scenario_type as scenarioType, rule_expression as ruleExpression, score_weight as scoreWeight, risk_action as riskAction, status from risk_engine.risk_rules where status = 1 and scenario_type = #{scenarioType}")
    List<RiskRule> findEnabledByScenario(@Param("scenarioType") String scenarioType);
}

