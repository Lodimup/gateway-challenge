"""
Handles application limits
"""


class UserLimit:
    """
    User limits are used to control the number of actions a user can perform
    in a given time window.
    See: app/services/limits.py
    Ex.
        - limit: 5
        - window: 30
        - A user can call upload 5 times every 30 seconds.

    UPLOAD: limit and window for upload endpoints
    OCR: limit and window for ocr endpoints
    EXTRACT: limit and window for extract endpoints
    CORE: limit and window for non heavy resource consuming endpoints
    """

    UPLOAD = {
        "limit": 5,
        "window": 30,
    }

    OCR = {
        "limit": 5,
        "window": 30,
    }

    EXTRACT = {
        "limit": 10,
        "window": 30,
    }

    CORE = {
        "limit": 300,
        "window": 10,
    }
