package com.khmerx.aire.risk.mapper;

import com.khmerx.aire.risk.model.Permission;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface PermissionMapper {
    @Insert("insert into api_center.permissions(perm_key, perm_name) values(#{permKey}, #{permName}) on conflict (perm_key) do nothing")
    int upsert(Permission permission);

    @Select("select * from api_center.permissions order by perm_key asc")
    List<Permission> listAll();
}

