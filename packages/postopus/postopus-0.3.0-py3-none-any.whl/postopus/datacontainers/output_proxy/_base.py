from __future__ import annotations

import abc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

    from postopus.output_collector import FieldFiles, OutputField

    from . import CalculationModes


class OutputProxy(abc.ABC):
    """Base class to wrap outputs of Octopus.

    To access the data of an output the output proxy has to be called:

    >>> from pospotus import Run
    >>> run = Run("path/to/octopusdata")
    >>> convergence_data = run.default.scf.convergence()

    As the data provided by Octopus is very diverse the interface of the
    output proxy depends on the accessed output. E.g. for "density" (or any
    other output in the output_iter/ folder) calling the proxy requires the
    source as an additional parameter (``run.default.scf.density('.vtk')``)
    returning an instance of `xarray.DataArray`. An additional attribute
    `available_sources` (``run.default.scf.density.available_sources``) is
    provided in this case. Other outputs like "convergence" is callable
    without any additional parameters and provides a `pandas.Dataframe`.

    It is possible to define the interface for an output by subclassing
    the `OutputProxy`. One way is to define the interface for one specific
    output by defining the attribute `__output__`.
    E.g. to define an own interface for the output 'convergence':

    >>> class ConvergenceProxy(OutputProxy):
    ...     __output__ = "convergence"
    ...     def __call__(self):
    ...         with open(self._available_files[0]) as f:
    ...             return f.readlines()

    To register a more generalized class, one has to define a ``_match`` method.
    This method should return true if for a given field the class is suitable
    and false if not. E.g. the ``_match`` method of the class which handles scalar
    and vector fields returnes True for 'density' but False for 'info' or
    'convergence'.

    >>> class MyOutput(OutputProxy):
    ...     @classmethod
    ...     def _match(cls, output) -> bool:
    ...         return MyOwnIndexVariant() in output.other_index.keys():
    ...     def __call__(self):
    ...         ...

    Finding the correct class for an given output follows the rules:

    1. If a class with the `__output__` attribute is defined and the value
       matches the name of the output that class is used. Defining a new
       class with the same value in `__output__` overwrites the previous class
       (the latest defined class is used).
    2. If no class with a matching `__output__` attribute is found the classes
       defining the `_match` method are considered. If this method returnes
       True for one class this class is used. Here, the classes defined first
       will be checked first.
    3. If no suitable class is found, `DefaultOutputProxy` will be used.
    """

    _output_class_map: dict[str, type[OutputProxy]] = dict()
    """Map of the output name and a class for that specefic output
    (defined by the `__output__` attribute).
    """

    _default_classes: list[type[OutputProxy]] = list()
    """List of proxy classes which are used as a default for a subset
    of outputs (defined by the `_match` method of such a class).
    """

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Check if the class is implemented for a specific output.
        if hasattr(cls, "__output__"):
            cls._output_class_map[cls.__output__] = cls

        # If the class can be used as a default proxy for a range of fields.
        # The _match method has to return True if the class can be used
        # as a proxy for a given OutputField.
        elif hasattr(cls, "_match"):
            cls._default_classes.append(cls)

    def __new__(
        cls,
        parent: CalculationModes,
        output_field: OutputField,
    ) -> OutputProxy:
        load_cls = DefaultOutputProxy

        # Check if any dedicated class exists for that field
        if output_field.field in cls._output_class_map:
            load_cls = cls._output_class_map[output_field.field]

        # Check which of the default proxy classes can be used otherwise.
        else:
            for default_cls in cls._default_classes:
                if default_cls._match(output_field):
                    load_cls = default_cls
                    break

        return abc.ABC.__new__(load_cls)

    def __init__(
        self,
        parent: CalculationModes,
        output_field: OutputField,
    ):
        self._parent = parent
        self._output_field = output_field

        self.__post_init__()

    def __post_init__(self):
        """Gets called at the end of __init__. Prefered place to
        initialize subclass specefic attributes.
        """

    def _get_output_files(self) -> FieldFiles:
        """Get the field files attribute of the output. There is no guarantee
        which of the field files is returned (could be the files of any iteration,
        not necessarily the first).
        """
        output = self._output_field
        # Make sure we terminate (the output collector *should* yield a finite
        # strutcure but a circular reference is not excluded)
        for _ in range(1024):
            while not output.is_static():
                output = output.iterations.get_any() or output.other_index.get_any()
            return output

        raise RuntimeError("Nesting depth exceeded.")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self._output_field.field!r})"

    @abc.abstractmethod
    def __call__(self) -> Any:
        """Return the data provided by the files of the output."""


class DefaultOutputProxy(OutputProxy):
    """Default output proxy if we have no further information about the given files"""

    def __repr__(self) -> str:
        files = self._get_output_files()
        anyfile = next(iter(files))
        return (
            f"Proxy to files like {anyfile}. This kind of file seems unknown "
            "to postopus and no further specialised reading can be provided."
        )

    def __call__(self) -> None:
        raise NotImplementedError("Unknown file type.")
