from core.expresions import Expression
from queue_simulator.queue_components.shared.units import UnitConversion


class UnitExpression(Expression):
    _expression: Expression
    _unit_conversion: UnitConversion
    _unit: str
    _base_unit: str

    def __init__(self, expression: Expression, unit: str, base_unit: str, unit_conversion: UnitConversion):
        self._expression = expression
        self._unit = unit
        self._base_unit = base_unit
        self._unit_conversion = unit_conversion

    def evaluate(self):
        return self._unit_conversion.convert(self._expression.evaluate(), self._unit, self._base_unit)

    def set_unit(self, unit: str):
        self._unit = unit

    def set_expression(self, expression: Expression):
        self._expression = expression

    def __str__(self):
        return str(self._expression)
