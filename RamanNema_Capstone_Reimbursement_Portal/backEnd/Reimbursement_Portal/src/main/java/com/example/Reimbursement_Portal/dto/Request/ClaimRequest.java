package com.example.Reimbursement_Portal.dto.Request;

import jakarta.validation.constraints.*;
import lombok.Data;

// DTO for claim submission request
@Data
public class ClaimRequest {

    // Amount must be present and positive
    @NotNull(message = "Amount is required")
    @Positive(message = "Amount must be greater than 0")
    private Double amount;

    // Description should not be empty
    @NotBlank(message = "Description is required")
    @Size(max = 255, message = "Description must not exceed 255 characters")
    private String description;

    // Employee ID must be valid
    @NotNull(message = "Employee ID is required")
    @Positive(message = "Employee ID must be a positive number")
    private Long employeeId;
}