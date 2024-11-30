import os
from pymongo import MongoClient
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()


class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            # Get MongoDB URI from environment
            mongodb_uri = os.getenv('MONGODB_URI')
            database_name = os.getenv('DATABASE_NAME', 'student_management')

            try:
                # Create client
                cls._instance = super(DatabaseConnection, cls).__new__(cls)
                cls._instance.client = MongoClient(mongodb_uri)
                cls._instance.db = cls._instance.client[database_name]
                cls._instance.collection = cls._instance.db['students']
            except Exception as e:
                print(f"Database connection error: {e}")
                raise
        return cls._instance

    def get_collection(self):
        return self.collection
