package com.example.todo_application.controller;

import com.example.todo_application.dto.*;
import com.example.todo_application.service.TodoService;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * REST Controller for managing Todo operations.
 * Exposes endpoints for CRUD functionalities.
 */
@RestController
@RequestMapping("/todos")
public class TodoController {

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
        return service.create(dto);
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