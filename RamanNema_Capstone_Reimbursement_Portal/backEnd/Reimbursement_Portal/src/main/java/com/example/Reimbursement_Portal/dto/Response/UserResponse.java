package com.example.Reimbursement_Portal.dto.Response;

import com.example.Reimbursement_Portal.entity.Role;
import lombok.Builder;
import lombok.Data;

// DTO for response
@Data
@Builder
public class UserResponse {

    private Long id;
    private String name;
    private String email;
    private Role role;
}