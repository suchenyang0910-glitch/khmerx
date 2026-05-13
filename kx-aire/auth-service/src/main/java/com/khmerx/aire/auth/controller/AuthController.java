package com.khmerx.aire.auth.controller;

import com.khmerx.aire.auth.dto.TokenRequest;
import com.khmerx.aire.auth.dto.TokenResponse;
import com.khmerx.aire.auth.service.AuthService;
import jakarta.validation.Valid;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.Instant;
import java.util.LinkedHashMap;
import java.util.Map;

@RestController
@RequestMapping("/auth")
public class AuthController {
    private final AuthService authService;

    public AuthController(AuthService authService) {
        this.authService = authService;
    }

    @PostMapping("/token")
    public TokenResponse token(@Valid @RequestBody TokenRequest request) {
        return authService.issueToken(request);
    }

    @GetMapping("/me")
    public Map<String, Object> me(Authentication authentication) {
        Map<String, Object> result = new LinkedHashMap<>();
        result.put("subject", authentication.getName());
        result.put("authorities", authentication.getAuthorities());
        result.put("issuedAt", Instant.now().toString());
        return result;
    }
}

