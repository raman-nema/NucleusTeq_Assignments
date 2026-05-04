package com.example.Reimbursement_Portal.service;

import com.example.Reimbursement_Portal.dto.Request.ClaimActionRequestDTO;
import com.example.Reimbursement_Portal.dto.Request.ClaimRequestDTO;
import com.example.Reimbursement_Portal.dto.Response.ClaimResponseDTO;
import com.example.Reimbursement_Portal.enums.ClaimStatus;

import java.util.List;

/**
 * Service interface for claim operations.
 */
public interface ClaimService {

    /**
     * Submits a new claim.
     *
     * @param request the claim request
     * @return the created claim
     */
    ClaimResponseDTO submitClaim(ClaimRequestDTO request);

    /**
     * Retrieves all claims.
     *
     * @return list of claims
     */
    List<ClaimResponseDTO> getAllClaims();

    /**
     * Retrieves claims by employee ID.
     *
     * @param employeeId the employee ID
     * @return list of claims
     */
    List<ClaimResponseDTO> getClaimsByEmployee(Long employeeId);

    /**
     * Retrieves claims by reviewer ID.
     *
     * @param reviewerId the reviewer ID
     * @return list of claims
     */
    List<ClaimResponseDTO> getClaimsByReviewer(Long reviewerId);

    /**
     * Retrieves claims by status.
     *
     * @param status the claim status
     * @return list of claims
     */
    List<ClaimResponseDTO> getClaimsByStatus(ClaimStatus status);

    /**
     * Takes action on a claim.
     *
     * @param claimId the claim ID
     * @param reviewerId the reviewer ID
     * @param request the action request
     * @return the updated claim
     */
    ClaimResponseDTO takeAction(Long claimId, Long reviewerId, ClaimActionRequestDTO request);
}