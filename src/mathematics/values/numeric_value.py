from core.components.expresions.expression import Expression


class NumericValue(Expression):
    __value: float

    def __init__(self, value: float):
        self.value = value

    def evaluate(self) -> float:
        return self.value

