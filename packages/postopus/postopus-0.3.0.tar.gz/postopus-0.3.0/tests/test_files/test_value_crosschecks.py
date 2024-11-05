from pathlib import Path

import numpy as np
import numpy.testing as npt
import pytest
from ase.units import Bohr

from postopus.files.cube import CubeFile
from postopus.files.netcdf import NetCDFFile
from postopus.files.text import TextFile
from postopus.files.vtk import VTKFile
from postopus.files.xcrysden import XCrySDenFile

"""
# Introduction to these Tests
These tests try to prove correctness of file readers by comparing different file formats
and their outputs. If the outputs between two different file formats are (almost)
equal, one can assume the reading to be correct.

test_cube_text() and test_text_xsf() check correctness of sliced data (".x=0", ".y=0"
and ".z=0" files) against two other formats. Those contain data in a 3D space, but were
sliced accordingly.

For all other tests XCrysden/".xsf" is used as reference. By showing correctness between
all formats and XCrysden, transitivity can be assumed (a=b and b=c == a=c).
Therefore if e. g. xsf and cube yield correct values and xsf and netcdf are correct,
comparing values from cube with netcdf will yield equal values.
"""

# TODO include also vector field tests


@pytest.fixture
def static_dir(benzene_run: Path) -> Path:
    return benzene_run / "static"


def test_cube_text(static_dir: Path):
    cubef = CubeFile(static_dir / "density.cube")
    textf = TextFile(static_dir / "density.z=0")

    cubeslice = cubef.xarray().sel(z=0, method="nearest")

    assert textf.values.shape == cubeslice.values.shape
    # only can check 5 decimals here with benzene data, because imprecision when octopus
    # writes the coordinates (TextFile) and when we calculate coords with linspace
    # (CubeFile). Might need to be even more restrictive?
    npt.assert_almost_equal(
        textf.coords["x"], cubeslice.coords["x"].values * Bohr, decimal=5
    )
    npt.assert_almost_equal(
        textf.coords["y"], cubeslice.coords["y"].values * Bohr, decimal=5
    )

    # Cannot compare values for equality, because with TextFile we might introduce NaNs
    # when the shape is not rectangular. Need nan_to_num for zeros.
    # Also (* Bohr**3), because density is based on volume, therefore length is cubic
    # Angstrom -> bohr -> divide by ase.Bohr, but density is 1/V, so multiply.
    npt.assert_almost_equal(
        np.nan_to_num(textf.values) * (Bohr**3),
        np.nan_to_num(cubeslice.values),
        decimal=5,
    )


def test_text_xsf(static_dir: Path):
    xsff = XCrySDenFile(static_dir / "density.xsf")
    textf = TextFile(static_dir / "density.z=0")

    xsfxarr = xsff.xarray()
    # need to get mid point of z axis (origin at 0)
    xsfslice = xsfxarr.sel(z=xsfxarr.coords["z"].values[-1] / 2, method="nearest")

    assert textf.values.shape == xsfslice.values.shape
    # XSF file has origin at (0, 0, 0), text file has center at (0, 0, 0), therefore
    # we need adjustment here
    npt.assert_almost_equal(
        textf.coords["x"],
        xsfslice.coords["x"].values - (xsfslice.coords["x"].values[-1] / 2),
    )
    npt.assert_almost_equal(
        textf.coords["y"],
        xsfslice.coords["y"].values - (xsfslice.coords["y"].values[-1] / 2),
    )

    # Cannot compare values for equality, because with TextFile we might introduce NaNs
    # when the shape is not rectangular. Need nan_to_num for zeros.
    npt.assert_almost_equal(np.nan_to_num(textf.values), np.nan_to_num(xsfslice.values))


