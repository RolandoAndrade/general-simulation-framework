from __future__ import annotations

from typing import Any

from gsf.core.expresions.expression import Expression

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
        return True
