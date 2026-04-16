package com.example.Spring_And_REST_Assignment.controller;

import com.example.Spring_And_REST_Assignment.model.User;
import com.example.Spring_And_REST_Assignment.service.UserService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
public class UserController {

    private final UserService service;

    public UserController(UserService service) {
        this.service = service;
    }

    // GET API
    @GetMapping("/users/search")
    public List<User> searchUsers(
            @RequestParam(required = false) String name,
            @RequestParam(required = false) Integer age,
            @RequestParam(required = false) String role
    ) {
        return service.search(name, age, role);
    }


}