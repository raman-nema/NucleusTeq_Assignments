package com.example.Reimbursement_Portal.repository;

import com.example.Reimbursement_Portal.entity.Role;
import com.example.Reimbursement_Portal.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

// JPA Repository for User entity
public interface UserRepository extends JpaRepository<User, Long> {

    // Fetch user by email
    Optional<User> findByEmail(String email);

    // Check if email already exists
    boolean existsByEmail(String email);

    // Fetch all employees reporting to a manager
    List<User> findByManagerId(Long managerId);

    // for deletion purpose
    boolean existsByManagerId(Long managerId);

    // Fetch users by role
    List<User> findByRole(Role role);
}