package com.example.Reimbursement_Portal.entity;

import com.example.Reimbursement_Portal.enums.Role;
import jakarta.persistence.*;
import lombok.*;

/**
 * Entity representing a user.
 */
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Entity
@Table(name = "users")
public class User {

    /**
     * User ID.
     */
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    /**
     * User name.
     */
    private String name;

    /**
     * User email.
     */
    @Column(unique = true)
    private String email;

    /**
     * User password.
     */
    private String password;

    /**
     * User role.
     */
    @Enumerated(EnumType.STRING)
    private Role role;

    /**
     * Manager of the user.
     */
    @ManyToOne
    @JoinColumn(name = "manager_id")
    private User manager;
}