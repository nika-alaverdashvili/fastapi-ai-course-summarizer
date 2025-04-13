import logging
from app.db.session_sync import SessionLocal
from app.models.course import Course
from app.openai_service import generate_course_summary_sync

logger = logging.getLogger(__name__)


def generate_and_store_summary(course_id: str, description: str):
    try:
        summary = generate_course_summary_sync(description)
    except Exception as e:
        logger.exception(f"[OpenAI Error] {e}")
        return

    try:
        with SessionLocal() as session:
            course = session.query(Course).filter(Course.id == course_id).first()

            if not course:
                logger.warning(f"[DB] Course not found: {course_id}")
                return

            course.ai_summary = summary
            course.status = "completed"
            session.commit()
            logger.info(f"[DB] Summary saved/updated for course {course_id}")
    except Exception as e:
        logger.exception(f"[DB Error] {e}")
