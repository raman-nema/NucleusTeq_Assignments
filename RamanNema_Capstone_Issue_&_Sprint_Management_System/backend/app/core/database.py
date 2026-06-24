from pymongo import MongoClient

from app.core.config import settings

# Shared MongoDB client configured from application settings.
client = MongoClient(settings.mongo_uri)

# Active database used by repositories and data access layers.
database = client[settings.database_name]
