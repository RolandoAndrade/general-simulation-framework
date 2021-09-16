from __future__ import annotations

from typing import Dict, Any, List

from core.expresions import Expression, UserExpression
from core.mathematics.distributions import (
    ExponentialDistribution,
    PoissonDistribution,
    TriangularDistribution,
)


class ExpressionManager:
    _available_expressions: Dict[str, Any]

    def __init__(self):
        self._available_expressions = {
            "Random": {
                "Exponential": {
                    "value": "Random.Exponential",
                    "call": ExponentialDistribution,
                    "params": ["mean"],
                },
                "Poisson": {
                    "value": "Random.Poisson",
                    "call": PoissonDistribution,
                    "params": ["mean"],
                },
                "Triangular": {
                    "value": "Random.Triangular",
                    "call": TriangularDistribution,
                    "params": ["minimum", "mode", "maximum"],
                },
            }
        }

    @staticmethod
    def _extract_params(value: str) -> List[float]:
        s = value[value.find("(") + 1 : value.find(")")]
        return [float(param) for param in s.split(",")]

    def get_expression(
        self, value: str, params: List[float] = None, options=None
    ) -> Expression:
        try:
            return UserExpression(eval(value))
        except Exception:
            if options is None:
                options = self._available_expressions
                start_params = value.find("(")
                has_params = start_params != -1
                if has_params:
                    params = params or ExpressionManager._extract_params(value)
                    value = value[:start_params]
                else:
                    params = []

            if "value" in options and isinstance(options["value"], str):
                if "call" in options:
                    return options["call"](*params)
                if "expression" in options:
                    return options["expression"].evaluate()
            key, _, next_keys = value.partition(".")
            if key in options:
                return self.get_expression(next_keys, params, options[key])

    def add_expression(self, value: str, options: Dict[str, Any]):
        self._available_expressions[value] = options

    def remove_expression(self, value: str):
        self._available_expressions.pop(value)

    def get_available_expressions(self):
        return self._available_expressions


static_expression_manager = ExpressionManager()
