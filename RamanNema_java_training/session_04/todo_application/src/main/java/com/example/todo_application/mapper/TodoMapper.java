package com.example.todo_application.mapper;

import com.example.todo_application.dto.TodoDTO;
import com.example.todo_application.dto.TodoResponseDTO;
import com.example.todo_application.entity.Todo;
import com.example.todo_application.entity.Status;

import java.time.LocalDateTime;

// Manual mapping class
public class TodoMapper {

    // DTO -> Entity
    public static Todo toEntity(TodoDTO dto) {

        Todo todo = new Todo();

        todo.setTitle(dto.getTitle());
        todo.setDescription(dto.getDescription());

        if (dto.getStatus() == null) {
            todo.setStatus(Status.PENDING);
        } else {
            todo.setStatus(Status.valueOf(dto.getStatus()));
        }

        todo.setCreatedAt(LocalDateTime.now());

        return todo;
    }

    // Entity -> DTO
    public static TodoResponseDTO toDTO(Todo todo) {

        TodoResponseDTO dto = new TodoResponseDTO();

        dto.setId(todo.getId());
        dto.setTitle(todo.getTitle());
        dto.setDescription(todo.getDescription());
        dto.setStatus(todo.getStatus());
        dto.setCreatedAt(todo.getCreatedAt());

        return dto;
    }
}