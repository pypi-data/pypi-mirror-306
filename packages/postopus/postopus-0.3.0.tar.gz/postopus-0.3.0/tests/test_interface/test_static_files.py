"""Collection of tests to test access on files in the `static` folder."""

from pathlib import Path

import pandas as pd

from postopus import Run


def test_info_file(methane_run: Path):
    run = Run(methane_run)
    data = run.default.scf.info()

    assert isinstance(data, list)
    assert all(isinstance(item, str) for item in data)


def test_convergence_file(methane_run: Path):
    run = Run(methane_run)
    convergence = run.default.scf.convergence
    data = convergence()

    assert isinstance(data, pd.DataFrame)
    assert data.shape == (19, 6)


def test_forces_file(methane_run: Path):
    run = Run(methane_run)
    forces = run.default.scf.forces
    data = forces()

    assert isinstance(data, pd.DataFrame)
    assert data.shape == (5, 31)


def test_bandstructure_data_reading(bn_monolayer_run: Path):
    exp_attrs_dict = {
        "units": {
            "coord.": "Coord",
            "kx": "(red.coord.)",
            "ky": "(red.coord.)",
            "kz": "(red.coord.)",
            "band_1": "[eV]",
            "band_2": "[eV]",
            "band_3": "[eV]",
            "band_4": "[eV]",
            "band_5": "[eV]",
            "band_6": "[eV]",
            "band_7": "[eV]",
            "band_8": "[eV]",
            "band_9": "[eV]",
            "band_10": "[eV]",
            "band_11": "[eV]",
            "band_12": "[eV]",
        },
        "metadata": {"filename": "bandstructure"},
    }

    run = Run(bn_monolayer_run)
    bandstructure = run.default.scf.bandstructure()
    assert bandstructure.shape == (32, 15)
    assert bandstructure.attrs == exp_attrs_dict


def test_eigenvalues_reading(bn_monolayer_run: Path, harmonic_oscillator_run: Path):
    info_dict = [
        "All states converged.",
        "Criterion =      0.100000E-06",
        "Eigenvalues [eV]",
    ]
    k_dict = {
        1: (0.0, 0.0, 0.0),
        2: (0.027778, 0.027778, 0.0),
        3: (0.055556, 0.055556, 0.0),
        4: (0.083333, 0.083333, 0.0),
        5: (0.111111, 0.111111, 0.0),
        6: (0.138889, 0.138889, 0.0),
        7: (0.166667, 0.166667, 0.0),
        8: (0.194444, 0.194444, 0.0),
        9: (0.222222, 0.222222, 0.0),
        10: (0.25, 0.25, 0.0),
        11: (0.277778, 0.277778, 0.0),
        12: (0.305556, 0.305556, 0.0),
        13: (0.333333, 0.333333, 0.0),
        14: (0.357143, 0.285714, 0.0),
        15: (0.380952, 0.238095, 0.0),
        16: (0.404762, 0.190476, 0.0),
        17: (0.428571, 0.142857, 0.0),
        18: (0.452381, 0.095238, 0.0),
        19: (0.47619, 0.047619, 0.0),
        20: (0.5, -0.0, 0.0),
        21: (0.458333, 0.0, 0.0),
        22: (0.416667, 0.0, 0.0),
        23: (0.375, -0.0, 0.0),
        24: (0.333333, -0.0, 0.0),
        25: (0.291667, 0.0, 0.0),
        26: (0.25, -0.0, 0.0),
        27: (0.208333, 0.0, 0.0),
        28: (0.166667, 0.0, 0.0),
        29: (0.125, -0.0, 0.0),
        30: (0.083333, -0.0, 0.0),
        31: (0.041667, -0.0, 0.0),
        32: (0.0, 0.0, 0.0),
    }

    monolayer_run = Run(bn_monolayer_run)
    eigenvalues = monolayer_run.default.scf.eigenvalues()

    assert eigenvalues.shape == (384, 4)
    assert eigenvalues.attrs["metadata"]["info"] == info_dict
    assert eigenvalues.attrs["metadata"]["k"] == k_dict

    oscillator_run = Run(harmonic_oscillator_run)
    eigenvalues = oscillator_run.default.scf.eigenvalues()
    assert eigenvalues.shape == (11, 4)
    assert (
        eigenvalues.attrs["metadata"]["k"] == {}
    )  # There are no k points for the harmonic oscillator
