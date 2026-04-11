package com.example.spring_core_assignment.model;

// User entity representing basic user details
public class User {

    private Long id;      // Unique ID
    private String name;  // User name
    private String email; // User email

    // Constructor to initialize fields
    public User(Long id, String name, String email) {
        this.id = id;
        this.name = name;
        this.email = email;
    }

    // Getters
    public Long getId() { return id; }
    public String getName() { return name; }
    public String getEmail() { return email; }

}
