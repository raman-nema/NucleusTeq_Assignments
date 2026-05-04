package com.example.Reimbursement_Portal.repository;

import com.example.Reimbursement_Portal.enums.Role;
import com.example.Reimbursement_Portal.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

/**
 * Repository for User entity.
 */
public interface UserRepository extends JpaRepository<User, Long> {

    /**
     * Finds user by email.
     *
     * @param email the email
     * @return optional user
     */
    Optional<User> findByEmail(String email);

    /**
     * Checks if email exists.
     *
     * @param email the email
     * @return true if exists
     */
    boolean existsByEmail(String email);

    /**
     * Finds users by manager ID.
     *
     * @param managerId the manager ID
     * @return list of users
     */
    List<User> findByManagerId(Long managerId);

    /**
     * Checks if users exist for a manager ID.
     *
     * @param managerId the manager ID
     * @return true if exists
     */
    boolean existsByManagerId(Long managerId);

    /**
     * Finds users by role.
     *
     * @param role the user role
     * @return list of users
     */
    List<User> findByRole(Role role);
}