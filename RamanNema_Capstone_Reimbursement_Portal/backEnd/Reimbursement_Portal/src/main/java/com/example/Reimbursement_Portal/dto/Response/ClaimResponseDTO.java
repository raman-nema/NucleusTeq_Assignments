package com.example.Reimbursement_Portal.dto.Response;

import com.example.Reimbursement_Portal.enums.ClaimStatus;
import lombok.Builder;
import lombok.Data;

import java.time.LocalDate;

/**
 * Response DTO for claim details.
 */
@Data
@Builder
public class ClaimResponseDTO {

    private Long id;
    private Double amount;
    private String description;
    private LocalDate date;
    private ClaimStatus status;

    private Long employeeId;
    private String employeeName;

    private Long reviewerId;
    private String reviewerName;

    private String comment;
}