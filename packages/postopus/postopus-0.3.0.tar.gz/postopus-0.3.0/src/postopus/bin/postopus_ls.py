"""postopus-ls utility gives information on a Octopus run in the current `pwd`."""
from __future__ import annotations

import os
import shutil
from pathlib import Path

from prettytable import ALL, PrettyTable

from postopus.octopus_run import Run
from postopus.utils import humanise_size


def get_metadata(rootdir: str) -> tuple[int, int, int]:
    """Collect metadata of a folder recursively.

    Get metadata from a folder. Get total size (in Bytes), earliest and latest mtime.
    Metadata is collected recursively, through all subdirs.

    Parameters
    ----------
    rootdir : str
        directory for which metadata is gathered (recursive)

    """
    bytesize = 0
    earliest_date = 0
    latest_date = 0
    for path, dirs, files in os.walk(rootdir):
        for f in files:
            fpath = Path(path, f)
            bytesize += fpath.stat().st_size
            if earliest_date > fpath.stat().st_mtime:
                earliest_date = fpath.stat().st_mtime
            elif latest_date < fpath.stat().st_mtime:
                latest_date = fpath.stat().st_mtime
    return bytesize, earliest_date, latest_date


def break_string(input: str, linelen: int, splitstr: str = "") -> str:
    """Line breaks a long string.

    Parameters
    ----------
    input : str
        String to split into multiple lines
    linelen : int
        max length of a line in the new string
    splitstr : str
        string, after which a new line can be inserted ("" is everywhere).
        If string cannot be found in range of `linelen`, force a newline
        (Default value = "")

    Returns
    -------
    str
        parameter `input`, contains linebreaks to fit a line with `linelen` chars

    """
    if splitstr == "":
        # stole this from https://stackoverflow.com/questions/9475241/
        #                 split-string-every-nth-character/9475354#9475354
        output = [input[i : i + linelen] for i in range(0, len(input), linelen)]
        output = "\n".join(output)
    else:
        input_parts = list(map(lambda elem: elem + splitstr, input.split(splitstr)))
        # remove splitstr from last element
        input_parts[-1] = input_parts[-1][: -len(splitstr)]
        output = [""]
        for part in input_parts:
            if len(output[-1]) + len(part) < linelen:
                output[-1] = output[-1] + part
            else:
                output.append(part)
        output = "\n".join(output)
    return output


def postopus_ls() -> None:
    """Control program flow. Main method."""
    # Check if input file is present
    if not Path("inp").exists():
        print("Found no input file 'inp' in current directory!")
        exit(-1)

    # Initialize data collection
    pwd = os.environ.get("PWD")
    run = Run(pwd)

    table = PrettyTable(["System", "CalculationMode", "Fields", "Size"])
    table.hrules = ALL
    table.align = "l"

    for syst in run.systems:
        if run.systems[syst].modes == {}:
            # system has no calculation modes, print only system-name
            table.add_row([syst, "", "", ""])
            continue

        for cm in run.systems[syst].modes:
            if run.systems[syst].modes[cm] == {}:
                # calculation mode has no fields, print only calculation mode
                table.add_row([syst, cm, "", ""])
                continue

            # get size of the terminal. we need the width to split the fields line
            termsize = shutil.get_terminal_size((80, 20))
            # fields should have length of 0.3 of the terminals width
            linelen = termsize.columns / 3

            # get all fields and put them into a printable format
            fields = run.systems[syst].modes[cm].fields.keys()
            # add ", " between elements and remove ", " from end
            fieldsstr = ", ".join(fields)
            fieldsstr = break_string(fieldsstr, linelen, ", ")

            # get the size of the output
            if syst == "_Global" or syst == "default":
                output_path = Path(pwd, "output_iter")
            else:
                output_path = Path(pwd, syst, "output_iter")
            size_res = humanise_size(get_metadata(output_path)[0])
            sizestr = f"{size_res[0]:.2f}" + " " + size_res[1]

            # add row to the table
            table.add_row([syst, cm, fieldsstr, sizestr])
    print(table)


if __name__ == "__main__":
    postopus_ls()
