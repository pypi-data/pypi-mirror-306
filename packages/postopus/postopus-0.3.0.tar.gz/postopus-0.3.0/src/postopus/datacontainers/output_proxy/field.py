from __future__ import annotations

import warnings
from collections import namedtuple
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
import xarray as xr

from postopus.files import VTKFile, openfile, parsable_sources
from postopus.files.file import File
from postopus.output_collector import STATIC_ITERNUM, VectorDimension
from postopus.utils import parser_log_retrieve_value

from ..util.lazy_xarray import make_lazy_backend_array
from ..util.units import update_units

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator
    from typing import TypeVar

    from numpy.typing import ArrayLike

    from postopus.output_collector import OutputField

    from ..util.lazy_xarray import CoordFileMap, Coords, Dims

    A = TypeVar("A")

from ._base import OutputProxy


def _first(it: Iterable[A]) -> A | None:
    return next(iter(it), None)


_STEP_DIM = "step"
_TIME_DIM = "t"


class _VTKFileComponentProxy(File):
    """File proxy to only access specific components of a vtk file,
    e.g. only the x compontent.
    """

    def __init__(self, orig_file: File, component: int):
        self._orig_file = orig_file
        self._component = component

    def _readfile(self):
        self._dims = self._orig_file.dims
        self._coords = self._orig_file.coords
        self._units = self._orig_file.units
        self._values = self._orig_file.values[self._component]


