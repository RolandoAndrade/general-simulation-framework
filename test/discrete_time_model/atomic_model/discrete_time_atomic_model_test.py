from dynamic_system.models.discrete_time_model import DiscreteTimeModel


class DiscreteTimeAtomicModelTest(DiscreteTimeModel):
    def __init__(self):
        super().__init__()
        self.setUpState(1)

    def stateTransitionFunction(self, s: float, x: float) -> float:
        return s / 2 + x

    def outputFunction(self, s: float) -> float:
        return 10 * s
