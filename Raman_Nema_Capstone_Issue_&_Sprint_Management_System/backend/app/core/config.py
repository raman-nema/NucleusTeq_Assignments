from dotenv import load_dotenv
import os

# Load environment variables from a local .env file when available.
load_dotenv()


class Settings:
    """Environment-backed configuration used by the application."""

    # MongoDB connection string used by the database client.
    mongo_uri = os.getenv("MONGO_URI")

    # Default database selected for application data.
    database_name = os.getenv("DATABASE_NAME")


# Shared settings instance imported by the rest of the application.
settings = Settings()