class FieldOutput(OutputProxy):
    """Proxy for Scalar and vector fields.
    Calling the object returns a xarray DataArray (for scalars) or a Dataset (for vectors).

    The given array provides all dimsions given by the files (e.g. all iteration steps).
    The values of the array are accessed lazy to avoid any performance issues.

    To get the data the proxy has to be called with the desired source, like
    `data = run.default.td.density(".ncdf")`.
    For a vector the vector compenents are `vx`, `vy` and `vz` (as `x/y/z` refers to the
    spatial coordinats).
    """

    @classmethod
    def _match(self, output: OutputField):
        """Consider all outputs in run/output_iter as scalar or vector fields
        (there is no counter example to that assumption yet).
        """
        return output.has_iterations()

    def __post_init__(self):
        self._example_file_per_src: dict[str, File] = dict()

    def __repr__(self) -> str:
        return "\n".join(self._repr_gen())

    def _repr_gen(self) -> Iterator[str]:
        yield f"{self.__class__.__name__}(name={self._output_field.field!r}):"

        yield "Available sources:"
        for src in sorted(self._get_available_sources()):
            yield f"    {src!r}"

    def _is_td(self) -> bool:
        return self._parent.mode == "td"

    def _get_td_step_size(self) -> float:
        assert self._is_td()

        system = self._parent.parent
        run = system.parent
        path_to_parser_log_file = Path(f"{run.path}/exec/parser.log")

        try:
            sysname = system.systemname
            timestep_key = f"{sysname}.TDTimeStep"
            timestep = parser_log_retrieve_value(
                path_to_parser_log_file, timestep_key, conversion=float
            )
        except ValueError:
            timestep = parser_log_retrieve_value(
                path_to_parser_log_file, "TDTimeStep", conversion=float
            )

        return timestep

    def _load_global_dims(self) -> tuple[Dims, Coords]:
        """Get the dimensions/coordinats accross the different output files.

        These do not include the dimensions each file provides (mainly x/y/z)
        but the dimensions which separates the file, for example:
        - the calculation step from the iteration folder name as in
            `output_iter/td.000010` or `output_iter/td.000020`
            (yielding `{"step": [10, 20]}`)
        - the state of a wave function as in `wf-st0001.vtk` or `wf-st0002.vtk`
            (yielding `{"st": [1, 2]}`)

        The first dimension is always the iteration id ('step').
        Further dimensions are defined be the OtherIndex provided
        by the output collector.

        The output provided by the output collector is stuctured
        either as
            iterations->files,
            e.g. `output.iterations[step].files`
        or as
            iterations->other_index->files,
            e.g. `output.iterations[step].other_index[idx].files`.
        There is (currently) no nesting of other_index, e.g.
        `output.iterations[step].other_index[idx_a].other_index[idx_a].files`
        and output always begins with iterations.
        """
        field = self._output_field

        steps = np.array(
            [
                self._get_static_itnum() if step is STATIC_ITERNUM else step
                for step in field.iterations
            ]
        )
        assert len(steps) > 0

        any_it = field.iterations.get_any()
        # The Vector dimension index is handled by using an
        # Dataset with the vector dimensions as variables and
        # therefore not treated as ordinary index here.
        if isinstance((k := _first(any_it.other_index.keys())), VectorDimension):
            any_it = any_it.other_index[k]

        if any_it.has_other_index():
            any_other_index = _first(any_it.other_index.keys())

            # Freeze order of additional dimensions
            any_other_index_coords = any_other_index.get_coordinates()
            dim_names = set(any_other_index_coords.keys())

            # collect dimension values
            dim_values: dict[str, set] = dict()
            for other_index in field.all_other_index():
                coords = other_index.get_coordinates()
                assert coords.keys() == dim_names
                for dim_name, dim_value in coords.items():
                    dim_values.setdefault(dim_name, set()).add(dim_value)
        else:
            dim_names = []

        # Sort dim names and values.
        # Use "step" as first dimension
        # (even for time dependent runs, the transition from step to t
        # as the dimension happens at a later point).
        dim_names_sorted = [_STEP_DIM] + sorted(dim_names)
        coords: dict[str, ArrayLike] = dict()
        for dim_name in dim_names:
            coords[dim_name] = np.array(sorted(dim_values[dim_name]))
        coords[_STEP_DIM] = np.array(sorted(steps))

        return dim_names_sorted, coords

    def _get_example_file(self, source: str) -> File:
        """Provide an example file for the given source.
        This could be any file of any iteration/other_index.
        """
        if source not in self._example_file_per_src:
            output = self._get_output_files()
            file = output.files.with_extension(source)
            self._example_file_per_src[source] = openfile(file)

        return self._example_file_per_src[source]

    def _get_available_sources(self) -> set[str]:
        output = self._get_output_files()
        return output.files.extensions

    def _get_auto_source(self) -> str:
        """Provide a default source if no source was provided.
        There is no real ranking what is the best source provided
        by Octopus so we only give a valid default if only one source
        if available.
        """
        src = self._get_available_sources()
        if len(src) != 1:
            raise ValueError(
                "There is more than one source available."
                " The source parameter can only be ommited if there"
                f" is only one source available. The available sources are {list(src)}"
            )
        return _first(src)

    @property
    def _has_static_data(self) -> bool:
        """Check if the field has a data file in the `run/static` folder."""
        return (
            self._parent.mode == "scf"
            and STATIC_ITERNUM in self._output_field.iterations
        )

    def _is_vector(self) -> bool:
        """Check if the field provides more than one component."""
        return isinstance(
            _first(self._output_field.iterations.get_any().other_index),
            VectorDimension,
        )

    def _get_static_itnum(self) -> int | None:
        """Get the step at which the scf calculation has stopped.
        This step number is used to provide files found in 'static/'
        (only relevant for fields of calculation mode 'scf').

        As default use the information given in 'static/convergence'.
        If that file is not present try do guess the step.
        E.g. if the given steps are [5, 10, 15] the result has converged
        between step 16 and 20 so 20 is used as the upper bound.
        """
        if hasattr(self._parent, "convergence"):
            return int(self._parent.convergence().index[-1])

        steps = set(self._output_field.iterations.keys())
        steps.discard(STATIC_ITERNUM)

        warnings.warn(
            "It was not possible to determine at which step the simulation has stopped. The correct id will be guessed based on the step size and is propably incorrect."
        )

        if len(steps) == 0:
            return 1

        return max(steps) + min(steps)

    def _make_coord_file_map(
        self,
        global_dims: Dims,
        global_coords: Coords,
        source: str,
        additional_index: VectorDimension | None = None,
    ) -> CoordFileMap:
        """Create a mapping of coordinates to the corresponing file.
        The mapping consists of a named tuple for the coordinats as key
        and the file object as value.

        An entry in the mapping could look like
        `{(step=42, st=19): File("output_iter/td.000042/wf-st0019.vtk")`
        """
        # If this is a time dependent run the provided index is the time
        # but the files are stored using the step id. A mapping between those is
        # required. (Different from the result of _load_global_dims the time
        # coordinates have to be provided for td mode).
        # Note that if this is not a time dependent run the mapping is
        # the identity (`step_to_step_or_time_lookup[x] is x`).
        step_or_time_dim = global_dims[0]
        steps = global_coords[_STEP_DIM]
        steps_or_times = global_coords[step_or_time_dim]
        step_to_step_or_time_lookup = {
            step: step_or_time for step, step_or_time in zip(steps, steps_or_times)
        }

        GlobalCoordPair = namedtuple("GlobalCoordPair", global_dims)
        coord_file_map = dict()

        for itnum, iteration in self._output_field.iterations.items():
            if itnum is STATIC_ITERNUM:
                itnum = self._get_static_itnum()
            step_or_time = step_to_step_or_time_lookup[itnum]
            output_files = iteration
            if additional_index:
                output_files = output_files.other_index[additional_index]
            if output_files.has_other_index():
                for idx, other_index in output_files.other_index.items():
                    other_index_coords = idx.get_coordinates()
                    other_index_coords[step_or_time_dim] = step_or_time
                    key = GlobalCoordPair(**other_index_coords)
                    assert key not in coord_file_map
                    file = other_index.files.with_extension(source)
                    coord_file_map[key] = openfile(file)
            else:
                file = output_files.files.with_extension(source)
                other_index_coords = {step_or_time_dim: step_or_time}
                key = GlobalCoordPair(**other_index_coords)
                coord_file_map[key] = openfile(file)

        # Special handling for vtk:
        # As the vtk file contains all vector components we need a proxy to assure the
        # lazy array uses the correct part.
        if additional_index and source in VTKFile.EXTENSIONS:
            component_number = [VectorDimension(d) for d in "xyz"].index(
                additional_index
            )
            for key in coord_file_map.keys():
                coord_file_map[key] = _VTKFileComponentProxy(
                    coord_file_map[key], component_number
                )

        return coord_file_map

    def _make_lazy_array(self, source: str):
        global_dims, global_coords = self._load_global_dims()
        steps = global_coords[_STEP_DIM]

        # Switch to time instead of step if this is a time dependent run.
        if self._is_td():
            td_step_size = self._get_td_step_size()
            time_steps = steps * td_step_size
            global_coords[_TIME_DIM] = time_steps
            global_dims[0] = _TIME_DIM

        # Build a lazy loadable xarray.
        # Therefor we need the shape/dims/coordinats
        # as well as a map between the coordinats and the corresponding file
        # (e.g. step=5, st=3 corresponds to the
        # file output_iter/scf.0005/wf-st0003.ncdf).
        example_file = self._get_example_file(source)
        file_dims = list(example_file.dims)
        file_coords = example_file.coords
        # We handle the component separatly (relevant for .vtk files)
        if "component" in file_coords:
            del file_coords["component"]
        if "component" in file_dims:
            file_dims.remove("component")

        dims = global_dims + file_dims
        coords = global_coords | file_coords
        assert len(coords) == len(global_coords) + len(file_coords)

        shape = tuple(len(coords[dim]) for dim in dims)

        # For time dependent provide `step` as an additional reference.
        if self._is_td():
            coords[_STEP_DIM] = (_TIME_DIM, coords[_STEP_DIM])

        # For vectors build a data set with components vx, vy, vz.
        # For scalarfields a data array is sufficient.
        if self._is_vector():
            # For a data set, build a lazy array for each vector component.
            vector_dims = self._output_field.iterations.get_any().other_index.keys()
            xarrays = dict()
            for vector_dim in vector_dims:
                coord_file_map = self._make_coord_file_map(
                    global_dims, global_coords, source, additional_index=vector_dim
                )

                data = make_lazy_backend_array(
                    shape=shape,
                    dims=dims,
                    global_dim_count=len(global_dims),
                    coords=coords,
                    coord_file_map=coord_file_map,
                    dtype=example_file.values.dtype,
                )

                xarrays[f"v{vector_dim.dim}"] = (dims, data)

            xarr = xr.Dataset(data_vars=xarrays, coords=coords)

        else:
            coord_file_map = self._make_coord_file_map(
                global_dims, global_coords, source
            )
            data = make_lazy_backend_array(
                shape=shape,
                dims=dims,
                global_dim_count=len(global_dims),
                coords=coords,
                coord_file_map=coord_file_map,
                dtype=example_file.values.dtype,
            )
            xarr = xr.DataArray(
                data, coords=coords, dims=dims, name=self._output_field.field
            )

        update_units(xarr, example_file)
        return xarr

    def _validate_source(self, source: str) -> None:
        """Check if the given source is valid.

        The source is considered valid if:
        - files with the given source exist
        - a parser is implemented for the given source.
        """
        # Check if the source is available
        if source not in self._get_available_sources():
            raise ValueError(
                f"We did not find any '*{source}' files \n"
                f"Available sources: \n"
                f"{self.available_sources}"
            )

        # Check if the source is parsable
        if source not in parsable_sources:
            output = self._get_output_files()
            file = output.files.with_extension(source)
            raise NotImplementedError(
                f"Existing file '{file}' found,"
                f" but no parser is implemented for the extension."
                f" Contact us if you need it! \n"
                f"Known extensions: {parsable_sources}"
            )

    def _check_consistency(self):
        """Check if for the output there are any missing iterations.
        This could happen if single files inside of an iteration are missing,
        a whole iteration step is missing or if multiple runs with different
        input files happened in the same directory.
        """
        steps = np.array(
            [
                step
                for step in self._output_field.iterations
                if step is not STATIC_ITERNUM
            ]
        )
        step_size = np.diff(np.sort(steps))
        if len(set(step_size)) > 1:
            warnings.warn(
                "Your data might have missing simulation steps. Distance "
                "between all steps is not consistent. Still loading "
                "your data."
            )

    def __call__(self, source: str | None = None) -> xr.DataArray | xr.Dataset:
        """Provide the data as a lazy loaded xarray DataArray or Dataset."""
        if source is None:
            source = self._get_auto_source()

        if not source.startswith("."):
            source = "." + source

        self._validate_source(source)
        self._check_consistency()

        return self._make_lazy_array(source)

    @property
    def available_sources(self) -> list[str]:
        """List the available sources usable to load the data."""
        return sorted(self._get_available_sources())
