import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://admin:password123@db/vulndb")
    SQLALCHEMY_TRACK_MODIFICATIONS = False