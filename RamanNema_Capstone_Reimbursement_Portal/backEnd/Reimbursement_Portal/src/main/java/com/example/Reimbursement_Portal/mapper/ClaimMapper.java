package com.example.Reimbursement_Portal.mapper;

import com.example.Reimbursement_Portal.dto.Request.ClaimRequestDTO;
import com.example.Reimbursement_Portal.dto.Response.ClaimResponseDTO;
import com.example.Reimbursement_Portal.entity.Claim;
import com.example.Reimbursement_Portal.entity.User;
import com.example.Reimbursement_Portal.enums.ClaimStatus;

import java.time.LocalDate;

/**
 * Mapper for Claim entity.
 */
public class ClaimMapper {

    /**
     * Converts Claim entity to ClaimResponseDTO.
     *
     * @param claim the claim entity
     * @return the claim response DTO
     */
    public static ClaimResponseDTO toResponse(Claim claim) {

        return ClaimResponseDTO.builder()
                .id(claim.getId())
                .amount(claim.getAmount())
                .description(claim.getDescription())
                .date(claim.getDate())
                .status(claim.getStatus())
                .employeeId(claim.getEmployee() != null ? claim.getEmployee().getId() : null)
                .employeeName(claim.getEmployee() != null ? claim.getEmployee().getName() : null)
                .reviewerId(claim.getReviewer() != null ? claim.getReviewer().getId() : null)
                .reviewerName(claim.getReviewer() != null ? claim.getReviewer().getName() : null)
                .comment(claim.getComment())
                .build();
    }

    /**
     * Converts ClaimRequestDTO to Claim entity.
     *
     * @param request the claim request
     * @param employee the employee
     * @param reviewer the reviewer
     * @return the claim entity
     */
    public static Claim toEntity(ClaimRequestDTO request, User employee, User reviewer) {

        Claim claim = new Claim();
        claim.setAmount(request.getAmount());
        claim.setDescription(request.getDescription());
        claim.setDate(LocalDate.now());
        claim.setStatus(ClaimStatus.SUBMITTED);
        claim.setEmployee(employee);
        claim.setReviewer(reviewer);

        return claim;
    }
}