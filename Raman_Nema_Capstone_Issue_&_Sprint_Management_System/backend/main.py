from fastapi import FastAPI
from app.routers.auth_router import router as auth_router
from app.exceptions.custom_exceptions import UserAlreadyExistsException
from app.exceptions.custom_exceptions import InvalidCredentialsException
from app.exceptions.exception_handlers import user_exists_handler
from app.exceptions.exception_handlers import invalid_credentials_handler
from fastapi.middleware.cors import CORSMiddleware
from app.core.seed import seed_admin

app = FastAPI(title="Issue & Sprint Management System")

# Register authentication routes under the application.
app.include_router(auth_router)

# Map custom authentication exceptions to consistent JSON responses.
app.add_exception_handler(UserAlreadyExistsException, user_exists_handler)
app.add_exception_handler(InvalidCredentialsException, invalid_credentials_handler)

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
