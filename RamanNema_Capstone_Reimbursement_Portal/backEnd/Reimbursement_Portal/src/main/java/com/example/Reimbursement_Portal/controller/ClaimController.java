package com.example.Reimbursement_Portal.controller;

import com.example.Reimbursement_Portal.dto.Request.ClaimActionRequest;
import com.example.Reimbursement_Portal.dto.Request.ClaimRequest;
import com.example.Reimbursement_Portal.dto.Response.ClaimResponse;
import com.example.Reimbursement_Portal.entity.ClaimStatus;
import com.example.Reimbursement_Portal.service.ClaimService;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

// REST controller for claim operations
@RestController
@RequestMapping("/api/claims")
@RequiredArgsConstructor
public class ClaimController {

    // Service layer dependency
    private final ClaimService claimService;

    // Submit a new claim
    @PostMapping
    public ClaimResponse submitClaim(@Valid @RequestBody ClaimRequest request) {
        return claimService.submitClaim(request);
    }

    // Fetch all claims
    @GetMapping
    public List<ClaimResponse> getAllClaims() {
        return claimService.getAllClaims();
    }

    // Fetch claims by employee ID
    @GetMapping("/employee/{id}")
    public List<ClaimResponse> getClaimsByEmployee(@PathVariable Long id) {
        return claimService.getClaimsByEmployee(id);
    }

    // Fetch claims by reviewer ID
    @GetMapping("/reviewer/{id}")
    public List<ClaimResponse> getClaimsByReviewer(@PathVariable Long id) {
        return claimService.getClaimsByReviewer(id);
    }

    // Fetch claims by status
    @GetMapping("/status/{status}")
    public List<ClaimResponse> getClaimsByStatus(@PathVariable ClaimStatus status) {
        return claimService.getClaimsByStatus(status);
    }

    // Approve or reject a claim
    @PutMapping("/{claimId}/action")
    public ClaimResponse takeAction(
            @PathVariable Long claimId,
            @RequestParam Long reviewerId,
            @Valid @RequestBody ClaimActionRequest request) {

        return claimService.takeAction(claimId, reviewerId, request);
    }
}