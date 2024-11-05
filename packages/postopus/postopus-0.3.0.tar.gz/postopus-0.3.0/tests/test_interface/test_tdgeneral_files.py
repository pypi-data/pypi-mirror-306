"""Collection of tests to test access on files in the `td.general` folder."""

import re
from pathlib import Path

import pandas as pd
from tests.utils.octopus_runner import OctopusRunner

from postopus import Run


def test_read_tdgeneralvectorfield(interference_run: Path):
    """Test reading vector fields occuring in td.general/.
    Similar to vector fields in output_iter the output consists
    of three files with a `_x`/`_y`/`_z` suffix (as in `total_e_field_y`).
    The files are structured the same as any other files in
    static/ and td.general/ and thus returned as a dataframe.
    """
    run = Run(interference_run)

    total_e_field = run.Maxwell.td.total_e_field()
    assert total_e_field.z.shape == (167, 2)
    assert isinstance(total_e_field.z, pd.DataFrame)
    assert total_e_field.z.attrs.keys() == {"units", "metadata"}
    assert total_e_field.z.attrs["units"] == {
        "Iter": "[Iter n.]",
        "t": "[hbar/H]",
        "E(1)": "[H/b]",
    }

    # Extract `0.210656423428E-02 [hbar/H]` from the line `# dt =   0.210656423428E-02 [hbar/H]`
    # which should occure in the metadata as via the key "dt".
    with open(interference_run / "Maxwell" / "td.general" / "total_e_field_z") as f:
        content = f.read()
        m = re.findall(r"# dt =\s+(\d+.\d+E[+0-]\d+\s+\[hbar/H\])", content)
        assert len(m) == 1
        dt = m[0]

    assert total_e_field.z.attrs["metadata"] == {
        "filename": "total_e_field_z",
        "dt": [dt],
    }


def test_loading_static_data(methane_run: Path):
    run = Run(methane_run)
    assert isinstance(run.default.td.energy(), pd.DataFrame)
    assert isinstance(run.default.td.laser(), pd.DataFrame)
    assert isinstance(run.default.td.multipoles(), pd.DataFrame)
    assert isinstance(run.default.td.multipoles().attrs, dict)


def test_coordinates_attrs_reading(
    octopus_runner: OctopusRunner, celestial_bodies_run: Path
):
    run = Run(celestial_bodies_run)
    if octopus_runner.octopus_version[0] <= 14:
        exp_unit_dict = {
            "Iter": "[Iter n.]",
            "t": "[hbar/H]",
            "x(  1)": "[b]",
            "x(  2)": "[b]",
            "x(  3)": "[b]",
            "v(  1)": "[bH(2pi/h)]",
            "v(  2)": "[bH(2pi/h)]",
            "v(  3)": "[bH(2pi/h)]",
            "f(  1)": "[H/b]",
            "f(  2)": "[H/b]",
            "f(  3)": "[H/b]",
        }
    else:
        exp_unit_dict = {
            "Iter": "[Iter n.]",
            "t": "[hbar/H]",
            "x(  1,  1)": "[b]",
            "x(  1,  2)": "[b]",
            "x(  1,  3)": "[b]",
            "v(  1,  1)": "[bH(2pi/h)]",
            "v(  1,  2)": "[bH(2pi/h)]",
            "v(  1,  3)": "[bH(2pi/h)]",
            "f(  1,  1)": "[H/b]",
            "f(  1,  2)": "[H/b]",
            "f(  1,  3)": "[H/b]",
        }
    act_unit_dict = run.SolarSystem.Sun.td.coordinates().attrs["units"]

    assert exp_unit_dict == act_unit_dict


def test_standard_attrs_reading(methane_run: Path):
    """
    Test expected standard reading routine for attrs in tdgeneral files

    """
    run = Run(methane_run)
    exp_unit_dict = {
        "Iter": "[Iter n.]",
        "t": "[hbar/H]",
        "E(1)": "[H/b]",
        "E(2)": "[H/b]",
        "E(3)": "[H/b]",
    }
    exp_metadata_dict = {"dt": ["0.500000000000E-01 [hbar/H]"], "filename": "laser"}

    act_unit_dict = run.default.td.laser().attrs["units"]
    act_metadata_dict = run.default.td.laser().attrs["metadata"]

    assert exp_unit_dict == act_unit_dict
    assert exp_metadata_dict == act_metadata_dict


def test_total_curr_attrs_reading(bulk_si_run: Path):
    run = Run(bulk_si_run)
    assert run.default.td.total_current().attrs["units"]["t"] == "Units not specified"


def test_multisystems_reading(celestial_bodies_run: Path):
    run = Run(celestial_bodies_run)
    assert run.SolarSystem.Earth.td.coordinates().shape == (73, 10)
    assert run.SolarSystem.Sun.td.coordinates().shape == (73, 10)
    assert run.SolarSystem.Moon.td.coordinates().shape == (73, 10)
