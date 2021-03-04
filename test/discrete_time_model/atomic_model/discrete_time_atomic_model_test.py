from dynamic_system.models.discrete_time_model import DiscreteTimeModel
from dynamic_system.utils.bag_of_values import BagOfValues


class DiscreteTimeAtomicModelTest(DiscreteTimeModel):
    def __init__(self):
        super().__init__()
        state = BagOfValues({
            'Color': 'White',
            'x': 100,
            'y': 100
        })
        self.setUpState(state)

    def internalStateTransitionFunction(self, s: BagOfValues, x: BagOfValues) -> BagOfValues:
        s['x'] = s['x'] + x['x']
        s['y'] = s['y'] + x['y']
        return s

    def outputFunction(self, s: BagOfValues) -> BagOfValues:
        return BagOfValues({
            'x': s['x'] - 100,
            'y': s['y'] - 100
        })