import os
import time
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:password123@db:5432/vulndb")

# Esperar hasta que la base de datos esté lista
engine = create_engine(DATABASE_URL)

for _ in range(10):
    try:
        conn = engine.connect()
        conn.close()
        print("✅ Base de datos disponible, continuando con el backend.")
        break
    except OperationalError:
        print("⏳ Esperando a que la base de datos esté lista...")
        time.sleep(5)
        
class Config:
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
