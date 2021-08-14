from __future__ import annotations

from typing import Any, Generic, TypeVar

from core.components.entity.core.entity_property import EntityProperty
from core.components.entity.core.property_type import PropertyType

T = TypeVar('T')


class AnyProperty(EntityProperty, Generic[T]):
    def __init__(self, value: Any):
        super().__init__(value, PropertyType.ANY)
