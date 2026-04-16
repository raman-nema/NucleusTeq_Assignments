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

    // POST API
    @PostMapping("/submit")
    public ResponseEntity<?> saveUser(@RequestBody User user) {

        // if the input is invalid
        if (user.getName() == null || user.getName().isEmpty()
                || user.getRole() == null
                || user.getAge() == 0) {

            return ResponseEntity.badRequest().body("Invalid input, please enter valid information.");
        }
        // if the input is valid
        return ResponseEntity.status(201).body(service.saveUser(user));
    }

    // DELETE API
    @DeleteMapping("/users/{id}")
    public String deleteUser(
            @PathVariable Long id,
            @RequestParam(required = false, defaultValue = "false") boolean confirm
    ) {
        return service.deleteUser(id, confirm);
    }



}