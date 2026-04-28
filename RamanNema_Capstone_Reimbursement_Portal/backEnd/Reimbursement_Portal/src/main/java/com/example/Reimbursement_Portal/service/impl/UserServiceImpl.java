package com.example.Reimbursement_Portal.service.impl;

import com.example.Reimbursement_Portal.dto.Request.UserRequestDTO;
import com.example.Reimbursement_Portal.dto.Response.UserResponseDTO;
import com.example.Reimbursement_Portal.enums.Role;
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

@Service
@RequiredArgsConstructor
public class UserServiceImpl implements UserService {

    private final UserRepository userRepository;
    private final BCryptPasswordEncoder passwordEncoder;

    // ========================= CREATE USER =========================
    @Override
    public UserResponseDTO createUser(UserRequestDTO request) {

        // 1. Validate email domain
        if (!ValidationUtil.isValidCompanyEmail(request.getEmail())) {
            throw new BadRequestException("Email must be @company.com");
        }

        // 2. Check duplicate email
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new BadRequestException("Email already exists");
        }

        // 3. Encrypt password
        String encryptedPassword = passwordEncoder.encode(request.getPassword());

        // 4. Create user entity FIRST
        User user = UserMapper.toEntity(request, encryptedPassword);

        // 5. Assign manager ONLY if provided (optional for EMPLOYEE)
        if (request.getRole() == Role.EMPLOYEE && request.getManagerId() != null) {

            User manager = userRepository.findById(request.getManagerId())
                    .orElseThrow(() -> new BadRequestException("Manager not found"));

            if (manager.getRole() != Role.MANAGER) {
                throw new BadRequestException("Assigned manager must have MANAGER role");
            }

            user.setManager(manager);
        }

        // 6. Save user
        User savedUser = userRepository.save(user);

        return UserMapper.toResponse(savedUser);
    }

    // ========================= GET ALL USERS =========================
    @Override
    public List<UserResponseDTO> getAllUsers() {
        return userRepository.findAll()
                .stream()
                .map(UserMapper::toResponse)
                .toList();
    }

    // ========================= GET USER BY ID =========================
    @Override
    public UserResponseDTO getUserById(Long id) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new BadRequestException("User not found with ID: " + id));

        return UserMapper.toResponse(user);
    }

    // ========================= GET EMPLOYEES UNDER MANAGER =========================
    @Override
    public List<UserResponseDTO> getEmployeesByManager(Long managerId) {

        if (!userRepository.existsById(managerId)) {
            throw new BadRequestException("Manager not found with ID: " + managerId);
        }

        return userRepository.findByManagerId(managerId)
                .stream()
                .map(UserMapper::toResponse)
                .toList();
    }

    // ========================= DELETE USER =========================
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