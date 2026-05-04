# ReimburseHub

A full-stack reimbursement management application built with Spring Boot, PostgreSQL, and a multi-page frontend using HTML, CSS, and JavaScript.

## 1. Project Overview

ReimburseHub is an enterprise-style web application designed to digitize and streamline employee claim and reimbursement workflows. In many organizations, reimbursement requests are handled through manual forms, emails, spreadsheets, or fragmented approval processes. This leads to delayed approvals, poor visibility, inconsistent audit trails, and limited reporting.

This system provides a centralized platform where employees can submit reimbursement claims, managers can review and approve or reject claims, and administrators can manage users, roles, and organization-wide claim data.

The frontend is implemented as a lightweight browser-based dashboard experience with separate pages for login, admin operations, manager review workflows, and employee claim submission. It communicates with the backend through REST APIs exposed under the `/api` base path.

### Real-World Use Case

The application is suitable for organizations that need a structured internal portal for expense reimbursement, employee claim tracking, managerial review, and administrative oversight.

### Target Users

| User Type | Responsibilities |
|---|---|
| Admin | Manage users, view all claims, oversee system-wide reimbursement activity |
| Manager | Review claims assigned to them, approve or reject employee submissions |
| Employee | Submit reimbursement claims and track claim status |


### Key Objectives

- Provide a secure authentication and authorization model.
- Implement role-based access for Admin, Manager, and Employee users.
- Support claim submission, review, approval, rejection, and tracking.
- Expose REST APIs for frontend and future integration clients.
- Maintain a clean layered backend architecture.
- Use PostgreSQL for reliable relational data persistence.
- Provide a maintainable foundation for future enterprise enhancements.

## 2. System Architecture

The application follows a layered architecture that separates request handling, business logic, persistence, data transfer, and security concerns.

```text
Client Browser
    |
    | HTTP Requests
    v
Frontend: HTML, CSS, JavaScript
    |
    | index.html, admin.html, manager.html, employee.html
    |
    | REST API Calls
    v
Spring Boot Backend
    |
    | Controller Layer
    v
Service Layer
    |
    | Repository Layer
    v
PostgreSQL Database
```

### Controller Layer

The controller layer is responsible for receiving HTTP requests, validating request entry points, delegating operations to the service layer, and returning standardized API responses.

Key responsibilities:

- Define REST API endpoints.
- Accept request payloads and path variables.
- Delegate business operations to services.
- Return consistent response structures using DTOs.
- Keep HTTP-specific concerns separate from business logic.

Primary controllers:

| Controller | Responsibility |
|---|---|
| `AuthController` | Handles authenticated-user lookup |
| `UserController` | Handles user creation, retrieval, manager-employee lookup, and deletion |
| `ClaimController` | Handles claim submission, claim retrieval, filtering, and reviewer actions |

### Frontend Layer

The frontend is organized as a simple multi-page application without a build framework. Each page loads shared JavaScript utilities and page-specific logic.

| File | Responsibility |
|---|---|
| `index.html` | Login screen |
| `admin.html` | Admin dashboard for user management and all-claims review |
| `manager.html` | Manager dashboard for assigned claims and approval or rejection actions |
| `employee.html` | Employee dashboard for submitting claims and viewing claim history |
| `js/auth.js` | Session handling, role-based redirection, route guards, and sidebar population |
| `js/api.js` | Centralized REST API client and shared UI utility functions |
| `js/claims.js` | Claim submission, claim rendering, manager actions, and employee claim history |
| `js/dashboard.js` | Admin dashboard, user filtering, pagination, user creation, deletion, and claim actions |
| `js/employee.js` | Employee page initialization and tab switching |
| `js/manager.js` | Manager page initialization and assigned-claim loading |

The frontend uses `fetch()` for HTTP communication, `localStorage` for the current session, role-based page guards, dynamic DOM rendering, loading skeletons, toast messages, modal dialogs, filters, and pagination.

