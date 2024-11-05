import numpy as np
import pytest
import xarray as xr

from postopus.datacontainers.util.lazy_xarray import (
    make_lazy_backend_array,
)
from postopus.files.file import File


class FakeFile(File):
    def __init__(self, dims, coords, values, units=None):
        self._values = values
        self._coords = coords
        self._dims = dims
        self._units = units

    def _readfile(self):
        pass


class FailingFile(File):
    def _readfile(self):
        assert False


L = 20
N = 10
FILE_COORDS = {
    "x": list(np.linspace(0, 3, L)),
    "y": list(np.linspace(0, 3, N)),
    "z": list(np.linspace(-1, 1, N)),
}
FILE_DIMS = list(FILE_COORDS.keys())
VALUE_BASE = np.linspace(-10, 10, L * N * N)
VALUE_BASE.shape = (L, N, N)


# Set the scope to `function` to avoid that one test loads the complete lazy array
# and the next test does not test anything because everything is loaded already.
@pytest.fixture(scope="function")
def testarrays():
    a_list = [10, 20, 30, 40, 50]
    b_list = ["foo", "bar"]
    global_coords = {"a": a_list, "b": b_list}

    files = dict()
    offset = 0
    for a in a_list:
        for b in b_list:
            key_pair = (a, b)
            files[key_pair] = FakeFile(FILE_DIMS, FILE_COORDS, VALUE_BASE + offset)
            offset += 10

    # Create a lazy array as well as a normal array for comparison
    shape = (len(a_list), len(b_list), L, N, N)
    dims = ["a", "b"] + FILE_DIMS
    coords = global_coords | FILE_COORDS
    lazy_backend_array = make_lazy_backend_array(
        shape=shape,
        dims=dims,
        global_dim_count=len(global_coords),
        coords=coords,
        coord_file_map=files,
        dtype=VALUE_BASE.dtype,
    )
    lazy = xr.DataArray(lazy_backend_array, coords=coords, dims=dims, name="lazy")

    data = np.empty(shape=shape, dtype=VALUE_BASE.dtype)
    for i, a in enumerate(a_list):
        for j, b in enumerate(b_list):
            data[i, j] = files[(a, b)].values
    diligent = xr.DataArray(data, coords=coords, dims=dims, name="diligent")

    return (lazy, diligent)


@pytest.fixture
def lazy(testarrays):
    return testarrays[0]


@pytest.fixture
def diligent(testarrays):
    return testarrays[1]


def compare_arrays(lazy, diligent, idx=None):
    if idx is not None:
        diligent = diligent[idx]
        lazy = lazy[idx]

    # Note that lazy.shape is managed `xr.core.indexing.LazilyIndexedArray`
    # but lazy.values.shape by the LazyBackendArray of postopus.
    # Therefore make sure that both shapes are correct.
    assert lazy.shape == lazy.values.shape == diligent.shape
    assert lazy.equals(diligent)


def test_full_access(lazy, diligent):
    compare_arrays(lazy, diligent)


@pytest.mark.skip(
    reason="""Fails due to a bug in xarray (see https://github.com/pydata/xarray/issues/9075).
    The lazy array uses `xarray.core.indexing.explicit_indexing_adapter` which translates
    any by xarray supported index to an more simpler index supperted by the own backend.
    To optimize access the `explicit_indexing_adapter` method scans the key including calls
    of min/max which fails on an empty list. This results in `lazy[[]]` raising exceptions
    deep inside the xarray implementation.
    """
)
def test_empty_access(lazy, diligent):
    compare_arrays(lazy, diligent, [])
    compare_arrays(lazy, diligent, ())


@pytest.mark.parametrize("idx", [0, (0,), -2, (0, 0), (1, -1), (1, -1, 3, 4, 5)])
def test_simple_indexing(lazy, diligent, idx):
    compare_arrays(lazy, diligent, idx=idx)


@pytest.mark.parametrize(
    "idx",
    [
        slice(0, 3),
        (0, 0, 0, 0, slice(None, None, -1)),
        (0, slice(None, None, -1), 0, 0, 0),
        (0, 0, 0, slice(None, None, 2), 0),
        (0, 0, 0, 0, slice(0, 3)),
        (slice(0, 3), slice(0, 3), slice(2, 4), slice(3, 6), slice(0, 3)),
        slice(0, 0),
        tuple(slice(0, 0) for _ in range(5)),
    ],
)
def test_slicing(lazy, diligent, idx):
    compare_arrays(lazy, diligent, idx=idx)


def test_outer_indexing(lazy, diligent):
    """Test if accessing with list of values is possible
    (as in https://docs.xarray.dev/en/latest/user-guide/indexing.html#vectorized-indexing).
    """
    compare_arrays(lazy, diligent, idx=([0, 1, 3], [0, 1], [0, 4]))


def test_where(lazy, diligent):
    a = lazy.where(lazy > 0, drop=True)
    b = diligent.where(diligent > 0, drop=True)

    compare_arrays(a, b)


def test_assure_outer_indexing():
    """Test not only, that outer indexing is supported but also
    implemented internally and not only using `explicit_indexing_adapter`
    of xarray. Otherwise there might be situations where only a few files
    are indexed but all files are loaded.
    E.g when accessing `arr.isel(a=[0, 9])` and only basic indexing is supported
    the indexing adapter translates the key `[0, 9]` to `slice(0, 10)` which
    results in loading also file with a in [1, 2, 3, ..., 9].
    """
    # Setup the array
    n = 10
    a_list = [i * 10 for i in range(n)]
    global_coords = {"a": a_list}

    # Put valid files at the start and the end of the array but fill the rest
    # with files which will raise an exception when accessed.

    files = dict()
    files[(a_list[0],)] = FakeFile(FILE_DIMS, FILE_COORDS, VALUE_BASE)
    files[(a_list[-1],)] = FakeFile(FILE_DIMS, FILE_COORDS, VALUE_BASE)
    for a in a_list[1:-1]:
        files[(a,)] = FailingFile()

    shape = (len(a_list), L, N, N)
    dims = ["a"] + FILE_DIMS
    coords = global_coords | FILE_COORDS
    lazy_backend_array = make_lazy_backend_array(
        shape=shape,
        dims=dims,
        global_dim_count=len(global_coords),
        coords=coords,
        coord_file_map=files,
        dtype=VALUE_BASE.dtype,
    )
    lazy = xr.DataArray(lazy_backend_array, coords=coords, dims=dims, name="lazy")

    # Do the actual test
    lazy.isel(a=[0, n - 1]).values
