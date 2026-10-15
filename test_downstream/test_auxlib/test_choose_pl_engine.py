import polars as pl
import pytest

from downstream._auxlib._choose_pl_engine import choose_pl_engine


@pytest.mark.parametrize("prefer", ["in-memory", "streaming"])
def test_choose_pl_engine_unset(monkeypatch: pytest.MonkeyPatch, prefer: str):
    monkeypatch.delenv("POLARS_ENGINE_AFFINITY", raising=False)
    assert choose_pl_engine(prefer=prefer) == prefer


@pytest.mark.parametrize("prefer", ["in-memory", "streaming"])
@pytest.mark.parametrize("affinity", ["streaming", "in-memory", "auto"])
def test_choose_pl_engine_set(
    monkeypatch: pytest.MonkeyPatch, affinity: str, prefer: str
):
    monkeypatch.setenv("POLARS_ENGINE_AFFINITY", affinity)
    assert choose_pl_engine(prefer=prefer) == affinity


def test_choose_pl_engine_requires_prefer():
    with pytest.raises(TypeError):
        choose_pl_engine()


@pytest.mark.parametrize("affinity", [None, "streaming", "in-memory"])
def test_choose_pl_engine_collectable(
    monkeypatch: pytest.MonkeyPatch, affinity: str
):
    if affinity is None:
        monkeypatch.delenv("POLARS_ENGINE_AFFINITY", raising=False)
    else:
        monkeypatch.setenv("POLARS_ENGINE_AFFINITY", affinity)
    lf = pl.LazyFrame({"a": [1, 2, 3]})
    res = lf.collect(engine=choose_pl_engine(prefer="in-memory"))
    assert res["a"].to_list() == [1, 2, 3]
