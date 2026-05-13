package com.khmerx.aire.risk.mapper;

import com.khmerx.aire.risk.model.ApiLog;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface ApiLogMapper {
    @Insert("insert into api_center.api_logs(log_id, merchant_id, api_name, request_body, response_body, response_time) values(#{logId}, #{merchantId}, #{apiName}, #{requestBody}, #{responseBody}, #{responseTime})")
    int insert(ApiLog log);
}

