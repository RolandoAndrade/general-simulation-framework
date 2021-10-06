"""Value
=============================
Is an generic expression that can be evaluated.


Example:
    Creating a value::

        my_numeric_value: Value[int] = Value(1)

    Evaluating::

        two = my_numeric_value.evaluate() + 1

"""

from __future__ import annotations

from typing import Generic, TypeVar

from gsf.core.expressions.expression import Expression

T = TypeVar("T")


class Value(Expression, Generic[T]):
    """Value

    Contains a generic constant value.
    """

    __value: T
    """Value of the expression"""

    def __init__(self, value: T):
        """
        Args:
            value (T): Value of the expression.
        """
        self.value = value

    def evaluate(self) -> T:
        """Returns the value"""
        return self.value

    def __str__(self):
        return str(self.evaluate())
