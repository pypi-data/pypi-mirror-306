from __future__ import annotations

import warnings
from collections import namedtuple
from typing import TYPE_CHECKING

from postopus.files import openfile
from postopus.output_collector import VectorDimension

if TYPE_CHECKING:
    from postopus.output_collector import OutputField

from ._base import OutputProxy


class TDGeneralVectorField(OutputProxy):
    """Proxy for files in `run/td.general`"""

    @classmethod
    def _match(cls, output_field: OutputField) -> bool:
        """The output field is consider a td.general vectorfield
        if the output provides only vector dimensions in the other_index
        and after that static files (no nested other_index, no iterations).
        """
        if not output_field.has_other_index():
            return False
        if not output_field.other_index.keys() <= {VectorDimension(d) for d in "xyz"}:
            return False

        return output_field.other_index.get_any().is_static()

    _GeneralVectorField = namedtuple("GeneralVectorField", ["x", "y", "z"])

    def __call__(self) -> _GeneralVectorField:
        """Load the data of each provided vector component as data frame and
        return those as a combined named tuple. The components are accessable
        using `output().x`, `output().y` and `output().z`.
        """

        data = list()
        for dim in "xyz":
            files = list(self._output_field.other_index[VectorDimension(dim)].files)
            if len(files) > 1:
                warnings.warn(
                    "There is more than one file found for the output which is unexpected."
                    f" All files other than {files[0]} will be ignored"
                )

            file = openfile(files[0])
            values = file.values
            values.attrs = file.attrs
            data.append(values)
        return self._GeneralVectorField(*data)
