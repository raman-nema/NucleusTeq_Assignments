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

    /**
     * Logger instance used to trace service layer operations
     * and monitor important events during execution.
     */
    private static final Logger logger = LoggerFactory.getLogger(TodoService.class);

    private final TodoRepository repository;
    private final NotificationServiceClient notificationClient;

    /**
     * Constructor-based dependency injection for TodoRepository.
     */
    public TodoService(TodoRepository repository, NotificationServiceClient notificationClient) {
        this.repository = repository;
        this.notificationClient = notificationClient;
    }

    /**
     * Creates a new Todo item.
     * Converts DTO to Entity, saves it, and returns response DTO.
     */
    public TodoResponseDTO create(TodoDTO dto) {

        /**
         * Logs the initiation of Todo creation in the service layer.
         * Helps in tracking the flow of data from controller to persistence.
         */
        logger.info("Processing request to create Todo");

        Todo todo = TodoMapper.toEntity(dto);
        Todo saved = repository.save(todo);

        /**
         * Logs successful persistence of Todo along with generated identifier.
         * Useful for auditing and debugging database operations.
         */
        logger.info("Todo successfully saved with ID: {}", saved.getId());
        // 
        notificationClient.sendNotification("New Todo created with ID: " + saved.getId());
        return TodoMapper.toDTO(saved);
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

        Todo todo = repository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Todo not found in the data."));

        todo.setTitle(dto.getTitle());
        todo.setDescription(dto.getDescription());

        Status newStatus = Status.valueOf(dto.getStatus());

        if (!isValid(todo.getStatus(), newStatus)) {
            throw new RuntimeException("Invalid status transition");
        }

        todo.setStatus(newStatus);

        return TodoMapper.toDTO(repository.save(todo));
    }

    /**
     * Deletes a Todo by its ID.
     */
    public void delete(Long id) {

        Todo todo = repository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Todo not found, cannot delete"));

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
