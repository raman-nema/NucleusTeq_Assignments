package com.example.Reimbursement_Portal.entity;

import jakarta.persistence.*;
import lombok.*;

// Lombok annotations reduce boilerplate code
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Entity // Marks this class as a database table
@Table(name = "users")
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // User basic details
    private String name;

    @Column(unique = true)
    private String email;

    private String password;

    // Role stored as String in DB
    @Enumerated(EnumType.STRING)
    private Role role;

    // Many employees can have one manager
    @ManyToOne
    @JoinColumn(name = "manager_id")
    private User manager;
}