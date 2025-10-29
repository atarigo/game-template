from functools import wraps
from typing import Callable, Type

import structlog

logger = structlog.get_logger(__name__)


def exception_handler(*exceptions: Type[Exception]):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exceptions:
                logger.exception("Raising exception", exc_info=True)
                raise

        return wrapper

    return decorator
