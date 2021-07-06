from __future__ import annotations

from typing import Any

expectedTypes = {
    "STRING": str,
    "BOOLEAN": bool,
    "EXPRESSION": Any,
    "EVENT": Any
}


class PropertyType:
    """Type of a property"""
    STRING = "STRING"
    BOOLEAN = "BOOLEAN"
    EXPRESSION = "EXPRESSION"
    EVENT = "EVENT"

    @staticmethod
    def validate(value: Any, property_type: str) -> bool:
        """Validates if the value type equals to the expected type"""
        return type(value) == expectedTypes[property_type]
