import os
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set")

# Create engine once
engine = create_engine(DATABASE_URL)

# Retry DB connection
max_retries = 10
retry_delay = 2

for attempt in range(max_retries):
    try:
        with engine.connect() as connection:
            print("Database connected successfully")
        break
    except OperationalError:
        print(f"Database not ready, retrying... ({attempt + 1}/{max_retries})")
        time.sleep(retry_delay)
else:
    # This runs if loop never breaks
    raise RuntimeError("Could not connect to the database after multiple attempts")

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()