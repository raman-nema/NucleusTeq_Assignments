from fastapi import FastAPI
from app.routers.auth_router import router as auth_router
from app.routers import project_router
from app.routers import admin_router
from fastapi.middleware.cors import CORSMiddleware
from app.core.seed import seed_admin
from app.exceptions.custom_exceptions import (
    ConflictException,
    InvalidCredentialsException,
    BadRequestException,
    NotFoundException,
    UnauthorizedException,
    ExpiredTokenException,
    ForbiddenException,
)
from app.exceptions.exception_handlers import (
    conflict_handler,
    invalid_credentials_handler,
    bad_request_handler,
    not_found_handler,
    unauthorized_handler,
    expired_token_handler,
    forbidden_handler,
)

app = FastAPI(title="Issue & Sprint Management System")

# Register authentication routes under the application.
app.include_router(auth_router)

app.include_router(admin_router.router)

app.include_router(project_router.router)

# Map custom authentication exceptions to consistent JSON responses.
app.add_exception_handler(ConflictException, conflict_handler)
app.add_exception_handler(InvalidCredentialsException, invalid_credentials_handler)
app.add_exception_handler(BadRequestException, bad_request_handler)
app.add_exception_handler(NotFoundException, not_found_handler)
app.add_exception_handler(UnauthorizedException, unauthorized_handler)
app.add_exception_handler(ExpiredTokenException, expired_token_handler)
app.add_exception_handler(ForbiddenException, forbidden_handler)

# Allow the local frontend application to call the backend APIs.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    # Ensure the default admin user exists when the application starts.
    seed_admin()
