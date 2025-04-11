from fastapi import APIRouter
from app.celery_worker import add

router = APIRouter()


@router.get("/run-task")
async def run_add_task(x: int = 5, y: int = 7):
    task = add.delay(x, y)
    return {"task_id": task.id, "status": "queued"}