### Service Layer

The service layer contains the core business logic of the application. It coordinates validation, authorization rules, entity creation, status transitions, and repository operations.

Key responsibilities:

- Validate business rules.
- Manage user creation and manager assignment.
- Manage claim submission and reviewer assignment.
- Enforce claim action rules.
- Prevent invalid claim status transitions.
- Coordinate repository access.

Examples of service-level rules:

- Claim amount must be greater than zero.
- Claim description is required.
- A rejected claim must include a reviewer comment.
- A processed claim cannot be approved or rejected again.
- A claim can be actioned only by the assigned reviewer or an admin.
- If an employee has a manager, the manager becomes the reviewer.
- If an employee has no manager, an admin is assigned as fallback reviewer.

### Repository and Database Interaction

The repository layer uses Spring Data JPA to abstract database operations. Repository interfaces provide standard CRUD operations and custom finder methods without requiring repetitive SQL implementation.

Key repositories:

| Repository | Purpose |
|---|---|
| `UserRepository` | Persists users and provides lookup operations by email, role, manager, and ID |
| `ClaimRepository` | Persists claims and provides lookup operations by employee, reviewer, and status |

PostgreSQL acts as the primary relational database. Hibernate maps Java entity classes to database tables and manages schema updates during development.

### DTO Mapping

DTOs, or Data Transfer Objects, are used to separate internal persistence models from external API contracts.

Benefits of DTO mapping:

- Prevents exposing entity internals directly through APIs.
- Allows API payloads to evolve independently from database entities.
- Improves request and response validation.
- Reduces accidental serialization of sensitive fields such as passwords.
- Provides clean, predictable API responses to frontend clients.

DTO categories:

| DTO Type | Purpose |
|---|---|
| Request DTOs | Capture incoming client payloads |
| Response DTOs | Return controlled response objects to clients |
| Standard API Response | Wrap success status, message, and data consistently |

### Security Layer and Authentication Flow

The project currently includes Spring Security configuration, BCrypt password hashing, role-aware frontend routing, and Basic Auth-style frontend headers for local development. For production readiness, the intended security model is JWT-based authentication with token validation and endpoint-level authorization.

#### Current Development Flow

In the current frontend implementation:

1. The login form collects email and password.
2. The frontend sends a Basic Auth-style `Authorization` header while requesting users.
3. The matching user profile is stored in `localStorage`.
4. Role guards redirect users to `admin.html`, `manager.html`, or `employee.html`.
5. API requests attach the stored token value to subsequent requests.

Current header style:

```http
Authorization: Basic <base64-email-password>
```
Temporary development-only authentication simulation (not secure, must not be used in production).
This implementation is strictly for local testing and demonstration purposes.
Passwords or reusable credentials must never be stored in localStorage in a production system.


### End-to-End Request Lifecycle

The following lifecycle describes how a production JWT-secured request should be processed:

1. The user logs in from the frontend.
2. The backend validates credentials and returns a JWT.
3. The frontend stores the token for the session.
4. The user performs an operation, such as submitting a claim.
5. The frontend sends a REST request with the JWT in the `Authorization` header.
6. The security filter validates the token.
7. The controller receives the request and delegates to the service layer.
8. The service layer applies validation and business rules.
9. The repository layer persists or retrieves data from PostgreSQL.
10. The mapper converts entities into response DTOs.
11. The controller returns a standardized API response.
12. The frontend updates the dashboard or view based on the response.

