package com.example.Reimbursement_Portal.controller;

import com.example.Reimbursement_Portal.dto.Response.UserResponseDTO;
import com.example.Reimbursement_Portal.entity.User;
import com.example.Reimbursement_Portal.mapper.UserMapper;
import com.example.Reimbursement_Portal.repository.UserRepository;
import com.example.Reimbursement_Portal.dto.StandardAPIResponse;
import org.springframework.http.ResponseEntity;

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
    public ResponseEntity<StandardAPIResponse<UserResponseDTO>> me(Authentication authentication) {

        String email = authentication.getName();

        User user = userRepository.findByEmail(email)
                .orElseThrow(() -> new RuntimeException("Logged-in user not found"));

        UserResponseDTO response = UserMapper.toResponse(user);

        StandardAPIResponse<UserResponseDTO> apiResponse =
                StandardAPIResponse.<UserResponseDTO>builder()
                        .success(true)
                        .message("User fetched successfully")
                        .data(response)
                        .build();

        return ResponseEntity.ok(apiResponse);
    }
}