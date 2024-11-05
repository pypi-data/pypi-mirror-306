"""
Implementation of several file readers for the different output formats.
"""

from pathlib import Path

from .cube import CubeFile
from .file import File
from .netcdf import NetCDFFile
from .pandas_text import PandasTextFile
from .text import TextFile
from .vtk import VTKFile
from .xcrysden import XCrySDenFile
from .xyz import XYZFile

extension_loader_map = {
    ext: cls
    for cls in [
        CubeFile,
        NetCDFFile,
        TextFile,
        VTKFile,
        XYZFile,
        XCrySDenFile,
        PandasTextFile,
    ]
    for ext in cls.EXTENSIONS
}

parsable_sources = set(extension_loader_map.keys())


def openfile(filepath: Path) -> File:
    """
    Will automatically choose the correct class to open a file.

    :param filepath: path to the file that shall be opened
    :return: instance class that was chosen to open the file with postopus file loaders
    """
    cls = extension_loader_map[filepath.suffix]

    # instantiate object for file type
    try:
        return cls(filepath)
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"There is a parser for '*{filepath.suffix}' files,"
            f" but {filepath} was not found. Please contact the developer team if you"
            f" see this message."
        ) from exc
