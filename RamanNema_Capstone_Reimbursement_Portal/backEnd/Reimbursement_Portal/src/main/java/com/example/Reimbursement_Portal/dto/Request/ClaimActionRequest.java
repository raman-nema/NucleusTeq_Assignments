package com.example.Reimbursement_Portal.dto.Request;

import com.example.Reimbursement_Portal.entity.ClaimStatus;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.Data;

// DTO for approve/reject action
@Data
public class ClaimActionRequest {

    @NotNull(message = "Status is required")
    private ClaimStatus status;

    @Size(max = 500, message = "Comment must not exceed 500 characters")
    private String comment;
}