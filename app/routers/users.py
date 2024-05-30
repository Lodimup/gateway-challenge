"""
Handles the user routes
"""

from services.auths import User, get_current_active_user

from fastapi import APIRouter, Depends

from typing import Annotated

router = APIRouter(prefix="/user", tags=["auth"])


@router.get(
    "/me",
    summary="Get the current user",
)
async def get_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> User:

    return current_user
