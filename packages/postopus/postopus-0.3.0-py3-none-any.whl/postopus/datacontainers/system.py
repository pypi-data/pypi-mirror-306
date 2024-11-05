from __future__ import annotations

from typing import TYPE_CHECKING

from postopus.datacontainers.calculationmodes import CalculationModes
from postopus.datacontainers.util.convenience_dict import ConvenienceDict

if TYPE_CHECKING:
    from collections.abc import Iterator
    from pathlib import Path

    from postopus import Run
    from postopus.datacontainers.util.output_collector import (
        System as OutputCollectorSystem,
    )


class System(ConvenienceDict):
    """
    The `System` class provides a dict with all found calculation modes written for the
    system.

    Parameters
    ----------
    systemname
        Name of this system
    rootpath
        Path to the Octopus output (not system folder)
    mode_field_info
        Calculation modes including the outputs of each calculation mode.
    """

    # Set name of dict in ConvenienceDict
    __dict_name__ = "system_data"

    def __init__(
        self,
        systemname: str,
        rootpath: Path,
        mode_field_info: OutputCollectorSystem,
        parent: Run,
    ) -> None:
        # Init system dict in super
        super().__init__()

        self.systemname = systemname
        self.path = rootpath
        self.mode_field_info = mode_field_info
        self.parent = parent

        for m in mode_field_info.keys():
            # self.modes is available through ConvenienceDict
            self.system_data[m] = CalculationModes(
                m,
                mode_field_info[m],
                self,
                self.path,
                self.systemname,
            )

    def __repr__(self) -> str:
        return "\n".join(self._repr_gen())

    def _repr_gen(self) -> Iterator[str]:
        yield f"{self.__class__.__name__}(name={self.systemname!r}, rootpath='{self.path!s}'):"

        yield "Found calculation modes:"
        for mode in sorted(self.system_data.keys()):
            yield f"    {mode!r}"
