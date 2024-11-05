from pathlib import Path

import pytest

from postopus.octopus_run import Run


def test_au_units(methane_run: Path):
    run_au = Run(methane_run)
    xarrays_scf = [
        run_au.default.scf.density("xsf").isel(step=-1),
        run_au.default.scf.density("vtk").sel(step=[1, 2]),
        run_au.default.scf.density("ncdf").isel(step=-1),
    ]
    xarrays_td = [
        run_au.default.td.density("ncdf"),
        run_au.default.td.current("ncdf").isel(t=1),
        run_au.default.td.current("ncdf").vx.isel(t=-1),
        run_au.default.td.current("ncdf").vy.isel(t=-1),
        run_au.default.td.current("ncdf"),
    ]
    xarrays = xarrays_scf + xarrays_td

    # units of whole xarray == au
    assert all(xarr.units == "au" for xarr in xarrays)

    # coord units
    for dim in "xyz":
        assert all(xarr[dim].units == "Bohr" for xarr in xarrays)

    assert all(xarr.t.units == "au" for xarr in xarrays_td)

    with pytest.raises(
        AttributeError, match=r"'DataArray' object has no attribute 'units'"
    ):
        xarrays_scf[0].step.units  # step doesn't have a physical unit


def test_ev_angstrom_units(benzene_run: Path):
    run_ev_angstrom = Run(benzene_run)
    # TODO: This is incomplete: test data is missing, e.g no td eV_Angstrom data
    xarr1 = run_ev_angstrom.default.scf.density("xsf").isel(step=-1)
    xarr2 = run_ev_angstrom.default.scf.density("cube").isel(step=-1)
    xarr3 = run_ev_angstrom.default.scf.density("vtk").isel(step=-1)
    xarr4 = run_ev_angstrom.default.scf.density("z=0").isel(step=-1)
    xarr5 = run_ev_angstrom.default.scf.density("y=0,z=0").isel(step=-1)

    # units of whole xarray == au
    assert xarr1.units == xarr3.units == xarr4.units == xarr5.units == "eV_Ångstrom"

    # units of cube always au, independent of UnitsOutput in parser.log
    xarr2.units == "au"

    # coord units
    for dim in "xyz":
        assert xarr1[dim].units == xarr3[dim].units == "Ångstrom"
        assert xarr2[dim].units == "Bohr"
        if dim in "xy":  # z=0
            assert xarr4[dim].units == "Ångstrom"
        if dim == "x":  # y=0, z=0
            assert xarr5[dim].units == "Ångstrom"

    with pytest.raises(
        AttributeError, match=r"'DataArray' object has no attribute 'units'"
    ):
        xarr1.step.units  # step doesn't have a physical unit
