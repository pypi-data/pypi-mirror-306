package com.kiatkoding.ecommerce.controller;

import com.kiatkoding.ecommerce.model.response.BaseResponse;
import com.kiatkoding.ecommerce.model.response.Pong;
import lombok.AllArgsConstructor;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/ping")
@AllArgsConstructor
public class PingController {

    private final JdbcTemplate jdbcTemplate;

    @GetMapping
    public BaseResponse ping() {
        BaseResponse response = new BaseResponse();

        try {

            jdbcTemplate.execute("SELECT 1");
            Pong pong = new Pong();

            pong.setMessage("Success");
            pong.setDatabaseConnection(true);

            response.setStatus(true);
            response.setMessage("Database connection success");
            response.setData(pong);

        } catch (Exception e) {
            Pong pong = new Pong();

            pong.setMessage("Failed");
            pong.setErrorMessage(e.getLocalizedMessage());
            pong.setDatabaseConnection(false);

            response.setStatus(false);
            response.setMessage("Database connection failed");
            response.setData(pong);
        }


        return response;
    }
}
