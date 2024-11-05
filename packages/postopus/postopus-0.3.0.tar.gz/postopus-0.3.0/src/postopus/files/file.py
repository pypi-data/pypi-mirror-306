from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import numpy


class File:
    @property
    def coords(self) -> dict[str, list[float]]:
        """
        Getter for the coords. Data only gets loaded, when it's accessed.
        Coords are analogous to xarray.Dataset.coords

        Returns
        -------
        dict
            existing coordinate points per dimension

        """
        try:
            # See if variable already exists (e. g. if "values" was accessed
            # before "coords")
            return self._coords
        except AttributeError:
            self._readfile()
        return self._coords

    @property
    def values(self) -> numpy.ndarray:
        """
        Getter for the field values. Data only gets loaded, when it's accessed.

        Returns
        -------
        numpy.ndarray
            data values from the file.

        """
        try:
            # See if variable already exists (e. g. if "coords" was accessed
            # before "values")
            return self._values
        except AttributeError:
            self._readfile()
        return self._values

    @property
    def dims(self) -> list[str]:
        """
        Getter for the dims. Data only gets loaded, when it's accessed.
        dims are analogous to xarray.Dataset.dims.

        Returns
        -------
        list[str]
            list with all dimension names

        """
        try:
            # See if variable already exists (e. g. if "coords" was accessed
            # before "dims")
            return self._dims
        except AttributeError:
            self._readfile()
        return self._dims

    @property
    def units(self) -> str:
        """
        Getter for the units. Data only gets loaded, when it's accessed.

        Returns
        -------
        str
            units, e.g. "au"

        """
        try:
            # See if variable already exists (e. g. if "coords" was accessed
            # before "units")
            return self._units
        except AttributeError:
            self._readfile()
        return self._units

    def xarray(self):
        from postopus.files.utils.xarray_converter import to_xarray

        return to_xarray(self)

    @abstractmethod
    def _readfile(self):
        """
        Method to be implement in derived classes which is specific to the file
        type we read.
        When called, we expect this method to populate
        - self._coords
        - self._values
        - self._dims
        - self._units

        """
