package com.khmerx.aire.risk.mapper;

import com.khmerx.aire.risk.model.AuditLog;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface AuditLogMapper {
    @Insert("insert into api_center.audit_logs(log_id, actor_id, action, object_type, object_id, diff_json, ip, user_agent) values(#{logId}, #{actorId}, #{action}, #{objectType}, #{objectId}, #{diffJson}, #{ip}, #{userAgent})")
    int insert(AuditLog log);

    @Select({
            "<script>",
            "select * from api_center.audit_logs",
            "where 1=1",
            "<if test='actorId != null and actorId != ""'> and actor_id = #{actorId} </if>",
            "<if test='action != null and action != ""'> and action ilike concat('%', #{action}, '%') </if>",
            "<if test='objectType != null and objectType != ""'> and object_type = #{objectType} </if>",
            "<if test='objectId != null and objectId != ""'> and object_id ilike concat('%', #{objectId}, '%') </if>",
            "order by created_at desc",
            "limit #{limit} offset #{offset}",
            "</script>"
    })
    List<AuditLog> list(
            @Param("actorId") String actorId,
            @Param("action") String action,
            @Param("objectType") String objectType,
            @Param("objectId") String objectId,
            @Param("limit") int limit,
            @Param("offset") int offset
    );

    @Select({
            "<script>",
            "select count(1) from api_center.audit_logs",
            "where 1=1",
            "<if test='actorId != null and actorId != ""'> and actor_id = #{actorId} </if>",
            "<if test='action != null and action != ""'> and action ilike concat('%', #{action}, '%') </if>",
            "<if test='objectType != null and objectType != ""'> and object_type = #{objectType} </if>",
            "<if test='objectId != null and objectId != ""'> and object_id ilike concat('%', #{objectId}, '%') </if>",
            "</script>"
    })
    long count(
            @Param("actorId") String actorId,
            @Param("action") String action,
            @Param("objectType") String objectType,
            @Param("objectId") String objectId
    );
}

