package com.example.Reimbursement_Portal.controller;

import com.example.Reimbursement_Portal.dto.Response.UserResponseDTO;
import com.example.Reimbursement_Portal.entity.User;
import com.example.Reimbursement_Portal.mapper.UserMapper;
import com.example.Reimbursement_Portal.repository.UserRepository;

import lombok.RequiredArgsConstructor;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

/**
 * Controller for authentication-related endpoints.
 */
@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
public class AuthController {

    private final UserRepository userRepository;

    /**
     * Retrieves details of the currently authenticated user.
     *
     * @param authentication the authentication object containing user details
     * @return the authenticated user's response DTO
     */
    @GetMapping("/me")
    public UserResponseDTO me(Authentication authentication) {
        String email = authentication.getName();

        User user = userRepository.findByEmail(email)
                .orElseThrow(() -> new RuntimeException("Logged-in user not found"));

        return UserMapper.toResponse(user);
    }
}