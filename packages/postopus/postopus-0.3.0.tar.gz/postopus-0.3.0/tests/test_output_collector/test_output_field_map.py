from pathlib import Path

import pytest

from postopus.output_collector.collector import (
    CalcModeFiles,
    OutputField,
    OutputFieldMap,
    System,
)


@pytest.fixture
def field() -> OutputField:
    system = System("test", Path("test"))
    calc_mode = CalcModeFiles("mode1", system)
    field = OutputField(calc_mode, "field")
    return field


def test_output_field_map(field):
    field_map = OutputFieldMap(field)
    sub1 = field_map.setdefault(1)
    assert sub1 is field_map.setdefault(1, OutputField(field))
    assert sub1 is field_map[1]

    field_map[2] = OutputField(field)
    assert len(field_map) == 2
    assert set(field_map) == {1, 2}

    del field_map[2]
    assert len(field_map) == 1
    assert set(field_map) == {1}

    assert field_map.get_any() is not None
    del field_map[1]
    assert field_map.get_any() is None

    with pytest.raises(TypeError):
        field_map.setdefault(1, "foo")