## 3. Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| Backend Language | Java 17 | Primary programming language for backend development |
| Backend Framework | Spring Boot | Application framework for REST APIs and dependency management |
| Web Layer | Spring Web MVC | REST controller and HTTP request handling |
| Security | Spring Security | Authentication and authorization foundation |
| Current Frontend Authentication | Basic Auth-style header and local session data | Local development login flow |
| Password Security | BCrypt | Secure password hashing |
| Persistence | Spring Data JPA | Repository abstraction and ORM integration |
| ORM | Hibernate | Entity mapping and database interaction |
| Database | PostgreSQL | Relational data storage |
| Frontend | HTML, CSS, JavaScript | Multi-page browser dashboard |
| Build Tool | Maven | Dependency management, build, and test execution |
| Testing | JUnit 5, Mockito, Spring Boot Test | Unit and integration testing |
| Test Database | H2 | Lightweight database for isolated test execution |
| Coverage | JaCoCo | Code coverage reporting |
| API Testing | Postman or similar tool | Manual API validation and documentation support |
| Version Control | Git | Source control and collaboration |

## 4. Features

### Authentication Features

- User registration through user creation APIs.
- Login workflow for authenticated access.
- Password hashing using BCrypt.
- Basic Auth-style local development flow.
- JWT-ready production authentication model.
- Authenticated user context retrieval.
- Session handling and role-based redirection from the frontend.

### Authorization Features

- Role-based access model with Admin, Manager, and Employee roles.
- Admin-level visibility across users and claims.
- Manager-level access to assigned employee claims.
- Employee-level claim submission and claim tracking.
- Reviewer-based claim approval and rejection rules.
- Admin override capability for claim actions.

### Business Logic Features

- Create and manage users.
- Assign employees to managers.
- Submit reimbursement claims.
- Automatically assign reviewers to claims.
- Retrieve claims by employee.
- Retrieve claims by reviewer.
- Filter claims by status.
- Approve submitted claims.
- Reject submitted claims with mandatory comments.
- Prevent duplicate processing of already reviewed claims.

### System Features

- REST API architecture.
- Layered backend design.
- Standardized API response structure.
- Centralized exception handling.
- DTO-based request and response contracts.
- PostgreSQL-backed persistence.
- CORS configuration for frontend integration.
- Dashboard-oriented frontend pages.
- Admin, manager, and employee page-specific JavaScript modules.
- Toast notifications, modal dialogs, loading skeletons, filtering, and pagination.
- Unit and integration test support.
- JaCoCo code coverage reporting.

## 5. Database Design

The application uses a relational database model suitable for user management, role-based access, and reimbursement claim workflows.

### Key Entities

#### User

Represents an application user.

Important fields:

| Field | Description |
|---|---|
| `id` | Unique user identifier |
| `name` | User full name |
| `email` | Unique email address used for login |
| `password` | Hashed password |
| `role` | User role: Admin, Manager, or Employee |
| `manager` | Optional manager relationship for employee users |

#### Claim

Represents a reimbursement claim submitted by an employee.

Important fields:

| Field | Description |
|---|---|
| `id` | Unique claim identifier |
| `amount` | Reimbursement amount |
| `description` | Claim description |
| `date` | Submission date |
| `status` | Claim status |
| `employee` | User who submitted the claim |
| `reviewer` | Manager or admin assigned to review the claim |
| `comment` | Reviewer comment, especially required for rejection |

### Entity Relationships

| Relationship | Description |
|---|---|
| User to Manager | Many employees can report to one manager |
| User to Claim | One employee can submit many claims |
| Reviewer to Claim | One manager or admin can review many claims |

### High-Level Schema Overview

```text
users
-----
id
name
email
password
role
manager_id

claims
------
id
amount
description
date
status
employee_id
reviewer_id
comment
```
### Constraints:
- email UNIQUE
- amount > 0
- status NOT NULL
- foreign keys enforced between claims and users

### Role of PostgreSQL

PostgreSQL is used as the primary persistent datastore. It provides relational integrity, indexing support, transactional reliability, and structured query capabilities for users, claims, roles, and approval workflows.

## 6. API Design

The backend exposes RESTful APIs under the `/api` base path.

### Current Authentication API

| Method | Endpoint | Description | Access Level |
|---|---|---|---|
| `GET` | `/api/auth/me` | Fetch currently authenticated user details | Authenticated |

