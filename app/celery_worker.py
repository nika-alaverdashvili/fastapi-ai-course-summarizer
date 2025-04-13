from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery = Celery(
    "app",
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery.autodiscover_tasks(["app"])
