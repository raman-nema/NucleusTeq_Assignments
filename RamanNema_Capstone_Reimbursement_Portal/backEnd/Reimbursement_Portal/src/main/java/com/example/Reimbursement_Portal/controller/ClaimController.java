package com.example.Reimbursement_Portal.controller;

import com.example.Reimbursement_Portal.dto.Request.ClaimActionRequestDTO;
import com.example.Reimbursement_Portal.dto.Request.ClaimRequestDTO;
import com.example.Reimbursement_Portal.dto.Response.ClaimResponseDTO;
import com.example.Reimbursement_Portal.enums.ClaimStatus;
import com.example.Reimbursement_Portal.service.ClaimService;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * Controller for managing reimbursement claims.
 */
@RestController
@RequestMapping("/api/claims")
@RequiredArgsConstructor
public class ClaimController {

    private final ClaimService claimService;

    /**
     * Submits a new claim.
     *
     * @param request the claim request data
     * @return the created claim response
     */
    @PostMapping
    public ClaimResponseDTO submitClaim(@Valid @RequestBody ClaimRequestDTO request) {
        return claimService.submitClaim(request);
    }

    /**
     * Retrieves all claims.
     *
     * @return list of all claims
     */
    @GetMapping
    public List<ClaimResponseDTO> getAllClaims() {
        return claimService.getAllClaims();
    }

    /**
     * Retrieves claims by employee ID.
     *
     * @param id the employee ID
     * @return list of claims for the employee
     */
    @GetMapping("/employee/{id}")
    public List<ClaimResponseDTO> getClaimsByEmployee(@PathVariable Long id) {
        return claimService.getClaimsByEmployee(id);
    }

    /**
     * Retrieves claims by reviewer ID.
     *
     * @param id the reviewer ID
     * @return list of claims assigned to the reviewer
     */
    @GetMapping("/reviewer/{id}")
    public List<ClaimResponseDTO> getClaimsByReviewer(@PathVariable Long id) {
        return claimService.getClaimsByReviewer(id);
    }

    /**
     * Retrieves claims by status.
     *
     * @param status the claim status
     * @return list of claims with the given status
     */
    @GetMapping("/status/{status}")
    public List<ClaimResponseDTO> getClaimsByStatus(@PathVariable ClaimStatus status) {
        return claimService.getClaimsByStatus(status);
    }

    /**
     * Approves or rejects a claim.
     *
     * @param claimId the claim ID
     * @param reviewerId the reviewer ID
     * @param request the action request data
     * @return the updated claim response
     */
    @PutMapping("/{claimId}/action")
    public ClaimResponseDTO takeAction(
            @PathVariable Long claimId,
            @RequestParam Long reviewerId,
            @Valid @RequestBody ClaimActionRequestDTO request) {

        return claimService.takeAction(claimId, reviewerId, request);
    }
}