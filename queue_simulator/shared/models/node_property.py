from dataclasses import dataclass
from typing import Any, Dict

from core.entity.core.property_type import PropertyType


@dataclass
class NodeProperty:
    property_name: str
    property_value: str
    property_type: str
    property_category: str

    def serialize(self) -> Dict[str, Any]:
        return {
            'propertyName': self.property_name,
            'propertyValue': self.property_value,
            'propertyType': self.property_type,
            'propertyCategory': self.property_category
        }
