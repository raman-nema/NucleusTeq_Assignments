package com.example.Spring_And_REST_Assignment.model;

public class User {

    private int id;
    private String name;
    private int age;
    private String role;

    // Constructor
    public User(int id, String name, int age, String role) {
        this.id = id;
        this.name = name;
        this.age = age;
        this.role = role;
    }

    // Getters
    public int getId() {
        return id;
    }
    public String getName() {
        return name;
    }
    public int getAge() {
        return age;
    }
    public String getRole() {
        return role;
    }
}
