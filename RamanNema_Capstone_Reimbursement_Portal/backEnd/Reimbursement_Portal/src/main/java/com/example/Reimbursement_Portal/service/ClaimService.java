package com.example.Reimbursement_Portal.service;

import com.example.Reimbursement_Portal.dto.Request.ClaimActionRequest;
import com.example.Reimbursement_Portal.dto.Request.ClaimRequest;
import com.example.Reimbursement_Portal.dto.Response.ClaimResponse;
import com.example.Reimbursement_Portal.entity.ClaimStatus;

import java.util.List;

// Claim service operations
public interface ClaimService {

    // Submit claim //
    ClaimResponse submitClaim(ClaimRequest request);

    //  Get all claims //
    List<ClaimResponse> getAllClaims();

    //  Get claims by employee //
    List<ClaimResponse> getClaimsByEmployee(Long employeeId);

    // Get claims by reviewer //
    List<ClaimResponse> getClaimsByReviewer(Long reviewerId);

    //  Get claims by status //
    List<ClaimResponse> getClaimsByStatus(ClaimStatus status);

    // Take action on claim //
    ClaimResponse takeAction(Long claimId, Long reviewerId, ClaimActionRequest request);
}