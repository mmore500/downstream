import itertools as it
import multiprocessing
import typing

from parallelbar import progress_starmap


def _apply_args_and_kwargs(
    fn: typing.Callable,
    args: list,
    kwargs: dict,
) -> object:
    """Implementation detail for starstarmap."""
    return fn(*args, **kwargs)


# adapted from https://stackoverflow.com/a/53173433/17332200
def starstarmap(
    pool: multiprocessing.Pool,
    fn: typing.Callable,
    args_iter: typing.Iterable[list],
    kwargs_iter: typing.Iterable[dict],
) -> list:
    """Invokes callable fn over zip of given args and kwargs."""
    args_for_starmap = zip(it.repeat(fn), args_iter, kwargs_iter)
    return pool.starmap(_apply_args_and_kwargs, args_for_starmap)


def progress_starstarmap(
    fn: typing.Callable,
    args_iter: typing.Iterable[list],
    kwargs_iter: typing.Iterable[dict],
    **kwargs: dict,
) -> list:
    """Invokes callable fn over zip of given args and kwargs."""
    args_for_starmap = zip(it.repeat(fn), args_iter, kwargs_iter)
    return progress_starmap(
        _apply_args_and_kwargs,
        args_for_starmap,
        **kwargs,
    )
