package com.kiatkoding.ecommerce.model.response;

import lombok.*;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class BaseResponse {

    public Boolean status;
    public String message;
    public Object data;
}
