from app.celery_worker import celery
from app.tasks.summary import generate_and_store_summary


@celery.task(name="generate_summary_task")
def generate_summary_task(course_id: str, description: str):
    generate_and_store_summary(course_id, description)
