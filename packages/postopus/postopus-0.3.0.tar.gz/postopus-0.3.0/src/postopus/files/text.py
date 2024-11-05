from __future__ import annotations

from typing import TYPE_CHECKING

import numpy
import numpy as np
import pandas as pd

from postopus.files.file import File
from postopus.files.utils.units import get_units
from postopus.utils import regular_grid_from_positions

if TYPE_CHECKING:
    from pathlib import Path


class TextFile(File):
    EXTENSIONS = [".x=0", ".y=0", ".z=0", ".x=0,y=0", ".x=0,z=0", ".y=0,z=0"]

    def __init__(self, filepath: Path) -> None:
        """
        Enable Postopus to read data, stored in text files with ASCII.
        Numpy's loadtxt provides functionality for loading:
        https://numpy.org/doc/stable/reference/generated/numpy.loadtxt.html

        Parameters
        ----------
        filepath : Path
            path to the file in ASCII/text format

        """
        self.filepath = filepath

    def _readfile(self) -> None:
        """
        Loads data from the given file using pandas.
        Sets internal variable states.
        """
        # Load data with pandas
        pdf = pd.read_table(self.filepath, sep="\s+", skip_blank_lines=True)
        # Fix headers (cyclic shift to left) - needed to ignore '#' as a column title
        newnames = list(pdf.keys())
        newnames.append(newnames.pop(0))
        pdf = pdf.rename(columns={old: new for old, new in zip(pdf.keys(), newnames)})
        # drop last two columns (values are NaN) - dropped columns are always "Im" and
        # '#' (if Octopus does not change its output). "Im" is dropped, because it
        # currently is not filled with values by Octopus.
        # pdf = pdf.drop(columns=[pdf.keys()[-2], pdf.keys()[-1]])
        # drop last two columns (values are NaN) - "Im" and "#" are last header names
        # after cyclic shift. Could be less specific here and just drop two last lines,
        # not using their column names, but specifying names offers potential to find
        # changes in output file formatting.
        pdf = pdf.drop(columns=["Im", "#"])
        np_data = pdf.to_numpy()

        self._dims = tuple(pdf.keys()[:-1])
        self._coords = self._get_coords(np_data)
        self._values = self._get_values(np_data)
        self._units = get_units(self.filepath)

    def _get_coords(self, in_vals: numpy.ndarray) -> dict[str, numpy.ndarray]:
        """
        Get coords.

        Coords and dims are analogous to xarray.Dataset.coords and
        xarray.Dataset.dims

        The number of dimensions is assumed to be variable, but the names
        should be
        either "x", "y" or "z"

        Example:

        >>> t._get_coords()
        {'x': array([-7.05, -6.9 , -6.75, -6.6 , -6.45, -6.3 , -6.15, -6.,
         -5.85, -5.7 , -5.55, -5.4 , -5.25, -5.1 , -4.95, -4.8 , -4.65, -4.5,
         -4.35, -4.2 , -4.05, -3.9 , -3.75, -3.6 , -3.45, -3.3 , -3.15,
         -3.  , -2.85, -2.7 , -2.55, -2.4 , -2.25, -2.1 , -1.95, -1.8 ,
         -1.65, -1.5 , -1.35, -1.2 , -1.05, -0.9 , -0.75, -0.6 , -0.45,
         -0.3 , -0.15,  0.  ,  0.15,  0.3 ,  0.45,  0.6 ,  0.75,  0.9 ,
          1.05,  1.2 ,  1.35,  1.5 ,  1.65,  1.8 ,  1.95,  2.1 ,  2.25,
          2.4 ,  2.55,  2.7 ,  2.85,  3.  ,  3.15,  3.3 ,  3.45,  3.6 ,
          3.75,  3.9 ,  4.05,  4.2 ,  4.35,  4.5 ,  4.65,  4.8 ,  4.95,
          5.1 ,  5.25,  5.4 ,  5.55,  5.7 ,  5.85,  6.  ,  6.15,  6.3 ,
          6.45,  6.6 ,  6.75,  6.9 ,  7.05]),
        'y': array([-7.35, -7.2 , -7.05, -6.9 , -6.75, -6.6 , -6.45, -6.3,
        -6.15, -6., -5.85, -5.7 , -5.55, -5.4 , -5.25, -5.1 , -4.95, -4.8,
         -4.65, -4.5 , -4.35, -4.2 , -4.05, -3.9 , -3.75, -3.6 , -3.45,
         -3.3 , -3.15, -3.  , -2.85, -2.7 , -2.55, -2.4 , -2.25, -2.1 ,
         -1.95, -1.8 , -1.65, -1.5 , -1.35, -1.2 , -1.05, -0.9 , -0.75,
         -0.6 , -0.45, -0.3 , -0.15,  0.  ,  0.15,  0.3 ,  0.45,  0.6 ,
          0.75,  0.9 ,  1.05,  1.2 ,  1.35,  1.5 ,  1.65,  1.8 ,  1.95,
          2.1 ,  2.25,  2.4 ,  2.55,  2.7 ,  2.85,  3.  ,  3.15,  3.3 ,
          3.45,  3.6 ,  3.75,  3.9 ,  4.05,  4.2 ,  4.35,  4.5 ,  4.65,
          4.8 ,  4.95,  5.1 ,  5.25,  5.4 ,  5.55,  5.7 ,  5.85,  6.  ,
          6.15,  6.3 ,  6.45,  6.6 ,  6.75,  6.9 ,  7.05,  7.2 ,  7.35])}

        Parameters
        ----------
        in_vals : numpy.ndarray
            values to process and build coordinates for

        Returns
        -------
        dict
            coordinates and dimensions for the available axes

        """
        coords = {}
        for i, dim in enumerate(self._dims):
            # set of known coordinate points (ps) is
            ps = in_vals[:, i]
            # convert into complete coordinate grid
            coords[dim] = regular_grid_from_positions(ps)
        return coords

    def _get_values(self, in_vals: numpy.ndarray) -> numpy.ndarray:
        """
        Get field values out of the data. Reshape if necessary.

        Parameters
        ----------
        in_vals : numpy.ndarray
            values to process reshape

        Returns
        -------
        numpy.ndarray
            values of the field

        """
        # Assuming there is no Im part, in that case we expect "x, y, Re" as the data.
        # we only read the real (Re) part here.
        lin_field = in_vals[:, -1]
        if len(self._dims) > 1:
            desired_shape = tuple(len(self._coords[dim]) for dim in self._dims)

            data_points_read = len(lin_field)
            # is this 2d grid complete (i.e. one data point has been written
            # for every grid point?)
            if data_points_read == np.prod(desired_shape):
                values = np.reshape(lin_field, desired_shape)
            else:
                # data from file is not complete, and we need to fill in the blanks
                # Build a static mapping from coordinate values to indexes. .index()
                # of list is slow (can't beat amortised O(1) of dict access).
                dim0_c_map = {
                    co: idx for idx, co in enumerate(self._coords[self._dims[0]])
                }
                dim1_c_map = {
                    co: idx for idx, co in enumerate(self._coords[self._dims[1]])
                }

                # create ndarray with correct shape and initialize with NaN
                filled_arr = np.empty(desired_shape)
                filled_arr[:] = np.nan

                # fill ndarray of correct shape
                for point in in_vals:
                    filled_arr[dim0_c_map[point[0]], dim1_c_map[point[1]]] = point[2]
                values = filled_arr
        else:
            values = lin_field
        return values
