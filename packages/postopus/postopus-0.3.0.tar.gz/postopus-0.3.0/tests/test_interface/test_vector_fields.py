from pathlib import Path

from postopus import Run
from postopus.files import openfile


def test_read_vectorfield(methane_run: Path):
    run = Run(methane_run)
    current = run.default.td.current
    data = current(".z=0")
    assert data.data_vars.keys() == {"vx", "vy", "vz"}


def test_vtk(kpoints_run: Path):
    """In vtk all vector components are stored in one file
    which introduces some special handling (the file reader for vtk
    provides all three components in one array). Check if the interface
    saparates the three components correctly (e.g. instead of always using
    the x component even when y or z is requested).
    """
    run = Run(kpoints_run)
    current = run.default.td.current
    xarr = current(source="vtk")
    file = openfile(kpoints_run / "output_iter" / "td.0000000" / "current.vtk")
    t0 = xarr.sel(t=0)
    # Make sure the correct vector components are provided.
    assert (t0.vx == file.values[0]).all()
    assert (t0.vy == file.values[1]).all()
    assert (t0.vz == file.values[2]).all()

    # The test could yield a false positiv if all values are the same...
    assert (t0.vx != t0.vy).any()
    assert (t0.vy != t0.vz).any()
    assert (t0.vz != t0.vx).any()
