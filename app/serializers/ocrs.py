from typing import Literal

from pydantic import BaseModel, Field, field_validator
from pydantic_core import Url


class FileMeta(BaseModel):
    """
    id: id
    ext: file extension
    md5: md5
    filename: original filename
    url: cdn url
    user_id: owner's user id
    """

    id: str
    ext: str
    md5: str
    file_name: str
    url: Url
    user_id: str


class UploadPostOut(BaseModel):
    files: list[FileMeta]


class OcrPostIn(BaseModel):
    url: str


class OcrPostOut(BaseModel):
    task_id: str


class OcrStatusGetOut(BaseModel):
    status: Literal[
        "PENDING",
        "STARTED",
        "RETRY",
        "FAILURE",
        "SUCCESS",
    ]


class ExtractPostIn(BaseModel):
    query: str = Field(
        ...,
        description="Query to search for",
        examples=["第一節の二 適用区域(第一条の二)"],
    )
    file_id: str = Field(
        ...,
        description="File id to search in",
        examples=[
            "9TMF2cDwGHg1yAz3aNtg_",
        ],
    )

    @field_validator("query")
    def query_validator(cls, value):
        if len(value) < 2:
            raise ValueError("Query must be at least 2 characters long")
        if len(value) > 30:
            raise ValueError("Query must be at most 30 characters long")
        return value


class MetaData(BaseModel):
    md5_hash: str
    meta: str
    user_id: str
    model: str
    user_id: str


class QueryResponse(BaseModel):
    id: str
    score: float
    metadata: MetaData


class ExtractPostOut(BaseModel):
    chatbot_response: str
    query_responses: list[QueryResponse]
