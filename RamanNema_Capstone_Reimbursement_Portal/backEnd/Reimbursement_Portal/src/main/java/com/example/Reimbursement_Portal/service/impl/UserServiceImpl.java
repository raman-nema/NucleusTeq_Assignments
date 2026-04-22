package com.example.Reimbursement_Portal.service.impl;

import com.example.Reimbursement_Portal.dto.Request.UserRequest;
import com.example.Reimbursement_Portal.dto.Response.UserResponse;
import com.example.Reimbursement_Portal.entity.Role;
import com.example.Reimbursement_Portal.entity.User;
import com.example.Reimbursement_Portal.exception.BadRequestException;
import com.example.Reimbursement_Portal.repository.UserRepository;
import com.example.Reimbursement_Portal.service.UserService;
import com.example.Reimbursement_Portal.util.ValidationUtil;

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

        return mapToResponse(savedUser);
    }


    // COMMON DTO MAPPING METHOD
    private UserResponse mapToResponse(User user) {
        return UserResponse.builder()
                .id(user.getId())
                .name(user.getName())
                .email(user.getEmail())
                .role(user.getRole())
                .build();
    }
}