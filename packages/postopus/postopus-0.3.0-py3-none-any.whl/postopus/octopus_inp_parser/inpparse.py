from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


class Parser:
    """
    Parses the input file for the given run.
    TODO: needs fixing, when we can read multisystems

    Variables for the user:

    fields_raw : dict[str, str | list[str]]
        raw dump of the lines of 'inp'
    systems : dict[str, dict[str, str]]
        systems and their types
    """

    def __init__(self, inputfile: Path) -> None:
        with open(inputfile) as inpf:
            self.inplines = inpf.readlines()

        self.fields_raw = self._parse()

        # First find all systems (as well as subsystems, subsubsystems, ...)
        self.systems = self._get_systems()
        self.read_systems_params()

    def _parse(self) -> dict[str, str | list[str]]:
        """
        Parse the input file. Every variable is saved with a new key in a dict,
        values of variables are stored as values to the keys. Blocks in the
        input file contain a list as value, every block line is a list element.
        :return: dict with all variables/blocknames as keys and values as
                 values
        """
        result = {}
        blockname = None
        for line in self.inplines:
            line = line.lstrip(" ")
            # skip line if comment
            if line == "\n" or line.lstrip()[0] == "#":
                continue
            # remove trailing comments and newline
            line = line.split("#")[0].rstrip("\n")

            # check if line is simple field
            if re.match(r"(\w+\.)*?\w+ *=", line):
                result[line.split("=")[0].rstrip(" ")] = line.split("=")[1].lstrip(" ")

            # check if line is start of block
            if blockname is None and "%" in line:
                # set name of found block and start block reading
                blockname = line.split("%")[1].rstrip(" ").lstrip(" ")
                result[blockname] = []
            elif blockname is not None and "%" in line:  # end of block
                # unset name of found block and end block reading
                blockname = None
            elif blockname is not None:  # we are currently reading a block
                result[blockname].append(line)

        return result

    """
    MULTISYSTEMS capable methods from here on, others might need fixing
    """

    def _get_systems(self) -> dict[str, dict[str, str]]:
        """
        Wrapper for self._get_systems_rec.
        Returns
        -------

            result from self._get_systems_rec starting from the root directory
        """
        return self._get_systems_rec(parent="")

    def _get_systems_rec(self, parent: str = "") -> dict[str, dict[str, str]]:
        """
        Read all systems from the input file. Either defined as block or
        globally for the while simulation. Recursive function, started by
        self._get_systems().

        Returns
        -------

            dict with all system names from the current "parent" level and above

        """
        # list containing all systems that are a multisystem on this level
        multisyslst = []
        systems_list = {}

        if parent != "":
            parent = parent + "."

        try:
            systems_list = self.fields_raw[parent + "Systems"]
        except KeyError:
            if parent == "":
                systems_list = {"default": "electronic"}

        systems_this_level = {}
        for system in systems_list:
            sysname = ""
            systype = ""
            try:
                # Try, in case there is no block for Systems
                sysname = system.split("|")[0].strip().strip("'").strip('"')
                systype = system.split("|")[1].strip().strip("'").strip('"')
            except IndexError:
                systems_this_level[parent + sysname] = {"": "electronic"}
                continue
            if systype == "multisystem":
                # store multisystem-name for recursive exploration
                multisyslst.append(parent + sysname)
            # Add found system to systems list (name prepended with parent)
            systems_this_level[parent + sysname] = {"_systemtype": systype}

        if multisyslst != []:
            # need to find subsystems of multisystem
            for ms in multisyslst:
                # merge list from lower levels into this level
                systems_this_level = dict(
                    list(systems_this_level.items())
                    + list(self._get_systems_rec(parent=ms).items())
                )

        return systems_this_level

    def read_systems_params(self) -> None:
        """
        This reads all information for all systems in 'inp'. Default/Top Level
        system is in system with name "", others (systems from 'Systems' block)
        use the system's name (including parent in multisystems) as their ID.
        """
        global_params = {}
        key_processed = False
        # Check every key once for every system
        for key in self.fields_raw.keys():
            for system in self.systems.keys():
                if system + "." in key:
                    # remove prefix with system "path" from key
                    shortened_key = key.replace(system + ".", "")
                    # value from fields_raw to the correct system
                    self.systems[system][shortened_key] = self.fields_raw[key]
                    key_processed = True

            # If key was not yet processed, add to global parameters
            if not key_processed:
                global_params[key] = self.fields_raw[key]
            key_processed = False

        # Add global parameters to self.systems
        if "default" in self.systems:
            global_params["_systemtype"] = self.systems["default"][""]
        self.systems["default"] = global_params
