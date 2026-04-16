# Raman Nema | Java Rest API

## Overview | Description:
This project is a Spring Boot-based REST API designed to demonstrate the development of scalable and maintainable backend services. It provides a structured approach to building web APIs using industry-standard practices.

Built with Java 17 and Spring Boot, the application showcases core backend concepts such as layered architecture, dependency injection, RESTful API design, and centralized exception handling.

The project follows a clean separation of concerns using controller, service, and repository layers, making the codebase easy to understand, test, and extend for future enhancements.

## Data Structure:

### User
    • id: Long
    • name: String
    • age: Integer
    • role: String

## Features:

    • User Search API with dynamic filtering (name, age, role)
    • Case-insensitive search for name and role, exact match for age
    • Structured data submission with basic validation (POST /submit)
    • Delete with confirmation to prevent accidental data removal
    • Layered architecture (Controller → Service → Repository)
    • Global exception handling for consistent error responses
    • Constructor-based dependency injection following Spring best practices


## Tech Stack:

    • Java 17 -- Core programming language 
    • Spring Boot -- Framework for building REST APIs 
    • Maven -- Dependency management and build tool 
    • REST API -- Communication between client and server 
    • IntelliJ IDEA -- Development environment

## Project Structure:
```
Spring_And_REST_Assignment/
├── src/
│   ├── main/
│   │   ├── java/spring_core_assignment/
│   │   │   ├── controller/
│   │   │   ├── service/
│   │   │   ├── repository/
│   │   │   ├── model/
│   │   │   ├── exception/
│   │   │   └── SpringAndRestAssignmentApplication.java
│   │   │
│   │   └── resources/
│   │       └── application.properties
│   │
│   └── test/
│
├── pom.xml
└── README.md
```

## How to Run:

### Prerequisites:
 - Java 17 installed 
 - Maven installed

### Steps:

### Clone the repository git clone
    • <https://github.com/raman-nema/NucleusTeq_Assignments/commits/main/RamanNema_java_training/session_03>

### Navigate to the project directory 
    • cd SpringCoreAssignmentApplication

### Start the application 
    • mvn spring-boot:run

### Access the API using browser or curl
    • http://localhost:8080/users/search

## Key Concepts Used:

• Spring Boot Framework
Used to quickly build and configure a RESTful web application with minimal setup.

• RESTful API Design
Implements standard HTTP methods (GET, POST, DELETE) and follows REST principles for clear and scalable API structure.

• Layered Architecture
Separates application logic into Controller, Service, and Repository layers to ensure maintainability and clear separation of concerns.

• Dependency Injection (Constructor-Based)
Uses constructor injection to manage dependencies, promoting loose coupling and easier testing.

• Inversion of Control (IoC)
Spring manages object creation and lifecycle, reducing manual dependency handling.

• Component Scanning & Annotations
Utilizes annotations like @RestController, @Service, and @Repository for automatic bean detection and configuration.

• Exception Handling
Centralized error handling using @RestControllerAdvice to return consistent and meaningful responses.

• Request Handling
Uses @RequestParam and @RequestBody to handle user inputs effectively in APIs.

• Java Streams & Filtering
Applies stream operations for dynamic and flexible filtering of in-memory data.

## Testing APIs (Using curl)

### 1. Search Users (All Users)
    • curl -X GET http://localhost:8080/users/search

### 2. Search Users with Filters
#### By name
    • curl -X GET "http://localhost:8080/users/search?name=Priya"
#### By age
    • curl -X GET "http://localhost:8080/users/search?age=30"
#### By role
    • curl -X GET "http://localhost:8080/users/search?role=USER"
#### Multiple filters
    • curl -X GET "http://localhost:8080/users/search?age=30&role=USER"

### 3. Submit Structured Data
    • curl -X POST http://localhost:8080/submit \
        -H "Content-Type: application/json" \
        -d '{"name":"John","age":25,"role":"USER"}'

### 4. Delete User (Without Confirmation)
    • curl -X DELETE "http://localhost:8080/users/1"
Response: Confirmation required for deletion.

### 5. Delete User (With Confirmation)
    • curl -X DELETE "http://localhost:8080/users/1?confirm=true"

## OUTPUT and API Endpoints:

### GET /users/search
    • Description: Retrieve users based on optional filters (name, age, role)
    • Behavior:
        – Returns all users if no parameters are provided
        – Applies filtering when query parameters are passed

### POST /submit
    • Description: Submit structured user data
    • Behavior:
        – Accepts JSON input using request body
        – Performs basic validation
        – Returns success or error response

### DELETE /users/{id}
    • Description: Delete a user by ID with confirmation check
    • Behavior:
        – Requires confirm=true to delete
        – If missing or false → returns “Confirmation required”


