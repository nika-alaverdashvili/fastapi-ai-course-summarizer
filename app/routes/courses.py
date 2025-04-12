from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseOut
from app.utils.token import get_current_user
from app.models.user import User

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
