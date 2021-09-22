from core.entity.properties import ExpressionProperty
from core.expresions import Expression


class UnitExpressionProperty(ExpressionProperty):
    __unit: str

    def __init__(self, value: Expression, unit: str):
        super().__init__(value)
        self.__unit = unit

    def get_unit(self):
        return self.__unit

    def set_unit(self, unit: str):
        self.__unit = unit
