from typing import Any

from core.expresions import Expression


class UserExpression(Expression):
    value: Any
    """Value of the expression."""

    def __init__(self, expression_value: Any):
        self.value = expression_value

    def evaluate(self):
        return self.value

    def __str__(self):
        return str(self.evaluate())
