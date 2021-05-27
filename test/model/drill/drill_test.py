import unittest

from dynamic_system.models.dynamic_system import DynamicSystem
from test.model.drill.drill import Drill
from test.model.drill.press import Press


class TestDrill(unittest.TestCase):
    def test_table(self):
        ds = DynamicSystem()
        press = Press(ds, "Press 1")
        drill = Drill(ds, "Drill 1")
        press.add(drill)

        inputs = [{press.getID(): {"ext": 1}}, {press.getID(): {"ext": 2}}, None, None, None, None, None, None]

        i = 0
        while True:
            print("------------------")
            print("time -> " + str(i))
            if inputs[i] is not None:
                print("Inserting " + str(inputs[i]["Press 1"]["ext"]) + " part(s)")
            print("output -> " + str(ds.getOutput()))
            print("--")
            if i < 1:
                ds.stateTransition(inputs[i], 0)
            else:
                ds.stateTransition(inputs[i], ds.getTimeOfNextEvent())
            print(str(press))
            print(str(drill))
            print("--")
            print(ds._scheduler)
            if ds.getTimeOfNextEvent() == 0:
                break
            i = i + ds.getTimeOfNextEvent()


if __name__ == '__main__':
    unittest.main()