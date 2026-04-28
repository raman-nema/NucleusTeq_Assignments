package com.example.Reimbursement_Portal.service;

import com.example.Reimbursement_Portal.dto.Request.UserRequestDTO;
import com.example.Reimbursement_Portal.dto.Response.UserResponseDTO;

import java.util.List;

/**
 * Service interface for user operations.
 */
public interface UserService {

    /**
     * Creates a new user.
     *
     * @param request the user request
     * @return the created user
     */
    UserResponseDTO createUser(UserRequestDTO request);

    /**
     * Retrieves all users.
     *
     * @return list of users
     */
    List<UserResponseDTO> getAllUsers();

    /**
     * Retrieves a user by ID.
     *
     * @param id the user ID
     * @return the user
     */
    UserResponseDTO getUserById(Long id);

    /**
     * Retrieves employees by manager ID.
     *
     * @param managerId the manager ID
     * @return list of employees
     */
    List<UserResponseDTO> getEmployeesByManager(Long managerId);

    /**
     * Deletes a user by ID.
     *
     * @param id the user ID
     */
    void deleteUser(Long id);
}