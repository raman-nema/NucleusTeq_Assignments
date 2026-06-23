from fastapi import APIRouter
from app.core.database import database

router = APIRouter()

@router.get("/health")
def health_check():

    database.command("ping")

    return {
        "status": "UP",
        "database": "CONNECTED"
    }