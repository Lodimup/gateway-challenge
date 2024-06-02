"""
Handles logging
Logs uncaught exceptions, and log level above errors to the error.log file.
Note:
Usually logging is handled by cloud providers like AWS CloudWatch, GCP Cloud Logging,
When deployed on managed infrastructure like K8s, Fargate, Cloud Run etc.
But, for the sake of this assignment, we will log to a file to simulate EC2 deployment
The file must be mounted to disk to persist logs. Ex. 
"""

import logging
import sys

logger = logging.getLogger(__name__)


def handle_uncaught_exception(exc_type, exc_value, exc_traceback):
    """
    Custom excepthook to log uncaught exceptions
    """
    if issubclass(exc_type, KeyboardInterrupt):
        # Will call default excepthook
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
        # Create a critical level log message with info from the except hook.
    logger.critical(
        "Unhandled exception", exc_info=(exc_type, exc_value, exc_traceback)
    )


# Assign the excepthook to the handler
sys.excepthook = handle_uncaught_exception

logging.basicConfig(
    filename="error.log",
    level=logging.ERROR,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
