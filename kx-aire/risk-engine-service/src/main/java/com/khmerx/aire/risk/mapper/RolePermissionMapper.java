package com.khmerx.aire.risk.mapper;

import org.apache.ibatis.annotations.Delete;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface RolePermissionMapper {
    @Insert("insert into api_center.role_permissions(id, role_id, perm_key) values(#{id}, #{roleId}, #{permKey})")
    int insert(@Param("id") String id, @Param("roleId") String roleId, @Param("permKey") String permKey);

    @Delete("delete from api_center.role_permissions where role_id = #{roleId}")
    int deleteByRole(@Param("roleId") String roleId);

    @Select("select perm_key from api_center.role_permissions where role_id = #{roleId} order by perm_key asc")
    List<String> listPermKeysByRole(@Param("roleId") String roleId);

    @Select({
            "<script>",
            "select distinct perm_key from api_center.role_permissions",
            "where role_id in",
            "<foreach collection='roleIds' item='id' open='(' separator=',' close=')'>#{id}</foreach>",
            "</script>"
    })
    List<String> listPermKeysByRoleIds(@Param("roleIds") List<String> roleIds);
}
