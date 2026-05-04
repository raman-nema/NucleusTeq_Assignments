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
import com.example.Reimbursement_Portal.repository.ClaimRepository;
import com.example.Reimbursement_Portal.repository.UserRepository;
import com.example.Reimbursement_Portal.service.impl.ClaimServiceImpl;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.time.LocalDate;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

/**
 * Unit tests for ClaimServiceImpl.
 *
 * We test all the business logic:
 * - Submitting claims
 * - Reviewing/approving/rejecting claims
 * - Error cases (wrong reviewer, missing claims, etc.)
 */
@ExtendWith(MockitoExtension.class)
class ClaimServiceImplTest {

    @Mock
    private ClaimRepository claimRepository;

    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private ClaimServiceImpl claimService;

    // ─── Helpers ─────────────────────────────────────────────────────────

    private User makeUser(Long id, String name, Role role) {
        User u = new User();
        u.setId(id);
        u.setName(name);
        u.setEmail(name.toLowerCase() + "@company.com");
        u.setRole(role);
        return u;
    }

    private Claim makeClaim(Long id, User employee, User reviewer, ClaimStatus status) {
        Claim c = new Claim();
        c.setId(id);
        c.setAmount(1000.0);
        c.setDescription("Test claim");
        c.setDate(LocalDate.now());
        c.setStatus(status);
        c.setEmployee(employee);
        c.setReviewer(reviewer);
        return c;
    }

    // ─── submitClaim() tests ──────────────────────────────────────────────

    @Test
    void submitClaim_withManager_shouldAssignManagerAsReviewer() {
        // GIVEN: An employee who has a manager
        User manager  = makeUser(10L, "Manager", Role.MANAGER);
        User employee = makeUser(1L, "Alice", Role.EMPLOYEE);
        employee.setManager(manager); // Alice reports to Manager

        ClaimRequestDTO req = new ClaimRequestDTO();
        req.setAmount(500.0);
        req.setDescription("Travel expenses");
        req.setEmployeeId(1L);

        Claim savedClaim = makeClaim(100L, employee, manager, ClaimStatus.SUBMITTED);

        when(userRepository.findById(1L)).thenReturn(Optional.of(employee));
        when(claimRepository.save(any(Claim.class))).thenReturn(savedClaim);

        // WHEN: Submit the claim
        ClaimResponseDTO result = claimService.submitClaim(req);

        // THEN: Manager should be the reviewer
        assertNotNull(result);
        assertEquals(ClaimStatus.SUBMITTED, result.getStatus());
        verify(claimRepository, times(1)).save(any(Claim.class));
    }



    @Test
    void submitClaim_employeeNotFound_shouldThrow() {
        // GIVEN: Invalid employee ID
        ClaimRequestDTO req = new ClaimRequestDTO();
        req.setAmount(100.0);
        req.setDescription("Test");
        req.setEmployeeId(999L);

        when(userRepository.findById(999L)).thenReturn(Optional.empty());

        // WHEN + THEN: Should throw
        assertThrows(BadRequestException.class, () -> claimService.submitClaim(req));
    }



    @Test
    void submitClaim_zeroAmount_shouldThrow() {
        // GIVEN: Amount is 0 (not allowed)
        ClaimRequestDTO req = new ClaimRequestDTO();
        req.setAmount(0.0);
        req.setDescription("Test");
        req.setEmployeeId(1L);

        // WHEN + THEN: Service validates amount > 0
        assertThrows(BadRequestException.class, () -> claimService.submitClaim(req));
    }


    // ─── getAllClaims() tests ─────────────────────────────────────────────

    @Test
    void getAllClaims_shouldReturnAllClaims() {
        User emp = makeUser(1L, "Alice", Role.EMPLOYEE);
        Claim c1 = makeClaim(1L, emp, null, ClaimStatus.SUBMITTED);
        Claim c2 = makeClaim(2L, emp, null, ClaimStatus.APPROVED);

        when(claimRepository.findAll()).thenReturn(Arrays.asList(c1, c2));

        List<ClaimResponseDTO> result = claimService.getAllClaims();

        assertEquals(2, result.size());
    }

    // ─── getClaimsByEmployee() tests ─────────────────────────────────────

    @Test
    void getClaimsByEmployee_validEmployee_shouldReturnClaims() {
        User emp = makeUser(1L, "Alice", Role.EMPLOYEE);
        Claim c  = makeClaim(1L, emp, null, ClaimStatus.SUBMITTED);

        when(userRepository.existsById(1L)).thenReturn(true);
        when(claimRepository.findByEmployeeId(1L)).thenReturn(List.of(c));

        List<ClaimResponseDTO> result = claimService.getClaimsByEmployee(1L);

        assertEquals(1, result.size());
    }

    @Test
    void getClaimsByEmployee_employeeNotFound_shouldThrow() {
        when(userRepository.existsById(999L)).thenReturn(false);

        assertThrows(BadRequestException.class,
                () -> claimService.getClaimsByEmployee(999L));
    }

    // ─── getClaimsByReviewer() tests ──────────────────────────────────────

