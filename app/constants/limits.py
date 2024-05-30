class UserLimit:
    """
    User limits are used to control the number of actions a user can perform
    in a given time window.
    See: app/services/limits.py
    Ex.
        - limit: 5
        - window: 30
        - A user can call upload 5 times every 30 seconds.
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
