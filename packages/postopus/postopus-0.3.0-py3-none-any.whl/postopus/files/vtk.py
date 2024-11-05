from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pyvista as pv

from postopus.files.file import File
from postopus.files.utils.units import get_units

if TYPE_CHECKING:
    from pathlib import Path


class VTKFile(File):
    EXTENSIONS = [".vtk"]

    def __init__(self, filepath):
        """
        Enable Postopus to read VTK data, as written by Octopus.
        https://vtk.org/wp-content/uploads/2015/04/file-formats.pdf
        To write VTK output, 'inp' files must set 'OutputFormat' to 'vtk'.

        Parameters
        ----------
        filepath: Path
            path to the file in VTK format
        """
        self.filepath = filepath

    def _readfile(self):
        """
        Actual reading of the file happens here.
        """
        self._mesh = pv.read(self.filepath)
        self._dims, self._coords = self._get_coords_and_dims()
        self._values = self._get_values()
        self._units = get_units(self.filepath)

    def _get_coords_and_dims(
        self,
    ) -> tuple[tuple[str, str, str], dict[str, np.ndarray]]:
        """
        Get coords and dims from a vtk mesh.

        Coords is analogous to xarray.Dataset.coords, same for dims.

        Usually we don't handle the components of the vector field in the file class
        but octopus vtk output is a special case s. self.is_vector_field_vtk

        From the documentation
         https://vtk.org/wp-content/uploads/2015/04/file-formats.pdf:
        'The file format supports 1D, 2D, and 3D structured point datasets.
         The dimensions nx, ny, nz must be greater than or equal to 1'.
         So that x, y and z will always exist, even for 1D or 2D data.

        Returns
        -------
        tuple[str, str, str]
            dims

        dict[str, np.ndarray]
            coords

        """
        base_coords = {
            "x": np.unique(self._mesh.x),
            "y": np.unique(self._mesh.y),
            "z": np.unique(self._mesh.z),
        }

        if len(self._mesh.active_scalars.shape) > 1:  # Vector fields
            dims = ("component", "x", "y", "z")
            coords = {
                "component": np.array(["x", "y", "z"]),
                **base_coords,
            }
        else:
            dims = ("x", "y", "z")
            coords = base_coords

        return dims, coords

    def _get_values(self) -> np.ndarray:
        """
        Get data values from vtk mesh

        self._mesh.points and self._mesh.active scalars needs to be taken into account
        for generating the value grid. A simple
        lin_data.reshape(grid_size) would only work, if the length of
        each dimension is equal.

        Returns
        -------
        np.ndarray
            data values
        """

        if len(self._mesh.active_scalars.shape) > 1:  # Vector fields
            lin_vector_comps = np.transpose(np.array(self._mesh.active_scalars))
            values = np.empty((len(lin_vector_comps), *self._mesh.dimensions))
            for i, lin_comp in enumerate(lin_vector_comps):
                comp = self._fill_array(lin_comp)
                values[i] = comp
        else:
            lin_data = np.array(self._mesh.active_scalars)
            values = self._fill_array(lin_data)
        return values

    def _fill_array(self, lin_data):
        """
        Fill the values array with the linear data from the vtk mesh.

        lin_data will correspond either to the data of one component of a vector field
        or to the data of a scalar field.

        Parameters
        ----------
        lin_data: np.ndarray
            linear data values from the vtk mesh
        Returns
        -------
        np.ndarray
            3D values array
        """
        grid_size = self._mesh.dimensions
        # associate the value to the right point in space ###
        filled_arr = np.full(grid_size, np.nan)

        # concatenate points in space with values
        points = np.c_[self._mesh.points, lin_data]

        # index-coordinate maps of dims
        first_dim_indx = 0
        if len(self._mesh.active_scalars.shape) > 1:  # Vector fields:
            first_dim_indx = 1
        dim0_c_map = {
            co: idx for idx, co in enumerate(self._coords[self._dims[first_dim_indx]])
        }
        dim1_c_map = {
            co: idx
            for idx, co in enumerate(self._coords[self._dims[first_dim_indx + 1]])
        }
        dim2_c_map = {
            co: idx
            for idx, co in enumerate(self._coords[self._dims[first_dim_indx + 2]])
        }

        for point in points:
            filled_arr[
                dim0_c_map[point[0]], dim1_c_map[point[1]], dim2_c_map[point[2]]
            ] = point[3]

        values = filled_arr
        return values

    @staticmethod
    def get_scalars_count(vtk_file: Path) -> int | None:
        """
        Determine the count of components by peeking the headers of a vtk file.

        VTK files might either contain a scalar field or a vector field (all
        three components -x, -y and -z are in a single file). To check if a
        field is a scalar field or a vector field the file headers have to be
        checked.

        The headers of vtk files are not written in binary but just plain strings.
        In the header starting with 'SCALARS' the component count is given.

        Reading the header with simple python file reading is preferred over
        reading the whole file with pyvista, because the latter can be very slow.

        Parameters
        ----------
        vtk_file:
            path to the vtk file

        Returns
        -------
            The count of components given by the vtk file or `None` if the count
            coult not be determined.

        Raises
        ------
        FileNotFoundError
            If the field could not be determined.
        """
        with open(vtk_file, "rb") as fil:
            for line in fil.readlines():
                if str(line).startswith("b'SCALARS"):
                    n_components = int(str(line)[-4])
                    return n_components
