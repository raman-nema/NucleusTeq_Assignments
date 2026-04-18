package com.example.todo_application.service;

import com.example.todo_application.client.NotificationServiceClient;
import com.example.todo_application.dto.*;
import com.example.todo_application.entity.*;
import com.example.todo_application.exception.ResourceNotFoundException;
import com.example.todo_application.mapper.TodoMapper;
import com.example.todo_application.repository.TodoRepository;
import org.springframework.stereotype.Service;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;
import java.util.stream.Collectors;

/**
 * Service layer responsible for handling business logic
 * related to Todo operations.
 */
@Service
public class TodoService {

    // Logger to trace execution flow and important events
    private static final Logger logger = LoggerFactory.getLogger(TodoService.class);

    private final TodoRepository repository;
    private final NotificationServiceClient notificationClient;

    // Constructor-based dependency injection (recommended practice)
    public TodoService(TodoRepository repository, NotificationServiceClient notificationClient) {
        this.repository = repository;
        this.notificationClient = notificationClient;
    }

    /**
     * Creates a new Todo.
     * - Converts DTO to Entity
     * - Saves to database
     * - Sends notification
     */
    public TodoResponseDTO create(TodoDTO dto) {

        logger.info("Processing request to create Todo");

        // Convert incoming DTO to entity
        Todo todo = TodoMapper.toEntity(dto);

        // Persist entity
        Todo saved = repository.save(todo);

        logger.info("Todo saved with ID: {}", saved.getId());

        // Simulate external service call
        notificationClient.sendNotification("New Todo created with ID: " + saved.getId());

        // Convert entity back to response DTO
        return TodoMapper.toDTO(saved);
    }

    /**
     * Retrieves all Todos.
     * - Fetches from DB
     * - Maps to response DTO list
     */
    public List<TodoResponseDTO> getAll() {

        logger.info("Fetching all Todos from database");

        List<TodoResponseDTO> list = repository.findAll()
                .stream()
                .map(TodoMapper::toDTO) // Entity → DTO mapping
                .collect(Collectors.toList());

        logger.info("Total Todos retrieved: {}", list.size());

        return list;
    }

    /**
     * Fetches a Todo by ID.
     * Throws exception if not found.
     */
    public TodoResponseDTO getById(Long id) {

        logger.info("Fetching Todo with ID: {}", id);

        // Retrieve entity or throw exception
        Todo todo = repository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Todo not found in the data."));

        logger.info("Todo found with ID: {}", id);

        return TodoMapper.toDTO(todo);
    }

    /**
     * Updates an existing Todo.
     * - Validates status transition
     * - Updates fields
     */
    public TodoResponseDTO update(Long id, TodoDTO dto) {

        logger.info("Updating Todo with ID: {}", id);

        // Fetch existing Todo
        Todo todo = repository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Todo not found in the data."));

        // Update basic fields
        todo.setTitle(dto.getTitle());
        todo.setDescription(dto.getDescription());

        // Convert status from String → Enum
        Status newStatus = Status.valueOf(dto.getStatus());

        // Validate allowed transitions
        if (!isValid(todo.getStatus(), newStatus)) {
            logger.warn("Invalid status transition for Todo ID: {}", id);
            throw new RuntimeException("Invalid status transition");
        }

        // Apply new status
        todo.setStatus(newStatus);

        logger.info("Todo updated successfully with ID: {}", id);

        // Save updated entity
        return TodoMapper.toDTO(repository.save(todo));
    }

    /**
     * Deletes a Todo by ID.
     * Throws exception if not found.
     */
    public void delete(Long id) {

        logger.info("Deleting Todo with ID: {}", id);

        // Fetch before delete (ensures existence)
        Todo todo = repository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Todo not found, cannot delete"));

        repository.delete(todo);

        logger.info("Todo deleted successfully with ID: {}", id);
    }

    /**
     * Validates allowed status transitions.
     * Only PENDING ↔ COMPLETED is allowed.
     */
    private boolean isValid(Status oldS, Status newS) {
        return (oldS == Status.PENDING && newS == Status.COMPLETED)
                || (oldS == Status.COMPLETED && newS == Status.PENDING);
    }
}