import polars as pl
import pytest

from downstream._auxlib._get_pl_collect_engine import get_pl_collect_engine


def test_get_pl_collect_engine_unset(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("POLARS_ENGINE_AFFINITY", raising=False)
    assert get_pl_collect_engine() == "in-memory"


def test_get_pl_collect_engine_empty(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("POLARS_ENGINE_AFFINITY", "")
    assert get_pl_collect_engine() == "in-memory"


@pytest.mark.parametrize("affinity", ["streaming", "in-memory", "auto"])
def test_get_pl_collect_engine_set(
    monkeypatch: pytest.MonkeyPatch, affinity: str
):
    monkeypatch.setenv("POLARS_ENGINE_AFFINITY", affinity)
    assert get_pl_collect_engine() == "auto"


@pytest.mark.parametrize("affinity", [None, "streaming", "in-memory"])
def test_get_pl_collect_engine_collectable(
    monkeypatch: pytest.MonkeyPatch, affinity: str
):
    if affinity is None:
        monkeypatch.delenv("POLARS_ENGINE_AFFINITY", raising=False)
    else:
        monkeypatch.setenv("POLARS_ENGINE_AFFINITY", affinity)
    lf = pl.LazyFrame({"a": [1, 2, 3]})
    res = lf.collect(engine=get_pl_collect_engine())
    assert res["a"].to_list() == [1, 2, 3]
