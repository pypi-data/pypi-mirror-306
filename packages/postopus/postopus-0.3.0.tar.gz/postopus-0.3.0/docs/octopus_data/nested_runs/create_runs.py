#!/usr/bin/env python
import os
import subprocess
from string import Template

import matplotlib.pyplot as plt
import pandas as pd

import postopus


def mkdir_p(path):
    os.makedirs(path, exist_ok=True)


def outer_product_from_dict(d):
    """Generate list of dictionaries as outer product from d"""
    result = [[]]
    for key in d:
        result = [x + [y] for x in result for y in d[key]]
    return [{key: value for key, value in zip(d.keys(), r)} for r in result]


def get_template(filename="inp", path="."):
    with open(os.path.join(path, filename)) as f_in:
        input_template = Template(f_in.read())
    return input_template


def get_path_from_combination(combination):
    return "-".join([k + "_" + str(v) for k, v in combination.items()])


def prepare_simulation_folder(combination, template):
    path = get_path_from_combination(combination)
    mkdir_p(path)
    with open(os.path.join(path, "inp"), "w") as inputfile:
        inputfile.write(template.substitute(**combination))


def create_simulation_folders(combinations):
    template = get_template()
    for combination in combinations:
        prepare_simulation_folder(combination, template)


def run_simulation(combination, executable="octopus"):
    path = get_path_from_combination(combination)
    with open(os.path.join(path, "log"), "w") as logfile:
        subprocess.run(executable, cwd=path, stdout=logfile, stderr=subprocess.STDOUT)


def run_simulations(combinations, executable="octopus"):
    for combination in combinations:
        run_simulation(combination, executable)


def create_folders_and_run_simulations(parameters):
    combinations = outer_product_from_dict(parameters)
    create_simulation_folders(combinations)
    run_simulations(combinations)


def get_parameter_from_path(path):
    # this is a hack to get the spacing from the path
    return float(path[-3:])


def get_converged_data(convergence):
    # get only the information from the last iteration for each run
    converged = convergence.groupby(level=0).tail(1).droplevel(1)
    i = converged.index
    combined = converged.set_index(i.map(get_parameter_from_path)).sort_index()
    return combined


def plot_convergence_results():
    n = postopus.nestedRuns()
    convergence = pd.concat(n.apply(lambda run: run.default.scf.convergence()))
    converged = get_converged_data(convergence)

    width = 5
    f, ax = plt.subplots(1, 1, figsize=(width, width * 0.6), sharex=True)
    ax.plot(converged.index, converged.energy)
    ax.set_ylabel("Total energy [eV]")
    ax.set_xlabel(r"Spacing [$\AA$]")
    f.tight_layout()
    f.savefig("convergence.png")

    f, ax = plt.subplots(1, 1, figsize=(width, width * 0.6), sharex=True)
    for k, group in convergence.groupby(level=0):
        ax.semilogy(
            group.loc[k].index,
            group.rel_dens,
            label=rf"Spacing {get_parameter_from_path(k)} $\AA$",
        )
    ax.legend()
    ax.set_ylabel("Relative density change")
    ax.set_xlabel(r"Iteration number")
    f.tight_layout()
    f.savefig("convergence_density.png")


if __name__ == "__main__":
    parameters = {"deltax": sorted([0.6, 0.5, 0.4])}
    create_folders_and_run_simulations(parameters)
    plot_convergence_results()
