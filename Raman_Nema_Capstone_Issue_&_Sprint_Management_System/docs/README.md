# SprintFlow - Issue & Sprint Management System


A full-stack project, sprint, issue, and comment management application with role-based access control.


## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Folder Structure](#folder-structure)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [API Documentation](#api-documentation)
- [Authentication Flow](#authentication-flow)
- [Database Design](#database-design)
- [Validation](#validation)
- [Error Handling](#error-handling)
- [Security](#security)
- [Frontend](#frontend)
- [Backend](#backend)
- [Application Workflow](#application-workflow)
- [Postman Documentation](#postman-documentation)
- [Running Tests](#running-tests)
- [Future Improvements](#future-improvements)
- [Known Limitations](#known-limitations)
- [Author](#author)


## Overview

SprintFlow is a full-stack issue and sprint management system built for teams that need a structured workflow for organizing projects, assigning members, planning sprints, tracking issues, and collaborating through issue comments.

The project exists to provide a role-aware project management workflow where administrators can manage users and projects, members can work on assigned project resources, and viewers can access read-oriented project data where permitted by the backend rules.

Major implemented capabilities include:

- User registration, login, logout, and bearer-token authentication.
- Role-based authorization for `ADMIN`, `MEMBER`, and `VIEWER`.
- Project creation, listing, editing, deletion, and member assignment.
- Sprint creation, listing, editing, deletion, status tracking, and project scoping.
- Issue creation, listing, editing, deletion, filtering, parent issue linking, and assignment.
- Embedded issue comments with create, update, and delete actions.
- Admin dashboard with aggregate counts and user management.
- Pagination, search, filtering, shared confirmation modals, and toast notifications.

## Features

### Authentication

- Register users with name, company email, password, and role.
- Login with company email and password.
- Logout by invalidating the active token.
- Passwords are hashed with bcrypt before storage.
- Frontend encodes password payloads with an `encoded:` Base64 prefix; backend decodes before validation and hashing.

### Authorization

- Supports `ADMIN`, `MEMBER`, and `VIEWER` roles.
- Backend dependency functions enforce route-level access.
- Admin-only access for project creation, project deletion, project member assignment, dashboard, and admin user APIs.
- Admin-or-member access for sprint, issue, and comment mutation APIs.
- Assigned-member checks enforce project-level access for member users.

### Project Management

- Create projects with name and description.
- List projects with pagination.
- Retrieve project details by ID.
- Update existing projects.
- Delete projects only when no sprints are assigned to the project.
- Assign and remove member users from projects.
- Display member summaries with friendly names and roles.

### Sprint Management

- Create sprints under a project.
- List sprints by project with pagination.
- Retrieve, update, and delete sprints.
- Sprint statuses: `PLANNED`, `ACTIVE`, `COMPLETED`.
- Prevent deleting a sprint when issues are assigned to it.
- Frontend supports project selection, sprint filtering, search, and navigation to sprint issues.

### Issue Management

- Create issues under a project and sprint.
- List issues by project with pagination.
- Filter issues by status.
- Filter issues by assignee.
- Retrieve, update, and delete issues.
- Issue priorities: `LOW`, `MEDIUM`, `HIGH`.
- Issue types: `TASK`, `BUG`, `STORY`.
- Issue statuses: `TODO`, `IN_PROGRESS`, `DONE`.
- Assign issues only to project members.
- Link issues to optional parent issues from the same project.
- Prevent deleting parent issues that still have child issues.
- Prevent member users from moving a `DONE` issue backward.

### Comments

- Add comments to issues.
- Update and delete issue comments.
- Comments are embedded inside issue documents.
- Admin users can modify member comments.
- Members can modify their own comments when they are assigned to the project.
- Viewer users cannot create, update, or delete comments.

### Notifications

- Frontend uses a reusable toast notification context.
- Toasts appear in the top-right area and auto-dismiss after 3 seconds.
- Success and error feedback is reused across authentication, project, sprint, issue, comment, and delete flows.

### Dashboard

- Admin dashboard route at `/dashboard` in the frontend.
- Backend dashboard route at `GET /admin/dashboard`.
- Shows total projects, sprints, issues, and users.
- Displays users with ID, name, email, role, and creation date.
- Supports user search.
- Allows admins to update user name and email.

### Search & Filtering

- Frontend project search by project name.
- Frontend sprint search by sprint name.
- Frontend sprint filtering by selected project and sprint.
- Frontend issue search by title or description.
- Frontend issue filtering by project, sprint, and status.
- Backend admin user search by name, email, or ObjectId.
- Backend admin user filtering by role.
- Backend issue filtering by status.
- Backend issue filtering by assignee.

### Role Management

- User roles are defined centrally as `ADMIN`, `MEMBER`, and `VIEWER`.
- Registration UI allows `MEMBER` and `VIEWER` self-registration.
- Default admin user is seeded at backend startup when no admin user exists.
- Admin user update currently supports name and email updates.

### Security

- bcrypt password hashing.
- Bearer token authentication.
- Token persistence in MongoDB through the `auth_tokens` collection.
- Token expiry validation.
- Single active token per user after login.
- Company email restriction using `@company.com`.
- CORS configured for the local Vite frontend origin.
- Backend RBAC enforcement through FastAPI dependencies.
- Pydantic request validation.

### Validation

- Backend Pydantic schemas validate request payloads.
- Frontend form validation mirrors backend constraints for common form fields.
- Password complexity is enforced.
- Company email domain is enforced.
- Sprint date ranges are validated.
- Issue priority, type, and status values are constrained.

### Error Handling

- Centralized FastAPI custom exception handlers.
- Consistent API response envelope:

```json
{
  "success": false,
  "message": "Error message",
  "data": null
}
```

- Custom errors are mapped to HTTP status codes such as `400`, `401`, `403`, `404`, and `409`.

### Logging

- No application-level logging configuration is currently implemented.

## Tech Stack

### Frontend

| Category | Technology |
| --- | --- |
| Framework | React 19 |
| Build Tool | Vite |
| Language | JavaScript |
| Libraries | Axios, React Router DOM, React Hook Form |
| State Management | React component state and Context API |
| Styling | Modular CSS files imported through style entry modules |
| Package Manager | npm with `package-lock.json` |

### Backend

| Category | Technology |
| --- | --- |
| Framework | FastAPI |
| Language | Python |
| Database | MongoDB |
| Database Driver | PyMongo |
| Authentication | Opaque bearer token stored in MongoDB |
| Password Hashing | bcrypt |
| Validation | Pydantic |
| File Upload | Not implemented |
| Logging | No custom logging configuration implemented |
| Testing | pytest, FastAPI TestClient |

### Development Tools

| Tool | Usage |
| --- | --- |
| Git | Version control |
| npm | Frontend dependency management and scripts |
| pip | Backend dependency management |
| Vite | Frontend development server and production build |
| ESLint | Frontend linting |
| pytest | Backend test runner |
| GitHub Actions | PR review workflow trigger |
| Postman | Not configured in repository, but APIs can be tested manually |
| Docker | No Docker configuration found |

## Architecture

SprintFlow uses a separated frontend/backend architecture:

- The React frontend renders pages, validates forms, stores session metadata in localStorage, and calls backend APIs through Axios services.
- The FastAPI backend exposes REST APIs, validates requests with Pydantic, enforces authentication and authorization through dependencies, runs business rules in services, and persists documents through repository classes.
- MongoDB stores users, tokens, projects, sprints, and issues.

### Layered Backend Architecture

```text
HTTP Request
  -> FastAPI Router
  -> Authentication / Authorization Dependency
  -> Pydantic Request Schema
  -> Service Layer
  -> Repository Layer
  -> MongoDB Collection
  -> Pydantic Response Schema
  -> ApiResponse Envelope
```

### Separation of Concerns

- `routers`: API route definitions and dependency wiring.
- `services`: Business rules, authorization checks beyond route-level roles, response construction.
- `repositories`: MongoDB queries and updates.
- `models`: MongoDB document builders.
- `schemas`: Request and response validation models.
- `dependencies`: Authentication and role authorization helpers.
- `exceptions`: Custom exceptions and response handlers.
- `common`: Shared response, enum, and pagination utilities.

## Folder Structure

```text
Raman_Nema_Capstone_Issue_&_Sprint_Management_System/
├── README.md
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── .gitignore
│   ├── app/
│   │   ├── common/
│   │   │   ├── api_response.py
│   │   │   ├── enums.py
│   │   │   └── pagination.py
│   │   ├── constants/
│   │   │   └── message_constants.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   ├── security.py
│   │   │   └── seed.py
│   │   ├── dependencies/
│   │   │   ├── authentication.py
│   │   │   └── authorization.py
│   │   ├── exceptions/
│   │   │   ├── custom_exceptions.py
│   │   │   └── exception_handlers.py
│   │   ├── models/
│   │   │   ├── issue_model.py
│   │   │   ├── project_model.py
│   │   │   ├── sprint_model.py
│   │   │   ├── token_model.py
│   │   │   └── user_model.py
│   │   ├── repositories/
│   │   │   ├── issue_repository.py
│   │   │   ├── project_repository.py
│   │   │   ├── sprint_repository.py
│   │   │   ├── token_repository.py
│   │   │   └── user_repository.py
│   │   ├── routers/
│   │   │   ├── admin_router.py
│   │   │   ├── auth_router.py
│   │   │   ├── issue_router.py
│   │   │   ├── project_router.py
│   │   │   └── sprint_router.py
│   │   ├── schemas/
│   │   │   ├── requests/
│   │   │   └── responses/
│   │   └── services/
│   │       ├── admin_service.py
│   │       ├── auth_service.py
│   │       ├── issue_service.py
│   │       ├── project_service.py
│   │       └── sprint_service.py
│   └── tests/
│       ├── auth/
│       ├── issues/
│       ├── projects/
│       └── sprints/
└── frontend/
    ├── index.html
    ├── package.json
    ├── package-lock.json
    ├── vite.config.js
    ├── eslint.config.js
    ├── .env.example
    ├── .gitignore
    └── src/
        ├── App.jsx
        ├── main.jsx
        ├── components/
        │   ├── common/
        │   ├── issue/
        │   ├── layout/
        │   ├── project/
        │   └── sprint/
        ├── config/
        ├── constants/
        ├── context/
        ├── pages/
        ├── services/
        ├── styles/
        └── utils/
```

### Major Folder Purpose

| Folder | Purpose |
| --- | --- |
| `backend/app/routers` | FastAPI route modules |
| `backend/app/services` | Business logic and permission-aware workflows |
| `backend/app/repositories` | MongoDB data access |
| `backend/app/models` | Document builder classes for MongoDB inserts |
| `backend/app/schemas` | Pydantic request and response schemas |
| `backend/app/dependencies` | Authentication and role authorization dependencies |
| `backend/app/exceptions` | Custom exception classes and handlers |
| `backend/tests` | Backend API test suites |
| `frontend/src/pages` | Top-level page components |
| `frontend/src/components` | Reusable UI components |
| `frontend/src/services` | Axios API service functions |
| `frontend/src/context` | Toast notification context |
| `frontend/src/utils` | Validation, storage, date, pagination, and password helpers |
| `frontend/src/styles` | Modular CSS grouped by UI domain |

## Installation

### 1. Clone Repository

```bash
git clone <repository-url>
cd Raman_Nema_Capstone_Issue_\&_Sprint_Management_System
```

### 2. Install Backend Dependencies

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Backend Environment

Create `backend/.env`:

```env
MONGO_URI=<your-mongodb-connection-string>
DATABASE_NAME=<your-database-name>
```

### 4. Configure Frontend Environment

Create `frontend/.env`:

```env
VITE_API_BASE_URL=http://localhost:8000
```

### 5. Database Setup

Ensure MongoDB is running and reachable through `MONGO_URI`.

The backend creates a default administrator account during startup when no
administrator exists. Configure the administrator credentials through
environment variables before running the application.

### 6. Run Backend

From the `backend` directory:

```bash
uvicorn main:app --reload
```

Backend API:

```text
http://localhost:8000
```

FastAPI interactive documentation:

```text
http://localhost:8000/docs
```

### 7. Run Frontend

From the `frontend` directory:

```bash
npm install
npm run dev
```

Frontend application:

```text
http://localhost:5173
```

### 8. Verify Installation

- Open `http://localhost:5173`.
- Login with the seeded admin account or register a `MEMBER` / `VIEWER` account.
- Confirm the backend docs load at `http://localhost:8000/docs`.
- Create a project as an admin.

## Environment Variables

### Backend

| Variable | Purpose | Required |
| --- | --- | --- |
| `MONGO_URI` | MongoDB connection string used by PyMongo | Required |
| `DATABASE_NAME` | MongoDB database name | Required |

### Frontend

| Variable | Purpose | Required |
| --- | --- | --- |
| `VITE_API_BASE_URL` | Base URL used by Axios for backend requests | Required |

Do not commit real secret values or production database credentials.

## API Documentation

All backend routes return the shared `ApiResponse` shape:

```json
{
  "success": true,
  "message": "Operation message",
  "data": {}
}
```

### Authentication

| Method | Route | Purpose | Auth Required | Roles Allowed |
| --- | --- | --- | --- | --- |
| `POST` | `/auth/register` | Register a new user | No | Public |
| `POST` | `/auth/login` | Login and receive an access token | No | Public |
| `POST` | `/auth/logout` | Delete the current token | Yes | Authenticated users |

### Admin / Dashboard / Users

| Method | Route | Purpose | Auth Required | Roles Allowed |
| --- | --- | --- | --- | --- |
| `GET` | `/admin/dashboard` | Get dashboard totals and users | Yes | `ADMIN` |
| `GET` | `/admin/users` | Get users with optional `search` and `role` filters | Yes | `ADMIN` |
| `PUT` | `/admin/users/{user_id}` | Update user name and email | Yes | `ADMIN` |

### Projects

| Method | Route | Purpose | Auth Required | Roles Allowed |
| --- | --- | --- | --- | --- |
| `POST` | `/projects` | Create a project | Yes | `ADMIN` |
| `GET` | `/projects` | List projects with pagination | Yes | `ADMIN`, `MEMBER`, `VIEWER` |
| `GET` | `/projects/{project_id}` | Get project by ID | Yes | `ADMIN`, `MEMBER`, `VIEWER` |
| `PUT` | `/projects/{project_id}` | Update project | Yes | `ADMIN`, assigned `MEMBER` |
| `DELETE` | `/projects/{project_id}` | Delete project | Yes | `ADMIN` |

### Members

| Method | Route | Purpose | Auth Required | Roles Allowed |
| --- | --- | --- | --- | --- |
| `POST` | `/projects/{project_id}/members` | Assign a member to a project | Yes | `ADMIN` |
| `DELETE` | `/projects/{project_id}/members/{user_id}` | Remove a member from a project | Yes | `ADMIN` |

### Sprints

| Method | Route | Purpose | Auth Required | Roles Allowed |
| --- | --- | --- | --- | --- |
| `POST` | `/projects/{project_id}/sprints` | Create a sprint for a project | Yes | `ADMIN`, assigned `MEMBER` |
| `GET` | `/projects/{project_id}/sprints` | List project sprints with pagination | Yes | `ADMIN`, assigned `MEMBER`, `VIEWER` |
| `GET` | `/sprints/{sprint_id}` | Get sprint by ID | Yes | `ADMIN`, assigned `MEMBER`, `VIEWER` |
| `PUT` | `/sprints/{sprint_id}` | Update sprint | Yes | `ADMIN`, assigned `MEMBER` |
| `DELETE` | `/sprints/{sprint_id}` | Delete sprint | Yes | `ADMIN`, assigned `MEMBER` |

### Issues

| Method | Route | Purpose | Auth Required | Roles Allowed |
| --- | --- | --- | --- | --- |
| `POST` | `/projects/{project_id}/issues` | Create an issue | Yes | `ADMIN`, assigned `MEMBER` |
| `GET` | `/projects/{project_id}/issues?status={{issue_status}}` | List project issues with optional `status` filter | Yes | `ADMIN`, assigned `MEMBER`, `VIEWER` |
| `GET` | `/projects/{project_id}/issues?assignee={{assignee_id}}` | List project issues with optional `assignee` filter | Yes | `ADMIN`|
| `GET` | `/issues/{issue_id}` | Get issue by ID | Yes | `ADMIN`, assigned `MEMBER`, `VIEWER` |
| `PUT` | `/issues/{issue_id}` | Update issue | Yes | `ADMIN`, assigned `MEMBER` |
| `DELETE` | `/issues/{issue_id}` | Delete issue | Yes | `ADMIN`, assigned `MEMBER` |

### Comments

| Method | Route | Purpose | Auth Required | Roles Allowed |
| --- | --- | --- | --- | --- |
| `POST` | `/issues/{issue_id}/comments` | Add comment to issue | Yes | `ADMIN`, assigned `MEMBER` |
| `PUT` | `/issues/{issue_id}/comments/{comment_id}` | Update issue comment | Yes | `ADMIN`, original assigned-member author |
| `DELETE` | `/issues/{issue_id}/comments/{comment_id}` | Delete issue comment | Yes | `ADMIN`, original assigned-member author |

### Pagination Query Parameters

Project, sprint, and issue list endpoints use:

| Query Parameter | Purpose | Default | Constraint |
| --- | --- | --- | --- |
| `page` | Page number | `1` | Must be `>= 1` |
| `limit` | Records per page | `10` | Must be between `1` and `100` |

## Authentication Flow

1. User registers with a company email, password, and role.
2. Backend validates the request and stores a bcrypt-hashed password.
3. User logs in with email and password.
4. Backend verifies the password, deletes older tokens for that user, creates a new opaque token, and stores it in `auth_tokens`.
5. Frontend stores `access_token`, `role`, and `user_name` in localStorage.
6. Axios attaches the token to authenticated requests:

```http
Authorization: Bearer <access_token>
```

7. Backend validates token existence and expiry on protected routes.
8. Role dependencies and service-level membership checks enforce access.
9. Logout deletes the token from MongoDB.

### JWT / Refresh Token Status

The current implementation does not use JWT claims and does not implement refresh tokens. It uses opaque UUID-style bearer tokens stored server-side in MongoDB with an expiration timestamp.

## Database Design

MongoDB collections used by the application:

| Collection | Purpose | Important Fields |
| --- | --- | --- |
| `users` | Stores user accounts | `name`, `email`, `password`, `role`, `created_at`, `updated_at` |
| `auth_tokens` | Stores active bearer tokens | `user_id`, `email`, `token`, `created_at`, `expires_at` |
| `projects` | Stores projects | `name`, `description`, `created_by`, `members`, `created_at`, `updated_at` |
| `sprints` | Stores project sprints | `project_id`, `name`, `goal`, `start_date`, `end_date`, `status`, `created_by` |
| `issues` | Stores project issues and embedded comments | `project_id`, `sprint_id`, `parent_id`, `title`, `description`, `priority`, `type`, `status`, `assignee`, `reporter`, `comments` |

### Relationships

- A user can create projects.
- A project stores member user IDs in `members`.
- A sprint belongs to one project through `project_id`.
- An issue belongs to one project through `project_id`.
- An issue belongs to a sprint through `sprint_id`.
- An issue can reference another issue through `parent_id`.
- Comments are embedded inside issue documents and store the comment author ID and name.

## Validation

Backend validation is implemented with Pydantic request schemas:

- `RegisterRequest` and `LoginRequest` validate email and password data.
- `CreateProjectRequest` and `UpdateProjectRequest` validate project fields.
- `CreateSprintRequest` and `UpdateSprintRequest` validate sprint fields and date order.
- `CreateIssueRequest` and `UpdateIssueRequest` validate issue fields and allowed enum-like values.
- `CreateIssueCommentRequest` and `UpdateIssueCommentRequest` validate comment text length.
- `UpdateUserRequest` validates admin user updates.

Frontend validation is implemented in `frontend/src/utils/validations.js` for login, registration, project, sprint, and issue forms.

## Error Handling

The backend registers exception handlers in `backend/main.py` for application-specific exceptions and FastAPI `HTTPException`.

Implemented response mapping includes:

| Status | Usage |
| --- | --- |
| `400` | Invalid request data or invalid issue status transition |
| `401` | Missing, invalid, or expired authentication token |
| `403` | Authenticated user does not have required permission |
| `404` | Requested user, project, sprint, issue, member, or comment not found |
| `409` | Duplicate resources or dependency-safe delete conflicts |

Dependency-safe delete rules include:

- Projects with sprints cannot be deleted.
- Sprints with issues cannot be deleted.
- Issues with child issues cannot be deleted.

## Security

Implemented security controls:

- bcrypt password hashing.
- Bearer token authentication.
- Server-side token storage and expiry checks.
- Previous user tokens are deleted when a new login succeeds.
- Logout deletes the active token.
- Role-based access control through FastAPI dependencies.
- Project membership checks for member-scoped workflows.
- Company email domain enforcement.
- Pydantic input validation.
- Local CORS configuration for `http://localhost:5173`.

Security notes:

- Tokens are stored in frontend localStorage.
- The seeded admin credential should be changed before non-local use.
- Refresh tokens are not implemented.

## Frontend

### Pages

| Page | Route | Purpose |
| --- | --- | --- |
| `LoginPage.jsx` | `/`, `/login` | User login |
| `RegisterPage.jsx` | `/register` | Member/viewer registration |
| `DashboardPage.jsx` | `/dashboard` | Admin dashboard and user table |
| `ProjectPage.jsx` | `/projects` | Project list, creation, editing, deletion, and member management |
| `SprintPage.jsx` | `/sprints` | Sprint list, creation, editing, deletion, and issue navigation |
| `IssuePage.jsx` | `/issues` | Issue list, creation, editing, deletion, filtering, and comments |

### Components

- Common: `Button`, `InputField`, `ConfirmModal`, `Pagination`.
- Layout: `Layout`, `Sidebar`.
- Project: `ProjectCard`, `ProjectForm`.
- Sprint: `SprintCard`, `SprintForm`.
- Issue: `IssueCard`, `IssueForm`.

### Context

- `NotificationContext.jsx` provides `showNotification`.
- Toast notifications auto-dismiss after 3 seconds.

### Services

- `api-client.js` configures Axios and injects bearer tokens.
- `auth-service.js` calls authentication APIs.
- `project-service.js` calls project and member APIs.
- `sprint-service.js` calls sprint APIs.
- `issue-service.js` calls issue and comment APIs.
- `admin-service.js` calls dashboard and user APIs.

### Routing

Routes are defined in `frontend/src/App.jsx`.

The frontend does not include a dedicated protected-route component. Protected behavior is enforced by backend APIs and the Axios response interceptor, which clears localStorage and redirects to `/login` on non-auth-route `401` responses.

## Backend

### Routers

- `auth_router.py`: registration, login, logout.
- `admin_router.py`: dashboard and admin user management.
- `project_router.py`: projects, project members, and nested project sprint routes.
- `sprint_router.py`: sprint get, update, and delete routes.
- `issue_router.py`: project issues, issue details, issue updates/deletes, and comments.

### Services

- `AuthService`: registration, login, logout, token creation.
- `AdminService`: dashboard totals, user search, user update.
- `ProjectService`: project CRUD and member assignment rules.
- `SprintService`: sprint CRUD and project-scoped permissions.
- `IssueService`: issue CRUD, parent issue checks, status rules, comment operations.

### Repositories

- `UserRepository`
- `TokenRepository`
- `ProjectRepository`
- `SprintRepository`
- `IssueRepository`

### Schemas

- Request schemas live in `backend/app/schemas/requests`.
- Response schemas live in `backend/app/schemas/responses`.

### Models

Document builders live in `backend/app/models` and create MongoDB-ready dictionaries for users, tokens, projects, sprints, and issues.

### Middleware

The backend registers FastAPI `CORSMiddleware` for:

```text
http://localhost:5173
```

### Configuration

Configuration is loaded from environment variables through `python-dotenv` in `backend/app/core/config.py`.

## Application Workflow

```text
User Login
  -> Backend validates credentials
  -> Backend creates bearer token
  -> Frontend stores token, role, and user name
  -> User accesses protected pages
  -> Admin creates projects
  -> Admin assigns members to projects
  -> Admin or assigned member creates sprints
  -> Admin or assigned member creates issues
  -> Issues are assigned to project members
  -> Admin or assigned members add comments
  -> Issues move through TODO, IN_PROGRESS, and DONE
  -> Sprints and projects are completed through managed updates
```

## Postman Documentation

A Postman collection is included in the repository for testing all backend APIs.

### Getting Started

1. Open **Postman**.
2. Click **Import** and select the collection file.
3. Open the imported collection and navigate to **Variables**.
4. Update the required variables:

- `access_token`
- `project_id`
- `member_user_id`
- `user_id`
- `assignee_user_id`
- `sprint_id`
- `issue_id`
- `comment_id`
- `login_password`
- `register_password`

5. Execute the **Login** request and copy the returned token into the `access_token` variable.

### Base URL

The collection uses the following variable:

```text
{{base_url}}
```

Default value:

```text
http://127.0.0.1:8000
```

> **Note:** The collection contains placeholder values only. No real access tokens, passwords, MongoDB IDs, or production credentials are included.



## Running Tests

Backend automated tests are included under `backend/tests`.

Covered areas include:

- Authentication registration, login, logout, and authorization.
- Project creation, retrieval, update, and deletion.
- Sprint creation, retrieval, update, and deletion.
- Issue creation, retrieval, update, deletion, status filtering, and status transition rules.
- Comment creation, update, deletion, and permission checks.

Run backend tests:

```bash
cd backend
pytest
```

Frontend automated tests are not currently included.

Frontend validation commands:

```bash
cd frontend
npm run lint
npm run build
```

## Future Improvements

- Add refresh-token support or migrate to signed JWTs if stateless authentication is required.
- Add a dedicated frontend protected-route component for clearer route-level guarding.
- Add frontend automated tests.
- Add structured backend logging.
- Add Docker and Docker Compose for local development.
- Add production deployment configuration.
- Move seeded admin credentials into environment variables.
- Add indexes for frequently queried MongoDB fields such as user email, project name, sprint project ID, issue project ID, and token value.
- Add role update support to admin user management if required by product rules.
- Add API documentation examples for request and response bodies.

## Known Limitations

- No Docker configuration is present.
- No production deployment workflow is present.
- No frontend automated test suite is present.
- No custom application logging is configured.
- Frontend route protection relies on backend authorization and Axios `401` handling rather than a dedicated protected-route wrapper.
- Authentication uses opaque bearer tokens stored in MongoDB, not JWTs.
- Refresh tokens are not implemented.
- CORS is configured only for `http://localhost:5173`.
- A default admin credential is seeded in code when no admin user exists.
- File upload is not implemented.

## Author

**Raman Nema**
- Project folder: `Raman_Nema_Capstone_Issue_&_Sprint_Management_System`