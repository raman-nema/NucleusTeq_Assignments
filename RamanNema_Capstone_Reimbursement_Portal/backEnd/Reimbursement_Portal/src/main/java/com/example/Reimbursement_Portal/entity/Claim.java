package com.example.Reimbursement_Portal.entity;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDate;

// Entity for Claim table
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Entity
@Table(name = "claims")
public class Claim {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // Claim amount
    @Column(nullable = false)
    private Double amount;

    // Description of claim
    @Column(nullable = false)
    private String description;

    // Date of claim submission (auto-set)
    private LocalDate date;

    // Claim status (default: SUBMITTED)
    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private ClaimStatus status = ClaimStatus.SUBMITTED;

    // Employee who created the claim
    @ManyToOne
    @JoinColumn(name = "employee_id", nullable = false)
    private User employee;

    // Reviewer (Manager or Admin)
    @ManyToOne
    @JoinColumn(name = "reviewer_id")
    private User reviewer;

    // Comment added by reviewer (approve/reject)
    @Column(length = 500)
    private String comment;


    // Automatically set date before saving
    @PrePersist
    public void prePersist() {
        this.date = LocalDate.now();
    }
}