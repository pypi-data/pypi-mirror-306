from pathlib import Path

import xarray

import postopus.files.file


def to_xarray(file_obj: postopus.files.file.File) -> xarray.DataArray:
    """
    Take a file object and return its correspondent xarray.

    Set the name corresponding to the filepath.

    Set the corresponding units.

    Parameters
    ----------
    file_obj : postopus.files.file.File
        File object that to build xarray.DataArray from

    Returns
    -------
    xarray.DataArray
        xarray.DataArray with information from the File

    """
    xarr = xarray.DataArray(file_obj.values, dims=file_obj.dims, coords=file_obj.coords)
    xarr.name = Path(file_obj.filepath).stem
    if file_obj.units == "au":
        xarr.attrs["units"] = "au"
        for dim in xarr.dims:
            if dim in "xyz":
                xarr[dim].attrs["units"] = "Bohr"
            elif dim == "t":
                xarr[dim].attrs["units"] = "au"
            else:
                continue

    elif file_obj.units == "eV_Ångstrom":
        xarr.attrs["units"] = "eV_Ångstrom"
        for dim in xarr.dims:
            if dim in "xyz":
                xarr[dim].attrs["units"] = "Ångstrom"
            elif dim == "t":
                xarr[dim].attrs["units"] = "h_bar/eV"
            else:
                continue
    else:
        # fileobj.units = None, neither ev_Angstrom, nor au
        pass

    return xarr