def test_xsf_cube(static_dir: Path):
    xsff = XCrySDenFile(static_dir / "density.xsf")
    cubef = CubeFile(static_dir / "density.cube")

    xsfxarr = xsff.xarray()
    cubexarr = cubef.xarray()

    # compare dimensions of data
    assert xsfxarr.values.shape == cubexarr.values.shape

    # XSF file has origin at (0, 0, 0), text file has center at (0, 0, 0), therefore
    # we need adjustment here. Plus, cube file output is always in bohr. While
    # our xcrysden data is in angstrom.
    # only comparing 5 decimals, as cube files only store 6 floating point decimals.
    # coords values are calculated, therefore some imprecision seems to be introduced,
    # loosing one decimal in precision

    # x-axis discretization
    npt.assert_almost_equal(
        cubexarr.coords["x"].values * Bohr,
        xsfxarr.coords["x"].values - (xsfxarr.coords["x"].values[-1] / 2),
        decimal=5,
    )
    # y-axis discretization
    npt.assert_almost_equal(
        cubexarr.coords["y"].values * Bohr,
        xsfxarr.coords["y"].values - (xsfxarr.coords["y"].values[-1] / 2),
        decimal=5,
    )
    # z-axis discretization
    npt.assert_almost_equal(
        cubexarr.coords["z"].values * Bohr,
        xsfxarr.coords["z"].values - (xsfxarr.coords["z"].values[-1] / 2),
        decimal=5,
    )

    # Compare field values
    # cube file only stores 6 floating point decimals
    npt.assert_almost_equal(xsfxarr.values * (Bohr**3), cubexarr.values, decimal=6)


def test_xsf_netcdf(static_dir: Path):
    """
    Consistency test between xsf output and netcdf output

    NetCDF coordinate values get numerically inaccurate after 6th decimal point, due to
    the np.linspace() "stop" parameter in netcdf.py:_get_coords().

    """
    xsff = XCrySDenFile(static_dir / "density.xsf")
    netcdff = NetCDFFile(static_dir / "density.ncdf")

    xsfxarr = xsff.xarray()
    netcdfxarr = netcdff.xarray()

    assert xsfxarr.values.shape == netcdfxarr.values.shape

    # XSF file has origin at (0, 0, 0), netcdf file has center at (0, 0, 0), therefore
    # we need adjustment here
    # Only compare 6 decimals, because numpy.linspace produces slightly
    # offset values. TODO: investigate
    npt.assert_almost_equal(
        netcdfxarr.coords["x"].values,
        xsfxarr.coords["x"].values - (xsfxarr.coords["x"].values[-1] / 2),
        decimal=6,
    )
    npt.assert_almost_equal(
        netcdfxarr.coords["y"].values,
        xsfxarr.coords["y"].values - (xsfxarr.coords["y"].values[-1] / 2),
        decimal=6,
    )
    npt.assert_almost_equal(
        netcdfxarr.coords["z"].values,
        xsfxarr.coords["z"].values - (xsfxarr.coords["z"].values[-1] / 2),
        decimal=6,
    )

    npt.assert_almost_equal(xsfxarr.values, netcdfxarr.values, decimal=6)


def test_xsf_vtk(static_dir: Path):
    """
    Consistency test between xsf output and vtk output
    """
    xsff = XCrySDenFile(static_dir / "density.xsf")
    vtkf = VTKFile(static_dir / "density.vtk")

    xsfxarr = xsff.xarray()
    vtkxarr = vtkf.xarray()

    assert xsfxarr.values.shape == vtkxarr.values.shape
    # XSF file has origin at (0, 0, 0), vtk file has center at (0, 0, 0), therefore
    # we need adjustment here
    npt.assert_almost_equal(
        vtkxarr.coords["x"].values,
        xsfxarr.coords["x"].values - (xsfxarr.coords["x"].values[-1] / 2),
        decimal=13,
    )

    npt.assert_almost_equal(
        vtkxarr.coords["y"].values,
        xsfxarr.coords["y"].values - (xsfxarr.coords["y"].values[-1] / 2),
        decimal=13,
    )

    npt.assert_almost_equal(
        vtkxarr.coords["z"].values,
        xsfxarr.coords["z"].values - (xsfxarr.coords["z"].values[-1] / 2),
        decimal=13,
    )

    npt.assert_almost_equal(xsfxarr.values, vtkxarr.values, decimal=7)
