from pylib import Literal


def test_Literal():
    value: Literal["asdf"] = "asdf"  # noqa: F821, F841
