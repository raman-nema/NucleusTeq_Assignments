# Raman Nema | Java spring core

## Overview | Description:

The User Management System is a Spring Boot-based web application designed to efficiently manage user data. It supports Create and Read operation operations through RESTful APIs in a structured and scalable way.

Built using Java 17 and Spring Boot, this project focuses on implementing core backend development concepts such as layered architecture, dependency injection, REST API design, and exception handling.

The application ensures clean separation of concerns using controller, service, and repository layers, making it easy to maintain and extend.

## Data Structure:

User:
 - id: Long  
 - name: String  
 - email: String

## Features:

• User Creation Allows adding new users to the system.

• Get All Users Fetches all users stored in the system.

• Get User By ID Retrieves a specific user using a unique identifier.

• Exception Handling Handles cases where a user is not found using
custom exceptions.

• Notification Component Demonstrates use of component-based design.

• Layered Architecture Separates logic into Controller, Service,
Repository, and Model layers.


## Tech Stack:

    • Java 17 -- Core programming language 
    • Spring Boot -- Framework for building REST APIs 
    • Maven -- Dependency management and build tool 
    • REST API -- Communication between client and server 
    • IntelliJ IDEA -- Development environment

## Project Structure:
```
spring-boot-user-management/
├── src/
│   ├── main/
│   │   ├── java/spring_core_assignment/
│   │   │   ├── controller/
│   │   │   ├── service/
│   │   │   ├── repository/
│   │   │   ├── model/
│   │   │   ├── exception/
│   │   │   ├── component/
│   │   │   └── SpringCoreAssignmentApplication.java
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
    • <https://github.com/raman-nema/NucleusTeq_Assignments/commits/main/RamanNema_java_training/session_02\>

### Navigate to the project directory 
    • cd SpringCoreAssignmentApplication

### Start the application 
    • mvn spring-boot:run

### Access the API using browser or curl
    • http://localhost:8080/users

## Key Concepts Used:

• Dependency Injection Used to manage object creation and dependencies using Spring.

• REST API Development Implemented using \@RestController and HTTP methods.

• Layered Architecture Separates controller, service, and repository logic for better maintainability.

• Exception Handling Custom exception (UserNotFoundException) is used to handle cases where a user is not found.

    - Short Explanation: If a user is requested with an ID that does not exist, the system throws a custom exception and returns an appropriate error message.

    - Detailed Explanation: A custom exception class \`UserNotFoundException\` is created to handle invalid user requests. When a user is not found in the repository, this exception is thrown from the service layer. This ensures that the application does not crash and instead returns ameaningful response to the client.

• Notification Component A NotificationComponent is used to simulate
sending notifications when user-related operations are performed.

    - Short Explanation: Used to trigger a notification when a user is created.

    - Detailed Explanation: The NotificationComponent is a Spring-managed component that is injected into the service layer. It is used to demonstrate component-based design and loose coupling. Whenever a user is successfully created, this component is invoked to perform additional logic such as logging or sending notifications.

## Testing APIs (Using curl)

### 1. Get All Users 
    • curl -X GET http://localhost:8080/users \

### 2. Create User
    • curl -X POST http://localhost:8080/users \  
      -H "Content-Type: application/json \" 
      -d '{"name":"JohnDoe","email":"john@example.com"}'

### 3. Get User By ID
    • curl -X GET http://localhost:8080/users/1

### 4. Trigger Notification
    • curl -X GET http://localhost:8080/notify

### 5. Get Message (SHORT) 
    • curl -X GET "http://localhost:8080/message?type=SHORT\"

### 6. Get Message (LONG)
    • curl -X GET "http://localhost:8080/message?type=LONG\"



## OUTPUT and API Endpoints:

###   GET /users
    • Description: Get all users

### POST /users 
    • Description: Create a new user

###  GET /users/{id}
    • Description: Get user by ID

###  GET /notify 
    • Description: Trigger notification

###   GET /message?type=SHORT/LONG 
    • Description: Get formatted message
