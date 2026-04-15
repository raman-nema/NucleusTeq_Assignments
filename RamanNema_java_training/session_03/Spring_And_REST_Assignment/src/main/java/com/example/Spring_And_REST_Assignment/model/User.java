package com.example.Spring_And_REST_Assignment.model;

// Represents User entity used in API requests and responses
public class User {

    private Long id;
    private String name;
    private int age;
    private String role;

    // Default constructor required for JSON deserialization
    public User() {}

    // Parameterized constructor for creating user objects
    public User(Long id, String name, int age, String role) {
        this.id = id;
        this.name = name;
        this.age = age;
        this.role = role;
    }

    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public int getAge() { return age; }
    public void setAge(int age) { this.age = age; }

    public String getRole() { return role; }
    public void setRole(String role) { this.role = role; }
}