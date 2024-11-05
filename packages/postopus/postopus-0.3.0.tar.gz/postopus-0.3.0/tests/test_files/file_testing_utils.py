#################################################################################
# Helper Methods for text_read_test.py and testing TextFile class
#################################################################################
import itertools

import numpy as np


def create_test_data(colnames):
    """
    Create test data for creating a line, a square or a cube.

    If a rectangle or parallelpiped is wanted instead for whatever reason the
    whole function should be changed

    Each dimension has per default two coordinate values: min_square and max_square.
    These define the length (max - min) of the dimension. Right now the length is
    10, chosen arbitrarily.

    These dimensions will be used in the build_header_tempfile() function to build a
    line, square, or cube with corresponding field values. Since each of the
    dimensions has only two points we need to multiply two by the number of
    dimensions that the final test shape will have to obtain the number of
    needed field values.

    For example, if the test shape is a square (2D, xy-plane)
    we would need 2**2 = 4 field values,
    each one for all the possible combinations between the defined coords.
    In this case between the two values of x and the two values of y.

    :param colnames: names of the columns in the created test-file

    :return: defined_coords: list of lists. Each sublist has the defined points for
             one dimension
             field_vals: np array
    """
    # if a square (or cube) is not wanted for whatever reason this should be changed
    min_square = float(-5)
    max_square = float(5)
    # Assuming there is 1 field value column, if there are more this should be
    # changed
    n_of_val_cols = 1

    n_dims = len(colnames) - n_of_val_cols
    defined_coords = [[min_square, max_square] for _ in range(n_dims)]
    n_possible_coords_comb = 2**n_dims
    field_vals = np.random.random((n_possible_coords_comb,))
    return defined_coords, field_vals


# TODO: Test missing to check if the right data is
#  in the right position in the value array, give data as a parameter
#  in a list form for example. Hans & Kevin 22.11.21
def build_header_tempfile(tmp_file, colnames):
    result = "#         "
    spacing = "                     "
    # Build a string with all elements from colnames and spacing
    for name in colnames:
        result += name + spacing
    # remove last spacing
    with open(tmp_file, "a+") as fil:
        fil.write(result[:-21] + "\n")

    invalid_headers = ["#", "Im"]
    colnames = [colname for colname in colnames if colname not in invalid_headers]

    defined_coords, field_vals = create_test_data(colnames)

    # write test data to file
    for coords, val in zip(itertools.product(*defined_coords), field_vals):
        coords_str = " ".join(map(str, coords))
        with open(tmp_file, "a+") as fil:
            fil.write(f"{coords_str} {str(val)}\n")
    return tmp_file
