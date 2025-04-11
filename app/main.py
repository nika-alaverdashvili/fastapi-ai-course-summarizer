from fastapi import FastAPI, Depends
from app.routes import tasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.db.redis import redis_client
from sqlalchemy import text


app = FastAPI()


@app.get("/")
def root():
    return {"message": "FastAPI AI Course Summarizer is running!"}


@app.get("/ping-db")
async def ping_db(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT 1"))
    return {"db_connected": result.scalar() == 1}


@app.get("/ping-redis")
async def ping_redis():
    try:
        await redis_client.set("healthcheck", "ok", ex=10)
        value = await redis_client.get("healthcheck")
        return {"redis_connected": value == "ok"}
    except Exception as e:
        return {"redis_connected": False, "error": str(e)}


app.include_router(tasks.router, tags=["tasks"])