### Recommended Production Authentication APIs

The following endpoints are recommended for a complete JWT implementation:

| Method | Endpoint | Description | Access Level |
|---|---|---|---|
| `POST` | `/api/auth/login` | Authenticate a user and return a JWT | Public |
| `POST` | `/api/auth/register` | Register a new user account | Public or Admin |
| `POST` | `/api/auth/refresh` | Issue a new access token using a refresh token | Authenticated |
| `POST` | `/api/auth/logout` | Invalidate or clear the active session | Authenticated |

### User Management APIs

| Method | Endpoint | Description | Access Level |
|---|---|---|---|
| `POST` | `/api/users` | Create a new user | Admin |
| `GET` | `/api/users` | Fetch all users | Admin |
| `GET` | `/api/users/{id}` | Fetch user details by ID | Admin or Same User |
| `GET` | `/api/users/manager/{managerId}` | Fetch employees assigned to a manager | Admin or Manager |
| `DELETE` | `/api/users/{id}` | Delete a user by ID | Admin |

### Claim and Reimbursement APIs

| Method | Endpoint | Description | Access Level |
|---|---|---|---|
| `POST` | `/api/claims` | Submit a new reimbursement claim | Employee |
| `GET` | `/api/claims` | Fetch all claims | Admin |
| `GET` | `/api/claims/employee/{employeeId}` | Fetch claims submitted by an employee | Admin, Manager, or Same Employee |
| `GET` | `/api/claims/reviewer/{reviewerId}` | Fetch claims assigned to a reviewer | Admin or Manager |
| `GET` | `/api/claims/status/{status}` | Fetch claims by status | Admin or Manager |
| `PUT` | `/api/claims/{claimId}/action/{reviewerId}` | Approve or reject a claim | Admin or Assigned Reviewer |

### Frontend API Client Mapping

The frontend centralizes backend communication in `js/api.js`.

| Frontend Function | Backend Endpoint | Purpose |
|---|---|---|
| `getAllUsers()` | `GET /api/users` | Load users for admin dashboard and login flow |
| `getUserById(id)` | `GET /api/users/{id}` | Refresh user profile and manager assignment |
| `createUserApi(payload)` | `POST /api/users` | Create Admin, Manager, or Employee users |
| `deleteUserApi(id)` | `DELETE /api/users/{id}` | Remove a user |
| `getUsersByManager(managerId)` | `GET /api/users/manager/{managerId}` | Load employees assigned to a manager |
| `getAllClaims()` | `GET /api/claims` | Load all claims for admin dashboard |
| `getClaimsByEmployee(employeeId)` | `GET /api/claims/employee/{employeeId}` | Load employee claim history |
| `getClaimsByReviewer(reviewerId)` | `GET /api/claims/reviewer/{reviewerId}` | Load manager assigned claims |
| `getClaimsByStatus(status)` | `GET /api/claims/status/{status}` | Filter claims by status |
| `submitClaimApi(payload)` | `POST /api/claims` | Submit a reimbursement claim |
| `takeClaimAction(claimId, reviewerId, status, comment)` | `PUT /api/claims/{claimId}/action/{reviewerId}` | Approve or reject a claim |

### Claim Status Values

| Status | Description |
|---|---|
| `SUBMITTED` | Claim has been submitted and is waiting for review |
| `APPROVED` | Claim has been approved |
| `REJECTED` | Claim has been rejected with reviewer comments |

## 7. Installation and Setup

### Prerequisites

Ensure the following tools are installed:

- Java 17 or later
- Maven 3.9 or later, or the included Maven wrapper
- PostgreSQL 14 or later
- Git
- A modern web browser
- Optional: Postman or another API testing tool

### Clone the Repository

```bash
git clone https://github.com/raman-nema/NucleusTeq_Assignments/tree/main/RamanNema_Capstone_Reimbursement_Portal
cd RamanNema_Capstone_Reimbursement_Portal
```

