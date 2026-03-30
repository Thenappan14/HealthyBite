from pymongo import MongoClient
from pymongo.database import Database

from app.core.config import settings

client = MongoClient(settings.mongodb_url)
database = client[settings.mongodb_db_name]


def get_db() -> Database:
    return database
