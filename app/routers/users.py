"""
Handles the user routes
"""

from typing import Annotated

from fastapi import APIRouter, Depends
from services.auths import User, get_current_active_user

router = APIRouter(prefix="/user", tags=["auth"])


@router.get(
    "/me",
    summary="Get the current user",
)
async def get_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> User:

    return current_user
