package com.khmerx.aire.risk.mapper;

import com.khmerx.aire.risk.model.RiskEvent;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;

import java.util.List;

@Mapper
public interface RiskEventMapper {
    @Insert("insert into risk_engine.risk_events(event_id, merchant_id, scenario_type, user_id, order_id, risk_score, risk_level, decision, reason, matched_rule_ids, input_snapshot, status) values(#{eventId}, #{merchantId}, #{scenarioType}, #{userId}, #{orderId}, #{riskScore}, #{riskLevel}, #{decision}, #{reason}, #{matchedRuleIds}, #{inputSnapshot}, #{status})")
    int insert(RiskEvent event);

    @Select("select * from risk_engine.risk_events where event_id = #{eventId}")
    RiskEvent findById(@Param("eventId") String eventId);

    @Update("update risk_engine.risk_events set status = #{status}, updated_at = now() where event_id = #{eventId}")
    int updateStatus(@Param("eventId") String eventId, @Param("status") String status);

    @Select({
            "<script>",
            "select * from risk_engine.risk_events",
            "where merchant_id = #{merchantId}",
            "<if test='scenarioType != null and scenarioType != ""'> and scenario_type = #{scenarioType} </if>",
            "<if test='status != null and status != ""'> and status = #{status} </if>",
            "<if test='fromTs != null and fromTs != ""'> and created_at &gt;= #{fromTs}::timestamp </if>",
            "<if test='toTs != null and toTs != ""'> and created_at &lt;= #{toTs}::timestamp </if>",
            "<if test='keyword != null and keyword != ""'>",
            " and (event_id ilike concat('%', #{keyword}, '%')",
            "   or user_id ilike concat('%', #{keyword}, '%')",
            "   or order_id ilike concat('%', #{keyword}, '%')",
            "   or matched_rule_ids ilike concat('%', #{keyword}, '%'))",
            "</if>",
            "order by created_at desc",
            "limit #{limit} offset #{offset}",
            "</script>"
    })
    List<RiskEvent> list(
            @Param("merchantId") String merchantId,
            @Param("scenarioType") String scenarioType,
            @Param("status") String status,
            @Param("keyword") String keyword,
            @Param("fromTs") String fromTs,
            @Param("toTs") String toTs,
            @Param("limit") int limit,
            @Param("offset") int offset
    );

    @Select({
            "<script>",
            "select count(1) from risk_engine.risk_events",
            "where merchant_id = #{merchantId}",
            "<if test='scenarioType != null and scenarioType != ""'> and scenario_type = #{scenarioType} </if>",
            "<if test='status != null and status != ""'> and status = #{status} </if>",
            "<if test='fromTs != null and fromTs != ""'> and created_at &gt;= #{fromTs}::timestamp </if>",
            "<if test='toTs != null and toTs != ""'> and created_at &lt;= #{toTs}::timestamp </if>",
            "<if test='keyword != null and keyword != ""'>",
            " and (event_id ilike concat('%', #{keyword}, '%')",
            "   or user_id ilike concat('%', #{keyword}, '%')",
            "   or order_id ilike concat('%', #{keyword}, '%')",
            "   or matched_rule_ids ilike concat('%', #{keyword}, '%'))",
            "</if>",
            "</script>"
    })
    long count(
            @Param("merchantId") String merchantId,
            @Param("scenarioType") String scenarioType,
            @Param("status") String status,
            @Param("keyword") String keyword,
            @Param("fromTs") String fromTs,
            @Param("toTs") String toTs
    );
}

