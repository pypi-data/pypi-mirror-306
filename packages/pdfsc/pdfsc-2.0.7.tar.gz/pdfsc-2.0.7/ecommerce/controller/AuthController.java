package com.kiatkoding.ecommerce.controller;

import com.kiatkoding.ecommerce.model.request.LoginRequest;
import com.kiatkoding.ecommerce.model.request.RegisterRequest;
import com.kiatkoding.ecommerce.model.response.BaseResponse;
import com.kiatkoding.ecommerce.service.AuthService;
import com.kiatkoding.ecommerce.service.UserService;
import lombok.AllArgsConstructor;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/auth")
@AllArgsConstructor
public class AuthController {

    private final AuthService authService;

    @PostMapping("/register")
    public BaseResponse postRegister(
            @RequestBody RegisterRequest registerRequest
    ) {
        Boolean result = authService.register(registerRequest);
        return new BaseResponse(result, "Success", result);
    }

    @PostMapping("/login")
    public BaseResponse postLogin(
            @RequestBody LoginRequest loginRequest
    ) {
        String token = authService.login(loginRequest);
        return new BaseResponse(true, "Success", token);
    }
}