    @Test
    void getClaimsByReviewer_validReviewer_shouldReturnClaims() {
        User emp      = makeUser(1L, "Alice", Role.EMPLOYEE);
        User reviewer = makeUser(10L, "Manager", Role.MANAGER);
        Claim c       = makeClaim(1L, emp, reviewer, ClaimStatus.SUBMITTED);

        when(userRepository.existsById(10L)).thenReturn(true);
        when(claimRepository.findByReviewerId(10L)).thenReturn(List.of(c));

        List<ClaimResponseDTO> result = claimService.getClaimsByReviewer(10L);

        assertEquals(1, result.size());
    }

    @Test
    void getClaimsByReviewer_reviewerNotFound_shouldThrow() {
        when(userRepository.existsById(888L)).thenReturn(false);

        assertThrows(BadRequestException.class,
                () -> claimService.getClaimsByReviewer(888L));
    }

    // ─── getClaimsByStatus() tests ────────────────────────────────────────

    @Test
    void getClaimsByStatus_submitted_shouldReturnOnlySubmitted() {
        User emp = makeUser(1L, "Alice", Role.EMPLOYEE);
        Claim c  = makeClaim(1L, emp, null, ClaimStatus.SUBMITTED);

        when(claimRepository.findByStatus(ClaimStatus.SUBMITTED)).thenReturn(List.of(c));

        List<ClaimResponseDTO> result = claimService.getClaimsByStatus(ClaimStatus.SUBMITTED);

        assertEquals(1, result.size());
        assertEquals(ClaimStatus.SUBMITTED, result.get(0).getStatus());
    }

    // ─── takeAction() tests ───────────────────────────────────────────────




    @Test
    void takeAction_unauthorizedUser_shouldThrow() {
        // GIVEN: A random manager tries to act on a claim not assigned to them
        User employee       = makeUser(1L, "Alice", Role.EMPLOYEE);
        User assignedMgr    = makeUser(10L, "AssignedMgr", Role.MANAGER);
        User unauthorizedMgr= makeUser(20L, "OtherMgr",   Role.MANAGER);
        Claim claim         = makeClaim(100L, employee, assignedMgr, ClaimStatus.SUBMITTED);

        ClaimActionRequestDTO actionReq = new ClaimActionRequestDTO();
        actionReq.setStatus(ClaimStatus.APPROVED);
        actionReq.setComment("Sneaky approval");

        when(claimRepository.findById(100L)).thenReturn(Optional.of(claim));
        when(userRepository.findById(20L)).thenReturn(Optional.of(unauthorizedMgr));

        // WHEN + THEN: Should throw — this manager is not authorized
        assertThrows(BadRequestException.class,
                () -> claimService.takeAction(100L, 20L, actionReq));
    }



    @Test
    void takeAction_settingStatusToSubmitted_shouldThrow() {
        // GIVEN: Someone tries to set status back to SUBMITTED (not allowed)
        User employee = makeUser(1L, "Alice", Role.EMPLOYEE);
        User manager  = makeUser(10L, "Manager", Role.MANAGER);
        Claim claim   = makeClaim(100L, employee, manager, ClaimStatus.SUBMITTED);

        ClaimActionRequestDTO actionReq = new ClaimActionRequestDTO();
        actionReq.setStatus(ClaimStatus.SUBMITTED); // Invalid — can't set back to SUBMITTED

        when(claimRepository.findById(100L)).thenReturn(Optional.of(claim));
        when(userRepository.findById(10L)).thenReturn(Optional.of(manager));

        // WHEN + THEN: Should throw
        assertThrows(BadRequestException.class,
                () -> claimService.takeAction(100L, 10L, actionReq));
    }

    @Test
    void takeAction_claimNotFound_shouldThrow() {
        // GIVEN: Claim ID doesn't exist
        ClaimActionRequestDTO actionReq = new ClaimActionRequestDTO();
        actionReq.setStatus(ClaimStatus.APPROVED);

        when(claimRepository.findById(999L)).thenReturn(Optional.empty());

        // WHEN + THEN: Should throw ResourceNotFoundException
        assertThrows(ResourceNotFoundException.class,
                () -> claimService.takeAction(999L, 10L, actionReq));
    }



    @Test
    void takeAction_managerRejectsWithComment_shouldSucceed() {
        // GIVEN: Claim submitted, manager rejects with reason
        User employee = makeUser(1L, "Alice", Role.EMPLOYEE);
        User manager  = makeUser(10L, "Manager", Role.MANAGER);
        Claim claim   = makeClaim(100L, employee, manager, ClaimStatus.SUBMITTED);

        ClaimActionRequestDTO actionReq = new ClaimActionRequestDTO();
        actionReq.setStatus(ClaimStatus.REJECTED);
        actionReq.setComment("Missing receipt");

        Claim updatedClaim = makeClaim(100L, employee, manager, ClaimStatus.REJECTED);
        updatedClaim.setComment("Missing receipt");

        when(claimRepository.findById(100L)).thenReturn(Optional.of(claim));
        when(userRepository.findById(10L)).thenReturn(Optional.of(manager));
        when(claimRepository.save(any(Claim.class))).thenReturn(updatedClaim);

        // WHEN: Manager rejects
        ClaimResponseDTO result = claimService.takeAction(100L, 10L, actionReq);

        // THEN: Status should be REJECTED and comment saved
        assertEquals(ClaimStatus.REJECTED, result.getStatus());
        assertEquals("Missing receipt", result.getComment());
    }
}