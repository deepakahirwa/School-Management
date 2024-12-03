from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()




MONGO_DB_URL = os.getenv("MONGO_DB_URL")
if not MONGO_DB_URL:
    raise ValueError("MONGO_DB_URL is not set in environment variables")

client = AsyncIOMotorClient(MONGO_DB_URL)
database = client["student_management"]
students_collection = database["students"]
