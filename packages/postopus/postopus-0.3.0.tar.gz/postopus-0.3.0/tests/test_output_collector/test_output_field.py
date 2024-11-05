from pathlib import Path

import pytest

from postopus.output_collector import (
    CalcModeFiles,
    OutputField,
    System,
    VectorDimension,
)
from postopus.output_collector.other_index import WFState


@pytest.fixture
def calc_mode() -> CalcModeFiles:
    system = System("test", Path("test"))
    calc_mode = CalcModeFiles("mode1", system)
    return calc_mode


def test_base_interface(calc_mode: CalcModeFiles):
    field = OutputField(calc_mode, "field")
    assert field.root_path == calc_mode.system.path

    with pytest.raises(ValueError):
        OutputField(field, "wrong_name")

    assert field.calc_mode is calc_mode
    it0 = field.iterations.setdefault(0)
    assert it0.calc_mode is calc_mode


def test_static_field(calc_mode):
    static_field = OutputField(calc_mode, "field")
    static_field.files.add(Path("file1.foo"))

    assert static_field.is_static()
    assert not static_field.has_iterations()
    assert not static_field.has_other_index()

    assert static_field.is_valid()


def test_field_with_iterations(calc_mode):
    field_with_iterations = OutputField(calc_mode, "field")
    iterations = field_with_iterations.iterations.setdefault(10)
    iterations.files.add(Path("file1.foo"))
    assert field_with_iterations.has_iterations()
    assert not field_with_iterations.is_static()
    assert not field_with_iterations.has_other_index()

    assert field_with_iterations.is_valid()


def test_field_with_other_index(calc_mode):
    field_with_other_index = OutputField(calc_mode, "field")
    other_index = field_with_other_index.other_index.setdefault(VectorDimension("x"))
    other_index.files.add(Path("file1.foo"))
    assert field_with_other_index.has_other_index()
    assert not field_with_other_index.has_iterations()
    assert not field_with_other_index.is_static()

    assert field_with_other_index.is_valid()


def test_invalid_fields(calc_mode):
    # Output field without any files
    field = OutputField(calc_mode, "no files")
    assert not field.is_valid()

    # -> Both, static files and iterations
    field = OutputField(calc_mode, "field1")
    field.files.add(Path("foo.bar"))
    iteration = field.iterations.setdefault(4)
    iteration.files.add(Path("foo.bar"))
    assert not field.is_valid()

    # -> Both, static files and other_index
    field = OutputField(calc_mode, "field2")
    field.files.add(Path("foo.bar"))
    other_field = field.other_index.setdefault(VectorDimension("x"))
    other_field.files.add(Path("foo.bar"))
    assert not field.is_valid()

    # -> Both, iterations and other_index
    field = OutputField(calc_mode, "field3")
    iteration = field.iterations.setdefault(4)
    iteration.files.add(Path("foo.bar"))
    other_field = field.other_index.setdefault(VectorDimension("x"))
    other_field.files.add(Path("foo.bar"))
    assert not field.is_valid()

    # Only a nested field is wrong
    field = OutputField(calc_mode, "field")
    it0 = field.iterations.setdefault(0)
    it0.files.add(Path("foo.bar"))
    it1 = it0.iterations.setdefault(1)
    it1.files.add(Path("foo.bar"))
    assert not field.is_valid()


def test_is_vector(calc_mode):
    field = OutputField(calc_mode, "simple")
    for dim in "xyz":
        field.other_index.setdefault(VectorDimension(dim))
    assert field.is_vector()

    # Test when vector components exists only nested
    field = OutputField(calc_mode, "nested")
    it0 = field.iterations.setdefault(0)
    it0.other_index.setdefault(VectorDimension("x"))
    assert field.is_vector()

    field = OutputField(calc_mode, "wf")
    field.other_index.setdefault(WFState(1))
    assert not field.is_vector()

    field = OutputField(calc_mode, "static")
    field.files.add(Path("file1.foo"))
    assert not field.is_vector()


def test_all_other_index(calc_mode):
    field = OutputField(calc_mode, "static")
    field.files.add("file0.foo")
    assert set(field.all_other_index()) == set()

    field = OutputField(calc_mode, "iter")
    it0 = field.iterations.setdefault(0)
    it0.other_index.setdefault(VectorDimension("x"))
    it1 = field.iterations.setdefault(1)
    it1.other_index.setdefault(VectorDimension("y"))
    it1.other_index.setdefault(VectorDimension("z"))
    expected = {VectorDimension(d) for d in "xyz"}
    assert set(field.all_other_index()) == expected
