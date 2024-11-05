from pathlib import Path

import pytest

from postopus.files.vtk import VTKFile


@pytest.fixture
def test_file(methane_run: Path) -> Path:
    return methane_run / "output_iter" / "scf.0005" / "density.vtk"


@pytest.fixture
def testfile_non_symmetric(benzene_run: Path) -> Path:
    return benzene_run / "static" / "density.vtk"


def test_vtk_cache_building(test_file: Path):
    """
    Test opens file, then accesses the data field. Data for values, coords and dims
    will be loaded asynchronously in the background. Therefore need to access both
    as the first action after generation of the object.
    """
    vtkfile = VTKFile(test_file)
    assert vtkfile.values is not None
    del vtkfile
    vtkfile = VTKFile(test_file)
    assert vtkfile.coords is not None
    del vtkfile
    vtkfile = VTKFile(test_file)
    assert vtkfile.dims is not None


def test_vtk_get_coords_and_dims(test_file: Path):
    """
    Test reading coordinates and dimensions from vtk file.

    """
    vtk_file = VTKFile(test_file)
    coords = vtk_file.coords

    assert list(coords.keys()) == ["x", "y", "z"]

    assert coords["x"].shape == coords["y"].shape == coords["z"].shape == (27,)

    assert coords["x"][0] == pytest.approx(-7.369932) == coords["x"].min()
    assert coords["x"][1] == pytest.approx(-6.803014)
    assert coords["y"][-1] == pytest.approx(7.369935999999996) == coords["y"].max()
    assert coords["z"][11] == pytest.approx(-1.1338339999999985, rel=1e-5)

    assert vtk_file.dims == ("x", "y", "z")


def test_vtk_get_coords_and_dims_non_symmetric(benzene_run: Path):
    """Non-symmetric case, x, y, z not eq. long"""
    testfile_non_symmetric = benzene_run / "static" / "density.vtk"
    ns_vtk_file = VTKFile(testfile_non_symmetric)
    ns_coords = ns_vtk_file.coords

    assert list(ns_coords.keys()) == ["x", "y", "z"]

    assert ns_coords["x"].shape == (47,)
    assert ns_coords["y"].shape == (49,)
    assert ns_coords["z"].shape == (33,)

    assert ns_coords["x"][0] == pytest.approx(-6.9) == ns_coords["x"].min()
    assert ns_coords["x"][-1] == pytest.approx(6.9) == ns_coords["x"].max()
    assert ns_coords["y"][-1] == pytest.approx(7.2) == ns_coords["y"].max()
    assert ns_coords["y"][10] == pytest.approx(-4.2)
    assert ns_coords["z"][-1] == pytest.approx(4.8) == ns_coords["z"].max()

    assert ns_vtk_file.dims == ("x", "y", "z")


def test_vtk_get_values(test_file: Path):
    """
    Test reading data values from a vtk file.

    """
    vtk_file = VTKFile(test_file)
    values = vtk_file.values

    assert values[18][18][18] == pytest.approx(0.0006063255231099469, rel=1e-3)
    assert values[5][13][14] == pytest.approx(0.0002975716035407837, rel=1e-3)
    assert values[0][7][23] == 0.0
    assert values.min() == 0.0
    assert values.max() == pytest.approx(0.30881128883688413, rel=1e-3)

    assert values.shape == (27, 27, 27)
