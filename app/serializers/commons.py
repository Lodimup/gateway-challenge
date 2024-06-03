"""
Common serializers
"""

from pydantic import BaseModel


class GenericErrorResp(BaseModel):
    """
    Generic error response
    """

    detail: str
