from __future__ import annotations

from typing import Dict, Any

from core.expresions import Expression, UserExpression
import core.mathematics.distributions as Random


class ExpressionManager:
    available_expressions = {
        'Random': {
            'ExponentialDistribution': {
                'value': 'Random.ExponentialDistribution',
                'params': ['mean']
            },
            'PoissonDistribution': {
                'value': 'Random.PoissonDistribution',
                'params': ['mean']
            },
            'TriangularDistribution': {
                'value': 'Random.TriangularDistribution',
                'params': ['minimum', 'mode', 'maximum']
            },
        }
    }

    @staticmethod
    def get_expression(value: str, options=None) -> Expression:
        try:
            return UserExpression(eval(value))
        except Exception:
            if options is None:
                options = ExpressionManager.available_expressions
            key, _, next_keys = value.partition('.')

            if key in options:
                return ExpressionManager.get_expression(next_keys, options[key])

    @staticmethod
    def add_expression(value: str, options: Dict[str, Any]):
        ExpressionManager.available_expressions[value] = options

    @staticmethod
    def remove_expression(value: str):
        ExpressionManager.available_expressions[value] = options
