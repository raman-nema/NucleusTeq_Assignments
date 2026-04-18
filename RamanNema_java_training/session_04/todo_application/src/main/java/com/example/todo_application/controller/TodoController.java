package com.example.todo_application.controller;

import com.example.todo_application.dto.*;
import com.example.todo_application.exception.ResourceNotFoundException;
import com.example.todo_application.service.TodoService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;

/**
 * REST Controller for Todo operations.
 * Handles CRUD APIs.
 */
@RestController
@RequestMapping("/todos")
public class TodoController {

    // Logger for tracking API calls
    private static final Logger logger = LoggerFactory.getLogger(TodoController.class);

    private final TodoService service;

    // Constructor injection
    public TodoController(TodoService service) {
        this.service = service;
    }

     // Create a new Todo.
    @PostMapping
    public TodoResponseDTO create(@RequestBody @Valid TodoDTO dto) {

        logger.info("Creating TODO with title: {}", dto.getTitle());

        TodoResponseDTO response = service.create(dto);

        logger.info("TODO created with ID: {}", response.getId());

        return response;
    }

     // Get all Todos.
    @GetMapping
    public List<TodoResponseDTO> getAll() {

        logger.info("Fetching all TODOs");

        List<TodoResponseDTO> todos = service.getAll();

        logger.info("Total TODOs: {}", todos.size());

        return todos;
    }


     //  Get Todo by ID.
    @GetMapping("/{id}")
    public TodoResponseDTO getById(@PathVariable Long id) {

        logger.info("Fetching TODO with ID: {}", id);

        TodoResponseDTO todo = service.getById(id);

        return todo;
    }

     // Update Todo.
    @PutMapping("/{id}")
    public TodoResponseDTO update(@PathVariable Long id,
                                  @RequestBody TodoDTO dto) {

        logger.info("Updating TODO with ID: {}", id);

        TodoResponseDTO updated = service.update(id, dto);

        return updated;
    }

     // Delete Todo by ID.
     @DeleteMapping("/{id}")

     public ResponseEntity<String> delete(@PathVariable Long id) {

         logger.info("DELETE /todos/{} - Request received", id);

         service.delete(id);

         logger.info("DELETE /todos/{} - Successfully deleted", id);

         return ResponseEntity.ok("Todo deleted successfully.");

     }
}