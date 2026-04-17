package com.example.todo_application.entity;

import ch.qos.logback.core.status.Status;
import jakarta.persistence.*;
import java.time.LocalDateTime;

// Marks this class as a JPA Entity
@Entity
@Table(name = "todos")
public class Todo {

    // Primary Key
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String title;
    private String description;

    // Enum stored as String in DB
    @Enumerated(EnumType.STRING)
    private Status status;

    // Timestamp when todo is created
    private LocalDateTime createdAt;

    // Getters and Setters

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

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

    public Status getStatus() {
        return status;
    }

    public void setStatus(Status status) {
        this.status = status;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }
}