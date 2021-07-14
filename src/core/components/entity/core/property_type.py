from __future__ import annotations

from typing import Any

from core.components.expresions.expression import Expression

expectedTypes = {
    "STRING": str,
    "BOOLEAN": bool,
    "NUMBER": float,
    "EXPRESSION": Expression,
    "ANY": Any,
    "EVENT": Any
}


class PropertyType:
    """Type of a property"""
    STRING = "STRING"
    BOOLEAN = "BOOLEAN"
    EXPRESSION = "EXPRESSION"
    EVENT = "EVENT"
    NUMBER = "NUMBER"
    ANY = "ANY"

    @staticmethod
    def validate(value: Any, property_type: str) -> bool:
        """Validates if the value type equals to the expected type"""
        if property_type == PropertyType.ANY:
            return True
        return type(value) == expectedTypes.get(property_type) or isinstance(value, expectedTypes.get(property_type))
