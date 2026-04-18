package com.example.todo_application.repository;

import com.example.todo_application.entity.Todo;
import org.springframework.data.jpa.repository.JpaRepository;


/**
 * Data Access Layer for {@link Todo} entities.
 * * Provides automated CRUD functionality and pagination by extending JpaRepository.
 * Implementation is generated at runtime by Spring Data JPA.
 */

public interface TodoRepository extends JpaRepository<Todo, Long> {
    // Handles DB operations
}