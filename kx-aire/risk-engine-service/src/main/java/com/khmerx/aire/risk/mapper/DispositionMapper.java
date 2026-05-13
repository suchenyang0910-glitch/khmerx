package com.khmerx.aire.risk.mapper;

import com.khmerx.aire.risk.model.Disposition;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface DispositionMapper {
    @Insert("insert into risk_engine.dispositions(disposition_id, event_id, action, remark, operator_id) values(#{dispositionId}, #{eventId}, #{action}, #{remark}, #{operatorId})")
    int insert(Disposition disposition);

    @Select("select * from risk_engine.dispositions where event_id = #{eventId} order by created_at asc")
    List<Disposition> listByEventId(@Param("eventId") String eventId);
}

