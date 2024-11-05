"""Provides supporting methods that are used in different modules."""
from __future__ import annotations

import math
from typing import TYPE_CHECKING

import numpy as np
import psutil

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path


def humanise_size(size: int) -> tuple[float, str]:
    """Given a positive integer, return a tuple (X, Unit) as in these examples.

    In [5]: h(2)
    Out[5]: (2.0, '')

    In [6]: h(2000)
    Out[6]: (1.953125, 'K')

    In [7]: h(1023)
    Out[7]: (1023.0, '')

    In [8]: h(1024)
    Out[8]: (1.0, 'K')

    In [9]: h(2**20)
    Out[9]: (1.0, 'M')

    Parameters
    ----------
    size : int
        size in bytes to convert into human readable format

    Returns
    -------
    tuple[float,str]
        tuple with size in new reference unit and unit

    """
    if not isinstance(size, int):
        raise TypeError(f"Expect integer, not {type(size)} (value={size})")
    if size < 0:
        raise ValueError(f"Expect non-negative number (not {size})")

    unit_index = int(math.log(size, 1024))
    unit_size = size / (1024.0**unit_index)

    prefix = (
        "B",
        "KiB",
        "MiB",
        "GiB",
        "TiB",
        "PiB",
        "EiB",
        "Hopefully this will never happen ^^",
    )
    return unit_size, prefix[unit_index]


def identify_regular_grid(xs: np.array) -> tuple:
    """Given a list of values xs which are sub sets of coordinates on a regular
    1d grid, identify the minimum (xmin), maximum (xmax) and grid spacing (h),
    and return those in a tuple.

    It should then be possible to compute all the grid positions using

    x_i = xmin + i * h  while x_i < xmax

    or using numpy:

    xs = numpy.arange(xmin, xmax + 0.5*h, h)

    Context: Octopus can write text-based data files which contain only data
    for the grid points at which a calculation has been carried out. Other grid
    points are not written to the data file, so we have the challenge here of
    reconstructing the grid.
    """

    # expect input data to be 1d
    assert len(xs.shape) == 1

    xmax = xs.max()
    xmin = xs.min()
    # here we make the assumption that the distance between the closest two
    # mesh points we can find is the correct grid spacing
    h = np.diff(np.unique(xs)).min()

    return xmin, xmax, h


def regular_grid_from_positions(xs: np.array) -> np.array:
    """Given a set of positions (in 1d) distributed on a regular grid of
    positions, identify the regular spacing, and return a vector which contains
    the missing positions (if any) together with the positions provided in xs.

    Example:

    >>> regular_grid_from_positions(np.array([0, 1, 2, 4])) -> np.array([0, 1, 2, 3, 4])

    In the process, we will return the exact numbers that are provided in xs,
    and only compute the others. See test_regular_grid_from_positions for more
    details on this.

    """

    xu = list(np.unique(xs))

    xmin, xmax, h = identify_regular_grid(xs)

    # number of data points
    n = round((xmax - xmin) / h + 1)

    # Go through all expected data points from xmin to xmax. If any of those
    # points was given in the input xs, then use that floating point number,
    # otherwise compute one.

    res = []
    for i in range(n):
        approx_pos = xmin + i * h
        # check if this value is present in the list
        if np.isclose(xu[0], approx_pos, atol=h / 100):
            # this data point is in the set already, use it
            res.append(xu.pop(0))
        else:
            # use the approximate position
            res.append(approx_pos)

    # Performance comment: we a use a loop over lists here for algorithmic
    # clarity. The effort is moderate as we only need to do this on 1d
    # data sets.

    # sanity checks: have we used all values in the input data set
    assert len(xu) == 0
    # are min and max as expected
    assert res[0] == xmin
    assert res[-1] == xmax

    return np.array(res)


def check_avail_memory(load_size: int) -> bool:
    """
    Can a number of bytes (`load_size`) safely be allocated or might the system run out
    of memory?
    Note: *might* - for some file types we use estimates, as they are larger on the FS
    than in memory (e. g. "cube").

    Parameters
    ----------
    load_size : int
        number of bytes that shall be allocated.

    Returns
    -------
    bool
        Is more memory available than we try to allocate?

    """
    return load_size < psutil.virtual_memory().available


def parser_log_retrieve_value(
    path: Path,
    key: str,
    conversion: Callable = None,
    ignore_comment: bool = True,
):
    """Scan `parser.log` file at path `path` for entries
    of the type "key = value", and return value.

    For "MaxwellTDOutput = 262153", the key is "MaxwellTDOutput" and the value
    is "262153".

    If the 'matrix format' is used, invidivdual lines can be retrieved:

    For "Maxwell.Lsize[0][0] = 50", the key is "Maxwell.Lsize[0][0]" and the
    value is "50".

    If keys exist more than once, report the value from the first matching line
    found.

    If a "key = value" line contains " # default" at the end of the line, this
    is ignored (unless the optional argument `ignore_comment=False` is used).


    Parameters
    ----------

    path : pathlib object
        path to `parser.log` file

    key : str
        key for which we are trying to retrieve the value

    conversion: Callable object
        The datatype of the returned value

    ignore_comment : bool
        If true (default), remove anything starting with "#"
        to the right of the value. If false, include the string.

    Returns
    -------

    str, int, float, Any
        value - possibly converted using user conversion function

        Return value as string if `conversion=None`.

        To convert the value string to an integer use `conversion=int`, and to
        a float use `conversion=float`.


    Example
    -------

    Example entry that we can parse and return:
    "MaxwellTDOutput = 262153"

    >>> parser_log_retrieve_value(path_to_parser_log_file,
                                  "MaxwellTDOutput", conversion=int)
    262153

    """

    with open(path, "tr", encoding="utf8") as f:
        lines = f.readlines()

    for line in lines:
        # only care about lines that contain "=":
        if "=" not in line:
            continue

        # attempt to split at "=" sign to identify key on the left
        left = line.split("=")[0]
        right = "=".join(line.split("=")[1:])

        if left.strip() == key:
            # Start processing line with format [key] "=" [value]
            # Look for "="
            if "=" in line:
                # focus on right-hand side to get value for key
                # chop off white space on left and right
                raw = right.strip()
            else:
                msg = f"This should be impossible. Looking for key={key} in "
                msg += f"line={line} and did not find '='."
                raise ValueError(msg)

            # If the line has a comment, such as:
            #   "SymmetriesCompute = 1		# default"
            # we may need to strip this off:
            if ignore_comment:
                raw = raw.split("#")[0]

                # remove remaining white space
                raw = raw.strip()

            if conversion is None:
                value = raw
            else:
                # attempt to convert to float
                try:
                    value = conversion(raw)
                except ValueError:
                    print(
                        f"Couldn't convert the value in line={line}"
                        + f"using conversion={conversion}."
                    )
                    raise
            return value

    # reached end of file, and have not found key
    raise ValueError(f"Couldn't find key='{key}' in '{path}'.")
