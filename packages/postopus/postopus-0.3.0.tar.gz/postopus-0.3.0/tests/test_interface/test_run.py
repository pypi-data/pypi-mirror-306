import os
from pathlib import Path

import pytest

from postopus import Run


@pytest.fixture
def restore_working_directory(
    request: pytest.FixtureRequest,
) -> None:
    """Reset the working directory to the original path after a test is finised.
    (pytest doesnt change back to the default directory after a test is run.)
    """
    orig_path = request.config.invocation_params.dir
    yield
    os.chdir(orig_path)


def test_bad_path(testdata_dir: Path, methane_run: Path):
    with pytest.raises(NotADirectoryError):
        Run(methane_run / "inp")

    with pytest.raises(FileNotFoundError):
        Run(testdata_dir)


def test_run_instantiation(restore_working_directory: None, methane_run: Path):
    """
    Test checks if the default value for the path of a run object
    is the current working directory.
    """
    os.chdir(methane_run.parent)
    run1 = Run(methane_run.name)
    run1_path = Path(os.path.join(os.getcwd(), run1.path))

    os.chdir(methane_run.name)
    run2 = Run()
    run2_path = Path(os.path.join(os.getcwd(), run2.path))

    assert run1_path == run2_path


def test_expected_outputs(methane_run: Path, benzene_run: Path):
    run = Run(methane_run)
    assert run.default.scf.outputs.keys() == {
        "density",
        "convergence",
        "forces",
        "info",
        "wf",
    }
    assert run.default.td.outputs.keys() == {
        "current",
        "density",
        "energy",
        "laser",
        "multipoles",
        "wf",
    }

    run = Run(benzene_run)
    assert run.default.scf.outputs.keys() == {
        "density",
        "convergence",
        "forces",
        "info",
    }


def test_repr(methane_run: Path):
    """Make sure the __repr__ methods are at least not
    throwing any exceptions.
    """
    run = Run(methane_run)

    # Test run object
    r = repr(run)
    assert "Found systems" in r
    assert "default" in r
    assert "Found calculation modes" in r
    assert "td" in r
    assert "scf" in r

    # Test system
    r = repr(run.default)
    assert "Found calculation modes" in r
    assert "td" in r
    assert "scf" in r

    # Test calculation modes
    r = repr(run.default.scf)
    assert "Ground state calculation" in r
    assert "convergence" in r
    assert "density" in r
    r = repr(run.default.td)
    assert "Time dependent simulation" in r
    assert "current" in r

    # Test output
    r = repr(run.default.scf.convergence)
    r = repr(run.default.scf.density)
    assert "Available sources" in r
    assert ".vtk" in r
    assert ".ncdf" in r
    r = repr(run.default.td.current)
    assert "Available sources" in r
    assert ".vtk" in r
    assert ".ncdf" in r
