package com.example.todo_application.service;

import com.example.todo_application.dto.*;
import com.example.todo_application.entity.*;
import com.example.todo_application.exception.ResourceNotFoundException;
import com.example.todo_application.mapper.TodoMapper;
import com.example.todo_application.repository.TodoRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

/**
 * Service layer responsible for handling business logic
 * related to Todo operations.
 */
@Service
public class TodoService {

    private final TodoRepository repository;

    /**
     * Constructor-based dependency injection for TodoRepository.
     */
    public TodoService(TodoRepository repository) {
        this.repository = repository;
    }

    /**
     * Creates a new Todo item.
     * Converts DTO to Entity, saves it, and returns response DTO.
     */
    public TodoResponseDTO create(TodoDTO dto) {
        Todo todo = TodoMapper.toEntity(dto);
        return TodoMapper.toDTO(repository.save(todo));
    }

    /**
     * Retrieves all Todo items from the database.
     * Maps each entity to its corresponding response DTO.
     */
    public List<TodoResponseDTO> getAll() {
        return repository.findAll()
                .stream()
                .map(TodoMapper::toDTO)
                .collect(Collectors.toList());
    }

    /**
     * Fetches a Todo by its ID.
     * Throws ResourceNotFoundException if not found.
     */
    public TodoResponseDTO getById(Long id) {
        Todo todo = repository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Todo not found in the data."));

        return TodoMapper.toDTO(todo);
    }

    /**
     * Updates an existing Todo.
     * Validates status transition before applying changes.
     */
    public TodoResponseDTO update(Long id, TodoDTO dto) {

        // Fetch existing Todo or throw exception if not found
        Todo todo = repository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Todo not found in the data."));

        // Update basic fields
        todo.setTitle(dto.getTitle());
        todo.setDescription(dto.getDescription());

        // Convert incoming status string to enum
        Status newStatus = Status.valueOf(dto.getStatus());

        // Validate allowed status transitions
        if (!isValid(todo.getStatus(), newStatus)) {
            throw new RuntimeException("Invalid status transition");
        }

        // Apply status update
        todo.setStatus(newStatus);

        // Save updated entity and return response DTO
        return TodoMapper.toDTO(repository.save(todo));
    }

    /**
     * Deletes a Todo by its ID.
     */
    public void delete(Long id) {

        // Check if Todo exists
        Todo todo = repository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Todo not found, cannot delete"));

        //  Delete only if found
        repository.delete(todo);
    }

    /**
     * Validates allowed status transitions.
     * Only PENDING <-> COMPLETED transitions are permitted.
     */
    private boolean isValid(Status oldS, Status newS) {
        return (oldS == Status.PENDING && newS == Status.COMPLETED)
                || (oldS == Status.COMPLETED && newS == Status.PENDING);
    }
}