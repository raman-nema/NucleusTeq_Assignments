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
                    boolean result = true;

                    // Name match (ignore if null or empty)
                    if (name != null && !name.trim().isEmpty()) {
                        result &= user.getName().equalsIgnoreCase(name.trim());
                    }

                    // Age match
                    if (age != null) {
                        result &= user.getAge() == age;
                    }

                    // Role match (ignore if null or empty)
                    if (role != null && !role.trim().isEmpty()) {
                        result &= user.getRole().equalsIgnoreCase(role.trim());
                    }

                    return result;
                })
                .toList();
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
                    return "User with ID " + id + " deleted successfully.";
                })
                .orElse("User not found in the data.");
    }
}