### Backend Setup Using Maven

Navigate to the backend application directory:

```bash
cd backEnd/Reimbursement_Portal
```

Install dependencies and build the project:

```bash
./mvnw clean install
```

For Windows:

```bash
mvnw.cmd clean install
```

### PostgreSQL Database Setup

Log in to PostgreSQL and create the application database:

```sql
CREATE DATABASE reimbursement_db;
```

Optional example for creating a dedicated database user:

```sql
CREATE USER reimbursement_user WITH PASSWORD 'change_me';
GRANT ALL PRIVILEGES ON DATABASE reimbursement_db TO reimbursement_user;
```

### Environment Configuration

Update the backend configuration file:

```text
backEnd/Reimbursement_Portal/src/main/resources/application.properties
```

Example configuration:

```properties
spring.application.name=Reimbursement_Portal

spring.datasource.url=jdbc:postgresql://localhost:5432/reimbursement_db
spring.datasource.username=<your-postgres-username>
spring.datasource.password=<your-postgres-password>

spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true

server.port=8080

logging.level.org.springframework=INFO
```

For a production environment, avoid hardcoding secrets in source files. Use environment variables, externalized configuration, or a secrets manager.

Recommended production-style configuration keys:

```properties
jwt.secret=<strong-secret-key>
jwt.expiration-ms=3600000
```

### Run the Application

Start the Spring Boot backend:

```bash
./mvnw spring-boot:run
```

The backend will be available at:

```text
http://localhost:8080
```

### Run the Frontend

The frontend is located in:

```text
frontEnd/
```

Open the login page in a browser:

```text
frontEnd/index.html
```

Ensure the frontend API base URL points to the backend:

```javascript
const API_BASE = 'http://localhost:8080/api';
```

The application pages are:

| Page | Purpose |
|---|---|
| `index.html` | Login page |
| `admin.html` | Admin dashboard for users and all claims |
| `manager.html` | Manager dashboard for assigned claims |
| `employee.html` | Employee dashboard for claim submission and history |

## 8. Usage Guide

### Register a User

Create a user by sending a request to the user creation API.

Example request:

```http
POST /api/users
Content-Type: application/json
```

Example payload:

```json
{
  "name": "Raman Nema",
  "email": "raman@example.com",
  "password": "password123",
  "role": "EMPLOYEE",
  "managerId": 2
}
```

### Login in the Current Frontend

The current frontend login flow is implemented in `js/auth.js` and `js/index.js`. It sends a Basic Auth-style header, fetches users, matches the entered email, stores session values in `localStorage`, and redirects the user based on role.

Current development header:

```http
Authorization: Basic <base64-email-password>
```

Current role-based redirects:

| Role | Redirect Page |
|---|---|
| `ADMIN` | `admin.html` |
| `MANAGER` | `manager.html` |
| `EMPLOYEE` | `employee.html` |

Important security note: storing raw passwords or reusable Basic Auth credentials in `localStorage` should be avoided in production.

### Login and Obtain JWT in Production

Example request:

```http
POST /api/auth/login
Content-Type: application/json
```

Example payload:

```json
{
  "email": "raman@example.com",
  "password": "password123"
}
```

Example response:

```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "token": "<jwt-token>",
    "tokenType": "Bearer",
    "role": "EMPLOYEE"
  }
}
```

### Access Secured Endpoints

In a production JWT-enabled configuration, use the JWT in the `Authorization` header:

```http
Authorization: Bearer <jwt-token>
```

Example secured request:

```http
GET /api/auth/me
Authorization: Bearer <jwt-token>
```

For the current development frontend, API requests are sent through `apiFetch()` in `js/api.js`, which attaches the stored Basic Auth-style token to the `Authorization` header.

### Perform Key Operations

#### Submit a Claim

```http
POST /api/claims
Authorization: Bearer <jwt-token>
Content-Type: application/json
```

