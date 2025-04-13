from typing import List
from uuid import UUID

from app.db.session import get_db
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseOut, CourseSummaryGenerate
from app.utils.token import get_current_user
from app.models.user import User
from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.tasks.task import generate_summary_task
router = APIRouter()

@router.post("/courses", response_model=CourseOut, status_code=status.HTTP_201_CREATED)
async def create_course(
    course_data: CourseCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_course = Course(
        user_id=current_user.id,
        course_title=course_data.course_title,
        course_description=course_data.course_description,
        status="pending"
    )
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)
    return new_course


@router.get("/courses", response_model=List[CourseOut])
async def get_all_courses(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Course).where(Course.user_id == current_user.id)
    )
    return result.scalars().all()


@router.get("/courses/{course_id}", response_model=CourseOut)
async def get_course(
    course_id: UUID = Path(..., description="The UUID of the course to retrieve"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Course).where(Course.id == course_id, Course.user_id == current_user.id)
    )
    course = result.scalar_one_or_none()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    return course


@router.post("/generate_summary", status_code=status.HTTP_202_ACCEPTED)
async def generate_summary(
    data: CourseSummaryGenerate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Course).where(Course.id == data.course_id, Course.user_id == current_user.id)
    )
    course = result.scalar_one_or_none()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Trigger celery task
    generate_summary_task.delay(str(course.id), data.new_description)

    return {"message": "Summary generation task started"}
