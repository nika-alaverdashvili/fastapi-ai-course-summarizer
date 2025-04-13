import logging

import httpx

from app.settings import settings

logger = logging.getLogger(__name__)
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"


def generate_course_summary_sync(course_description: str) -> str:
    headers = {
        "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": settings.OPENAI_MODEL,
        "messages": [
            {
                "role": "user",
                "content": f"Summarize this online course: {course_description}",
            }
        ],
    }

    for attempt in range(3):
        try:
            with httpx.Client(timeout=30) as client:
                response = client.post(OPENAI_API_URL, headers=headers, json=data)
                response.raise_for_status()
                content = response.json()["choices"][0]["message"].get("content")
                if not content:
                    raise ValueError("OpenAI response content is missing")
                return content
        except (httpx.ReadTimeout, httpx.ConnectTimeout):
            logger.warning(f"[OpenAI] Timeout on attempt {attempt + 1}")
            if attempt < 2:
                continue
            raise
        except httpx.HTTPError as e:
            logger.error(f"[OpenAI] HTTP error: {e}")
            raise
