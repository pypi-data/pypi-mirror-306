from pathlib import Path

import numpy as np
import pytest
from ase.units import Bohr

from postopus.files.cube import CubeFile


@pytest.fixture
def test_file(benzene_run: Path) -> Path:
    return benzene_run / "static" / "density.cube"


def test_read_values_types(test_file: Path):
    cf = CubeFile(test_file)

    # check types of data
    assert isinstance(cf.values, np.ndarray)
    assert isinstance(cf.dims, list)
    assert isinstance(cf.coords, dict)
    assert isinstance(cf.coords["x"], np.ndarray)


def test_read_values(test_file: Path):
    cf = CubeFile(test_file)

    # Values from file. Data in file is in Bohr. ASE returns data referenced to
    # Angstrom - and Postopus in thise case return data referenced to Angstrom,
    # as this is defined in `inp` file
    comp_origin = list(np.array([-13.03911, -13.606028, -9.070685]))

    # This forces updating of tests when new dimensions are introduced
    assert cf.dims == ["x", "y", "z"]

    origin_from_file = []
    for ax in cf.coords:
        origin_from_file.append(cf.coords[ax][0])

    # check origin
    assert origin_from_file == comp_origin

    # check read values
    assert cf.values.min() == 0
    assert cf.values.max() == pytest.approx(0.324769, abs=1e-4)
    assert cf.values.shape == (47, 49, 33)

    # check dimensions of coords and values are consistent
    coords_shape = tuple([dim.shape[0] for dim in cf.coords.values()])
    assert cf.values.shape == coords_shape

    # check for uniform spacing
    assert np.allclose(np.diff(cf.coords["x"]), np.diff(cf.coords["x"])[0])
    assert np.allclose(np.diff(cf.coords["y"]), np.diff(cf.coords["y"])[0])
    assert np.allclose(np.diff(cf.coords["z"]), np.diff(cf.coords["z"])[0])

    # check spacing. use [0], because last test proves uniform spacing.
    # We expect a spacing of 0.15 angstrom, because it was specified like this in
    # the inp file (tests/data/benzene/inp).
    assert np.diff(cf.coords["x"])[0] * Bohr == pytest.approx(0.3, rel=1e-6)
    assert np.diff(cf.coords["y"])[0] * Bohr == pytest.approx(0.3, rel=1e-6)
    assert np.diff(cf.coords["z"])[0] * Bohr == pytest.approx(0.3, rel=1e-6)


def test_cube_non_orthogonal_basis_raises_error(tmp_path: Path):
    test_content = """Mock data from Postotpus. Atom coordinates are meaningless.
With non-orthogonal basis vectors (HF)
   12  -13.322569  -13.889487   -9.354144
   2    1.000000    0.000000    0.000000
   2    0.500000    0.283459    0.000000
   2    0.000000    0.7070000    0.1
    6    0.000000    0.000000    2.638058    0.000000
    6    0.000000    2.284679    1.319029    0.000000
    6    0.000000    2.284679   -1.319029    0.000000
    6    0.000000    0.000000   -2.638058    0.000000
    6    0.000000   -2.284679   -1.319029    0.000000
    6    0.000000   -2.284679    1.319029    0.000000
    1    0.000000    0.000000    4.684631    0.000000
    1    0.000000    4.057242    2.343260    0.000000
    1    0.000000    4.057242   -2.343260    0.000000
    1    0.000000    0.000000   -4.684631    0.000000
    1    0.000000   -4.057242   -2.343260    0.000000
    1    0.000000   -4.057242    2.343260    0.000000
  0.000000E+00  0.000000E+00  0.000000E+00  0.000000E+00
  0.000000E+00  0.000000E+00  0.000000E+00  0.000000E+00
 """
    test_file = tmp_path / "cube-read-non-orthogonal.cube"
    test_file.write_text(test_content)

    cf2 = CubeFile(test_file)

    # force reading
    with pytest.raises(NotImplementedError):
        cf2.coords
