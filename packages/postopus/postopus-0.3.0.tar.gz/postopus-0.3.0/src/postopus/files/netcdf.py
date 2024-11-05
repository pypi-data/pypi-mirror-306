from __future__ import annotations

from typing import TYPE_CHECKING

import netCDF4
import numpy as np

from postopus.files.file import File
from postopus.files.utils.units import get_units

if TYPE_CHECKING:
    from pathlib import Path


class NetCDFFile(File):
    EXTENSIONS = [".ncdf", ".nc"]

    def __init__(self, filepath: Path) -> None:
        """
        Enable Postopus to read NetCDF 4 data, as written by Octopus.
        https://www.unidata.ucar.edu/software/netcdf/
        To write NetCDF 4 output, 'inp' files must set 'OutputFormat' to 'netcdf'.
        Additionally, Octopus has to be compiled with NetCDF support (not default).

        Parameters
        ----------
        filepath: Path
            path to the file in NetCDF format
        """
        self.filepath = filepath

    def _readfile(self) -> None:
        """
        Read a netCDF file located at param filepath.
        Read data and spacing between points.
        Sets internal variable states.
        """
        rootgroup = netCDF4.Dataset(self.filepath, "r", format="NETCDF4")
        self._values = rootgroup.variables["rdata"][:].filled()
        self._dims = self._get_dims(rootgroup)
        self._coords = self._get_coords(rootgroup)
        self._units = get_units(self.filepath)

    def _get_dims(self, rootgroup: netCDF4.Dataset) -> tuple[str]:
        """
        Get dims.

        Dims is analogous to xarray.Dataset.dims

        Parameters
        ----------
        rootgroup: netCDF4.Dataset
            netCDF4 Dataset read from file

        Returns
        -------
        tuple[str]
            A tuple with the name of each dimension.

        """
        old_dims = rootgroup.variables["rdata"].dimensions
        new_dims = list(old_dims)
        mapping_dict = {"dim_3": "x", "dim_2": "y", "dim_1": "z"}
        for idx, oname in enumerate(old_dims):
            new_dims[idx] = mapping_dict[oname]
        return tuple(new_dims)

    def _get_coords(self, rootgroup: netCDF4.Dataset) -> dict[str, np.ndarray]:
        """
        Get coords.

        Coords is analogous to xarray.Dataset.coords

        This code should handle an arbitrary number of dims.

        Parameters
        ----------
        rootgroup: netCDF4.Dataset
            netCDF4 Dataset read from file

        Returns
        -------
        dict[str, numpy.ndarray]
            Dictionary with one key-value pair for each dimension.
            The key is the dimension name. The value represents the domain
            of the dimension. It starts at the origin and goes, in evenly
            spaced steps, until the length of the dimension is achieved. The number
            of steps is defined by the shape of the value array.

        """
        origin = []
        spacing = []
        for origin_spacing in rootgroup.variables["pos"]:
            origin.append(origin_spacing[0])
            spacing.append(origin_spacing[1])
        origin = tuple(origin)
        spacing = tuple(spacing)
        coords = {}
        for key, dim in enumerate(self._dims):
            coords[dim] = np.linspace(
                origin[key],
                origin[key] + spacing[key] * (self._values.shape[key] - 1),
                self._values.shape[key],
            )
        return coords
