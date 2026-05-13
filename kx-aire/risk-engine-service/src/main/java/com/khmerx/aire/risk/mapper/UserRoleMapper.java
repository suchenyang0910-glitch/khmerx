package com.khmerx.aire.risk.mapper;

import org.apache.ibatis.annotations.Delete;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface UserRoleMapper {
    @Insert("insert into api_center.user_roles(id, merchant_id, user_id, role_id) values(#{id}, #{merchantId}, #{userId}, #{roleId})")
    int insert(@Param("id") String id, @Param("merchantId") String merchantId, @Param("userId") String userId, @Param("roleId") String roleId);

    @Delete("delete from api_center.user_roles where merchant_id = #{merchantId} and user_id = #{userId}")
    int deleteByUser(@Param("merchantId") String merchantId, @Param("userId") String userId);

    @Select("select r.role_key from api_center.user_roles ur join api_center.roles r on ur.role_id = r.role_id where ur.merchant_id = #{merchantId} and ur.user_id = #{userId}")
    List<String> listRoleKeysByUser(@Param("merchantId") String merchantId, @Param("userId") String userId);

    @Select("select r.role_id from api_center.user_roles ur join api_center.roles r on ur.role_id = r.role_id where ur.merchant_id = #{merchantId} and ur.user_id = #{userId}")
    List<String> listRoleIdsByUser(@Param("merchantId") String merchantId, @Param("userId") String userId);
}

