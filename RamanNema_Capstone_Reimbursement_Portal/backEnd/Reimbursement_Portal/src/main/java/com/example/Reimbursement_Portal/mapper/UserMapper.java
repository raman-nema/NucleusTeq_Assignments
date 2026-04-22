package com.example.Reimbursement_Portal.mapper;

import com.example.Reimbursement_Portal.dto.Response.UserResponse;
import com.example.Reimbursement_Portal.entity.User;

// Mapper class for converting Entity ↔ DTO
public class UserMapper {

    // Convert User entity to UserResponse DTO
    public static UserResponse toResponse(User user) {
        return UserResponse.builder()
                .id(user.getId())
                .name(user.getName())
                .email(user.getEmail())
                .role(user.getRole())
                .build();
    }
}