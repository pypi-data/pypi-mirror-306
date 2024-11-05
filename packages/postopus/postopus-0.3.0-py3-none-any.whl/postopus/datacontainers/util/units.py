from __future__ import annotations

import typing

import xarray

if typing.TYPE_CHECKING:
    import postopus.files.file

unit_map = {
    "au": {
        "x": "Bohr",
        "y": "Bohr",
        "z": "Bohr",
        "t": "au",
    },
    "eV_Ångstrom": {
        "x": "Ångstrom",
        "y": "Ångstrom",
        "z": "Ångstrom",
        "t": "h_bar/eV",
    },
}


def update_units(
    xarr: xarray.DataArray | xarray.Dataset, file: postopus.files.file.File
):
    """Set the `units` attrs for the given xarray data array."""
    # No/unknown units? Nothing to do
    if file.units not in unit_map:
        return

    xarr.attrs["units"] = file.units
    for dim in xarr.dims:
        if (unit := unit_map[file.units].get(dim)) is not None:
            xarr[dim].attrs["units"] = unit

    if isinstance(xarr, xarray.Dataset):
        for component in xarr.data_vars:
            xarr[component].attrs["units"] = file.units
