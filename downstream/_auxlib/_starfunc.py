import functools
import typing


def starfunc(fn: typing.Callable) -> typing.Callable:
    """Decorator that unpacks a single tuple argument into ``*args``.

    Useful for adapting multi-argument functions to work with
    ``pool.imap`` and ``pool.map``, which pass a single iterable item
    to the worker function.
    """

    @functools.wraps(fn)
    def wrapper(args: tuple) -> object:
        return fn(*args)

    return wrapper
