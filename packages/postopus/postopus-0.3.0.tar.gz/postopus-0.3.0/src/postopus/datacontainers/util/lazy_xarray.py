from __future__ import annotations

import itertools
import logging

import numpy as np
import xarray as xr
from numpy.typing import ArrayLike

from postopus.files.file import File

Shape = tuple[int]
Dim = str
Dims = list[Dim]
Coords = dict[Dim:ArrayLike]
CoordFileMap = dict[tuple:File]

logger = logging.Logger(__name__)


class LazyBackendArray(xr.backends.BackendArray):
    """Implementation of a xarray backend array to provide a lazy access on octopus files,
    following https://docs.xarray.dev/en/latest/internals/how-to-add-new-backend.html#rst-lazy-loading.

    The goal is to provide all octopus iterations in a single
    xarray without having to wait ages for the data and explode the memory.

    It is suggested to use the backend in combination with `xr.core.indexing.LazilyIndexedArray`.
    Otherwise the files are loaded after the first index access.
    (When doing `arr[1][3].values` without `LazilyIndexedArray` the files are accessed already
    at `arr[1]` loading all files of the second dimension.
    With `LazilyIndexedArray` the files are only loaded when `.values` is used
    (or any other function which requires the values like min, max, +, -, *, /, ...)).

    Similar to "normal" xarrays the dimensions, coordinates, shape and data type has to be provided.
    Additionally, a map has to be given which defines what file corresponds to which coordinate.
    E.g. when the coordinates are:
    .. code-block:: python
        {
            "step": [5, 10, 15],
            "st": [1, 2],
            "x": [0.0, 0.1, 0.2],
            "y": [0.0, 0.1, 0.2],
            "z": [0.0, 0.1, 0.2],
        }

    the map has to yield `File("output_iter/scf.000015/wf-st0001.vtk")`
    when accessing `coord_file_map[(15, 1)]`.
    As `x/y/z` are not relevant in the file lookup here (as they are provided inside of each file),
    `global_dim_count=2` has to be passed here when initializing the lazy array. It as also mandatory,
    that the file dependent dimensions are the last entries in the dimension array
    (so `["step", "x", "y", "z", "st"]` would not work, valid is `["step",  "st", "x", "y", "z"]`).
    """

    def __init__(
        self,
        shape: Shape,
        coords: Coords,
        dims: Dims,
        coord_file_map: CoordFileMap,
        dtype,
        global_dim_count: int,
    ):
        self.shape = shape
        # Work with np arrays internally to simplify outer indexing.
        self.coords = dict()
        for dim, values in coords.items():
            # Check for munti index, e.g. when step is passed as `("t", [1, 2, 3])`
            if isinstance(values, tuple):
                values = values[1]
            self.coords[dim] = np.array(values)
        self.dims = dims
        self.dtype = dtype

        self.coord_file_map = coord_file_map
        self.number_of_global_dims = global_dim_count
        self.number_of_file_dims = len(dims) - global_dim_count

    def __getitem__(self, key):
        # For details check https://docs.xarray.dev/en/latest/internals/how-to-add-new-backend.html#backendarray-subclassing
        return xr.core.indexing.explicit_indexing_adapter(
            key,
            self.shape,
            xr.core.indexing.IndexingSupport.OUTER_1VECTOR,
            self._raw_indexing_method,
        )

    def _raw_indexing_method(self, key: tuple[int | slice, list[int]]):
        """Do the actual index access.

        Using xr.core.indexing.explicit_indexing_adapter will convert any
        possible complex index to a more simpler one. E.g. if
        xr.core.indexing.IndexingSupport.BASIC is used but for the access on
        the array a list of values is used the key will be
        converted to a slice - `array[1, 2, 5]` becomes internally
        `array[slice(1, 6)]`. In this example this means that the values
        relating to index 3 and 4 are loaded but thrown away but xarray
        later in the process!

        Using IndexingSupport.BASIC would therefor result in loading all
        iterations of Octopus even if only the first and last iteration
        is requested. To avoid this, we support at least
        IndexingSupport.OUTER_1VECTOR (one list of values is allowed,
        all other lists are still converted to slices). Implementing
        IndexingSupport.OUTER or even IndexingSupport.VECTORIZED would be
        more optimal, but an other index than the iteration step is rare
        and limited to a few values.

        See also:
        https://docs.xarray.dev/en/latest/generated/xarray.core.indexing.OuterIndexer.html#xarray.core.indexing.OuterIndexer
        https://docs.xarray.dev/en/latest/user-guide/indexing.html
        """

        logger.debug("Loading key %s", key)
        # Translate the given key to the corresponding coordinates.
        # If e.g. the first dimension is step with coordinates [5, 10, 15, 20]
        # and `key[0]` yields `slice(1, 3)` load `sliced_coords["step"] = [10, 15]`.
        sliced_coords = dict()
        for s, dim in zip(key, self.dims):
            if isinstance(s, int):
                # Plain integer keys should be wrapped in list to,
                # e.g. `sliced_coords["step"] = [5]`, not `sliced_coords["step"] = 5`.
                sliced_coords[dim] = [self.coords[dim][s]]
            else:
                sliced_coords[dim] = self.coords[dim][s]

        # Prepare the partial array which should be loaded.
        # Note that at this point we treet the shape slightly wrong:
        # Let x.shape be (5, 20, 30). When accessing `x[3, 0:5, 7]` the returned shape
        # woulde be (5,) but at this point working with the shape (1, 5, 1) is simpler.
        # The transformation to (5,) is done at the end.
        partial_shape = tuple(len(sliced_coords[dim]) for dim in self.dims)
        data = np.full(shape=partial_shape, fill_value=np.nan, dtype=self.dtype)

        # Load the requested files.
        # E.g. if dim1=[1, 2], dim2=[5, 10] is requested we have to load all 4 combinations:
        # load_file(dim1=1, dim2=5),  load_file(dim1=2, dim2=5),
        # load_file(dim1=1, dim2=10), load_file(dim1=2, dim2=10).
        ranges = [range(n) for n in partial_shape[: self.number_of_global_dims]]
        # If file dimensions are selected, e.g. the 'x' coordinate,
        # still the whole file has to be loaded and the array per file
        # has to be sliced.
        per_file_slice = key[self.number_of_global_dims :]
        # Wrap int indices in a list.
        per_file_slice = tuple(
            s if isinstance(s, slice) else [s] for s in per_file_slice
        )
        for t in itertools.product(*ranges):
            # Get all relevant coordinate values to find the correct file.
            file_coords = list()
            for dim_name, coord_value in zip(self.dims, t):
                file_coords.append(sliced_coords[dim_name][coord_value])
            file_coords = tuple(file_coords)
            # Access the data of the file
            file = self.coord_file_map[file_coords]
            values = file.values
            sliced_values = values[per_file_slice]
            # In numpy the shape after indexing is different from xarray,
            # but as we only add `1` to the shape we can simply overwrite it.
            # E.g. nparray[3, 0:5, 7] yields the shape (5,) but we want
            # to work with (1, 5, 1).
            sliced_values.shape = data[t].shape
            data[t] = sliced_values

        # Squeeze axis which are only selected as int, not as slice
        # (converting the shape from (1, 5, 1,) back to (5,)).
        # Do not use builtin squeeze as this also drops dims
        # where the given slice only slices a single value (e.g. array[0:1]).
        final_shape = []
        for s, dim in zip(key, self.dims):
            if not isinstance(s, int):
                dim_coords = self.coords[dim]
                selected = dim_coords[s]
                final_shape.append(len(selected))
        final_shape = tuple(final_shape)
        data.shape = final_shape

        return data


def make_lazy_backend_array(
    shape: tuple[int],
    dims: Dims,
    global_dim_count: int,
    coords: Coords,
    coord_file_map: CoordFileMap,
    dtype,
):
    """Construct a lazy loadable array
    (wrapped with `xr.core.indexing.LazilyIndexedArray`).
    Check `LazyBackendArray` for details.
    """
    backend_array = LazyBackendArray(
        shape,
        coords=coords,
        dims=dims,
        coord_file_map=coord_file_map,
        dtype=dtype,
        global_dim_count=global_dim_count,
    )

    data = xr.core.indexing.LazilyIndexedArray(backend_array)
    return data
