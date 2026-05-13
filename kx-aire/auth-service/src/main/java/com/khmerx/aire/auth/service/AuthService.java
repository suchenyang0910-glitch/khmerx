package com.khmerx.aire.auth.service;

import com.khmerx.aire.auth.config.JwtProperties;
import com.khmerx.aire.auth.dto.TokenRequest;
import com.khmerx.aire.auth.dto.TokenResponse;
import com.khmerx.aire.auth.mapper.MerchantMapper;
import com.khmerx.aire.auth.model.Merchant;
import com.khmerx.aire.auth.security.JwtService;
import org.springframework.stereotype.Service;

import java.nio.charset.StandardCharsets;
import java.time.Instant;

@Service
public class AuthService {
    private final MerchantMapper merchantMapper;
    private final JwtService jwtService;
    private final JwtProperties jwtProperties;

    public AuthService(MerchantMapper merchantMapper, JwtService jwtService, JwtProperties jwtProperties) {
        this.merchantMapper = merchantMapper;
        this.jwtService = jwtService;
        this.jwtProperties = jwtProperties;
    }

    public TokenResponse issueToken(TokenRequest request) {
        Merchant merchant = merchantMapper.findByMerchantId(request.getMerchantId());
        if (merchant == null) {
            throw new UnauthorizedException("invalid_credentials");
        }
        if (merchant.getStatus() != null && merchant.getStatus() == 0) {
            throw new UnauthorizedException("merchant_disabled");
        }
        if (merchant.getExpireTime() != null && merchant.getExpireTime().isBefore(Instant.now())) {
            throw new UnauthorizedException("merchant_expired");
        }
        if (!secureEquals(merchant.getApiKey(), request.getApiKey())) {
            throw new UnauthorizedException("invalid_credentials");
        }

        String token = jwtService.createToken(merchant.getMerchantId());
        return new TokenResponse(token, "Bearer", jwtProperties.getExpiration());
    }

    private boolean secureEquals(String a, String b) {
        if (a == null || b == null) {
            return false;
        }
        byte[] ba = a.getBytes(StandardCharsets.UTF_8);
        byte[] bb = b.getBytes(StandardCharsets.UTF_8);
        if (ba.length != bb.length) {
            return false;
        }
        int result = 0;
        for (int i = 0; i < ba.length; i++) {
            result |= ba[i] ^ bb[i];
        }
        return result == 0;
    }
}

