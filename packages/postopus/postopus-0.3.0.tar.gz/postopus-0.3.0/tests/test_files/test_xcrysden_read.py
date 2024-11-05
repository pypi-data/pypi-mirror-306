from pathlib import Path

import pytest

from postopus.files.xcrysden import XCrySDenFile


@pytest.fixture
def test_file(methane_run: Path) -> Path:
    return methane_run / "output_iter" / "scf.0004" / "density.xsf"


@pytest.fixture
def testfile_non_symmetric(benzene_run: Path) -> Path:
    return benzene_run / "static" / "density.xsf"


def test_xcrysden_cache_building(test_file: Path):
    xcrysd_file = XCrySDenFile(test_file)
    assert xcrysd_file.values is not None
    del xcrysd_file
    xcrysd_file = XCrySDenFile(test_file)
    assert xcrysd_file.coords is not None
    del xcrysd_file
    xcrysd_file = XCrySDenFile(test_file)
    assert xcrysd_file.dims is not None


def test_xcrysden_get_coords(test_file: Path, testfile_non_symmetric: Path):
    xsf_file = XCrySDenFile(test_file)
    coords = xsf_file.coords

    assert list(coords.keys()) == ["x", "y", "z"]

    assert coords["x"].shape == coords["y"].shape == coords["z"].shape == (27,)

    assert coords["x"][0] == 0.0 == coords["x"].min()
    assert coords["x"][1] == pytest.approx(0.5669178461538462)
    assert coords["y"][-1] == pytest.approx(14.739864) == coords["y"].max()
    assert coords["z"][11] == pytest.approx(6.236096307692309)


def test_xcrysden_get_coords_non_symmetric(benzene_run: Path):
    """Non-symmetric case, x, y, z not eq. long"""
    testfile_non_symmetric = benzene_run / "static" / "density.xsf"
    ns_xsf_file = XCrySDenFile(testfile_non_symmetric)
    ns_coords = ns_xsf_file.coords

    assert list(ns_coords.keys()) == ["x", "y", "z"]

    assert ns_coords["x"].shape == (47,)
    assert ns_coords["y"].shape == (49,)
    assert ns_coords["z"].shape == (33,)

    assert ns_coords["x"][0] == 0.0 == ns_coords["x"].min()
    assert ns_coords["x"][-1] == 13.8 == ns_coords["x"].max()
    assert ns_coords["y"][-1] == 14.4 == ns_coords["y"].max()
    assert ns_coords["y"][10] == 3.0
    assert ns_coords["z"][-1] == 9.6 == ns_coords["z"].max()


def test_xcrysden_get_dims(test_file: Path):
    xsf_file = XCrySDenFile(test_file)
    dims = xsf_file.dims
    assert dims == ("x", "y", "z")


def test_xcrysden_get_values(test_file: Path):
    xsf_file = XCrySDenFile(test_file)
    values = xsf_file.values

    assert values[18][18][18] == pytest.approx(0.0005, rel=0.5)
    assert values[5][13][14] == pytest.approx(0.0003, rel=0.5)

    assert values[0][7][23] == 0.0
    assert values.min() == 0.0
    assert values.max() == pytest.approx(0.3, rel=0.5)

    assert values.shape == (27, 27, 27)


def test_error_raising(tmp_path: Path):
    tmpfile = tmp_path / "two_d.xsf"

    twod_date = """ATOMS
         C    7.483315    7.483315    7.483315
         H    8.680180    8.680180    8.680180
         H    6.286451    6.286451    8.680180
         H    8.680180    6.286451    6.286451
         H    6.286451    8.680180    6.286451
BEGIN_BLOCK_DATAGRID_2D
units: coords = b, function = b^-3
BEGIN_DATAGRID_2D_function
     2     2
0.0 0.0 0.0
   14.966631    0.000000
    0.000000   14.966631
        0.000000000000000
        0.000000000000000
        0.000000000000000
        0.000000000000000
END_DATAGRID_2D
END_BLOCK_DATAGRID_2D

"""

    # create test data file
    tmpfile.write_text(twod_date)

    with pytest.raises(
        AssertionError, match=r"xcrysden per se supports 2([a-zA-Z23., /-:]*)"
    ):
        xsf_file = XCrySDenFile(tmpfile)
        xsf_file.values
