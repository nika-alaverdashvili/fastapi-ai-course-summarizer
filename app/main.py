from fastapi import FastAPI
from app.routes import tasks

app = FastAPI()


@app.get("/")
def root():
    return {"message": "FastAPI AI Course Summarizer is running!"}


app.include_router(tasks.router, tags=["tasks"])
