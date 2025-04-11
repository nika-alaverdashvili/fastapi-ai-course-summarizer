from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()


REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery = Celery(
    "worker",
    broker=REDIS_URL,
    backend=REDIS_URL
)

# test
@celery.task
def add(x, y):
    return x + y
