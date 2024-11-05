from pathlib import Path

import pytest

from postopus.output_collector import (
    CalcModeFiles,
    System,
)


def test_system():
    system = System("test", Path("test/"))

    scf = system.setdefault("scf")
    system.setdefault("td", CalcModeFiles("td", system))
    assert len(system) == 2
    assert system.keys() == {"scf", "td"}
    assert system["scf"] is scf

    del system["scf"]
    assert len(system) == 1
    assert system.keys() == {"td"}

    system["scf"] = scf
    assert len(system) == 2
    assert system.keys() == {"scf", "td"}

    with pytest.raises(ValueError):
        system["foo"] = CalcModeFiles("bar", system)
    with pytest.raises(ValueError):
        system.setdefault("foo", CalcModeFiles("bar", system))
    with pytest.raises(TypeError):
        system.setdefault("foo", "bar")
