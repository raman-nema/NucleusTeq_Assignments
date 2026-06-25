from fastapi import FastAPI

from app.routers.auth_router import router as auth_router

from app.exceptions.custom_exceptions import UserAlreadyExistsException

from app.exceptions.exception_handlers import user_exists_handler
from fastapi.middleware.cors import CORSMiddleware
from app.core.seed import seed_admin

app = FastAPI(title="Issue & Sprint Management System")

app.include_router(auth_router)

app.add_exception_handler(UserAlreadyExistsException, user_exists_handler)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    seed_admin()
