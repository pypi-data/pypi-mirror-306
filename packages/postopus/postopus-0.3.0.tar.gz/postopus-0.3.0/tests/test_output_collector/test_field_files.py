from pathlib import Path

import pytest

from postopus.output_collector import (
    CalcModeFiles,
    OutputField,
    System,
)


@pytest.fixture
def field() -> OutputField:
    system = System("test", Path("test"))
    calc_mode = CalcModeFiles("mode1", system)
    field = OutputField(calc_mode, "field")
    return field


def test_field_files():
    root = Path("/test")
    system = System("test", root)
    calc_mode = CalcModeFiles("td", system)
    field = OutputField(calc_mode, "current")
    files = field.files

    txt1 = root / "file1.txt"
    txt2 = root / "file2.txt"
    txt3_relative = "file3.txt"
    txt3 = root / txt3_relative
    csv1 = root / "file1.csv"

    files.add(txt1)
    files.add(txt2)
    files.add(txt3_relative)
    files.add(csv1)

    assert len(files) == 4
    assert files.extensions == {".txt", ".csv"}
    assert txt1 in files
    assert txt3 in files

    # should not be added again as file is already known with relative path
    files.add(txt3)
    assert len(files) == 4

    files.discard(txt3_relative)
    assert len(files) == 3
    assert txt3 not in files

    assert files.with_extension("csv") == csv1
    assert files.with_extension(".csv") == csv1
    with pytest.raises(FileNotFoundError):
        files.with_extension("foo")

    assert set(files) == {txt1, txt2, csv1}
