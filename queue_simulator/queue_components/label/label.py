from __future__ import annotations

from typing import Any, Callable

from queue_simulator.queue_components.shared.expressions import ExpressionManager, static_expression_manager


class Label:
    """Label that indicates the value of a property"""

    __expression: str
    """Expression to be observed"""

    __expression_manager: ExpressionManager
    """Expression manager to get the value of the expression."""

    def __init__(
            self,
            expression: str,
            expression_manager: ExpressionManager = None
    ):
        """
        Args:
            expression (Callable): Expression to be observed by the label.
        """
        self.__expression = expression
        self.__expression_manager = expression_manager or static_expression_manager

    def get_value(self) -> Any:
        """Gets the value of the property."""
        if self.__expression is not None:
            return self.__expression_manager.get_expression(self.__expression)
        return 0

    def __str__(self):
        return str(self.get_value())
