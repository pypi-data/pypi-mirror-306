from pathlib import Path

import numpy as np
import numpy.testing as npt
import pytest

from postopus.files.pandas_text import PandasTextFile


def test_dataframe_dimensionality(methane_run: Path):
    ptf_forces = PandasTextFile(methane_run / "static" / "forces")
    assert ptf_forces.values.shape == (5, 31)

    ptf_convergence = PandasTextFile(methane_run / "static" / "convergence")
    assert ptf_convergence.values.shape == (19, 6)


def test_dataframe_values(methane_run: Path):
    forces_headers = [
        "species",
        "total_x",
        "total_y",
        "total_z",
        "ion-ion_x",
        "ion-ion_y",
        "ion-ion_z",
        "vdw_x",
        "vdw_y",
        "vdw_z",
        "local_x",
        "local_y",
        "local_z",
        "nl_x",
        "nl_y",
        "nl_z",
        "fields_x",
        "fields_y",
        "fields_z",
        "hubbard_x",
        "hubbard_y",
        "hubbard_z",
        "scf_x",
        "scf_y",
        "scf_z",
        "nlcc_x",
        "nlcc_y",
        "nlcc_z",
        "phot_x",
        "phot_y",
        "phot_z",
    ]

    convergence_headers = [
        "energy",
        "energy_diff",
        "abs_dens",
        "rel_dens",
        "abs_ev",
        "rel_ev",
    ]

    ptf_forces = PandasTextFile(methane_run / "static" / "forces")
    assert ptf_forces.values.columns.values.tolist() == forces_headers
    assert ptf_forces.values["species"].values.tolist() == ["C", "H", "H", "H", "H"]
    assert ptf_forces.values["local_x"][4] == pytest.approx(-0.6, rel=0.5)
    assert ptf_forces.values["scf_y"][2] == pytest.approx(-2e-09, rel=0.5)
    assert ptf_forces.values["scf_z"][2] == pytest.approx(-2e-09, rel=0.5)

    ptf_convergence = PandasTextFile(methane_run / "static" / "convergence")
    assert ptf_convergence.values.columns.values.tolist() == convergence_headers
    assert ptf_convergence.values["rel_dens"][15] == pytest.approx(6e-06, rel=0.5)
    assert ptf_convergence.values["energy"][5] == pytest.approx(-8, rel=0.5)
    assert ptf_convergence.values["rel_ev"][15] == pytest.approx(2e-05, rel=0.5)


def test_read_other_data(tmp_path: Path):
    test_file = tmp_path / "pandas_readable_other_file.txt"

    testdata = "title1 title2 title3" "# 10 11 12\n" "1 2 3\n" "4 5 6\n" "7 8 9"

    test_file.write_text(testdata)

    pdf = PandasTextFile(test_file)
    npt.assert_array_equal(
        pdf.values.values, np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    )
    assert all(pdf.values.columns.values == ["title1", "title2", "title3"])


def test_read_other_data_unreadable(tmp_path: Path):
    test_file = tmp_path / "pandas_readable_other_file.txt"

    testdata = (
        "this is a\n"
        "// file containing some random words\n"
        "hoping\n"
        "pandas is unable to read it or make any sense out of it\n"
        "so we can have an error\n"
    )

    test_file.write_text(testdata)

    pdf = PandasTextFile(test_file)
    with pytest.warns(UserWarning):
        pdf.values
    # split("\n")[:-1] because list comprehension generates one newline extra at the end
    assert pdf.values == [s + "\n" for s in testdata.split("\n")[:-1]]


def test_attrs_attribute(methane_run: Path):
    ptf = PandasTextFile(methane_run / "td.general" / "laser")
    assert ptf.attrs is not None
