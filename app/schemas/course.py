from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
from datetime import datetime


class CourseCreate(BaseModel):
    course_title: str = Field(..., max_length=255)
    course_description: str


class CourseOut(BaseModel):
    id: UUID
    user_id: UUID
    course_title: str
    course_description: str
    ai_summary: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class CourseSummaryGenerate(BaseModel):
    course_id: UUID
    new_description: str


class ManualSummaryUpdate(BaseModel):
    course_id: UUID
    new_summary: str = Field(..., min_length=10, max_length=2000)
