from __future__ import annotations

import typing

import pytest

if typing.TYPE_CHECKING:
    from pathlib import Path

    from tests.utils.octopus_runner import OctopusRunner


@pytest.fixture(scope="session")
def nested_runs(testdata_dir: Path, octopus_runner: OctopusRunner) -> Path:
    basepath = testdata_dir / "nested_runs"
    run_path = basepath / "run"
    inp = basepath / "inp_gs"
    run_path.mkdir(exist_ok=True)
    for delta in [0.4, 0.5, 0.6]:
        path = run_path / f"deltax_{delta}"
        params = {"deltax": delta}
        octopus_runner.run(
            inputfiles=inp,
            run_path=path,
            parameters=params,
        )
    return run_path
