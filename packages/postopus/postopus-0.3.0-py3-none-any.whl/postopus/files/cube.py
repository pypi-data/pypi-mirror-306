from pathlib import Path

import numpy as np
from ase.io.cube import read_cube
from ase.units import Bohr

from postopus.files.file import File


class CubeFile(File):
    EXTENSIONS = [".cube"]

    def __init__(self, filepath: Path) -> None:
        """
        Prepare to read a CUBE file.

        Parameters
        ----------
        filepath : Path
            path to cube file

        """
        self.filepath = filepath

    def _readfile(self) -> None:
        """Sets internal variable states."""
        # TODO: This ignores all information on Atoms in cube files. Postopus currently
        #  does not support this, but might in the future.
        with open(self.filepath) as cfile:
            # Read cube data
            contents = read_cube(cfile)
            # store values without postprocessing
            values = contents["data"]
            # ase transforms to Angstrom, rollback to Bohr, since octopus' output is b
            origin = contents["origin"] / Bohr

            # spacing from cube results in a (3, 3) array.
            # At the moment, only orthogonal basis vectors are
            # supported (for which only the elements on the diagonal can be non-zero).
            # Raise error, if off-diagonal elements are non-zero.
            # ase transforms to Angstrom, rollback to Bohr, since octopus' output is b
            spacing_array = contents["spacing"] / Bohr
            for i in range(3):
                for j in range(3):
                    if i == j:
                        assert spacing_array[i, j] > 0
                    else:
                        if spacing_array[i, j] != 0:
                            msg = "Can only deal with orthogonal basis vectors. "
                            msg += "Spacing matrix is:\n"
                            msg += str(spacing_array)
                            raise NotImplementedError(msg)
            # at this point, we know that basis vectors are orthogonal, and
            # we can take the diagonal elements as therefore
            # spacing distance for each basis vector direction:
            spacing = np.array(
                [spacing_array[0, 0], spacing_array[1, 1], spacing_array[2, 2]]
            )

        # TODO: cannot determine any name for self.dims, as no naming is in cube files.
        #  For now, we can assume 3D data, therefore x, y, z, but what happens, when
        #  dimensionality changes? Does that even work with cube?
        dims = ["x", "y", "z"]

        # compute values for coords for every dimension in dim
        coords = {}
        for idx, dim in enumerate(dims):
            min_point = origin[idx]
            n_points = values.shape[idx]
            max_point = origin[idx] + (n_points - 1) * spacing[idx]

            coords[dim] = np.linspace(min_point, max_point, n_points)

        self._values = values
        self._dims = dims
        self._coords = coords
        # Cube files have Bohr as the native unit and is consistent with Octopus output
        # TODO: Test for this
        self._units = "au"
