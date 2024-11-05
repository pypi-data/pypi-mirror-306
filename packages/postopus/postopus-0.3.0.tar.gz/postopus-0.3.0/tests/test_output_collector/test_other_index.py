from pathlib import Path

import pytest

from postopus.output_collector.other_index import (
    FieldFileInfo,
    OtherIndex,
    VectorDimension,
    WFState,
)


def test_vector_dim():
    with pytest.raises(ValueError):
        VectorDimension("a")

    info = FieldFileInfo(Path("dummy"), "current-x", "")
    field_name, index = OtherIndex.find_match(info)
    assert field_name == "current"
    assert index == VectorDimension("x")
    assert index.get_coordinates() == {"dim": "x"}

    info = FieldFileInfo(Path("dummy"), "current-z", "")
    field_name, index = OtherIndex.find_match(info)
    assert field_name == "current"
    assert index == VectorDimension("z")
    assert index.get_coordinates() == {"dim": "z"}

    info = FieldFileInfo(Path("dummy"), "current-a", "")
    match = OtherIndex.find_match(info)
    assert match is None


def test_wf_state():
    info = FieldFileInfo(Path("dummy"), "wf-st0001.xsf", ".xsf")
    field_name, index = OtherIndex.find_match(info)
    assert field_name == "wf"
    assert index == WFState(st=1)
    assert index.get_coordinates() == {"st": 1}

    info = FieldFileInfo(Path("dummy"), "wf-k0004-st0002.xsf", ".xsf")
    field_name, index = OtherIndex.find_match(info)
    assert field_name == "wf"
    assert index == WFState(st=2, k=4)
    assert index.get_coordinates() == {"st": 2, "k": 4}

    info = FieldFileInfo(Path("dummy"), "wf-k0004-st0002-sp1234.xsf", ".xsf")
    field_name, index = OtherIndex.find_match(info)
    assert field_name == "wf"
    assert index == WFState(st=2, k=4, sp=1234)
    assert index.get_coordinates() == {"st": 2, "k": 4, "sp": 1234}


def test_vtk_match(methane_run: Path):
    data = methane_run / "output_iter" / "td.0000000"

    info = FieldFileInfo(data / "current.vtk", "current", ".vtk")
    field_name, index = OtherIndex.find_match(info)
    for dim in "xyz":
        assert VectorDimension(dim) in index

    info = FieldFileInfo(data / "density.vtk", "density", ".vtk")
    match = OtherIndex.find_match(info)
    assert match is None
