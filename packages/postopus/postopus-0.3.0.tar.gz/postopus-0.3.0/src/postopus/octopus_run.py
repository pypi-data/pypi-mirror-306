"""
Top level module acting as the only class the user interfaces with directly.

Classes:
    Run: Initialization point for Postopus which triggers all data collection and allows
    to access the found data in a unified way.

Examples can be found in the "examples" directory.
"""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from postopus.datacontainers.system import System
from postopus.datacontainers.util.convenience_dict import ConvenienceDict
from postopus.output_collector import OutputCollector

if TYPE_CHECKING:
    from collections.abc import Iterator


class Run(ConvenienceDict):
    """
    Starting point for users of Postopus.

    Root object for Postopus, initializing the module and providing access to all
    data and functions.
    """

    # Set name of dict in ConvenienceDict
    __dict_name__ = "systems"

    def __init__(self, basedir: Path = Path(".")) -> None:
        """
        Entrypoint for the user to initialize the Postopus module.

        Given a path, the collection of all Octopus data below this directory is
        triggered and a dedicated datastructure is build.
        By using the given data structure, data to access can be selected by the user.

        Parameters
        ----------
        basedir
            directory where the results can be found (directory has to contain inp file)

        """
        # Init system dict in super
        super().__init__()
        self.path = self._check_provided_path(basedir)

        # get fields from FS
        output_from_fs = OutputCollector(self.path)

        for sysname, outputdata in output_from_fs.output.items():
            # self.systems is available through ConvenienceDict
            self.systems[sysname] = System(sysname, self.path, outputdata, self)

        # Multisytem handlling:
        # self.systems["SolarSystem"].system_data["Earth"].system_data["Europe"] =
        # self.systems["SolarSystem.Earth.Europe"]
        # del self.systems["SolarSystem.Earth.Europe"] and so on
        # Now the user could do run.SolarSystem.Earth.Europe.td...
        for system in sorted(self.systems.keys()):
            if "." in system:
                multisys_string = (
                    f"self.systems['{system.split('.', )[0]}'].system_data['"
                )
                multisys_string += "'].system_data['".join(system.split(".")[1:])
                multisys_string += f"'] = self.systems['{system}']"
                exec(multisys_string)
                del self.systems[system]

        self.structures = None

    def __repr__(self) -> str:
        return "\n".join(self._repr_gen())

    def _repr_gen(self) -> Iterator[str]:
        yield f"{self.__class__.__name__}('{self.path!s}'):"

        yield "Found systems:"
        for system_name in sorted(self.systems.keys()):
            yield f"    {system_name!r}"

        yield "Found calculation modes:"
        calculation_modes = set()
        for system in self.systems.values():
            calculation_modes |= system.system_data.keys()
        for mode in sorted(calculation_modes):
            yield f"    {mode!r}"

    def _check_provided_path(self, path: Path | str) -> Path:
        """
        Check if the provided path is valid

        Parameters
        ----------
        path : Path
            path/to/Octopus/output/with/inp

        """
        path = Path(path)
        if path.is_file():
            # Path to an 'inp' file was provided. Open it and read config
            raise NotADirectoryError(
                "Please provide the path to the directory containing the 'inp' file!"
            )
        elif not (path / "inp").is_file():
            # Abort, no 'inp' file found
            raise FileNotFoundError("'inp' file missing - aborting!")
        return path.absolute()
