package com.kiatkoding.ecommerce.service;

import com.kiatkoding.ecommerce.component.JwtUtils;
import com.kiatkoding.ecommerce.model.entity.UserEntity;
import com.kiatkoding.ecommerce.model.request.LoginRequest;
import com.kiatkoding.ecommerce.model.request.RegisterRequest;
import com.kiatkoding.ecommerce.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.Optional;


@Service
@RequiredArgsConstructor
public class AuthService {

    private final UserRepository userRepository;
    private final BCryptPasswordEncoder bCryptPasswordEncoder;
    private final AuthenticationManager authenticationManager;
    private final JwtUtils jwtUtils;

    public Boolean register(RegisterRequest registerRequest) {
        Optional<UserEntity> userEntity = userRepository.findByPhoneNumber(registerRequest.getPhoneNumber());

        if (userEntity.isPresent()) {
            // save
            return false;
        } else {
            // existing
            try {
                UserEntity newUserEntity = new UserEntity();
                newUserEntity.name = registerRequest.getName();
                newUserEntity.password = bCryptPasswordEncoder.encode(registerRequest.getPassword());
                newUserEntity.phoneNumber = registerRequest.getPhoneNumber();

                userRepository.save(newUserEntity);
                return true;
            } catch (Exception e) {
                return false;
            }
        }
    }

    public String login(LoginRequest loginRequest) {
        UsernamePasswordAuthenticationToken authenticationToken = new UsernamePasswordAuthenticationToken(
                loginRequest.getPhoneNumber(), loginRequest.getPassword()
        );

        authenticationManager.authenticate(authenticationToken);

        UserEntity userEntity = userRepository.findByPhoneNumber(loginRequest.getPhoneNumber())
                .orElseThrow();

        return jwtUtils.generateToken(userEntity);
    }
}
