# Import the modules which implement proxy classes
# so they can register themself at the OutputProxy base class.
from . import field, static, tdgeneral
from ._base import OutputProxy

__all__ = ["OutputProxy", "field", "static", "tdgeneral"]
