"""
Extra validators for OCRs endpoints
"""

from fastapi import HTTPException, UploadFile


def validate_file_size(file: UploadFile, max_size: int) -> bool:
    """
    File size validator for /upload endpoint
    Args:
        file (UploadFile): UploadFile
    Returns:
        bool: True if valid
    """
    file_size = 0
    for chunk in file.file:
        file_size += len(chunk)
        if file_size > max_size:
            raise HTTPException(
                status_code=413,
                detail="File too large",
            )

    return True


def validate_files(files: list[UploadFile] = []) -> bool:
    """
    File validator for /upload endpoint
    Args:
        files (list[UploadFile]): list of UploadFile
    Returns:
        bool: True if valid
    """
    ALLOW_TYPES = [
        "application/pdf",
        "image/tiff",
        "image/jpeg",
        "image/png",
    ]
    MAX_FILES = 5
    MAX_SIZE = 100 * 1024 * 1024  # 10MB

    if len(files) > MAX_FILES:
        raise HTTPException(
            status_code=413,
            detail="Too many files. Max 5 files allowed.",
        )
    for file in files:
        if not validate_file_size(file, MAX_SIZE):
            raise HTTPException(
                status_code=413,
                detail="File too large",
            )
        if file.content_type not in ALLOW_TYPES:
            raise HTTPException(
                status_code=406,
                detail="Invalid file type",
            )

    return True
