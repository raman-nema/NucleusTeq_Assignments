package com.example.todo_application.dto;

import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

// DTO for request
public class TodoDTO {

    // basic validations check to maintain consistency.
    @NotNull(message = "Title cannot be null")
    @Size(min = 3, message = "Title must be at least 3 characters")
    private String title;

    private String description;
    private String status;

    // Getters and Setters

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }
}