package com.example.Spring_And_REST_Assignment.service;

import com.example.Spring_And_REST_Assignment.model.User;
import com.example.Spring_And_REST_Assignment.repository.UserRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class UserService {

    // Repository dependency
    private final UserRepository repository;

    // Constructor Injection
    public UserService(UserRepository repository) {
        this.repository = repository;
    }

    // Save a new user
    public User saveUser(User user) {
        return repository.save(user);
    }

    // Search users based on optional filters
    public List<User> search(String name, Integer age, String role) {

        // various filters for filtering the user while searching across data
        return repository.findAll().stream()
                .filter(user -> {
                    boolean matches = true;

                    // Case-insensitive name match
                    if (name != null) {
                        matches &= user.getName().equalsIgnoreCase(name);
                    }

                    // Exact age match
                    if (age != null) {
                        matches &= user.getAge() == age;
                    }

                    // Case-insensitive role match
                    if (role != null) {
                        matches &= user.getRole().equalsIgnoreCase(role);
                    }

                    return matches;
                })
                .collect(Collectors.toList()); // after filtering convert to list from stream
    }

    // Delete user only if confirmation is true
    public String deleteUser(Long id, boolean confirm) {

        // Prevent deletion without confirmation
        if (!confirm) {
            return "Confirmation required for deletion.";
        }

        // Find user and delete if present
        return repository.findById(id)
                .map(user -> {
                    repository.delete(user);
                    return "User deleted from the data.";
                })
                .orElse("User not found in the data.");
    }
}

