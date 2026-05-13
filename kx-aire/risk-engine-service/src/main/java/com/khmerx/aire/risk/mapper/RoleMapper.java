package com.khmerx.aire.risk.mapper;

import com.khmerx.aire.risk.model.Role;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface RoleMapper {
    @Insert("insert into api_center.roles(role_id, merchant_id, role_key, role_name, built_in) values(#{roleId}, #{merchantId}, #{roleKey}, #{roleName}, #{builtIn})")
    int insert(Role role);

    @Select("select * from api_center.roles where merchant_id = #{merchantId} and role_key = #{roleKey} limit 1")
    Role findByKey(@Param("merchantId") String merchantId, @Param("roleKey") String roleKey);

    @Select("select * from api_center.roles where merchant_id = #{merchantId} order by created_at asc")
    List<Role> listByMerchant(@Param("merchantId") String merchantId);

    @Select("select * from api_center.roles where merchant_id = #{merchantId} and role_id = #{roleId} limit 1")
    Role findById(@Param("merchantId") String merchantId, @Param("roleId") String roleId);
}

