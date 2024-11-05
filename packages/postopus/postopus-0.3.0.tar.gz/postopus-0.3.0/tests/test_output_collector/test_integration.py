from pathlib import Path

from postopus.output_collector import (
    OutputCollector,
    VectorDimension,
)


def test_fields_single_system(interference_run: Path):
    check_fields_maxwell = {
        "td": {
            "maxwell_energy",
            "total_b_field",
            "total_e_field",
            "b_field",
            "e_field",
            "e_field_trans",
            "maxwell_energy_density",
        }
    }
    check_avail_systems = {"Maxwell", "default"}

    oc = OutputCollector(interference_run)
    output = oc.output

    # Check available systems
    assert output.keys() == check_avail_systems

    # Check available fields of the maxwell system
    maxwell_system = output["Maxwell"]
    assert maxwell_system.keys() == check_fields_maxwell.keys()
    assert maxwell_system["td"].keys() == check_fields_maxwell["td"]

    # Assert that the default system is empty
    default_system = output["default"]
    assert len(default_system) == 0


def test_fields_default_system(methane_run: Path):
    # Data for checking correctness
    check_fields_default = {
        # fields from static/ and output_iter/scf.*
        "scf": {
            "convergence",
            "density",
            "forces",
            "info",
            "wf",
        },
        # fields from td_generel/ and output_iter/td.*
        "td": {
            "energy",
            "laser",
            "multipoles",
            "current",
            "density",
            "wf",
        },
    }
    check_avail_systems = {"default"}

    oc = OutputCollector(methane_run)
    output = oc.output

    # Check available systems
    assert output.keys() == check_avail_systems

    # Check available fields in the default system
    default_system = output["default"]
    assert default_system.keys() == check_fields_default.keys()
    assert default_system["td"].keys() == check_fields_default["td"]
    assert default_system["scf"].keys() == check_fields_default["scf"]


def test_extensions(methane_run):
    collector = OutputCollector(methane_run)
    output = collector.output
    wf = output["default"]["td"]["wf"]
    files = wf.iterations.get_any().other_index.get_any().files
    expected = {
        ".ncdf",
        ".real.xsf",
        ".imag.xsf",
        ".vtk",
        ".z=0",
    }
    assert files.extensions == expected


def test_is_vector(methane_run):
    collector = OutputCollector(methane_run)
    output = collector.output
    current = output["default"]["td"]["current"]
    assert current.is_vector()

    density = output["default"]["td"]["density"]
    assert not density.is_vector()


def test_is_static(benzene_run):
    collector = OutputCollector(benzene_run)
    output = collector.output

    field = output["default"]["scf"]["info"]
    assert field.is_static()

    field = output["default"]["scf"]["convergence"]
    assert field.is_static()

    field = output["default"]["scf"]["density"]
    assert not field.is_static()


def test_is_valid(methane_run):
    collector = OutputCollector(methane_run)
    output = collector.output

    field = output["default"]["scf"]["density"]
    assert field.is_valid()

    field = output["default"]["td"]["current"]
    assert field.is_valid()


def test_vector_access(methane_run):
    collector = OutputCollector(methane_run)
    output = collector.output
    current = output["default"]["td"]["current"]
    assert current.is_vector()

    assert current.has_iterations()
    any_iteration = current.iterations.get_any()

    assert any_iteration.has_other_index()

    for dim in "xyz":
        index = VectorDimension(dim)
        assert index in any_iteration.other_index
        assert any_iteration.other_index[index].is_static()
