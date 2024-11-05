from pathlib import Path

import numpy as np
import pytest

from postopus import Run


def test_read_scalarfield(methane_run: Path):
    run = Run(methane_run)
    assert run.default.system_data.keys() == {"scf", "td"}


def test_basic_access(methane_run: Path):
    """Test the access to data of a scalar field.
    As postopus delegates most work to xarray some basic tests
    should be sufficient.
    """
    run = Run(methane_run)
    density_gs = run.default.scf.density(source="ncdf")

    assert density_gs.dims == ("step", "x", "y", "z")

    assert density_gs.sel(step=2).values.shape == (27, 27, 27)
    assert density_gs.values.shape == (19, 27, 27, 27)

    density_td = run.default.td.density(source="ncdf")
    assert density_td.dims == ("t", "x", "y", "z")
    # Work with .values.shape instead of .shape to trigger the lazy data access.
    assert density_td.sel(t=2, method="nearest").values.shape == (27, 27, 27)
    assert density_td.values.shape == (31, 27, 27, 27)

    # td fields can only be sliced by time by default, but step slicing can be enabled.
    density_td = density_td.set_xindex("step")
    assert density_td.sel(step=10).values.shape == (27, 27, 27)


def test_missing_static(methane_min_no_static: Path):
    run = Run(methane_min_no_static)
    density = run.default.scf.density(".ncdf")
    assert density.values.shape == (18, 27, 27, 27)


def test_missing_convergence_file(benzene_no_convergence: Path):
    run = Run(benzene_no_convergence)
    with pytest.warns(
        UserWarning,
        match="It was not possible to determine at which step the simulation has stopped.",
    ):
        density = run.default.scf.density(".z=0")

    # Convergence as at step 16 but as the convercence file is missing
    # postopus should assume step 20 here.
    assert (density.step == [5, 10, 15, 20]).all()


def test_wave_function_slicing(methane_run: Path):
    """Test if the selection of the wave function state is working.
    In this output the files wf-st0001, wf-st0002, ..., wf-st<n> are
    combined into a single DataArray providing the additional dimension "st".
    """
    run = Run(methane_run)
    wf = run.default.scf.wf("xsf")
    xarr = wf.isel(step=-1)
    xarr.sel(st=1).values.shape == (27, 27, 27)
    xarr.sel(st=2).values.shape == (27, 27, 27)
    assert (xarr.sel(st=1) != xarr.sel(st=2)).any()


def test_get_wave_function_with_kpoint(kpoints_run: Path):
    run = Run(kpoints_run)
    wf = run.default.td.wf("ncdf")
    xarr = wf.isel(t=-1)
    xarr.sel(st=1, k=2).values.shape == (27, 27, 27)


@pytest.mark.skip(
    reason="""Loading complex numbers is barely supported in Postopus
            as all file formats have own specialties,
            see https://gitlab.com/octopus-code/postopus/-/issues/162.
            """
)
def test_get_complex(methane_run: Path):
    run = Run(methane_run)
    wf = run.default.td.wf("xsf")
    xarr = wf.isel(t=-1)
    xarr.sel(st=1).values
    xarr.sel(st=2).values


def test_get_bad_params(
    tmp_path: Path,
    mock_inp_and_parser_log_and_output: None,
    methane_run: Path,
    methane_min_no_static: Path,
):
    # Found extension and no parser
    mock_run = Run(tmp_path)
    with pytest.raises(
        NotImplementedError, match=r"Existing file '[^']+' found, but no parser"
    ):
        mock_run.default.scf.mock_scalarfield("sdfjk")

    run = Run(methane_run)
    # Not found extension and existing parser
    with pytest.raises(ValueError, match=r"We did not find any '\*\.y=0' files"):
        run.default.scf.density("y=0")

    # Not found extension and no parser
    with pytest.raises(ValueError, match=r"We did not find any '\*\.bla' files"):
        run.default.scf.density("bla")

    # Not specifying the source, although there is more than one
    with pytest.raises(ValueError, match=r"There is more than one source available."):
        run.default.scf.density()


def test_iteration_num_for_static_methane(methane_run: Path):
    run = Run(methane_run)
    # methane has 18 iterations for 'scf' in output_iter, but we add one more for static
    assert (run.default.scf.density("z=0").step == np.array(range(1, 20))).all()


def test_warning_on_missing_iteration_scf(methane_missing_scf_iter: Path):
    run = Run(methane_missing_scf_iter)
    with pytest.warns(UserWarning):
        assert (run.default.scf.density(".z=0").step[0:6] == [1, 2, 3, 5, 6, 7]).all()


def test_warning_on_missing_iteration_td(methane_missing_td_iter: Path):
    run = Run(methane_missing_td_iter)
    with pytest.warns(UserWarning):
        assert (run.default.td.density(".vtk").step[0:6] == [0, 1, 2, 4, 5, 6]).all()
