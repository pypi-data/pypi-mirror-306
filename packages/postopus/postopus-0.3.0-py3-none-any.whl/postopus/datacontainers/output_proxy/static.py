from __future__ import annotations

import warnings
from typing import TYPE_CHECKING

from postopus.files import openfile

if TYPE_CHECKING:
    import pandas as pd

    from postopus.output_collector import OutputField


from ._base import OutputProxy


class StaticOutput(OutputProxy):
    """Proxy for outputs in run/static like `info`, `convergence`, etc."""

    @classmethod
    def _match(self, output: OutputField) -> bool:
        return output.is_static()

    def __post_init__(self):
        self._available_files = list(self._output_field.files)
        self._file = openfile(self._available_files[0])

    def __call__(self) -> pd.DataFrame:
        """Load table-structured data from the output and provide it as
        data frame. The meta data in the header of the output file is also
        provided in `.attrs` of the returned data frame.
        """

        if len(self._available_files) > 1:
            warnings.warn(
                "There is more than one file found for the output which is unexpected."
                f" All files other than {self._available_files[0]} will be ignored"
            )

        # Rely on (lazy loaded) file reader implementation.
        df = self._file.values
        # Update attributes
        df.attrs = self._file.attrs

        return df


class Info(StaticOutput):
    """Proxy class specific for the info file"""

    __output__ = "info"

    def __call__(self) -> list:
        """Return the content of the info file as list of its lines."""
        return self._file.values
