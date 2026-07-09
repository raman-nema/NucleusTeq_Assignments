from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    """Environment-backed configuration used by the application."""

    mongo_uri = os.getenv("MONGO_URI")
    database_name = os.getenv("DATABASE_NAME")


settings = Settings()
