"""Collection of common octopus runs, e.g. the methane molecule.

These runs are used across multiple tests (explicit by requesting those as a fixture
or implicit by requesting a fixture which is based on a common run, e.g. from
duplicate_with_missing).
Changing the parameters of the runs will affect these tests!
"""

from __future__ import annotations

import typing

import pytest

if typing.TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

    from .octopus_runner import OctopusRunner


def make_common_run(
    name: str,
    path: str,
    input_files: list[str],
    additional_files: list[str] | None = None,
) -> Callable[[Path, OctopusRunner], Path]:
    """Create a fixture for a common run.

    Parameters
    ----------
    name
        Name of the fixture.
    path
        Path to the input files in the test data directory (tests/data/<path>).
    input_files
        List of the input files, e.g. `["inp_gs", "inp_td"].
    additional_files
        Additional files which should be provided in the octopus run directory,
        e.g. `["benzene.xyz"]`.
    """

    @pytest.fixture(name=name, scope="session")
    def run(testdata_dir: Path, octopus_runner: OctopusRunner) -> Path:
        basepath = testdata_dir / path
        return octopus_runner.run_simple(
            basepath, input_files=input_files, additional_files=additional_files
        )

    return run


methane_run = make_common_run(
    "methane_run",
    "methane",
    ["inp_gs", "inp_td"],
)
benzene_run = make_common_run("benzene_run", "benzene", "inp_gs", "benzene.xyz")
celestial_bodies_run = make_common_run(
    "celestial_bodies_run", "celestial_bodies", "inp_td"
)
kpoints_run = make_common_run("kpoints_run", "kpoints", ["inp_gs", "inp_td"])
bn_monolayer_run = make_common_run(
    "bn_monolayer_run", "2-h-BN_monolayer", ["inp_gs", "inp_unocc"]
)
harmonic_oscillator_run = make_common_run(
    "harmonic_oscillator_run", "1d-harmonic-oscillator", ["inp_gs", "inp_unocc"]
)
bulk_si_run = make_common_run("bulk_si_run", "3-bulk_Si", ["inp_gs", "inp_td"])


@pytest.fixture
def interference_run(testdata_dir: Path, octopus_runner: OctopusRunner) -> Path:
    basepath = testdata_dir / "interference"
    # Beginning with Octopus 14, the input option MaxwellIncidentWaves requires an
    # additional parameter.
    if octopus_runner.octopus_version[0] <= 13:
        inp = "inp_td_13.0"
    else:
        inp = "inp_td"

    return octopus_runner.run_simple(basepath, input_files=[inp])
