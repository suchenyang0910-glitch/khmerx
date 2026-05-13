package com.khmerx.aire.risk.mapper;

import com.khmerx.aire.risk.model.AdminUser;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;

import java.util.List;

@Mapper
public interface AdminUserMapper {
    @Insert("insert into api_center.admin_users(user_id, merchant_id, email, display_name, status) values(#{userId}, #{merchantId}, #{email}, #{displayName}, #{status})")
    int insert(AdminUser user);

    @Select("select * from api_center.admin_users where merchant_id = #{merchantId} and user_id = #{userId}")
    AdminUser findById(@Param("merchantId") String merchantId, @Param("userId") String userId);

    @Select("select * from api_center.admin_users where merchant_id = #{merchantId} and email = #{email}")
    AdminUser findByEmail(@Param("merchantId") String merchantId, @Param("email") String email);

    @Update("update api_center.admin_users set status = #{status} where merchant_id = #{merchantId} and user_id = #{userId}")
    int updateStatus(@Param("merchantId") String merchantId, @Param("userId") String userId, @Param("status") int status);

    @Select({
            "<script>",
            "select * from api_center.admin_users",
            "where merchant_id = #{merchantId}",
            "<if test='keyword != null and keyword != ""'>",
            " and (email ilike concat('%', #{keyword}, '%')",
            "   or display_name ilike concat('%', #{keyword}, '%')",
            "   or user_id ilike concat('%', #{keyword}, '%'))",
            "</if>",
            "order by created_at desc",
            "limit #{limit} offset #{offset}",
            "</script>"
    })
    List<AdminUser> list(
            @Param("merchantId") String merchantId,
            @Param("keyword") String keyword,
            @Param("limit") int limit,
            @Param("offset") int offset
    );

    @Select({
            "<script>",
            "select count(1) from api_center.admin_users",
            "where merchant_id = #{merchantId}",
            "<if test='keyword != null and keyword != ""'>",
            " and (email ilike concat('%', #{keyword}, '%')",
            "   or display_name ilike concat('%', #{keyword}, '%')",
            "   or user_id ilike concat('%', #{keyword}, '%'))",
            "</if>",
            "</script>"
    })
    long count(@Param("merchantId") String merchantId, @Param("keyword") String keyword);
}

