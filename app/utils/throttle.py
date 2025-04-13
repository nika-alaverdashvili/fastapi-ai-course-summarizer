from fastapi import HTTPException, status
from limits import RateLimitItemPerDay
from limits.storage import MemoryStorage

rate_limit = RateLimitItemPerDay(3)
storage = MemoryStorage()


def check_throttle(user_id: str):
    """
    Limits summary generation to 3 times per user per day.

    Raises:
        HTTPException: If the user exceeds the daily limit.
    """
    key = f"generate_summary:{user_id}"

    if not storage.acquire_entry(
        key, rate_limit.amount, expiry=rate_limit.get_expiry()
    ):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="You have exceeded the daily limit of 3 summaries. Try again tomorrow.",
        )
