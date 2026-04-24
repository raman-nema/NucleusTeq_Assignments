package com.example.Reimbursement_Portal.repository;

import com.example.Reimbursement_Portal.entity.Claim;
import com.example.Reimbursement_Portal.entity.ClaimStatus;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

// Repository for Claim entity
public interface ClaimRepository extends JpaRepository<Claim, Long> {

    // Get all claims submitted by a specific employee
    List<Claim> findByEmployeeId(Long employeeId);

    // Get all claims assigned to a reviewer (manager/admin)
    List<Claim> findByReviewerId(Long reviewerId);

    // Get claims by status (SUBMITTED, APPROVED, REJECTED)
    List<Claim> findByStatus(ClaimStatus status);

    // Get claims for a reviewer filtered by status
    List<Claim> findByReviewerIdAndStatus(Long reviewerId, ClaimStatus status);
}