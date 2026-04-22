package com.example.Reimbursement_Portal.controller;

import com.example.Reimbursement_Portal.dto.Request.UserRequest;
import com.example.Reimbursement_Portal.dto.Response.UserResponse;
import com.example.Reimbursement_Portal.service.UserService;

import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

// REST Controller
@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    // CREATE USER
    @PostMapping
    public UserResponse createUser(@RequestBody UserRequest request) {
        return userService.createUser(request);
    }

}