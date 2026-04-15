package com.example.Spring_And_REST_Assignment.repository;

import com.example.Spring_And_REST_Assignment.model.User;
import org.springframework.stereotype.Repository;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@Repository
public class UserRepository {

    // In-memory list to store users (acts like a database)
    private final List<User> users = new ArrayList<>();

    // Counter to generate unique IDs for users
    private Long idCounter = 1L;

    // Save a new user and assign a unique ID
    public User save(User user) {
        user.setId(idCounter++);
        users.add(user);
        return user;
    }

    // Return all users
    public List<User> findAll() {
        return users;
    }

    // Find user by ID using stream filtering
    public Optional<User> findById(Long id) {
        return users.stream()
                .filter(u -> u.getId().equals(id))
                .findFirst();
    }

    // Delete a user from the list
    public void delete(User user) {
        users.remove(user);
    }
}