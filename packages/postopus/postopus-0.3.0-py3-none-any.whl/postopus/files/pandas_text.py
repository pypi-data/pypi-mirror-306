from __future__ import annotations

import ast
import re
import warnings
from typing import TYPE_CHECKING

import numpy as np
import pandas

if TYPE_CHECKING:
    from pathlib import Path


class PandasTextFile:
    """Inspired by @sohlmann 's readers, #38."""

    EXTENSIONS = [""]  # TODO: check me if I break stuff elsewhere

    _forces_columns = [
        "index",
        "species",
        "total_x",
        "total_y",
        "total_z",
        "ion-ion_x",
        "ion-ion_y",
        "ion-ion_z",
        "vdw_x",
        "vdw_y",
        "vdw_z",
        "local_x",
        "local_y",
        "local_z",
        "nl_x",
        "nl_y",
        "nl_z",
        "fields_x",
        "fields_y",
        "fields_z",
        "hubbard_x",
        "hubbard_y",
        "hubbard_z",
        "scf_x",
        "scf_y",
        "scf_z",
        "nlcc_x",
        "nlcc_y",
        "nlcc_z",
        "phot_x",
        "phot_y",
        "phot_z",
    ]

    def __init__(self, filepath: Path) -> None:
        """
        Allow reading a file with pandas.

        Parameters
        ----------
        filepath : Path
            Path to the file made accessible by this object
        """
        self.filepath = filepath

    def _readfile(self) -> None:
        """
        Enable Postopus to read data, stored in text files with ASCII and headers.

        Either uses pandas or just reads the contents as a string.
        Sets internal variable states.

        """
        unit_dict = {}
        metadata_dict = {"filename": self.filepath.name}
        tdgeneral_known_files = {
            "energy",
            "maxwell_energy",
            "laser",
            "multipoles",
            "coordinates",
            "total_current",
            "current_at_points",
            "photons",
        }
        tdgeneral_regular_endings = ("field_x", "field_y", "field_z")

        ##############################
        # Files in 'static'
        ##############################
        if self.filepath.name == "convergence":
            # Special read for convergence file
            values = pandas.read_csv(self.filepath, sep=r"\s+", index_col=0)
        elif self.filepath.name == "forces":
            # Special read for forces file
            values = pandas.read_csv(
                self.filepath,
                sep=r"\s+",
                index_col=0,
                header=None,
                skiprows=1,
                names=self._forces_columns,
            )
        elif self.filepath.name in {"info"}:
            # Special read for info file
            with open(self.filepath) as fil:
                values = fil.readlines()

        elif self.filepath.name == "bandstructure":
            unit_dict, values = self.read_bandstructure_file()

        elif self.filepath.name == "eigenvalues":
            metadata_dict, values = self.read_eigenvalues_file()

        ##############################
        # Files in 'td.general'
        ##############################

        elif (
            self.filepath.name.endswith(tdgeneral_regular_endings)
            or self.filepath.name in tdgeneral_known_files
        ):
            # Standard td general reading ###
            with open(self.filepath) as file:
                # skip "HEADER" line
                for i in range(2):
                    _ = file.readline()

                # After HEADER and until # Iter, everything is metadata
                metadata_lines = 0
                for line in file:
                    if line.startswith("# Iter"):
                        break
                    metadata_lines += 1
                    # split key and values if two spaces or more, ignore breaklines
                    # and eq. signs
                    split_line = re.split(
                        r"\s{2,}", line[2:].replace("\n", "").replace("=", "")
                    )
                    metadata_dict[split_line[0]] = split_line[1:]

                # last two lines are column headers and units
                col_line = line
                unit_line = file.readline()

            # complicated splitting needed because some column titles have a
            # space inside
            column_headers = [
                s.strip() for s in col_line[1:-1].split("  ") if len(s.strip()) >= 1
            ]

            # unit dict
            units = [
                s.strip() for s in unit_line[1:-1].split("  ") if len(s.strip()) >= 1
            ]

            # Deviations from standard ###
            if self.filepath.name == "coordinates" or self.filepath.name == "photons":
                # column header spacing deviates from the standard, split 3 spaces
                column_headers = [
                    s.strip()
                    for s in col_line[1:-1].split("   ")
                    if len(s.strip()) >= 1
                ]
                # split by comma and assign the last units to 3 columns each.
                units = units[:-1] + [
                    unit for unit in units[-1].split(",") for _ in range(3)
                ]
            elif self.filepath.name == "total_current":
                warnings.warn(
                    "From the seen examples, total_current files do not include units, "
                    "but maybe this is wrong. In case the units are given, the reading"
                    " routine should be changed."
                )
                units = ["Units not specified" for _ in range(len(column_headers))]
                metadata_lines = -1  # one line less in the header as we should

            unit_dict = dict(zip(column_headers, units))

            values = pandas.read_csv(
                self.filepath,
                sep=r"\s+",
                index_col=0,
                skiprows=metadata_lines + 5,
                header=None,
                names=column_headers,
            )

        else:
            try:
                """
                If yet unknown file (or no special flags needed), try reading with
                pandas (and some (hopefully sane) defaults).
                """
                warnings.warn(
                    f"We do not know this type of static/td.general file "
                    f"({self.filepath})."
                    " It is probably easily possible to optimize the reading"
                    " of it. So, please contact us!"
                )
                values = pandas.read_csv(self.filepath, sep=r"\s+", comment="#")
            except pandas.errors.ParserError:
                # Can't read with pandas. Just read as text, better than nothing..
                with open(self.filepath) as fil:
                    values = fil.readlines()
                warnings.warn(
                    f"Could not read file {self.filepath} with Pandas! Only "
                    f"returning file contents linewise.",
                    UserWarning,
                )

        if isinstance(values, pandas.DataFrame) and not hasattr(values, "filepath"):
            values.filepath = self.filepath

        self._values = values
        self._attrs = {"units": unit_dict, "metadata": metadata_dict}

    @property
    def values(self) -> pandas.DataFrame | str:
        """
        Getter for the field values. Data only gets loaded, when it's accessed.

        Returns
        -------
        pandas.DataFrame | str
            pandas DataFrame or string with values from the file
        """
        try:
            # See if variable already exists (e. g. if "coords" was accessed
            # before "values")
            return self._values
        except AttributeError:
            self._readfile()
        return self._values

    @property
    def attrs(self) -> dict[str, dict[str, str]]:
        """
        Attributes from header pandas Text file.
        """
        try:
            # See if variable already exists (e. g. if "coords" was accessed
            # before "values")
            return self._attrs
        except AttributeError:
            self._readfile()
        return self._attrs

    def read_bandstructure_file(self) -> tuple[dict[str, str], pandas.DataFrame]:
        """
        Read bandstructure files from static folder.

        Returns
        -------
        unit_dict: {column_header_name: corresponding_unit}
        values: pd.Dataframe with bandstructure values

        """
        with open(self.filepath) as file:
            headers = file.readline()

        orig_headers = headers[1:-1].split()
        coords = orig_headers[0:4]
        number_of_bands = int(orig_headers[-2])
        unit_of_bands = orig_headers[-1]
        unit_of_vectors = "".join(orig_headers[4:6])[0:-1]
        band_headers = [f"band_{i}" for i in range(1, number_of_bands + 1)]
        column_headers = coords + band_headers

        units = (
            ["Coord"]
            + [unit_of_vectors for _ in range(3)]
            + [unit_of_bands for _ in range(number_of_bands)]
        )

        unit_dict = dict(zip(column_headers, units))

        values = pandas.read_csv(
            self.filepath,
            sep=r"\s+",
            index_col=0,
            header=None,
            skiprows=1,
            names=column_headers,
        )
        return unit_dict, values

    def read_eigenvalues_file(
        self,
    ) -> tuple[dict[str, list[str]], list[pandas.DataFrame]]:
        """
        Read Eigenvalues file

        Represents the eigenvalues data as a multiindex pandas Dataframe, each outer
        index represents one k-point block.

        The rest of the information (e.g. which coordinates each of the k-points has)
        is stored as metadata information.

        """
        metadata = []
        with open(self.filepath) as file:
            for line_number, line in enumerate(file):
                if line.startswith(" #st"):
                    break
                metadata.append(line.replace("\n", ""))
            column_headers = (line[2:]).split()
            for line in file:
                if line.startswith("#k"):
                    metadata.append(line.replace("\n", ""))
        metadata = list(filter(None, metadata))
        kpoints_dict = {}
        k_number = 1
        for info in metadata:
            if info.startswith("#k ="):
                k_coord = ast.literal_eval("(" + info.split("(")[1])
                kpoints_dict[k_number] = k_coord
                k_number += 1
        info_dict = [info for info in metadata if not info.startswith("#k =")]
        metadata_dict = {
            "filename": self.filepath,
            "info": info_dict,
            "k": kpoints_dict,
        }

        if bool(metadata_dict["k"]):
            skip_rows = line_number + 2
        else:
            skip_rows = line_number + 1

        df = pandas.read_csv(
            self.filepath,
            sep=r"\s{2,}",  # due to Error column, at least two spaces
            index_col=0,
            header=None,
            skiprows=skip_rows,
            comment="#",
            names=column_headers,
            engine="python",  # regex is supported only by python engine
        )
        block_length = df.index.max()
        list_of_dfs = np.split(
            df, [i for i in range(block_length, df.shape[0], block_length)]
        )
        ks = [i for i in range(1, len(list_of_dfs) + 1)]

        # Multiindex
        if metadata_dict["k"]:
            values = pandas.concat(list_of_dfs, keys=ks, axis=0, names="k")
            return metadata_dict, values

        values = pandas.concat(list_of_dfs)

        return metadata_dict, values
