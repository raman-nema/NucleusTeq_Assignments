from pymongo import MongoClient
from app.core.config import settings

client = MongoClient(settings.mongo_uri)
database = client[settings.database_name]
