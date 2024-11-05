from __future__ import annotations

import os
from itertools import product
from pathlib import Path
from shutil import copytree, rmtree

import pytest


def duplicate_with_missing(basepath: Path, targetpath: Path, missing: list[Path]):
    """
    Creates a new "example" in Postopus' tests/data directory from an existing one.
    New example may have missing files/folders. Data is not copied, but hard linked.

    Parameters
    ----------
    base
        Name of the example that shall be "duplicated"
    target
        Name of the "duplicated" example (result folder)
    missing
        List of files or folders in the original data that are not duplicated. Paths
        are relative to `base`.

        Examples
        --------
        Duplicate "methane" with missing "scf.0003" and "inp".

    >>> from pathlib import Path
    >>> duplicate_with_missing(
    ...     Path("methane"),
    ...     Path("methane_copy"),
    ...     [Path("output_iter/scf.0003"), Path("inp")]
    ... )
    """
    target = targetpath / basepath.name

    missing_paths = [basepath / elem for elem in missing]

    def ignore_patterns(src, names):
        check_paths = set(Path(src) / name for name in names)
        ignored_paths = check_paths.intersection(missing_paths)
        return set(ignored.name for ignored in ignored_paths)

    testdatadir = Path(__file__).parent

    # Check if there exists some example to duplicate
    if not basepath.is_dir():
        raise FileNotFoundError(f"No folder '{basepath}' in path {testdatadir}!")

    # Check if there is something to do or everything is up to date.
    # Use the .gitignore file to get the timestamp.
    gitignore_file = targetpath / ".gitignore"
    if (
        targetpath.exists()
        and gitignore_file.exists()
        and gitignore_file.stat().st_mtime >= basepath.stat().st_mtime
    ):
        return target

    if targetpath.exists():
        rmtree(targetpath)

    copytree(
        basepath,
        target,
        ignore=ignore_patterns,
        copy_function=os.link,
    )

    # Create a dummy file to know if timestamps of the source are newer for
    # the next run. (Doesnt work directly by getting any timestamp of the
    # duplicated folder as os.link is used...). As we should place a proper
    # .gitignore inside anyway combine this.
    gitignore_file.write_text(f"# created by {Path(__file__).name}\n*")

    return target


# Create extra test cases
@pytest.fixture
def methane_min_no_static(testdata_dir: Path, methane_run: Path) -> Path:
    target = testdata_dir / "methane_min_no_static"
    return duplicate_with_missing(methane_run, target, [Path("static")])


@pytest.fixture
def benzene_no_convergence(testdata_dir: Path, benzene_run: Path) -> Path:
    target = testdata_dir / "benzene_no_convergence"
    return duplicate_with_missing(benzene_run, target, [Path("static/convergence")])


@pytest.fixture
def methane_missing_scf_iter(testdata_dir: Path, methane_run: Path) -> Path:
    target = testdata_dir / "methane_missing_scf_iter"
    return duplicate_with_missing(methane_run, target, [Path("output_iter/scf.0004")])


@pytest.fixture
def methane_missing_td_iter(testdata_dir: Path, methane_run: Path) -> Path:
    target = testdata_dir / "methane_missing_td_iter"
    return duplicate_with_missing(methane_run, target, [Path("output_iter/td.0000003")])


@pytest.fixture
def methane_missing_td_extensions(testdata_dir: Path, methane_run: Path) -> Path:
    target = testdata_dir / "methane_missing_td_extensions"
    # Only leave ncdf files for iterations 1, 5, 7, 12 for testing.
    missing_td_exts = [
        Path(f"output_iter/td.00000{i}/density.{ext}")
        for i, ext in product(("01", "05", "07", "12"), ("xsf", "vtk", "z=0"))
    ]
    return duplicate_with_missing(methane_run, target, missing_td_exts)


@pytest.fixture
def methane_missing_vector_dimensions(testdata_dir: Path, methane_run: Path) -> Path:
    target = testdata_dir / "methane_missing_vector_dimensions"
    return duplicate_with_missing(
        methane_run,
        target,
        [
            Path("output_iter/td.0000000/current-z.z=0"),
            Path("output_iter/td.0000000/current-z.ncdf"),
            Path("output_iter/td.0000000/current-z.xsf"),
            Path("output_iter/td.0000000/current.vtk"),
        ],
    )
