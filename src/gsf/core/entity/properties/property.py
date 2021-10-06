"""Property
=============================
Concrete property with Any type.

Example:
    Creating the property::

        property: Property[int] = Property(1)
"""

from __future__ import annotations

from typing import Any, Generic, TypeVar

from gsf.core.entity.core.entity_property import EntityProperty
from gsf.core.entity.core.property_type import PropertyType

T = TypeVar("T")


class Property(EntityProperty, Generic[T]):
    """Any Property

    Defines a property with type Any
    """

    def __init__(self, value: Any):
        super().__init__(value, PropertyType.ANY)
