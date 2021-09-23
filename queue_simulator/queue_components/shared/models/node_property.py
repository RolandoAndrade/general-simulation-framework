from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional, TypedDict

from core.entity.core.property_type import PropertyType


class NodePropertyDict(TypedDict):
    propertyName: str
    propertyValue: str
    propertyType: str
    propertyCategory: str
    unit: Optional[str]


@dataclass
class NodeProperty:
    property_name: str
    property_value: str
    property_type: str
    property_category: str
    property_unit: Optional[str] = None

    def serialize(self) -> NodePropertyDict:
        return {
            "propertyName": self.property_name,
            "propertyValue": self.property_value,
            "propertyType": self.property_type,
            "propertyCategory": self.property_category,
            "unit": self.property_unit
        }

    @staticmethod
    def deserialize(properties: Dict[str, Any]) -> NodeProperty:
        return NodeProperty(
            properties["propertyName"],
            properties["propertyValue"],
            properties["propertyType"],
            properties["propertyCategory"],
            properties.get("unit", None)
        )
