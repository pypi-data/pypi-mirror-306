from __future__ import annotations

import warnings
from typing import TYPE_CHECKING

from postopus.utils import parser_log_retrieve_value

if TYPE_CHECKING:
    from pathlib import Path


def get_units(filepath: Path) -> str | None:
    """
    Get units corresponding to the file data.

    Check if UnitsOutput is set to "eV_Angstrom" or "atomic".

    Returns
    -------
    units string

    """

    units_output = parser_log_retrieve_value(
        find_run_root(filepath) / "exec" / "parser.log",
        "UnitsOutput",
        conversion=int,
    )
    if units_output == 0:
        return "au"

    elif units_output == 1:
        return "eV_Ångstrom"
    else:
        warnings.warn(
            f"We don't know UnitsOutput == {units_output}"
            f" (s. parser.log). \n"
            f"Neither it is au, nor"
            f"eV_Angstrom. The data will be displayed without units"
        )
        return None


def find_run_root(startpath: Path) -> Path:
    """
    Finds the root directory of this octopus run. Root directory contains inp file

    Parameters
    ----------
    startpath : Path
        path to start searching from

    Returns
    -------
    Path
        path to Octopus' output root directory
    """
    # find inp file
    inp_file = startpath.joinpath("inp")
    if inp_file.exists():
        return startpath
    else:
        # if no inp file is found, we need to go up one level
        return find_run_root(startpath.parent)
