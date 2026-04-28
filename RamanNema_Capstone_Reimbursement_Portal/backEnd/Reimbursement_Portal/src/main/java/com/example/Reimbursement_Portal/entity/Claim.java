package com.example.Reimbursement_Portal.entity;

import com.example.Reimbursement_Portal.enums.ClaimStatus;
import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDate;

/**
 * Entity representing a reimbursement claim.
 */
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Entity
@Table(name = "claims")
public class Claim {

    /**
     * Claim ID.
     */
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    /**
     * Claim amount.
     */
    @Column(nullable = false)
    private Double amount;

    /**
     * Claim description.
     */
    @Column(nullable = false)
    private String description;

    /**
     * Claim submission date.
     */
    private LocalDate date;

    /**
     * Claim status.
     */
    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private ClaimStatus status = ClaimStatus.SUBMITTED;

    /**
     * Employee who submitted the claim.
     */
    @ManyToOne
    @JoinColumn(name = "employee_id", nullable = false)
    private User employee;

    /**
     * Reviewer of the claim.
     */
    @ManyToOne
    @JoinColumn(name = "reviewer_id")
    private User reviewer;

    /**
     * Reviewer comment.
     */
    @Column(length = 500)
    private String comment;

    /**
     * Sets the claim date before persisting.
     */
    @PrePersist
    public void prePersist() {
        this.date = LocalDate.now();
    }
}