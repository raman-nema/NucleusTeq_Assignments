package com.example.Reimbursement_Portal.service.impl;

import com.example.Reimbursement_Portal.dto.Request.UserRequest;
import com.example.Reimbursement_Portal.dto.Response.UserResponse;
import com.example.Reimbursement_Portal.entity.Role;
import com.example.Reimbursement_Portal.entity.User;
import com.example.Reimbursement_Portal.exception.BadRequestException;
import com.example.Reimbursement_Portal.repository.UserRepository;
import com.example.Reimbursement_Portal.service.UserService;
import com.example.Reimbursement_Portal.util.ValidationUtil;
import com.example.Reimbursement_Portal.mapper.UserMapper;

import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.List;

// Service implementation for User operations
@Service
@RequiredArgsConstructor
public class UserServiceImpl implements UserService {

    private final UserRepository userRepository;
    private final BCryptPasswordEncoder passwordEncoder;

    // CREATE USER
    @Override
    public UserResponse createUser(UserRequest request) {

        // Validate email domain
        if (!ValidationUtil.isValidCompanyEmail(request.getEmail())) {
            throw new BadRequestException("Email must be @company.com");
        }

        // Check duplicate email
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new BadRequestException("Email already exists");
        }

        // Validate manager requirement for EMPLOYEE
        if (request.getRole() == Role.EMPLOYEE && request.getManagerId() == null) {
            throw new BadRequestException("Manager ID is required for EMPLOYEE");
        }

        // Encrypt password
        String encryptedPassword = passwordEncoder.encode(request.getPassword());

        // Create user entity
        User user = new User();
        user.setName(request.getName());
        user.setEmail(request.getEmail());
        user.setPassword(encryptedPassword);
        user.setRole(request.getRole());

        // Assign manager if provided
        if (request.getManagerId() != null) {
            User manager = userRepository.findById(request.getManagerId())
                    .orElseThrow(() -> new BadRequestException("Manager not found in the records."));

            user.setManager(manager);
        }

        // Save user
        User savedUser = userRepository.save(user);

        return UserMapper.toResponse(savedUser);
    }

    // GET ALL USERS
    @Override
    public List<UserResponse> getAllUsers() {
        List<User> users = userRepository.findAll();

        return users.stream()
                .map(UserMapper::toResponse)
                .toList();
    }

    // GET USER BY ID
    @Override
    public UserResponse getUserById(Long id) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new BadRequestException("User not found with ID: " + id));

        return UserMapper.toResponse(user);
    }

    // GET EMPLOYEES UNDER MANAGER
    @Override
    public List<UserResponse> getEmployeesByManager(Long managerId) {

        // Validate manager exists
        if (!userRepository.existsById(managerId)) {
            throw new BadRequestException("Manager not found with ID: " + managerId);
        }

        return userRepository.findByManagerId(managerId)
                .stream()
                .map(UserMapper::toResponse)
                .toList();
    }

    @Override
    public void deleteUser(Long id) {

        User user = userRepository.findById(id)
                .orElseThrow(() -> new BadRequestException("User not found with ID: " + id));

        if (userRepository.existsByManagerId(id)) {
            throw new BadRequestException("Cannot delete manager with assigned employees");
        }

        userRepository.delete(user);
    }
}