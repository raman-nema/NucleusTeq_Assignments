package com.example.Reimbursement_Portal.service.impl;

import com.example.Reimbursement_Portal.dto.Request.ClaimActionRequestDTO;
import com.example.Reimbursement_Portal.dto.Request.ClaimRequestDTO;
import com.example.Reimbursement_Portal.dto.Response.ClaimResponseDTO;
import com.example.Reimbursement_Portal.entity.Claim;
import com.example.Reimbursement_Portal.entity.User;
import com.example.Reimbursement_Portal.enums.ClaimStatus;
import com.example.Reimbursement_Portal.enums.Role;
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

/**
 * Implementation of ClaimService.
 */
@Service
@RequiredArgsConstructor
public class ClaimServiceImpl implements ClaimService {

    private final ClaimRepository claimRepository;
    private final UserRepository userRepository;

    /**
     * Submits a new claim.
     *
     * @param request the claim request
     * @return the created claim
     */
    @Override
    public ClaimResponseDTO submitClaim(ClaimRequestDTO request) {

        if (request.getAmount() == null || request.getAmount() <= 0) {
            throw new BadRequestException("Amount must be greater than 0");
        }

        if (request.getDescription() == null || request.getDescription().isBlank()) {
            throw new BadRequestException("Description is required");
        }

        User employee = userRepository.findById(request.getEmployeeId())
                .orElseThrow(() ->
                        new BadRequestException("Employee not found with id: " + request.getEmployeeId()));

        User reviewer = resolveReviewer(employee);

        Claim claim = ClaimMapper.toEntity(request, employee, reviewer);

        return ClaimMapper.toResponse(claimRepository.save(claim));
    }

    /**
     * Retrieves all claims.
     *
     * @return list of claims
     */
    @Override
    public List<ClaimResponseDTO> getAllClaims() {
        return claimRepository.findAll()
                .stream()
                .map(ClaimMapper::toResponse)
                .toList();
    }

    /**
     * Retrieves claims by employee ID.
     *
     * @param employeeId the employee ID
     * @return list of claims
     */
    @Override
    public List<ClaimResponseDTO> getClaimsByEmployee(Long employeeId) {

        if (!userRepository.existsById(employeeId)) {
            throw new BadRequestException("Employee not found");
        }

        return claimRepository.findByEmployeeId(employeeId)
                .stream()
                .map(ClaimMapper::toResponse)
                .toList();
    }

    /**
     * Retrieves claims by reviewer ID.
     *
     * @param reviewerId the reviewer ID
     * @return list of claims
     */
    @Override
    public List<ClaimResponseDTO> getClaimsByReviewer(Long reviewerId) {

        if (!userRepository.existsById(reviewerId)) {
            throw new BadRequestException("Reviewer not found");
        }

        return claimRepository.findByReviewerId(reviewerId)
                .stream()
                .map(ClaimMapper::toResponse)
                .toList();
    }

    /**
     * Retrieves claims by status.
     *
     * @param status the claim status
     * @return list of claims
     */
    @Override
    public List<ClaimResponseDTO> getClaimsByStatus(ClaimStatus status) {

        return claimRepository.findByStatus(status)
                .stream()
                .map(ClaimMapper::toResponse)
                .toList();
    }

    /**
     * Takes action on a claim.
     *
     * @param claimId the claim ID
     * @param reviewerId the reviewer ID
     * @param request the action request
     * @return the updated claim
     */
    @Override
    public ClaimResponseDTO takeAction(Long claimId, Long reviewerId, ClaimActionRequestDTO request) {

        Claim claim = claimRepository.findById(claimId)
                .orElseThrow(() -> new ResourceNotFoundException("Claim not found"));

        User reviewer = userRepository.findById(reviewerId)
                .orElseThrow(() -> new ResourceNotFoundException("Reviewer not found"));

        if (claim.getStatus() != ClaimStatus.SUBMITTED) {
            throw new BadRequestException("Claim already processed");
        }

        if (claim.getReviewer() == null ||
                (!claim.getReviewer().getId().equals(reviewerId)
                        && reviewer.getRole() != Role.ADMIN)) {
            throw new BadRequestException("Not authorized to take action");
        }

        if (request.getStatus() == ClaimStatus.SUBMITTED) {
            throw new BadRequestException("Invalid action");
        }

        if (request.getStatus() == ClaimStatus.REJECTED &&
                (request.getComment() == null || request.getComment().isBlank())) {
            throw new BadRequestException("Comment required for rejection");
        }

        claim.setStatus(request.getStatus());
        claim.setComment(request.getComment());

        return ClaimMapper.toResponse(claimRepository.save(claim));
    }

    /**
     * Resolves reviewer for a claim.
     *
     * @param employee the employee
     * @return the reviewer
     */
    private User resolveReviewer(User employee) {

        if (employee.getManager() != null) {
            return employee.getManager();
        }

        return userRepository.findByRole(Role.ADMIN)
                .stream()
                .findFirst()
                .orElseThrow(() ->
                        new BadRequestException("No admin available for fallback"));
    }
}