import numpy as np
import pytest

from postopus.utils import (
    humanise_size,
    identify_regular_grid,
    regular_grid_from_positions,
)


def test_utils_humanise_size():
    h = humanise_size

    assert h(1) == (1.0, "B")
    assert h(2) == (2.0, "B")

    assert h(2000) == (1.953125, "KiB")

    assert h(1023) == (1023.0, "B")
    assert h(1024) == (1.0, "KiB")
    assert h(2**20) == (1.0, "MiB")
    assert h(2**30) == (1.0, "GiB")
    assert h(2**40) == (1.0, "TiB")
    assert h(2**50) == (1.0, "PiB")
    assert h(2**60) == (1.0, "EiB")

    # check prerequisites
    with pytest.raises(ValueError):
        h(-1)

    # check prerequisites
    with pytest.raises(TypeError):
        h("A")

    with pytest.raises(TypeError):
        h(0.5)


def test_identify_regular_grid():
    # trivial example
    i = identify_regular_grid
    xs = np.array([0, 1, 2, 3, 4])
    xmin, xmax, h = i(xs)
    assert (xmin, xmax, h) == (0, 4, 1)
    assert np.arange(xmin, xmax + 0.5 * h, h) == pytest.approx(xs)

    # multiple entries
    xs = np.array([0, 1, 2, 3, 4, 3, 0, 1, 2, 4, 0])
    xmin, xmax, h = i(xs)
    assert (xmin, xmax, h) == (0, 4, 1)
    assert np.arange(xmin, xmax + 0.5 * h, h) == pytest.approx(np.unique(xs))

    # gaps in the coordinates
    xs = np.array([0, 1, 3, 4])
    xmin, xmax, h = i(xs)
    assert (xmin, xmax, h) == (0, 4, 1)
    assert np.arange(xmin, xmax + 0.5 * h, h) == pytest.approx([0, 1, 2, 3, 4])

    # floats, and xmin not 0
    xs = np.array([10.1, 10.2, 10.3, 10.7])
    xmin, xmax, h = i(xs)
    assert (xmin, xmax, h) == pytest.approx([10.1, 10.7, 0.1])
    assert np.arange(xmin, xmax + 0.5 * h, h) == pytest.approx(
        [10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7]
    )

    # negative values in coordinates
    xs = np.array([-2, 0, 1, 3])
    xmin, xmax, h = i(xs)
    assert (xmin, xmax, h) == (-2, 3, 1)
    assert np.arange(xmin, xmax + 0.5 * h, h) == pytest.approx([-2, -1, 0, 1, 2, 3])


def test_regular_grid_from_positions():
    # integer with gap
    xs = np.array([0, 1, 2, 4])
    res = regular_grid_from_positions(xs)
    assert list(res) == [0, 1, 2, 3, 4]
    # use comparison of lists to check exact identify of numbers

    # floats with gap
    xs = np.array([0, 0.5, 1, 2])
    res = regular_grid_from_positions(xs)
    assert list(res) == [0, 0.5, 1, 1.5, 2]  # 1.5 seems to be exact by chance

    # tricky floats with gap - here we check that floats are exactly passed on
    # from the input to the output
    eps0 = 6e-8
    eps2 = -1e-6
    eps3 = 2e-7
    eps5 = -1e-8

    xs = np.array([0 + eps0, 2 + eps2, 3 + eps3, 5 + eps5])
    res = regular_grid_from_positions(xs)
    # for initial positions, we need to get exactly the right value
    assert list(res)[0] == 0 + eps0
    assert list(res)[2:4] == [2 + eps2, 3 + eps3]
    assert list(res)[5] == 5 + eps5

    # check that reconstructed positions are approximately right
    assert list(res)[1] == pytest.approx(1, abs=1e-5)
    assert list(res)[4] == pytest.approx(4, abs=1e-5)
