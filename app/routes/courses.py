from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.session import get_db
from app.models.course import Course
from app.models.user import User
from app.schemas.course import (
    CourseCreate,
    CourseOut,
    CourseSummaryGenerate,
    ManualSummaryUpdate,
)
from app.tasks.task import generate_summary_task
from app.utils.throttle import check_throttle
from app.utils.token import get_current_user

router = APIRouter()


@router.post("/courses", response_model=CourseOut, status_code=status.HTTP_201_CREATED)
async def create_course(
    course_data: CourseCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new course for the authenticated user.

    This endpoint allows a logged-in user to create a course entry by providing
    a title and description. The newly created course will have a status of "pending"
    until it is processed for summary generation.

    Returns:
        CourseOut: The created course with full metadata.
    """
    new_course = Course(
        user_id=current_user.id,
        course_title=course_data.course_title,
        course_description=course_data.course_description,
        status="pending",
    )
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)
    return new_course


@router.post("/generate_summary", status_code=status.HTTP_202_ACCEPTED)
async def generate_summary(
    data: CourseSummaryGenerate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Triggers background task to generate AI summary for a course.
    Limited to 3 uses per user per day.
    """

    check_throttle(str(current_user.id))

    result = await db.execute(
        select(Course).where(
            Course.id == data.course_id, Course.user_id == current_user.id
        )
    )
    course = result.scalar_one_or_none()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Trigger celery task
    generate_summary_task.delay(str(course.id), data.new_description)

    return {"message": "Summary generation task started"}


@router.get("/courses", response_model=List[CourseOut])
async def get_all_courses(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve all courses created by the authenticated user.

    This endpoint returns a list of all course entries associated with the
    currently logged-in user. Each course includes its title, description,
    AI-generated summary (if available), and status.

    Returns:
        List[CourseOut]: A list of the user's courses.
    """
    result = await db.execute(select(Course).where(Course.user_id == current_user.id))
    return result.scalars().all()


@router.get("/courses/{course_id}", response_model=CourseOut)
async def get_course(
    course_id: UUID = Path(..., description="The UUID of the course to retrieve"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve a specific course by its ID for the authenticated user.

    This endpoint fetches a single course that belongs to the currently logged-in user.
    If the course does not exist or is not associated with the user, a 404 error is returned.

    Args:
        course_id (UUID): Unique identifier of the course to retrieve.

    Returns:
        CourseOut: The requested course details.
        :param current_user:
        :param course_id:
        :param db:
    """
    result = await db.execute(
        select(Course).where(Course.id == course_id, Course.user_id == current_user.id)
    )
    course = result.scalar_one_or_none()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    return course


@router.patch("/courses/update-summary", status_code=status.HTTP_200_OK)
async def update_course_summary(
    data: ManualSummaryUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Manually update the AI-generated summary for a specific course.

    Args:
        data (ManualSummaryUpdate): Includes the course ID and new summary content.

    Returns:
        dict: Confirmation message.
        :param data:
        :param current_user:
        :param db:
    """
    result = await db.execute(
        select(Course).where(
            Course.id == data.course_id, Course.user_id == current_user.id
        )
    )
    course = result.scalar_one_or_none()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    course.ai_summary = data.new_summary
    course.status = "completed"
    await db.commit()

    return {"message": "AI summary updated successfully"}


@router.delete("/courses/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(
    course_id: UUID = Path(..., description="The UUID of the course to delete"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a course by its ID for the authenticated user.

    This endpoint allows the authenticated user to delete a specific course
    they have created by providing the course's UUID. If the course does not
    exist or does not belong to the user, a 404 error is returned.

    Args:
        course_id (UUID): Unique identifier of the course to delete.
        db (AsyncSession): Database session dependency.
        current_user (User): The authenticated user making the request.

    Raises:
        HTTPException: 404 if the course is not found or doesn't belong to the user.

    Returns:
        None: Responds with HTTP 204 No Content on successful deletion.
    """
    result = await db.execute(
        select(Course).where(Course.id == course_id, Course.user_id == current_user.id)
    )
    course = result.scalar_one_or_none()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    await db.delete(course)
    await db.commit()
