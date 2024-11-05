from pathlib import Path

import pytest

from postopus.output_collector import (
    CalcModeFiles,
    OutputField,
    System,
)


@pytest.fixture
def system():
    system = System("test", Path("test/"))
    return system


def test_calc_mode_files(system):
    td = CalcModeFiles("td", system)
    assert td.root_path == Path("test/")
    density1 = td.get_or_init("density")
    density2 = td.get_or_init("density")
    assert density1 is density2
    assert td["density"].field == "density"

    td["wf"] = OutputField(td, "wf")
    assert len(td) == 2
    assert set(td) == {"density", "wf"}

    del td["density"]
    assert len(td) == 1
    assert set(td) == {"wf"}

    with pytest.raises(ValueError):
        td["foo"] = OutputField(td, "bar")
