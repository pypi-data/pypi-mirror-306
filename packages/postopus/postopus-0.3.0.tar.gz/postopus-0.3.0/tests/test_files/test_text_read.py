import os
from pathlib import Path

import file_testing_utils as ftutils
import numpy as np
import pytest
from numpy import testing as npt

from postopus.files.text import TextFile


@pytest.fixture
def testfile(methane_run: Path):
    return methane_run / "output_iter" / "td.0000000" / "current-z.z=0"


@pytest.fixture
def testaxisfile(benzene_run: Path):
    return benzene_run / "static" / "density.y=0,z=0"


def test_cache_building(testfile: Path):
    """
    Test opens file, then accesses the data field. Data for 'data'
    will be loaded asynchronously in the background. Therefore need to access both
    as the first action after generation of the object.
    """
    txt = TextFile(testfile)
    assert txt.values is not None
    del txt
    txt = TextFile(testfile)
    assert txt.coords is not None
    del txt
    txt = TextFile(testfile)
    assert txt.dims is not None


def test_get_coords_and_dims(testfile: Path):
    a = TextFile(testfile)
    coords = a.coords
    dims = a.dims

    assert dims == ("x", "y")

    assert isinstance(coords, dict)
    assert list(coords.keys()) == ["x", "y"]

    xpos = coords["x"]
    assert xpos.shape == (27,)

    ypos = coords["y"]
    assert ypos.shape == (27,)

    assert xpos.max() == pytest.approx(7.36993191825401)
    assert xpos.min() == pytest.approx(-7.36993191825401)

    assert ypos.max() == pytest.approx(7.36993191825401)
    assert ypos.min() == pytest.approx(-7.36993191825401)


def test_get_valid_headers(testfile: Path):
    file = TextFile(testfile)
    valid_headers = file.dims
    assert valid_headers == ("x", "y")


def test_get_valid_headers_axisfile(testaxisfile: Path):
    axisfile = TextFile(testaxisfile)
    axis_valid_headers = axisfile.dims
    assert axis_valid_headers == ("x",)


def test_get_valid_headers_simulated_files(
    tmp_path: Path, mock_inp_and_parser_log_and_output: None
):
    # Other headers, as written out by Octopus
    header1 = ("y", "z", "Re", "Im")
    header2 = ("y", "Re", "Im")
    # "Random" header, not output by Octopus
    header3 = ("bla", "bli", "blubb")
    # Duplicate key handling by Pandas is done automatically - but this should never
    # happen with Octopus
    header4 = ("bla", "bla", "blubb", "blubb", "Im")

    # For all headers the following will happen: For len(header) = 3 only the first
    # element will be returned, with len(header) = 4 the first two elements are
    # returned. In ftutils.build_header_tempfile() a '#' is prepended (as normally found
    # in real files). Therefore the last provided element is equivalent to the title
    # "Im" in Octopus' output, while the penultimate element is equivalent to "Re". Both
    # are not "dimension" of the data, but values and therefore are not found in
    # TextFile.dims

    file1 = ftutils.build_header_tempfile(tmp_path / "header_test1.txt", header1)
    file2 = ftutils.build_header_tempfile(tmp_path / "header_test2.txt", header2)
    file3 = ftutils.build_header_tempfile(tmp_path / "header_test3.txt", header3)
    file4 = ftutils.build_header_tempfile(tmp_path / "header_test4.txt", header4)

    t1 = TextFile(file1)
    assert t1.dims == header1[:-2]
    t2 = TextFile(file2)
    assert t2.dims == header2[:-2]
    # Raise a KeyError if "Im" is not in headers (fails to drop)
    with pytest.raises(KeyError):
        t3 = TextFile(file3)
        assert t3.dims == header3
    t4 = TextFile(file4)
    # With duplucate titles Pandas will add a ".1" to the second, already existing title
    assert t4.dims != header4
    assert (t4.dims[0], t4.dims[1]) == (header4[0], header4[1] + ".1")


def test_data_equivalence(testfile: Path):
    a = TextFile(testfile)
    xarr = a.xarray()

    npt.assert_equal(
        a.values,
        xarr.values,
        err_msg="Xarray Values are not the same as the numpy data",
    )

    npt.assert_equal(
        a.values, xarr.data, err_msg="xarray.values should be equal to xarray.data"
    )


def test_non_rectangular_data1(
    tmp_path: Path, mock_inp_and_parser_log_and_output: None
):
    tmpfile = tmp_path / "non_rectangular_data.txt"

    dummy_data = (
        f"# x        y        Re        Im{os.linesep}"
        f"1        10        100{os.linesep}"
        f"{os.linesep}"
        f"0        11        400{os.linesep}"
        f"2        11        200{os.linesep}"
        f"{os.linesep}"
        f"1        12        300{os.linesep}"
    )

    # create test data file
    tmpfile.write_text(dummy_data)

    # read test data file with numpy
    np_check = np.loadtxt(tmpfile)
    # numpy ignores empty lines and the header,
    # and returns 4 rows of data with the 3 columns each:
    assert np_check.shape == (4, 3)

    # read test data file with postopus
    txtfile = TextFile(tmpfile)

    # Check coordinates first:
    npt.assert_equal(txtfile.coords["x"], np.array([0, 1, 2]))
    npt.assert_equal(txtfile.coords["y"], np.array([10, 11, 12]))

    # data has been written to positions with x-values 0, 1, 2 and
    # y-values 0, 1, 2. Expect a 3x3 matrix of values. Some of those are nan:
    assert txtfile.values.shape == (3, 3)
    npt.assert_equal(txtfile.values[0, :], np.array([np.nan, 400, np.nan]))
    npt.assert_equal(txtfile.values[:, 1], np.array([400, np.nan, 200]))


def test_non_rectangular_data2(
    tmp_path: Path, mock_inp_and_parser_log_and_output: None
):
    """Use a set of test data with 4-grid points in x direction
     (at positions 0, 1, 2, 3)
    and 3 points in y at 0, 1, 2. Tricky: no data has been written at x=2.
    """
    tmpfile = tmp_path / "non_rectangular_data2.txt"
    dummy_data = (
        f"# x      y        Re        Im{os.linesep}"
        f"1        10        100{os.linesep}"
        f"{os.linesep}"
        f"0        11        400{os.linesep}"
        f"3        11        200{os.linesep}"
        f"{os.linesep}"
        f"1        12        300{os.linesep}"
    )

    # create test data file
    tmpfile.write_text(dummy_data)

    # read test data file with numpy
    np_check = np.loadtxt(tmpfile)
    # numpy ignores empty lines and the header,
    # and returns 4 rows of data with the 3 columns each:
    assert np_check.shape == (4, 3)

    # read test data file with postopus
    txtfile = TextFile(tmpfile)

    # check coordinates
    npt.assert_equal(txtfile.coords["x"], np.array([0, 1, 2, 3]))
    npt.assert_equal(txtfile.coords["y"], np.array([10, 11, 12]))

    print(txtfile.values)
    # data has been written to positions with x-values 0, 1, 2 and
    # y-values 0, 1, 2. Expect a 3x3 matrix of values. Some of those are nan:
    assert txtfile.values.shape == (4, 3)
    npt.assert_equal(txtfile.values[0, :], np.array([np.nan, 400, np.nan]))
    npt.assert_equal(txtfile.values[:, 1], np.array([400, np.nan, np.nan, 200]))
