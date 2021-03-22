import unittest

from dynamic_system.models.discrete_event_dynamic_system import DiscreteEventDynamicSystem
from test.discrete_event_model.drill.drill import Drill
from test.discrete_event_model.drill.press import Press


class TestDrill(unittest.TestCase):
    def test_table(self):
        ds = DiscreteEventDynamicSystem()
        press = Press(ds)
        drill = Drill(ds)
        drill.add(press)

        inputs = [{press.getID(): 1}, {press.getID(): 2}, None, None, None, None, None]

        i = 0
        while i < 7:
            print("------------------")
            print("time -> " + str(i))
            if inputs[i] is not None:
                print("Inserting " + str(inputs[i]["Press"]) + " part(s)")
            print("output -> " + str(ds.getOutput()))
            print("--")
            ds.stateTransition(inputs[i], i)
            print(str(press))
            print(str(drill))
            print("--")
            print(ds._scheduler)
            i = i + 1


if __name__ == '__main__':
    unittest.main()
