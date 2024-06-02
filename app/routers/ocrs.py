"""
Handles OCR functionalities, and extractions
"""

import asyncio
from typing import Annotated

from celery.result import AsyncResult
from constants.limits import UserLimit
from fastapi import APIRouter, Body, Depends, HTTPException, UploadFile
from scheduler import app
from serializers.commons import GenericErrorResp
from serializers.ocrs import OcrPostIn, OcrPostOut, OcrStatusGetOut, UploadPostOut
from services.auths import User, get_current_active_user
from services.limits import is_rate_limited
from services.storages import handle_file_upload
from tasks.ocrs import mock_ocr_and_embed_to_pc
from validators.ocrs import validate_files

# FIXME: prefix should be ocr for namspacing, but let's follow the
# Take Home Assignment's instructions for now.
router = APIRouter(
    # prefix="/ocr",
    tags=["ocr"],
)


@router.post(
    "/upload",
    responses={
        200: {"model": UploadPostOut},
        413: {"model": GenericErrorResp},
        406: {"model": GenericErrorResp},
        500: {"model": GenericErrorResp},
    },
)
async def post_upload(
    user: Annotated[User, Depends(get_current_active_user)],
    files: list[UploadFile],
) -> UploadPostOut:
    """
    # Note
    Take Home Assignment dictates that the endpoint should accept
    a list of files.<br>
    However, the endpoint should only accept one file at a time.<br>
    Multiple files upload should be handled by the client.<br>
    So, progress bar for each upload is possible.<br>

    This endpoint follows the Take Home Assignment's instructions.

    # Upload
    - Validate the file(s)
    - Rename the file to a unique web-safe name
    - Calculate the md5 hash of the file
    - Upload the file to a S3 bucket
    - Store file's metadata in mongodb
    """
    if is_rate_limited(f"{user.user_id}:upload", **UserLimit.UPLOAD):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded",
        )
    if not files:
        raise HTTPException(
            status_code=406,
            detail="No file(s) uploaded",
        )
    validate_files(files)

    async def _task(file, user_id):
        return handle_file_upload(file, user_id)

    res = await asyncio.gather(*[_task(file, user.user_id) for file in files])

    if not all(res):
        raise HTTPException(
            status_code=500,
            detail="Failed to upload file(s) to s3",
        )

    return UploadPostOut(files=res)


@router.post("/ocr")
def post_ocr(
    user: Annotated[User, Depends(get_current_active_user)],
    payload: OcrPostIn = Body(...),
) -> OcrPostOut:
    """
    OCR and embed paragraphs to Pinecone using task queue.
    Note: Since we do keep document's id in mongodb we can actually implement
    POST /document/:doc_id/ocr instead of this route
    It would be more RESTful and user friendly but let's follow the
    Take Home Assignment's instructions for now.
    - If the file is not uploaded, being processed, or failed, the status in
    `AsyncResult(task_id, app=app).get()` will have a not None error object
    - If the file is uploaded, mock the ocr result and embed to Pinecone
    - file can only be OCR'd once
    - while OCR is pending, user can't request another OCR
    user can be notified immediately if we implement POST /document/:doc_id/ocr
    """
    if is_rate_limited(f"{user.user_id}:ocr", **UserLimit.OCR):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded",
        )
    result = mock_ocr_and_embed_to_pc.s(payload.url, payload.user_id).delay()
    return {"task_id": result.id}


@router.get("/ocr/{task_id}/status")
def get_ocr_status(
    user: Annotated[User, Depends(get_current_active_user)],
    task_id: str,
) -> OcrStatusGetOut:
    """
    Return the status of the OCR task given the task_id
    """
    if is_rate_limited(f"{user.user_id}:core", **UserLimit.CORE):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded",
        )
    result = AsyncResult(task_id, app=app).status
    return {"status": result}
