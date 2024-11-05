from pathlib import Path

from postopus import Run

"""
This script is for testing. It provides a collection of calls
endusers would do.
"""

if __name__ == "__main__":
    # This works
    repodir = Path(__file__).parents[3]
    exampleinp = repodir / "tests" / "data" / "methane"
    run = Run(exampleinp)
    exampleinp2 = repodir / "tests" / "data" / "methane_wo_vtk"
    run2 = Run(exampleinp2)
    print("Data Container: ", end="")
    print(run)
    print("Fields Container: ", end="")
    print(run.default.scf)
    print("Density Field: ", end="")
    print(run.default.scf.density)
    print("Number of iterations for 'density' field: ", end="")
    print(run.default.scf.density.n_iterations)
    print("IDs for iterations: ", end="")
    print(run.default.scf.density.iteration_ids)
    print("Data from single iteration: ", end="")
    print(run.default.td.current.get_all("vtk"))

    # For reference, data still can be accessed with the usual dict syntax:
    # run.default.scf.density.iteration(5, outputformat="netcdf") replaces
    # run.systems["default"].modes["scf"].fields["density"]
    # .iteration(5, outputformat="netcdf")

    data = run.default.scf.density.get(1, source="ncdf")
