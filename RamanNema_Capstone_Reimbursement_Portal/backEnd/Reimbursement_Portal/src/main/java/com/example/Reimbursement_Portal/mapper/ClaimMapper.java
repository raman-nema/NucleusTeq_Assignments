package com.example.Reimbursement_Portal.mapper;

import com.example.Reimbursement_Portal.dto.Response.ClaimResponse;
import com.example.Reimbursement_Portal.entity.Claim;

// Mapper class to convert Claim entity to ClaimResponse DTO
public class ClaimMapper {

    // Convert Claim entity to response DTO
    public static ClaimResponse toResponse(Claim claim) {

        // Build response object from entity fields
        return ClaimResponse.builder()
                .id(claim.getId()) // Set claim ID
                .amount(claim.getAmount()) // Set claim amount
                .description(claim.getDescription()) // Set description
                .date(claim.getDate()) // Set claim date
                .status(claim.getStatus()) // Set claim status

                // Map employee details safely
                .employeeId(claim.getEmployee() != null ? claim.getEmployee().getId() : null)
                .employeeName(claim.getEmployee() != null ? claim.getEmployee().getName() : null)

                // Map reviewer details safely
                .reviewerId(claim.getReviewer() != null ? claim.getReviewer().getId() : null)
                .reviewerName(claim.getReviewer() != null ? claim.getReviewer().getName() : null)

                .comment(claim.getComment()) // Set reviewer comment

                .build(); // Build and return response
    }
}