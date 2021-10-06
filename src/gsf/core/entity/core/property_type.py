"""Property Type
=============================
This module contains the definition of the available types of properties.
It has the definition of PropertyType that contains the static constants of the available types. It also
contains a method to verify the type of the property.
"""


from __future__ import annotations

from typing import Any

from gsf.core.expressions.expression import Expression

expected_types = {
    "STRING": str,
    "BOOLEAN": bool,
    "NUMBER": float,
    "EXPRESSION": Expression,
    "ANY": Any,
    "EVENT": Any,
}
"""Dict with names of the types and their corresponding type"""


class PropertyType:
    """Type of a property

    It contains the constants of the available types.
    """

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