```json
{
  "employeeId": 1,
  "amount": 2500.00,
  "description": "Client travel reimbursement"
}
```

#### View Claims for an Employee

```http
GET /api/claims/employee/1
Authorization: Bearer <jwt-token>
```

#### Approve a Claim

```http
PUT /api/claims/10/action/2
Authorization: Bearer <jwt-token>
Content-Type: application/json
```

```json
{
  "status": "APPROVED",
  "comment": "Approved after verification"
}
```

#### Reject a Claim

```http
PUT /api/claims/10/action/2
Authorization: Bearer <jwt-token>
Content-Type: application/json
```

```json
{
  "status": "REJECTED",
  "comment": "Receipt is missing"
}
```

## 9. Security Implementation

### Current Implementation

The current implementation provides the following security-related foundations:

- BCrypt password hashing on the backend.
- Spring Security configuration.
- A custom user details service.
- CORS configuration for frontend-to-backend communication.
- Frontend route guards based on the logged-in user's role.
- Basic Auth-style headers for local development API calls.
- Frontend session data stored in `localStorage`.

The current frontend session model is useful for demonstrating role-based screens and workflows, but it should be hardened before production deployment.

### Role-Based Authorization

Role-based authorization ensures users can access only the operations relevant to their role.

| Role | Intended Permissions |
|---|---|
| Admin | Manage users, view all claims, approve or reject any claim |
| Manager | View and action claims assigned to them |
| Employee | Submit claims and view their own claims |

## 10. Project Structure

```text
RamanNema_Capstone_Reimbursement_Portal/
├── backEnd/
│   └── Reimbursement_Portal/
│       ├── src/
│       │   ├── main/
│       │   │   ├── java/com/example/Reimbursement_Portal/
│       │   │   │   ├── config/
│       │   │   │   ├── controller/
│       │   │   │   ├── dto/
│       │   │   │   │   ├── Request/
│       │   │   │   │   └── Response/
│       │   │   │   ├── entity/
│       │   │   │   ├── enums/
│       │   │   │   ├── exception/
│       │   │   │   ├── mapper/
│       │   │   │   ├── repository/
│       │   │   │   ├── service/
│       │   │   │   ├── service/impl/
│       │   │   │   └── util/
│       │   │   └── resources/
│       │   │       └── application.properties
│       │   └── test/
│       ├── docs/
│       ├── scripts/
│       ├── pom.xml
│       └── mvnw
└── frontEnd/
    ├── index.html
    ├── admin.html
    ├── manager.html
    ├── employee.html
    ├── css/
    │   └── styles.css
    └── js/
        ├── api.js
        ├── auth.js
        ├── claims.js
        ├── dashboard.js
        ├── employee.js
        ├── index.js
        └── manager.js
```

### Key Backend Packages

| Package | Description |
|---|---|
| `config` | Security, CORS, password encoder, user details, and request logging configuration |
| `controller` | REST controllers that expose application endpoints |
| `dto` | Request and response models used by APIs |
| `entity` | JPA entity classes mapped to database tables |
| `enums` | Enumerations such as user roles and claim statuses |
| `exception` | Custom exceptions and centralized exception handling |
| `mapper` | Entity-to-DTO and DTO-to-entity transformation logic |
| `repository` | Spring Data JPA repositories |
| `service` | Service interfaces defining business contracts |
| `service.impl` | Service implementations containing business logic |
| `util` | Shared validation and utility logic |

### Key Frontend Files

| File | Description |
|---|---|
| `index.html` | Login page |
| `admin.html` | Admin dashboard |
| `manager.html` | Manager dashboard |
| `employee.html` | Employee dashboard |
| `api.js` | API client functions |
| `auth.js` | Login helpers, session storage, role redirects, route guards, logout, and sidebar population |
| `claims.js` | Shared claim submission, rendering, employee history, manager approval, and rejection logic |
| `dashboard.js` | Admin user listing, filtering, pagination, creation, deletion, and all-claims actions |
| `employee.js` | Employee page initialization, user refresh, manager banner, and tab switching |
| `index.js` | Login form submission and loading state |
| `manager.js` | Manager page initialization and assigned-claim loading |

