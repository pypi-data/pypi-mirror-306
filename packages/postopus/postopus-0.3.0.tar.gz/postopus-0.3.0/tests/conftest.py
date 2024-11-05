"""
    Dummy conftest.py for postopus.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html
"""

from pathlib import Path

import pytest

# Provide global fixtures
pytest_plugins = [
    "tests.utils.common_runs",
    "tests.utils.nested_runs",
    "tests.utils.octopus_runner",
    "tests.utils.duplicate_with_missing",
]


@pytest.fixture(scope="session")
def testdata_dir() -> Path:
    """Path to the testdata dir (`<repo_dir>/tests/data/`)"""
    return Path(__file__).parent / "data"


@pytest.fixture
def mock_inp_and_parser_log_and_output(tmp_path):
    # mock inp file & parser.log
    tmpinpfile = tmp_path / "inp"
    tmpinpfile.write_text("Mock inp file")
    tmpexec = tmp_path / "exec"
    tmpexec.mkdir()
    tmpparser = tmpexec / "parser.log"
    tmpparser.write_text("UnitsOutput = 1")

    # output_iter
    tmpoutput = tmp_path / "output_iter"
    tmpoutput.mkdir()

    not_known_ext = "sdfjk"
    mock_content = "Mock"
    # scf
    tmpscf = tmpoutput / "scf.0001"
    tmpscf.mkdir()

    scf_mock_files = []
    for dim in ["x", "y", "z"]:
        scf_mock_files.append(tmpscf / f"mock_vectorfield-{dim}.{not_known_ext}")
    scf_mock_files.append(tmpscf / f"mock_scalarfield.{not_known_ext}")
    scf_mock_files.append(tmpscf / "test_structures.xyz")
    for mock_file in scf_mock_files:
        mock_file.write_text(mock_content)

    # td
    tmptd = tmpoutput / "td.0001"
    tmptd.mkdir()

    td_mock_files = scf_mock_files[:-1]
    for mock_file in td_mock_files:
        mock_file.write_text(mock_content)
