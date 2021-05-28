import unittest

from dynamic_system.discrete_events.dynamic_systems.discrete_event_dynamic_system import DiscreteEventDynamicSystem
from test.model.drill.drill import Drill
from test.model.drill.press import Press


class TestDrill(unittest.TestCase):
    def test_table(self):
        ds = DiscreteEventDynamicSystem()
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

    def test_network(self):
        ds = DiscreteEventDynamicSystem()
        press1 = Press(ds, "Press 1")
        press2 = Press(ds, "Press 2")
        drill = Drill(ds, "Drill")
        press1.add(drill)
        press2.add(drill)

        inputs = [{
            press1.getID(): {"ext": 1},
            press2.getID(): {"ext": 2}
        }, {
            press1.getID(): {"ext": 2},
            press2.getID(): {"ext": 3}
        }, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]

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
            print(str(press1))
            print(str(press2))
            print(str(drill))
            print("--")
            print(ds._scheduler)
            if ds.getTimeOfNextEvent() == 0:
                break
            i = i + ds.getTimeOfNextEvent()


if __name__ == '__main__':
    unittest.main()