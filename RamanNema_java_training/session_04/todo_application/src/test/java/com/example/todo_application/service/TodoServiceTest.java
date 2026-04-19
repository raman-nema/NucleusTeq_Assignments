package com.example.todo_application.service;

import com.example.todo_application.client.NotificationServiceClient;
import com.example.todo_application.dto.TodoDTO;
import com.example.todo_application.dto.TodoResponseDTO;
import com.example.todo_application.entity.Status;
import com.example.todo_application.entity.Todo;
import com.example.todo_application.exception.ResourceNotFoundException;
import com.example.todo_application.repository.TodoRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class TodoServiceTest {

    @Mock
    private TodoRepository repository;

    @Mock
    private NotificationServiceClient notificationClient;

    @InjectMocks
    private TodoService service;

    private Todo todo;
    private TodoDTO dto;

    @BeforeEach
    void setup() {
        dto = new TodoDTO();
        dto.setTitle("Test Todo");
        dto.setDescription("Test Desc");
        dto.setStatus("PENDING");

        todo = new Todo();
        todo.setId(1L);
        todo.setTitle("Test Todo");
        todo.setDescription("Test Desc");
        todo.setStatus(Status.PENDING);
    }

    @Test
    void testCreate() {
        when(repository.save(any(Todo.class))).thenReturn(todo);

        TodoResponseDTO result = service.create(dto);

        assertNotNull(result);
        assertEquals("Test Todo", result.getTitle());
        verify(repository).save(any(Todo.class));
        verify(notificationClient).sendNotification(any(String.class));
    }

    @Test
    void testGetAll() {
        when(repository.findAll()).thenReturn(List.of(todo));

        List<TodoResponseDTO> list = service.getAll();

        assertEquals(1, list.size());
    }

    @Test
    void testGetById() {
        when(repository.findById(1L)).thenReturn(Optional.of(todo));

        TodoResponseDTO result = service.getById(1L);

        assertEquals(1L, result.getId());
    }

    @Test
    void testGetByIdNotFound() {
        when(repository.findById(1L)).thenReturn(Optional.empty());

        assertThrows(ResourceNotFoundException.class, () -> service.getById(1L));
    }

    @Test
    void testUpdate() {
        when(repository.findById(1L)).thenReturn(Optional.of(todo));
        when(repository.save(any(Todo.class))).thenAnswer(inv -> inv.getArgument(0));

        dto.setStatus("COMPLETED");
        TodoResponseDTO result = service.update(1L, dto);

        assertEquals(Status.COMPLETED, result.getStatus());
    }

    @Test
    void testDelete() {
        when(repository.findById(1L)).thenReturn(Optional.of(todo));

        service.delete(1L);

        verify(repository).delete(todo);
    }

    @Test
    void testDeleteNotFound() {
        when(repository.findById(1L)).thenReturn(Optional.empty());

        assertThrows(ResourceNotFoundException.class, () -> service.delete(1L));
        verify(repository, never()).delete(any(Todo.class));
    }
}
