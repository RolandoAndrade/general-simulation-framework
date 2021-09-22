from core.entity.properties import ExpressionProperty
from core.expresions import Expression
from queue_simulator.queue_components.shared.expressions import UnitExpression
from queue_simulator.queue_components.shared.units import TimeConversion


class TimeUnitExpressionProperty(ExpressionProperty):
    __unit: str

    def __init__(self, value: Expression, unit: str):
        super().__init__(UnitExpression(value, unit, "Milliseconds", TimeConversion()))
        self.__unit = unit

    def get_unit(self):
        return self.__unit

    def get_value(self) -> UnitExpression:
        return super(TimeUnitExpressionProperty, self).get_value()

    def set_unit(self, unit: str):
        self.__unit = unit
        self.get_value().set_unit(unit)

    def set_value(self, value: Expression):
        self.get_value().set_expression(value)
