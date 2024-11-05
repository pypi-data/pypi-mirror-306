from pathlib import Path

import pandas as pd
import pytest
import xarray as xr

from postopus import nestedRuns


def test_nested_runs(nested_runs: Path):
    n = nestedRuns(nested_runs)
    nruns = n.get_path(nested_runs)

    # convergence
    convergence = pd.concat(nruns.apply(lambda run: run.default.scf.convergence()))
    level_values = convergence.index.get_level_values(None)  # get values of deltas
    expected_deltas = ["deltax_0.6", "deltax_0.5", "deltax_0.4"]
    assert all(element in level_values for element in expected_deltas) is True
    assert len(convergence) == 48
    assert pytest.approx(-133.932888, rel=1e-5) in list(convergence["energy"].values)
    assert pytest.approx(-120.397692, rel=1e-3) in list(convergence["energy"].values)
    assert pytest.approx(-136.33116, rel=1e-5) in list(convergence["energy"].values)

    # density fields
    fields = nruns.apply(lambda run: run.default.scf.density())
    assert isinstance(fields["deltax_0.6"], xr.DataArray)
    assert fields["deltax_0.6"].max() == pytest.approx(2.4, rel=0.5)
