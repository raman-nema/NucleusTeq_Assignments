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

import java.util.Arrays;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class TodoServiceTest {

    // mock dependencies
    @Mock
    private TodoRepository repository;

    @Mock
    private NotificationServiceClient notificationClient;

    // service under test
    @InjectMocks
    private TodoService service;

    private Todo todo;
    private TodoDTO dto;

    @BeforeEach
    void setup() {

        // sample input
        dto = new TodoDTO();
        dto.setTitle("Test Todo");
        dto.setDescription("Test Desc");
        dto.setStatus("PENDING");

        // sample entity
        todo = new Todo();
        todo.setId(1L);
        todo.setTitle("Test Todo");
        todo.setDescription("Test Desc");
        todo.setStatus(Status.PENDING);
    }

    // create test
    @Test
    void testCreate() {

        when(repository.save(any())).thenReturn(todo);

        TodoResponseDTO result = service.create(dto);

        assertNotNull(result);
        assertEquals("Test Todo", result.getTitle());

        verify(repository).save(any());
        verify(notificationClient).sendNotification(anyString());
    }

    // get all test
    @Test
    void testGetAll() {

        when(repository.findAll()).thenReturn(Arrays.asList(todo));

        var list = service.getAll();

        assertEquals(1, list.size());
    }

    // get by id test
    @Test
    void testGetById() {

        when(repository.findById(1L)).thenReturn(Optional.of(todo));

        TodoResponseDTO result = service.getById(1L);

        assertEquals(1L, result.getId());
    }

}