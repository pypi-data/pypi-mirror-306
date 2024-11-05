from __future__ import annotations

import abc
import re
from typing import TYPE_CHECKING

import attrs

from postopus.files import VTKFile

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path
    from typing import Any, ClassVar

    from .output_collector import FieldName

    MatchResult = (
        tuple[FieldName, OtherIndex] | tuple[FieldName, list[OtherIndex]] | None
    )
    Matcher = Callable[[FieldFileInfo], MatchResult]


@attrs.frozen
class FieldFileInfo:
    """Collection of information which is passed to a field Matcher"""

    path: Path
    """Path to the file. E.g. '/system_path/static/density.z=0'"""

    field_name: str
    """By the output collector assumed field name. This name can be incorrect
    and must be fixed by an OtherIndex in some cases.
    E.g. for the file `current-x.ncdf` the output collector assumed field name
    is `current-x` but is changed to `current` by `VectorDimension` to group
    the file together with `current-y.ncdf` and `current-z.ncdf` in one field.
    """

    extension: str
    """Extension of the file, e.g. '.z=0'."""


class OtherIndex(abc.ABC):
    """
    Base class for indicies of files, e.g. wave function state or vector
    component.

    To define a new variant of an OtherIndex subclassing is sufficient (the
    subclass is registered by using `__init_subclass__`). The subclass has to
    define the methods:
    - `match` to check if the subclass is usable as index for the given
        `FieldFileInfo`.
    - `get_coordinates` to get a dict[dimension_name, coordinate_value] which
        is used to generate a xarray for the field.
    """

    _matcher_classes: ClassVar[dict[str, type]] = dict()
    """Collection of classes used to match a FieldFileInfo.

    As key `f"{cls.__module__}.{cls.__name__}"` is used to support working
    with attrs. The problem here is, that for
    ```
    @attrs.define
    class WFState(OtherIndex):
        ...
    ```
    the method `__init_subclass__` is called twice, first when
    declaring `class WFState(OtherIndex)` but then `@attrs.define`
    creates a new class by copying and modifying attributes of the original
    class. By using `f"{cls.__module__}.{cls.__name__}"` as dict key we simply
    replace the original class with the class declared by `attrs`. (This may
    lead to problems if one defines a class with the same name as an existing
    class if those are additionally defined in a module with the same name by
    accident.)
    """

    def __init_subclass__(cls, /, **kwargs):
        super().__init_subclass__(**kwargs)
        key = f"{cls.__module__}.{cls.__qualname__}"
        cls._matcher_classes[key] = cls

    @classmethod
    def find_match(cls, field_file_info: FieldFileInfo) -> MatchResult:
        """Check if any matcher matches the given field."""
        for match_cls in cls._matcher_classes.values():
            if (match_result := match_cls.match(field_file_info)) is not None:
                return match_result
        return None

    @classmethod
    def regex_match(cls, pattern: str, field_file_info: FieldFileInfo) -> MatchResult:
        """Match a field name with the given pattern."""
        if re_match := re.match(pattern, field_file_info.field_name):
            re_dict = re_match.groupdict()
            field_name = re_dict.pop("field_name")
            indices = cls(**re_dict)
            return (field_name, indices)

    @classmethod
    @abc.abstractmethod
    def match(cls, field_file_info: FieldFileInfo) -> MatchResult:
        """Check if `cls` can be used as an index for the given field file."""

    @abc.abstractmethod
    def get_coordinates(self) -> dict[str, Any]:
        """Provide a dict with the dimension names (keys)
        and the coordinates (values) to define how the index is represented in
        a xarray.
        """


@attrs.frozen
class WFState(OtherIndex):
    """
    Wave function states following Octopus indexing
    """

    st: int = attrs.field(converter=int, validator=attrs.validators.ge(0))
    """State index"""
    k: int | None = attrs.field(
        default=None,
        converter=attrs.converters.optional(int),
        validator=attrs.validators.optional(attrs.validators.ge(0)),
    )
    """K point index"""
    sp: int | None = attrs.field(
        default=None,
        converter=attrs.converters.optional(int),
        validator=attrs.validators.optional(attrs.validators.ge(0)),
    )
    """Spin index"""
    # TODO: Add reference to the system and convert index to actual physical quantities

    pattern: ClassVar[str] = (
        r"(?P<field_name>.*[-_]?wf)"
        r"(?:-st(?P<st>\d+)|-k(?P<k>\d+)|-(?:sp|sd)(?P<sp>\d+))*(?:[-_\.].*)?"
    )

    @classmethod
    def match(cls, field_file_info: FieldFileInfo) -> MatchResult:
        return cls.regex_match(cls.pattern, field_file_info)

    def get_coordinates(self) -> dict[str, int]:
        coords = dict()
        coords["st"] = self.st
        if self.k is not None:
            coords["k"] = self.k
        if self.sp is not None:
            coords["sp"] = self.sp

        return coords


@attrs.frozen
class VectorDimension(OtherIndex):
    """
    Vector field index
    """

    dim: str = attrs.field(validator=attrs.validators.instance_of(str))
    """The dimension of the vector. One of `x`, `y`, `z`"""

    @dim.validator
    def is_dim(self, attribute, value):
        if value not in ("x", "y", "z"):
            raise ValueError(f"Attribute dim={value} is not a valid vector dimension")

    pattern: ClassVar[str] = r"(?P<field_name>.*)[-_](?P<dim>[xyz])(?:[-_\.].*)?"

    @classmethod
    def match(cls, field_file_info: FieldFileInfo) -> MatchResult:
        return cls.vtk_match(field_file_info) or cls.regex_match(
            cls.pattern, field_file_info
        )

    @classmethod
    def vtk_match(cls, field_file_info: FieldFileInfo) -> MatchResult:
        """Check if a .vtk file contains vector components.

        In .vtk files all components of a vector are stored in one file.
        If the given .vtk file provides more than one component it is
        considered as a vector. If there is just one component it is
        considered as a scalar field.
        """
        if field_file_info.extension != ".vtk":
            return
        component_count = VTKFile.get_scalars_count(field_file_info.path)
        if component_count > 1:
            assert component_count <= 3
            field_name = field_file_info.field_name
            other_index = [
                cls(component) for component in ("x", "y", "z")[0 : component_count + 1]
            ]
            return (field_name, other_index)

    def get_coordinates(self) -> dict[str, str]:
        return {"dim": self.dim}
