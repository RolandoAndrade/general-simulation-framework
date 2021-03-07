from dynamic_system.models.discrete_time_model import DiscreteTimeModel


class Cell(DiscreteTimeModel):
    ALIVE = True
    DEAD = False

    def __init__(self, state: bool):
        super().__init__()
        self.setUpState(state)

    def stateTransitionFunction(self, state: bool, inputs: bool) -> bool:
        return inputs

    def outputFunction(self, state: bool) -> bool:
        return state
