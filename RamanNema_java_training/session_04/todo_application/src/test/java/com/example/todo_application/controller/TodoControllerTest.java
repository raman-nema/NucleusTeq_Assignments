package com.example.todo_application.controller;

import com.example.todo_application.dto.TodoDTO;
import com.example.todo_application.dto.TodoResponseDTO;
import com.example.todo_application.service.TodoService;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.ResponseEntity;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class TodoControllerTest {

    @Mock
    private TodoService todoService; // mock service layer

    @InjectMocks
    private TodoController todoController; // controller under test

    // test create API method
    @Test
    void create_shouldReturnCreatedTodo() {

        // input data
        TodoDTO dto = new TodoDTO();
        dto.setTitle("Test Todo");

        // expected response
        TodoResponseDTO expected = new TodoResponseDTO();
        expected.setId(1L);
        expected.setTitle("Test Todo");

        // mock service behavior
        when(todoService.create(dto)).thenReturn(expected);

        // call controller method
        TodoResponseDTO response = todoController.create(dto);

        // check result
        assertEquals(1L, response.getId());
        assertEquals("Test Todo", response.getTitle());

        // verify service call
        verify(todoService).create(dto);
    }

    // test get by id method
    @Test
    void getById_shouldReturnTodo() {

        TodoResponseDTO expected = new TodoResponseDTO();
        expected.setId(1L);
        expected.setTitle("Test Todo");

        when(todoService.getById(1L)).thenReturn(expected);

        TodoResponseDTO response = todoController.getById(1L);

        assertEquals(1L, response.getId());

        verify(todoService).getById(1L);
    }

    // test get all method
    @Test
    void getAll_shouldReturnTodos() {

        TodoResponseDTO item = new TodoResponseDTO();
        item.setId(1L);
        item.setTitle("Test Todo");

        when(todoService.getAll()).thenReturn(List.of(item));

        List<TodoResponseDTO> response = todoController.getAll();

        assertEquals(1, response.size());
        assertEquals("Test Todo", response.get(0).getTitle());

        verify(todoService).getAll();
    }

    // test delete method
    @Test
    void delete_shouldReturnSuccessMessage() {

        ResponseEntity<String> response = todoController.delete(1L);

        // check response message and status
        assertEquals(200, response.getStatusCode().value());
        assertEquals("Todo deleted successfully.", response.getBody());

        // verify delete call
        verify(todoService).delete(1L);
    }
}
