package com.example.Reimbursement_Portal.service.impl;

import com.example.Reimbursement_Portal.dto.Request.ClaimActionRequest;
import com.example.Reimbursement_Portal.dto.Request.ClaimRequest;
import com.example.Reimbursement_Portal.dto.Response.ClaimResponse;
import com.example.Reimbursement_Portal.entity.*;
import com.example.Reimbursement_Portal.exception.BadRequestException;
import com.example.Reimbursement_Portal.exception.ResourceNotFoundException;
import com.example.Reimbursement_Portal.mapper.ClaimMapper;
import com.example.Reimbursement_Portal.repository.ClaimRepository;
import com.example.Reimbursement_Portal.repository.UserRepository;
import com.example.Reimbursement_Portal.service.ClaimService;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.util.List;

@Service
@RequiredArgsConstructor
public class ClaimServiceImpl implements ClaimService {

    // Repository for claim data access
    private final ClaimRepository claimRepository;

    // Repository for user data access
    private final UserRepository userRepository;

    @Override
    public ClaimResponse submitClaim(ClaimRequest request) {

        // Validate claim amount
        if (request.getAmount() == null || request.getAmount() <= 0) {
            throw new BadRequestException("Amount must be greater than 0");
        }

        // Fetch employee or throw exception
        User employee = userRepository.findById(request.getEmployeeId())
                .orElseThrow(() -> new BadRequestException("Employee not found"));

        // Assign reviewer (manager or fallback admin)
        User reviewer = (employee.getManager() != null)
                ? employee.getManager()
                : userRepository.findAll().stream()
                  .filter(u -> u.getRole() == Role.ADMIN)
                  .findFirst()
                  .orElseThrow(() -> new BadRequestException("Admin not found"));

        // Create new claim entity
        Claim claim = new Claim();
        claim.setAmount(request.getAmount());
        claim.setDescription(request.getDescription());
        claim.setDate(LocalDate.now());
        claim.setStatus(ClaimStatus.SUBMITTED);
        claim.setEmployee(employee);
        claim.setReviewer(reviewer);

        // Save and map to response
        return ClaimMapper.toResponse(claimRepository.save(claim));
    }

    @Override
    public List<ClaimResponse> getAllClaims() {

        // Fetch and map all claims
        return claimRepository.findAll().stream()
                .map(ClaimMapper::toResponse)
                .toList();
    }

    @Override
    public List<ClaimResponse> getClaimsByEmployee(Long employeeId) {

        // Validate employee existence
        if (!userRepository.existsById(employeeId)) {
            throw new BadRequestException("Employee not found");
        }

        // Fetch and map claims by employee
        return claimRepository.findByEmployeeId(employeeId)
                .stream()
                .map(ClaimMapper::toResponse)
                .toList();
    }

    @Override
    public List<ClaimResponse> getClaimsByReviewer(Long reviewerId) {

        // Validate reviewer existence
        if (!userRepository.existsById(reviewerId)) {
            throw new BadRequestException("Reviewer not found");
        }

        // Fetch and map claims by reviewer
        return claimRepository.findByReviewerId(reviewerId)
                .stream()
                .map(ClaimMapper::toResponse)
                .toList();
    }

    @Override
    public List<ClaimResponse> getClaimsByStatus(ClaimStatus status) {

        // Fetch and map claims by status
        return claimRepository.findByStatus(status)
                .stream()
                .map(ClaimMapper::toResponse)
                .toList();
    }

    @Override
    public ClaimResponse takeAction(Long claimId, Long reviewerId, ClaimActionRequest request) {

        // Fetch claim or throw exception
        Claim claim = claimRepository.findById(claimId)
                .orElseThrow(() -> new ResourceNotFoundException("Claim not found"));

        // Fetch reviewer or throw exception
        User reviewer = userRepository.findById(reviewerId)
                .orElseThrow(() -> new ResourceNotFoundException("Reviewer not found"));

        // Ensure claim is not already processed
        if (claim.getStatus() != ClaimStatus.SUBMITTED) {
            throw new BadRequestException("Claim already processed");
        }

        // Validate reviewer authorization
        if (claim.getReviewer() == null ||
                (!claim.getReviewer().getId().equals(reviewerId)
                        && reviewer.getRole() != Role.ADMIN)) {
            throw new BadRequestException("Not authorized to take action");
        }

        // Prevent invalid status transition
        if (request.getStatus() == ClaimStatus.SUBMITTED) {
            throw new BadRequestException("Invalid action");
        }

        // Ensure rejection includes a comment
        if (request.getStatus() == ClaimStatus.REJECTED &&
                (request.getComment() == null || request.getComment().isBlank())) {
            throw new BadRequestException("Comment required for rejection");
        }

        // Update claim status and comment
        claim.setStatus(request.getStatus());
        claim.setComment(request.getComment());

        // Save and return updated claim
        return ClaimMapper.toResponse(claimRepository.save(claim));
    }
}