## 11. Testing

The backend includes test coverage for application startup, configuration, controllers, services, mappers, exceptions, and utility logic.

### Testing Tools

| Tool | Purpose |
|---|---|
| JUnit 5 | Test framework |
| Mockito | Mocking dependencies for unit tests |
| Spring Boot Test | Application context and integration testing |
| Spring Security Test | Security-related test utilities |
| H2 | In-memory database for isolated tests |
| JaCoCo | Code coverage reporting |

### What Is Tested

- Application context loading.
- Security configuration behavior.
- Controller request and response behavior.
- Service-layer business rules.
- User creation and manager assignment logic.
- Claim submission and reviewer assignment logic.
- Claim approval and rejection validation.
- Mapper transformations.
- Custom exception classes.
- Global exception response handling.
- Validation utility behavior.

### Run Tests

From the backend directory:

```bash
./mvnw test
```

For Windows:

```bash
mvnw.cmd test
```

### Generate Coverage Report

```bash
./mvnw clean test
```

JaCoCo coverage report (Here 78% coverage):

```text
target/site/jacoco/index.html
```


## 12. Error Handling

The application uses centralized exception handling to provide consistent API responses across controllers.

### Exception Strategy

| Exception Type | Purpose |
|---|---|
| `BadRequestException` | Used for invalid input or business rule violations |
| `ResourceNotFoundException` | Used when a requested resource does not exist |
| `GlobalExceptionHandler` | Converts exceptions into structured HTTP responses |

### Standard API Response

API responses follow a consistent structure:

```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {}
}
```

Error responses should follow a similar format:

```json
{
  "success": false,
  "message": "Error message",
  "data": null
}
```

Benefits of standardized responses:

- Predictable frontend error handling.
- Cleaner API client implementation.
- Consistent developer experience.
- Easier debugging and logging.
- Improved maintainability across endpoints.

## 13. Future Enhancements

- Add complete JWT login, refresh token, and logout implementation.
- Enforce endpoint-level role authorization using method security.
- Replace Basic Auth-style frontend storage with a token-based session strategy.
- Move shared frontend helpers into smaller modules such as `utils.js`, `modal.js`, and `toast.js`.
- Replace inline event handlers with `addEventListener()` and `data-*` attributes.
- Add Docker and Docker Compose support for backend and PostgreSQL.
- Add CI/CD pipelines for automated build, test, and deployment.
- Add Redis caching for frequently accessed dashboard metrics.
- Add file upload support for reimbursement receipts.
- Add email notifications for claim approval and rejection.
- Add audit logging for sensitive user and claim operations.
- Add pagination and sorting for claim and user listing APIs.
- Add OpenAPI or Swagger documentation.
- Add microservices migration for authentication, claims, notifications, and reporting modules.

## 14. Contribution Guidelines

Contributions should follow a structured workflow to maintain code quality and project consistency.

### Contribution Process

1. Fork the repository.
2. Create a new feature branch:

```bash
git checkout -b feature/your-feature-name
```

3. Make changes in a focused and well-scoped manner.
4. Run tests before submitting:

```bash
./mvnw test
```

5. Commit changes with a clear message:

```bash
git commit -m "Add reimbursement claim validation"
```

6. Push your branch:

```bash
git push origin feature/your-feature-name
```

7. Open a pull request with a clear description of the change.

### Contribution Standards

- Keep changes focused and easy to review.
- Follow the existing package structure and naming conventions.
- Add or update tests for business logic changes.
- Avoid committing credentials or environment-specific secrets.
- Update documentation when API behavior or setup steps change.
- Ensure the project builds successfully before opening a pull request.

## 15. Author
- Raman Nema
- nraman2045@gmail.com
