from __future__ import annotations

from typing import Any

from core.components.expresions.expression import Expression

expectedTypes = {
    "STRING": str,
    "BOOLEAN": bool,
    "NUMBER": float,
    "EXPRESSION": Expression,
    "EVENT": Any
}


class PropertyType:
    """Type of a property"""
    STRING = "STRING"
    BOOLEAN = "BOOLEAN"
    EXPRESSION = "EXPRESSION"
    EVENT = "EVENT"
    NUMBER = "NUMBER"

    @staticmethod
    def validate(value: Any, property_type: str) -> bool:
        """Validates if the value type equals to the expected type"""
        return type(value) == expectedTypes.get(property_type) or isinstance(value, expectedTypes.get(property_type))
