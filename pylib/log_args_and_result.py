import functools
import typing


# adapted from https://realpython.com/primer-on-python-decorators/
def log_args_and_result(
    logger: typing.Any,
    log_level: int,
) -> typing.Callable:
    """Decorates function to log arguments and return value.

    Parameters
    ----------
    logger : logging.Logger
        The logger to be used.
    log_level : int
        Logging level to add entries at (e.g. logging.INFO, logging.DEBUG).

    Examples
    --------
    >>> import logging
    >>> logging.basicConfig(level=logging.INFO)
    >>> logger = logging.getLogger()
    >>> @log_args_and_result(logger=logger, log_level=logging.INFO)
    ... def add(a, b):
    ...     return a + b
    ...
    >>> add(2, 3)
    calling add(2, 3)
    'add' returned 5
    """

    def decorator(func: typing.Callable) -> typing.Callable:
        """Print the function signature, args and return value"""
        @functools.wraps(func)
        def wrap(*args, **kwargs):
            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)
            logger.log(
                level=log_level,
                msg=f">>> calling {func.__name__}({signature})",
            )
            value = func(*args, **kwargs)
            logger.log(
                level=log_level,
                msg=f">> {func.__name__!r} returned {value!r}",
            )
            return value

        return wrap

    return decorator
