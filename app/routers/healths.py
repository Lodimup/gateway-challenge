"""
Handles app health routes
"""

from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/live")
def get_live():
    """
    Returns 200 {"status": "ok"} if the server is live
    """
    return {"status": "ok"}
