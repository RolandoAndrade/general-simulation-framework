from __future__ import annotations

from typing import Any

from core.expresions.expression import Expression

expected_types = {
    "STRING": str,
    "BOOLEAN": bool,
    "NUMBER": float,
    "EXPRESSION": Expression,
    "ANY": Any,
    "EVENT": Any,
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
        return type(value) == expected_types.get(property_type) or isinstance(
            value, expected_types.get(property_type)
        )
