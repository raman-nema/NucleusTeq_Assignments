package com.example.Reimbursement_Portal.service;

import com.example.Reimbursement_Portal.dto.Request.UserRequest;
import com.example.Reimbursement_Portal.dto.Response.UserResponse;

import java.util.List;

// Service interface
public interface UserService {

    UserResponse createUser(UserRequest request);

//    List<UserResponse> getAllUsers();
//
//    UserResponse getUserById(Long id);
//
//    List<UserResponse> getEmployeesByManager(Long managerId);
}