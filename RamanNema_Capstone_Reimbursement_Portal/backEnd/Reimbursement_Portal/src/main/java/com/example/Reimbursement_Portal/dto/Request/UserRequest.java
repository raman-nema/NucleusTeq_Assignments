package com.example.Reimbursement_Portal.dto.Request;

import com.example.Reimbursement_Portal.entity.Role;
import lombok.Data;
import jakarta.validation.constraints.*;

// DTO for incoming request
@Data
public class UserRequest {

    @NotBlank(message = "Name is required")
    @Size(min = 2, max = 30, message = "Name must be between 2 and 30 characters")
    private String name;

    @Email(message = "Invalid email format")
    @NotBlank(message = "Email is required")
    @Size(max = 30, message = "Email must not exceed 30 characters")
    private String email;

    @NotBlank(message = "Password is required")
    @Size(min = 6, message = "Password must be at least 6 characters")
    private String password;

    @NotNull(message = "Role is required")
    private Role role;

    // Required only when role = EMPLOYEE
    @Positive(message = "Manager ID must be a positive number")
    private Long managerId;
}
