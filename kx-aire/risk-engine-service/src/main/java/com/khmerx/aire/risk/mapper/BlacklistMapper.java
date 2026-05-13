package com.khmerx.aire.risk.mapper;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

@Mapper
public interface BlacklistMapper {
    @Select("select count(1) from blacklist_center.blacklist_subjects where subject_type = #{subjectType} and subject_id = #{subjectId}")
    int countHit(@Param("subjectType") String subjectType, @Param("subjectId") String subjectId);
}

