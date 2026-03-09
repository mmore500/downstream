import multiprocessing

from downstream._auxlib._starfunc import starfunc


def _add(a, b):
    return a + b


@starfunc
def _add_star(a, b):
    return a + b


def test_starfunc_basic():
    wrapped = starfunc(_add)
    assert wrapped((1, 2)) == 3


def test_starfunc_strings():
    wrapped = starfunc(_add)
    assert wrapped(("foo", "bar")) == "foobar"


def test_starfunc_single_arg():
    @starfunc
    def negate(x):
        return -x

    assert negate((42,)) == -42


def test_starfunc_preserves_name():
    wrapped = starfunc(_add)
    assert wrapped.__name__ == "_add"


def test_starfunc_with_pool_imap():
    ctx = multiprocessing.get_context("spawn")
    with ctx.Pool(1) as pool:
        results = list(pool.imap(_add_star, [(1, 2), (3, 4), (5, 6)]))
    assert results == [3, 7, 11]


def test_starfunc_with_pool_map():
    ctx = multiprocessing.get_context("spawn")
    with ctx.Pool(1) as pool:
        results = pool.map(_add_star, [(10, 20), (30, 40)])
    assert results == [30, 70]
