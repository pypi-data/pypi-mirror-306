from time import perf_counter

from .log import logger


def measureTime(func):
    def wrapper(*args, **kwargs):
        start_time = perf_counter()
        error = None
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            error = e
        end_time = perf_counter()
        logger.info(
            f"Function {func.__name__!r} took {end_time - start_time} seconds to run"
        )
        if error:
            raise error
        return result

    return wrapper
