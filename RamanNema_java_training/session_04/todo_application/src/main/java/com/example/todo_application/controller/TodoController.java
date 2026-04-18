package com.example.todo_application.controller;

import com.example.todo_application.dto.*;
import com.example.todo_application.service.TodoService;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;

/**
 * REST Controller for managing Todo operations.
 * Exposes endpoints for CRUD functionalities.
 */
@RestController
@RequestMapping("/todos")
public class TodoController {

    /**
     * Logger instance used for tracking application flow and important events.
     * Helps in monitoring request processing and debugging issues in production.
     */
    private static final Logger logger = LoggerFactory.getLogger(TodoController.class);

    private final TodoService service;

    /**
     * Constructor-based dependency injection for TodoService.
     */
    public TodoController(TodoService service) {
        this.service = service;
    }

    /**
     * Creates a new Todo.
     * Validates request body before passing it to the service layer.
     */
    @PostMapping
    public TodoResponseDTO create(@RequestBody @Valid TodoDTO dto) {

        /**
         * Logs the incoming request with the title of the Todo.
         * Useful for tracing user actions and verifying input data.
         */
        logger.info("Creating TODO with title: {}", dto.getTitle());

        TodoResponseDTO response = service.create(dto);

        /**
         * Logs successful creation along with generated Todo ID.
         * Helps in tracking successful operations and auditing.
         */
        logger.info("TODO created successfully with ID: {}", response.getId());

        return response;
    }

    /**
     * Retrieves all Todos.
     */
    @GetMapping
    public List<TodoResponseDTO> getAll() {
        return service.getAll();
    }

    /**
     * Retrieves a specific Todo by its ID.
     */
    @GetMapping("/{id}")
    public TodoResponseDTO getById(@PathVariable Long id) {
        return service.getById(id);
    }

    /**
     * Updates an existing Todo by ID.
     * Accepts updated data in request body.
     */
    @PutMapping("/{id}")
    public TodoResponseDTO update(@PathVariable Long id,
                                  @RequestBody TodoDTO dto) {
        return service.update(id, dto);
    }

    /**
     * Deletes a Todo by its ID.
     */
    @DeleteMapping("/{id}")
    public String delete(@PathVariable Long id) {
        service.delete(id);
        return "Deleted successfully.";
    }
}