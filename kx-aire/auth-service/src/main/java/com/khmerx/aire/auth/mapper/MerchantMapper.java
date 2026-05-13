package com.khmerx.aire.auth.mapper;

import com.khmerx.aire.auth.model.Merchant;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

@Mapper
public interface MerchantMapper {
    @Select("select merchant_id as merchantId, api_key as apiKey, status, expire_time as expireTime from merchant_center.merchants where merchant_id = #{merchantId}")
    Merchant findByMerchantId(@Param("merchantId") String merchantId);
}

