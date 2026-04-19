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

    // mock dependencies (simulate DB and external service)
    @Mock
    private TodoRepository repository;

    @Mock
    private NotificationServiceClient notificationClient;

    // actual service to test
    @InjectMocks
    private TodoService service;

    private Todo todo;
    private TodoDTO dto;

    @BeforeEach
    void setup() {

        // sample input DTO
        dto = new TodoDTO();
        dto.setTitle("Test Todo");
        dto.setDescription("Test Desc");
        dto.setStatus("PENDING");

        // sample entity object
        todo = new Todo();
        todo.setId(1L);
        todo.setTitle("Test Todo");
        todo.setDescription("Test Desc");
        todo.setStatus(Status.PENDING);
    }

    // test create method
    @Test
    void testCreate() {

        // mock save behavior
        when(repository.save(any())).thenReturn(todo);

        // call service method
        TodoResponseDTO result = service.create(dto);

        // verify response
        assertNotNull(result);
        assertEquals("Test Todo", result.getTitle());

        // verify interactions
        verify(repository).save(any());
        verify(notificationClient).sendNotification(anyString());
    }

    // test getAll method
    @Test
    void testGetAll() {

        // mock findAll
        when(repository.findAll()).thenReturn(Arrays.asList(todo));

        // call method
        var list = service.getAll();

        // verify result
        assertEquals(1, list.size());
    }

    // test getById method
    @Test
    void testGetById() {

        // mock findById
        when(repository.findById(1L)).thenReturn(Optional.of(todo));

        // call method
        TodoResponseDTO result = service.getById(1L);

        // verify result
        assertEquals(1L, result.getId());
    }

    // test when todo is not found
    @Test
    void testGetById_NotFound() {

        // return empty
        when(repository.findById(1L)).thenReturn(Optional.empty());

        // expect exception
        assertThrows(ResourceNotFoundException.class,
                () -> service.getById(1L));
    }

    // test update method
    @Test
    void testUpdate() {

        // mock existing todo and save
        when(repository.findById(1L)).thenReturn(Optional.of(todo));
        when(repository.save(any())).thenReturn(todo);

        // update status in DTO
        dto.setStatus("COMPLETED");

        // call update
        TodoResponseDTO result = service.update(1L, dto);

        // verify updated status
        assertEquals(Status.COMPLETED, result.getStatus());
    }

    // test delete method
    @Test
    void testDelete() {

        // mock existing todo
        when(repository.findById(1L)).thenReturn(Optional.of(todo));

        // call delete
        service.delete(1L);

        // verify delete operation
        verify(repository).delete(todo);
    }

}