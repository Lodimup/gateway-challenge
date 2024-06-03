"""
Handles rate limiting
"""

from db.clients import rdb
from fastapi import HTTPException
from pydantic import validate_call


@validate_call
def is_rate_limited(key: str, limit: int, window: int) -> bool:
    """
    Fixed window rate limiting
    Args:
        key (str): key to rate limit
        limit (int): limit allowed within the window
        window (int): window in seconds
    Returns:
        bool: True if rate limited, False otherwise
    """
    cache_key = f"ratelimit:{key}"
    cache_value = rdb.get(name=cache_key)
    if cache_value is None:
        rdb.set(name=cache_key, value=1, ex=window)
        return False
    if int(cache_value) >= limit:
        return True
    rdb.incr(cache_key)

    return False


@validate_call
def user_ratelimit(
    username: str,
    action: str,
    limit: int,
    window: int,
) -> None:
    """
    User rate limiting for a specific action
    Args:
        username (str): username
        action (str): action to rate limit
        limit (int): limit allowed within the window
        window (int): window in seconds
    Raises:
        HTTPException: Rate limit exceeded
    """
    key = f"ratelimit:{username}:{action}"
    if is_rate_limited(key, limit, window):
        raise HTTPException(status_code=429, detail="Rate limit exceeded.")
