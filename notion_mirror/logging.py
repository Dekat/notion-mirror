import logging
import sys

from instance import settings


def __init_logger() -> logging.Logger:
    handler = logging.StreamHandler(sys.stdout)

    logger = logging.getLogger("notion_mirror")
    logger.setLevel(settings.LOG_LEVEL)
    logger.addHandler(handler)

    return logger


logger = __init_logger()
