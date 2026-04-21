package com.example.Reimbursement_Portal.repository;

import com.example.Reimbursement_Portal.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;

// JpaRepository provides CRUD operations automatically
public interface UserRepository extends JpaRepository<User, Long> {

    // Custom method to find user by email (used in login)
    Optional<User> findByEmail(String email);
}