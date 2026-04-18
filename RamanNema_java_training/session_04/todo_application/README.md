# Raman Nema | Java (SpringBoot) Todo Application 

## Overview

This project is a Spring Boot-based REST API designed to manage Todo tasks as part of the Java Training — Session 4 assignment. It demonstrates the development of scalable and maintainable backend services following industry-standard practices.

Built with Java 17 and Spring Boot, the application showcases core backend concepts including layered architecture, dependency injection, RESTful API design, JPA-based persistence, and centralized exception handling.

The project follows a clean separation of concerns using controller, service, and repository layers, making the codebase straightforward to understand, test, and extend.

---

## Data Structure

### Todo

    - id          : Long
    - title       : String
    - description : String
    - status      : Enum (PENDING / COMPLETED)
    - createdAt   : LocalDateTime

---

## Features

    - Create, retrieve, update, and delete Todo tasks
    - Default status set to PENDING on creation
    - Status transition validation (PENDING to COMPLETED and vice versa)
    - Automatic server-side assignment of createdAt timestamp
    - Input validation using Jakarta Bean Validation (@NotNull, @Size)
    - DTO layer to prevent direct entity exposure in API responses
    - Manual DTO to Entity and Entity to DTO conversion
    - Layered architecture (Controller -> Service -> Repository)
    - Global exception handling for consistent error responses
    - Constructor-based dependency injection following Spring best practices
    - H2 in-memory database — no external database setup required

---

## Tech Stack

    - Java 17          -- Core programming language
    - Spring Boot 3.x  -- Framework for building REST APIs
    - Spring Data JPA  -- Data access and repository abstraction
    - Hibernate        -- ORM implementation
    - H2 Database      -- In-memory database for runtime use
    - Maven            -- Dependency management and build tool
    - IntelliJ IDEA    -- Development environment

---

## Project Structure

```
todo_application/
└── src/
    ├── main/
    │   ├── java/com/example/todo_application/
    │   │   ├── controller/
    │   │   │   └── TodoController.java
    │   │   ├── service/
    │   │   │   └── TodoService.java
    │   │   ├── repository/
    │   │   │   └── TodoRepository.java
    │   │   ├── entity/
    │   │   │   ├── Todo.java
    │   │   │   └── Status.java
    │   │   ├── dto/
    │   │   │   ├── TodoDTO.java
    │   │   │   └── TodoResponseDTO.java
    │   │   ├── exception/
    │   │   │   ├── ResourceNotFoundException.java
    │   │   │   └── GlobalExceptionHandler.java
    │   │   ├── mapper/
    │   │   │   └── TodoMapper.java
    │   │   └── TodoApplication.java
    │   └── resources/
    │       └── application.properties
    └── test/
        └── (test classes)
├── pom.xml
└── README.md
```

---

## How to Run

### Prerequisites

    - Java 17 installed
    - Maven installed

### Steps

#### Clone the repository
    - https://github.com/raman-nema/NucleusTeq_Assignments/tree/main/RamanNema_java_training/session_04/

# Navigate to the project directory
    - cd todo_application

#### Build the project
    - mvn clean install

#### Start the application
    - mvn spring-boot:run

#### Access the API using browser or curl
    - http://localhost:8080/todos

---

## Key Concepts Used

**Spring Boot Framework**
Used to quickly build and configure a RESTful web application with minimal boilerplate setup.

**RESTful API Design**
Implements standard HTTP methods (GET, POST, PUT, DELETE) and follows REST principles for a clear and scalable API structure.

**Layered Architecture**
Separates application logic into Controller, Service, and Repository layers to ensure maintainability and a clear separation of concerns. No business logic exists inside the Controller.

**JPA and Hibernate**
Uses @Entity, @Id, and @Table annotations for object-relational mapping. JpaRepository is used for all data access operations.

**DTO Layer**
Introduces a dedicated DTO class to decouple the API contract from the internal entity model. All conversions are done manually without external mapping libraries.

**Dependency Injection (Constructor-Based)**
Uses constructor injection throughout the application to manage dependencies, promoting loose coupling and easier unit testing.

**Inversion of Control (IoC)**
Spring manages object creation and lifecycle, reducing the need for manual dependency handling.

**Component Scanning and Annotations**
Utilizes annotations such as @RestController, @Service, @Repository, and @Entity for automatic bean detection and configuration.

**Validation**
Uses @Valid along with @NotNull and @Size on the DTO to enforce input rules before any business logic executes.

**Exception Handling**
Centralized error handling using @RestControllerAdvice to return consistent and meaningful HTTP error responses across all endpoints.

**Status Transition Validation**
Business logic in the service layer validates that only allowed status transitions are processed. Invalid transitions return a 400 Bad Request response.

---

## Testing APIs (Using curl)

### 1. Create a Todo
    - curl -X POST http://localhost:8080/todos \
        -H "Content-Type: application/json" \
        -d '{"title":"Buy groceries","description":"Milk, Eggs, Bread","status":"PENDING"}'

### 2. Get All Todos
    - curl -X GET http://localhost:8080/todos

### 3. Get Todo by ID
    - curl -X GET http://localhost:8080/todos/1

### 4. Update a Todo
    - curl -X PUT http://localhost:8080/todos/1 \
        -H "Content-Type: application/json" \
        -d '{"title":"Buy groceries","description":"Updated list","status":"COMPLETED"}'

### 5. Delete a Todo
    - curl -X DELETE http://localhost:8080/todos/1

---

## Status Transition Rules

    - PENDING   -> COMPLETED : Allowed
    - COMPLETED -> PENDING   : Allowed
    - Any other transition   : Not allowed — returns 400 Bad Request

---

## API Endpoints and Output

### POST /todos
    - Description : Create a new Todo task
    - Behavior    :
        - Accepts JSON input using request body with @Valid
        - Sets createdAt automatically on the server side
        - Defaults status to PENDING if not provided
        - Returns the created Todo with HTTP 201

### GET /todos
    - Description : Retrieve all Todo tasks
    - Behavior    :
        - Returns a list of all todos
        - Returns an empty list if no todos exist

### GET /todos/{id}
    - Description : Retrieve a single Todo by its ID
    - Behavior    :
        - Returns the matching Todo if found
        - Returns 404 Not Found if the ID does not exist

### PUT /todos/{id}
    - Description : Update an existing Todo by its ID
    - Behavior    :
        - Accepts updated title, description, and status
        - Validates status transition before applying update
        - Returns 400 Bad Request for invalid transitions
        - Returns 404 Not Found if the ID does not exist

### DELETE /todos/{id}
    - Description : Delete a Todo by its ID
    - Behavior    :
        - Permanently removes the Todo from the system
        - Returns 404 Not Found if the ID does not exist

---

## Author
Raman Nema

---