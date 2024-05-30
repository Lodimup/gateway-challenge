"""
Handles OCR functionalities, and extractions
"""

import asyncio
from fastapi import APIRouter, HTTPException, UploadFile

from serializers.commons import GenericErrorResp
from serializers.ocrs import UploadPostOut
from services.storages import handle_file_upload
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
    # auth
    # user_id = get_user_id()
    validate_files(files)

    async def _task(file, user_id):
        return handle_file_upload(file, user_id)

    res = await asyncio.gather(*[_task(file, "user_id") for file in files])

    if not all(res):
        raise HTTPException(
            status_code=500,
            detail="Failed to upload file(s) to s3",
        )

    return UploadPostOut(files=res)
