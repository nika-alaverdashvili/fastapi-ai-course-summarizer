import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_SYNC_URL = os.getenv("DATABASE_SYNC_URL")

engine = create_engine(DATABASE_SYNC_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
