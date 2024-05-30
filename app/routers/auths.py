"""
Handles authentication routes
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from typing import Annotated

from services.auths import UserInDB, fake_hash_password, FAKE_USERS_DB

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = FAKE_USERS_DB.get(form_data.username)
    if not user_dict:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
        )
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
        )

    return {"access_token": user.username, "token_type": "bearer"}
